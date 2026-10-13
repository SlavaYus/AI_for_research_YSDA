"""Parameter-scaling experiments: width sweep with the sqrt-K lr rule.

Rule under test: when the total number of trainable parameters grows K-fold,
the learning rate is scaled down as lr(K) = lr_base / sqrt(K).

Design:
- The parameter-count knob is the model width: hidden_units in {64, 128, 256}
  with num_blocks=2 fixed (isolates the width effect; matches the setup the
  base lr / muon_lr were tuned in). Total params approximately double per
  width step because the item embedding (catalog x hidden) dominates.
- K is measured exactly: K = n_params(hidden) / n_params(hidden=128), the
  base width of the "optimal config".
- Two arms per width:
    * 'scaled'  — the rule: lr_base / sqrt(K) (lr decreases as params grow);
    * 'constlr' — control: lr fixed at lr_base.
  At hidden=128 (K=1) the arms coincide, so one run per optimizer serves both.
- Both optimizers (AdamW; Muon with Muon on 2D weights + AdamW on 1D and
  embeddings). The rule scales every lr of the run: the AdamW lr and, in the
  muon arm, muon_lr as well (same 1/sqrt(K) factor).
- Budgets: Beauty keeps the base config (max_epochs 200, patience 10 — runs
  converge naturally well before the cap); Yambda uses a uniform
  max_epochs 60 / patience 8 for every run of this experiment so that the
  slower-converging small-lr runs are not disadvantaged by the epoch cap.

Usage:
    python -m src.param_scaling --datasets beauty yambda [--force]
"""

import argparse
import json
import time
from dataclasses import replace
from datetime import date

import pandas as pd
import torch

from src.configs import (DATASETS, DIARY_PATH, OPTIMIZER_SETTINGS,
                         RESULTS_DIR, TOP_K, DatasetConfig)
from src.experiment import load_split
from src.metrics import evaluate
from src.train import build_model, predict_topk, train_model

WIDTHS = (64, 128, 256)
BASE_WIDTH = 128
ARMS = ("scaled", "constlr")
OUT_DIR = RESULTS_DIR / "param_scaling"

YAMBDA_MAX_EPOCHS = 60
YAMBDA_PATIENCE = 8


def count_params(cfg: DatasetConfig, item_count: int, hidden_units: int,
                 num_blocks: int = 2) -> int:
    model = build_model(replace(cfg, hidden_units=hidden_units), item_count,
                        num_blocks, device="cpu")
    return sum(p.numel() for p in model.parameters())


def arm_lr(base_lr: float, arm: str, k: float) -> float:
    if arm in ("constlr", "base"):
        return base_lr
    if arm == "scaled":
        return base_lr / k ** 0.5
    raise ValueError(f"Unknown arm: {arm!r}")


def run_name(dataset_key, optimizer, hidden, arm):
    if hidden == BASE_WIDTH:
        return f"{dataset_key}_{optimizer}_h{hidden}_base"
    return f"{dataset_key}_{optimizer}_h{hidden}_{arm}"


def log_to_diary(run, cfg, optimizer, hidden, arm, k, lr, muon_lr, n_params,
                 metrics, info):
    k10 = TOP_K
    entry = [
        "",
        f"### {run} (param-scaling) — {date.today().isoformat()}",
        f"- Конфиг: {cfg.name}, hidden={hidden} (params={n_params / 1e6:.2f}M, "
        f"K={k:.3f} от h={BASE_WIDTH}), num_blocks=2, optimizer={optimizer}, "
        f"arm={arm} (lr={'base/sqrt(K)' if arm == 'scaled' else 'const'}), "
        f"lr={lr:.2e}, muon_lr={muon_lr if muon_lr is not None else '-'}, "
        f"loss={cfg.loss}, max_seq_len={cfg.max_sequence_length}",
        f"- Обучение: best_epoch={info.get('best_epoch')}, "
        f"best_val_NDCG@{k10}={round(info.get('best_val_ndcg@10', 0), 4)}, "
        f"время={info.get('train_time_h')} ч",
        f"- Тест: HR@{k10}={round(metrics[f'HR@{k10}'], 4)}, "
        f"NDCG@{k10}={round(metrics[f'NDCG@{k10}'], 4)}, "
        f"Coverage@{k10}={round(metrics[f'Coverage@{k10}'], 4)}",
        f"- Точка проверки: results/param_scaling/{run}.json",
    ]
    with open(DIARY_PATH, "a", encoding="utf-8") as f:
        f.write("\n".join(entry) + "\n")


