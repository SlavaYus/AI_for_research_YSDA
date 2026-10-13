"""Single experiment: load split -> train -> predict test -> metrics -> save.

Every run appends a structured entry to diary.md (as required by AGENT.md:
"все эксперименты заносить в diary") and saves machine-readable results to
results/<dataset>/<run_name>.json plus a training log to results/logs/.
"""

import json
import sys
import time
from dataclasses import asdict
from datetime import date
from pathlib import Path

import pandas as pd
import torch

from src.configs import (DIARY_PATH, OPTIMIZER_SETTINGS, RESULTS_DIR, TOP_K,
                         DatasetConfig, split_paths)
from src.metrics import evaluate
from src.train import predict_topk, train_model


LIPSCHITZ_SUFFIXES = {"attn": "_lip", "mlp": "_lipmlp", "attn+mlp": "_lipfull"}
LIPSCHITZ_TITLES = {
    "attn": "lipschitz attention",
    "mlp": "lipschitz MLP",
    "attn+mlp": "lipschitz attention+MLP",
}
# Yambda lipschitz runs converge slower (and the AdamW ones may need to escape
# the popularity basin), so they get the extended budget used by the final
# attention-lipschitz reruns (see diary 2026-10-13).
YAMBDA_LIP_MAX_EPOCHS = 80
YAMBDA_LIP_PATIENCE = 15


def run_name(dataset_key, optimizer, num_blocks, lipschitz_mode):
    mode = lipschitz_mode or "none"
    parts = [dataset_key, optimizer, f"l{num_blocks}"]
    if mode != "none":
        parts.append(LIPSCHITZ_SUFFIXES[mode].lstrip("_"))
    return "_".join(parts)


def log_to_diary(run, cfg, optimizer, num_blocks, lipschitz_mode, metrics, info):
    """Append one experiment record to diary.md (append-only, per AGENT.md)."""
    k = TOP_K
    mode = lipschitz_mode or "none"
    reg_txt = f" + {LIPSCHITZ_TITLES[mode]}" if mode != "none" else ""
    entry = [
        "",
        f"### {run} — {date.today().isoformat()}",
        f"- Конфиг: {cfg.name}, num_blocks={num_blocks}, optimizer={optimizer}"
        f"{reg_txt}, "
        f"hidden={cfg.hidden_units}, heads={cfg.num_heads}, "
        f"dropout={cfg.dropout_rate}, lr={cfg.lr:.2e}, loss={cfg.loss}, "
        f"max_seq_len={cfg.max_sequence_length}, batch={cfg.batch_size}",
        f"- Регуляризация: "
        + ("нет" if mode == "none" else
           "Lipschitz (W <- W/sigma_max(W), power iteration) на "
           + {"attn": "in_proj_weight и out_proj.weight каждого attention-блока",
              "mlp": "conv1.weight и conv2.weight каждого FFN-блока (MLP)",
              "attn+mlp": "attention и MLP веса каждого блока"}[mode]),
        f"- Оптимизатор: "
        + ("AdamW (все параметры)" if optimizer == "adamw" else
           "Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)"),
        f"- Обучение: best_epoch={info.get('best_epoch')}, "
        f"best_val_NDCG@{k}={round(info.get('best_val_ndcg@10', 0), 4)}, "
        f"время={info.get('train_time_h')} ч",
        f"- Тест: HR@{k}={round(metrics[f'HR@{k}'], 4)}, "
        f"NDCG@{k}={round(metrics[f'NDCG@{k}'], 4)}, "
        f"Coverage@{k}={round(metrics[f'Coverage@{k}'], 4)}",
        f"- Бакеты (users 1/2/3) NDCG@{k}: "
        + "/".join(str(round(metrics.get(f'ubucket{b}_NDCG@{k}', 0), 4)) for b in (1, 2, 3))
        + f"; (items 1/2/3) NDCG@{k}: "
        + "/".join(str(round(metrics.get(f'ibucket{b}_NDCG@{k}', 0), 4)) for b in (1, 2, 3)),
        f"- Бакеты (users 1/2/3) HR@{k}: "
        + "/".join(str(round(metrics.get(f'ubucket{b}_HR@{k}', 0), 4)) for b in (1, 2, 3))
        + f"; (items 1/2/3) HR@{k}: "
        + "/".join(str(round(metrics.get(f'ibucket{b}_HR@{k}', 0), 4)) for b in (1, 2, 3)),
        f"- Точка проверки: results/{run}.json (полные метрики и история обучения)",
    ]
    with open(DIARY_PATH, "a", encoding="utf-8") as f:
        f.write("\n".join(entry) + "\n")


