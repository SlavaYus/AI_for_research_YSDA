"""Training / prediction loop for SASRec experiments (plain PyTorch).

The loss and prediction logic mirror the parent repo's Lightning modules
(src/models/sequential_wrappers.py): SeqRec for the full cross-entropy loss,
SeqRecWithSCE for the scalable cross-entropy loss, and
convert_outputs_to_preds for ranking (last non-padding position, optional
seen-item filtering).
"""

import copy
import random
import time
from datetime import datetime

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader

from src.datasets import (CausalLMDataset, CausalLMPredictionDataset,
                          PaddingCollateFn)
from src.sce import SCEObjectiveFlat


def fix_seeds(random_state: int):
    """Seed everything (python, numpy, torch) and make cudnn deterministic."""
    random.seed(random_state)
    np.random.seed(random_state)
    torch.manual_seed(random_state)
    torch.cuda.manual_seed_all(random_state)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def build_model(cfg, item_count: int, num_blocks: int, device: str):
    from src.sasrec import SASRec

    use_sce = cfg.loss == "sce"
    model = SASRec(
        item_num=item_count,
        max_sequence_length=cfg.max_sequence_length,
        hidden_units=cfg.hidden_units,
        num_blocks=num_blocks,
        num_heads=cfg.num_heads,
        dropout_rate=cfg.dropout_rate,
        add_head=not use_sce,
    )
    return model.to(device)


def compute_loss(cfg, model, batch, sce):
    outputs = model(batch["input_ids"], batch["attention_mask"])
    if cfg.loss == "sce":
        # outputs: [B, T, D] hidden states (add_head=False)
        labels = batch["labels"]
        valid = labels != -100
        x = outputs[valid]
        y = labels[valid].long()
        return sce({"sce_x": x, "sce_y": y, "item_emb_weight": model.item_emb.weight})
    # full cross-entropy over the catalog (add_head=True)
    loss_fct = nn.CrossEntropyLoss()
    return loss_fct(outputs.view(-1, outputs.size(-1)), batch["labels"].view(-1))


def last_position_logits(model, batch):
    """Full-vocab logits at the last non-padding position.

    Handles both head modes: with add_head=True the model already returns
    logits [B, T, C]; otherwise hidden states are projected onto the item
    embedding table.
    """
    outputs = model(batch["input_ids"], batch["attention_mask"])
    input_ids = batch["input_ids"]
    rows = torch.arange(input_ids.shape[0], device=input_ids.device)
    last_item_idx = (input_ids != 0).sum(axis=1) - 1
    last = outputs[rows, last_item_idx, :]
    if not model.add_head:
        last = torch.matmul(last, model.item_emb.weight.transpose(0, 1))
    return last


def predict_topk(model, df, cfg, top_k=10, validation_mode=False,
                 device="cuda", desc="predict"):
    """Top-k items per user.

    validation_mode=True: input is all but the last item, target is the last
    (used for validation monitoring); otherwise input is the last
    max_sequence_length items and full_history carries everything the user
    interacted with (used for seen-item filtering at test time).
    """
    dataset = CausalLMPredictionDataset(
        df, max_sequence_length=cfg.max_sequence_length,
        validation_mode=validation_mode,
    )
    loader = DataLoader(
        dataset, batch_size=cfg.eval_batch_size, shuffle=False,
        num_workers=cfg.num_workers, collate_fn=PaddingCollateFn(left_padding=False),
    )
    model.eval()
    recs, targets = {}, {}
    with torch.no_grad():
        for batch in loader:
            batch = {k: v.to(device) if torch.is_tensor(v) else v
                     for k, v in batch.items()}
            logits = last_position_logits(model, batch)  # [B, C]
            if cfg.filter_seen and "full_history" in batch:
                seen = batch["full_history"]
                seen_mask = torch.zeros_like(logits, dtype=torch.bool, device=logits.device)
                seen_mask.scatter_(1, seen.clamp(min=0, max=logits.shape[1] - 1), True)
                logits = logits.masked_fill(seen_mask, float("-inf"))
            _, preds = torch.topk(logits, top_k, dim=1)
            preds = preds.cpu().numpy()
            users = batch["user_id"].cpu().numpy()
            for u, p in zip(users, preds):
                recs[int(u)] = [int(i) for i in p]
            if "target" in batch:
                for u, t in zip(users, batch["target"].cpu().numpy()):
                    targets[int(u)] = int(t)
    model.train()
    return recs, targets