def run_scaling_experiment(dataset_key, optimizer, hidden, arm,
                           device=None, skip_existing=True):
    cfg = DATASETS[dataset_key]
    run = run_name(dataset_key, optimizer, hidden, arm)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{run}.json"
    if skip_existing and out_path.exists():
        print(f"[skip] {run}: {out_path} already exists")
        return json.load(open(out_path))

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    log_path = OUT_DIR / "logs"
    log_path.mkdir(parents=True, exist_ok=True)
    log_file = open(log_path / f"{run}.log", "w", encoding="utf-8")

    def log(msg):
        print(msg)
        log_file.write(str(msg) + "\n")
        log_file.flush()

    start = time.time()
    parts, item_count = load_split(cfg)

    n_params = count_params(cfg, item_count, hidden)
    n_base = count_params(cfg, item_count, BASE_WIDTH)
    k = n_params / n_base
    lr = arm_lr(cfg.lr, arm, k)

    muon_base = OPTIMIZER_SETTINGS["muon"]["muon_lr"]
    muon_lr = None
    if optimizer == "muon":
        muon_lr = arm_lr(muon_base, arm, k)

    max_epochs, patience = cfg.max_epochs, cfg.patience
    if dataset_key == "yambda":
        max_epochs, patience = YAMBDA_MAX_EPOCHS, YAMBDA_PATIENCE

    log(f"=== {run} ===")
    log(f"params={n_params} ({n_params / 1e6:.2f}M), base(h={BASE_WIDTH})="
        f"{n_base / 1e6:.2f}M, K={k:.4f}, arm={arm}, lr={lr:.6e}"
        + (f", muon_lr={muon_lr}" if muon_lr is not None else ""))

    cfg_run = replace(cfg, hidden_units=hidden, lr=lr)

    validation_full = pd.concat([parts["validation_input"],
                                 parts["validation_target"]], axis=0)

    model, info = train_model(
        cfg_run, parts["train"], validation_full, item_count,
        num_blocks=2, optimizer_kind=optimizer, lipschitz_mode="none",
        device=device, log=log, max_epochs=max_epochs, patience=patience,
        muon_lr=muon_lr if muon_lr is not None else OPTIMIZER_SETTINGS["muon"]["muon_lr"],
        muon_momentum=OPTIMIZER_SETTINGS["muon"]["muon_momentum"],
    )

    recs, _ = predict_topk(model, parts["test_input"], cfg_run, top_k=TOP_K,
                           validation_mode=False, device=device)
    targets = {int(u): int(i) for u, i in
               zip(parts["test_target"].user_id, parts["test_target"].item_id)}

    metrics = evaluate(recs, targets, parts["test_input"], catalog_size=item_count,
                       max_sequence_length=cfg.max_sequence_length, k=TOP_K)
    log(f"test metrics: {metrics}")

    result = {
        "run": run,
        "experiment": "param_scaling",
        "dataset": dataset_key,
        "dataset_name": cfg.name,
        "optimizer": optimizer,
        "hidden_units": hidden,
        "arm": arm,
        "num_blocks": 2,
        "lipschitz": False,
        "n_params": n_params,
        "n_params_base": n_base,
        "k": k,
        "lr": lr,
        "lr_base": cfg.lr,
        "muon_lr": muon_lr,
        "muon_lr_base": muon_base if optimizer == "muon" else None,
        "max_epochs": max_epochs,
        "patience": patience,
        "item_count": item_count,
        "n_test_users": len(targets),
        "metrics": metrics,
        "training": info,
        "wall_time_sec": round(time.time() - start, 1),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    log(f"saved: {out_path}")

    log_to_diary(run, cfg, optimizer, hidden, arm, k, lr, muon_lr, n_params,
                 metrics, info)
    log_file.close()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", default=["beauty", "yambda"],
                        choices=list(DATASETS))
    parser.add_argument("--optimizers", nargs="+", default=["adamw", "muon"],
                        choices=["adamw", "muon"])
    parser.add_argument("--widths", nargs="+", type=int, default=list(WIDTHS))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    jobs = []
    for dataset in args.datasets:
        for optimizer in args.optimizers:
            for hidden in args.widths:
                if hidden == BASE_WIDTH:
                    jobs.append((dataset, optimizer, hidden, "base"))
                else:
                    jobs.extend((dataset, optimizer, hidden, arm)
                                for arm in ARMS)

    print(f"planned runs ({len(jobs)}):")
    for job in jobs:
        print("  ", run_name(*job))

    failures = []
    for i, job in enumerate(jobs, 1):
        print(f"\n[{i}/{len(jobs)}] starting {run_name(*job)}")
        try:
            run_scaling_experiment(*job, device=args.device,
                                   skip_existing=not args.force)
        except Exception as exc:
            print(f"FAILED: {exc}")
            failures.append((run_name(*job), str(exc)))
        time.sleep(2)

    print("\n=== param-scaling sweep done ===")
    if failures:
        print("failures:")
        for name, err in failures:
            print(f"  {name}: {err}")
    else:
        print("all runs completed")


if __name__ == "__main__":
    main()