def load_split(cfg: DatasetConfig):
    paths = split_paths(cfg)
    parts = {}
    max_item_id = 0
    for name, path in paths.items():
        df = pd.read_csv(path)
        parts[name] = df
        max_item_id = max(max_item_id, int(df.item_id.max()))
    return parts, max_item_id + 1


def run_experiment(dataset_key, optimizer, num_blocks, lipschitz_mode="none",
                   max_epochs=None, patience=None, device=None,
                   skip_existing=True):
    from src.configs import DATASETS

    cfg = DATASETS[dataset_key]
    mode = lipschitz_mode or "none"
    if mode not in ("none", "attn", "mlp", "attn+mlp"):
        raise ValueError(f"Unknown lipschitz_mode: {mode!r}")
    run = run_name(dataset_key, optimizer, num_blocks, mode)
    out_path = RESULTS_DIR / f"{run}.json"
    if skip_existing and out_path.exists():
        print(f"[skip] {run}: {out_path} already exists")
        return json.load(open(out_path))

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    if (dataset_key == "yambda" and mode != "none"
            and max_epochs is None and patience is None):
        max_epochs, patience = YAMBDA_LIP_MAX_EPOCHS, YAMBDA_LIP_PATIENCE

    log_path = RESULTS_DIR / "logs" / f"{run}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_file = open(log_path, "w", encoding="utf-8")

    def log(msg):
        print(msg)
        log_file.write(str(msg) + "\n")
        log_file.flush()

    start = time.time()
    log(f"=== {run} ===")
    log(f"config: dataset={cfg.name} blocks={num_blocks} optimizer={optimizer} "
        f"lipschitz_mode={mode} loss={cfg.loss} hidden={cfg.hidden_units} "
        f"heads={cfg.num_heads} dropout={cfg.dropout_rate} lr={cfg.lr} "
        f"muon={OPTIMIZER_SETTINGS.get(optimizer, {})} "
        f"max_epochs={max_epochs or cfg.max_epochs} patience={patience or cfg.patience}")

    parts, item_count = load_split(cfg)
    for name, df in parts.items():
        log(f"{name}: {df.shape[0]} rows, {df.user_id.nunique()} users, "
            f"{df.item_id.nunique()} items")
    log(f"item_count (catalog): {item_count}")

    validation_full = pd.concat([parts["validation_input"],
                                 parts["validation_target"]], axis=0)

    model, info = train_model(
        cfg, parts["train"], validation_full, item_count,
        num_blocks=num_blocks, optimizer_kind=optimizer,
        lipschitz_mode=mode,
        device=device, log=log, max_epochs=max_epochs, patience=patience,
        **OPTIMIZER_SETTINGS.get(optimizer, {}),
    )

    recs, _ = predict_topk(model, parts["test_input"], cfg, top_k=TOP_K,
                           validation_mode=False, device=device, desc="test")
    targets = {int(u): int(i) for u, i in
               zip(parts["test_target"].user_id, parts["test_target"].item_id)}

    metrics = evaluate(
        recs, targets, parts["test_input"], catalog_size=item_count,
        max_sequence_length=cfg.max_sequence_length, k=TOP_K,
    )
    log(f"test metrics: {metrics}")

    result = {
        "run": run,
        "dataset": dataset_key,
        "dataset_name": cfg.name,
        "optimizer": optimizer,
        "optimizer_settings": OPTIMIZER_SETTINGS.get(optimizer, {}),
        "num_blocks": num_blocks,
        "lipschitz": mode != "none",
        "lipschitz_mode": mode,
        "config": {k: v for k, v in asdict(cfg).items()
                   if not k.startswith("_") and k != "data_dir"},
        "item_count": item_count,
        "n_test_users": len(targets),
        "metrics": metrics,
        "training": info,
        "wall_time_sec": round(time.time() - start, 1),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    log(f"saved: {out_path}")

    log_to_diary(run, cfg, optimizer, num_blocks, mode, metrics, info)
    log_file.close()
    return result