def validation_ndcg(model, val_df, cfg, device, top_k=10):
    """Quick NDCG@k on a subsample of validation users (early-stopping signal)."""
    recs, targets = predict_topk(model, val_df, cfg, top_k=top_k,
                                 validation_mode=True, device=device,
                                 desc="val")
    hits, ndcgs = [], []
    for user, target in targets.items():
        top = list(recs.get(user, []))[:top_k]
        try:
            rank = top.index(target)
        except ValueError:
            rank = -1
        if rank >= 0:
            hits.append(1.0)
            ndcgs.append(1.0 / np.log2(rank + 2))
        else:
            hits.append(0.0)
            ndcgs.append(0.0)
    return float(np.mean(ndcgs)) if ndcgs else 0.0, float(np.mean(hits)) if hits else 0.0


def train_model(cfg, train_df, val_full, item_count, num_blocks, optimizer_kind,
                lipschitz_mode="none", device="cuda", log=print, max_epochs=None,
                patience=None, muon_lr=0.01, muon_momentum=0.99):
    """Train one SASRec model; returns (model, info dict).

    Early stopping monitors NDCG@10 on a fixed subsample of validation users.
    lipschitz_mode: 'none' | 'attn' | 'mlp' | 'attn+mlp' (see src/lipschitz.py).
    """
    from src.configs import ADAMW_BETAS, WEIGHT_DECAY
    from src.lipschitz import apply_lipschitz
    from src.optimizers import make_optimizer

    fix_seeds(cfg.random_state)

    val_users = val_full.user_id.unique()
    rng = np.random.RandomState(cfg.random_state)
    if cfg.val_size and cfg.val_size < len(val_users):
        val_users = rng.choice(val_users, size=cfg.val_size, replace=False)
    val_sub = val_full[val_full.user_id.isin(val_users)]

    train_dataset = CausalLMDataset(train_df, max_sequence_length=cfg.max_sequence_length)
    train_loader = DataLoader(
        train_dataset, batch_size=cfg.batch_size, shuffle=True,
        num_workers=cfg.num_workers, collate_fn=PaddingCollateFn(left_padding=False),
        drop_last=False,
    )

    model = build_model(cfg, item_count, num_blocks, device)

    n_lip = 0
    if lipschitz_mode:
        n_lip = apply_lipschitz(model, lipschitz_mode)
        log(f"lipschitz regularization (mode={lipschitz_mode}): "
            f"{n_lip} weight matrices renormalized")

    optimizer = make_optimizer(
        model, optimizer_kind, cfg.lr,
        muon_lr=muon_lr, muon_momentum=muon_momentum,
        betas=ADAMW_BETAS, weight_decay=WEIGHT_DECAY,
    )
    if hasattr(optimizer, "muon_param_names"):
        log(f"muon params ({len(optimizer.muon_param_names)}): {optimizer.muon_param_names}")
        log(f"adamw params ({len(optimizer.adamw_param_names)}): {optimizer.adamw_param_names}")

    sce = None
    if cfg.loss == "sce":
        sce = SCEObjectiveFlat(**cfg.sce)

    max_epochs = max_epochs if max_epochs is not None else cfg.max_epochs
    patience = patience if patience is not None else cfg.patience

    history = []
    best_ndcg, best_epoch, best_state = -1.0, -1, None
    bad_epochs = 0
    start = time.time()

    for epoch in range(max_epochs):
        model.train()
        epoch_loss, n_batches = 0.0, 0
        for batch in train_loader:
            batch = {k: v.to(device) if torch.is_tensor(v) else v
                     for k, v in batch.items()}
            optimizer.zero_grad()
            loss = compute_loss(cfg, model, batch, sce)
            loss.backward()
            optimizer.step()
            epoch_loss += float(loss.item())
            n_batches += 1

        val_ndcg, val_hr = validation_ndcg(model, val_sub, cfg, device)
        history.append({"epoch": epoch, "train_loss": epoch_loss / max(n_batches, 1),
                        "val_ndcg@10": val_ndcg, "val_hr@10": val_hr})
        improved = val_ndcg > best_ndcg
        if improved:
            best_ndcg, best_epoch = val_ndcg, epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            bad_epochs = 0
        else:
            bad_epochs += 1
        log(f"epoch {epoch}: train_loss={epoch_loss / max(n_batches, 1):.4f} "
            f"val_ndcg@10={val_ndcg:.4f} val_hr@10={val_hr:.4f}"
            f"{' *best*' if improved else ''}")
        if bad_epochs >= patience:
            log(f"early stopping at epoch {epoch} (no val NDCG improvement for "
                f"{patience} epochs)")
            break

    train_time = time.time() - start
    if best_state is not None:
        model.load_state_dict(best_state)
    return model, {
        "history": history,
        "best_epoch": best_epoch,
        "best_val_ndcg@10": best_ndcg,
        "train_time_sec": round(train_time, 1),
        "train_time_h": round(train_time / 3600, 2),
        "n_lipschitz_weights": n_lip,
        "finished": datetime.now().isoformat(timespec="seconds"),
    }
