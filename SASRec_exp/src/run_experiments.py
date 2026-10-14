"""Experiment driver.

Grid: {beauty, yambda} x {adamw, muon} x {blocks 2, 4, 6} x regularization
{none, attn, mlp, attn+mlp} (Lipschitz W <- W/sigma_max(W) on attention
projections and/or FFN conv weights; see src/lipschitz.py).
Completed runs (results/<run>.json exists) are skipped, so the driver can be
re-invoked to resume an interrupted sweep.

Yambda lipschitz runs automatically get the extended budget
(max_epochs 80, patience 15) unless overridden — see src/experiment.py.

Examples:
    python -m src.run_experiments --datasets beauty --reg none
    python -m src.run_experiments --reg mlp attn+mlp
    python -m src.run_experiments --stage lipschitz   # backward compat: --reg attn
"""

import argparse
import time

from src.configs import DATASETS, NUM_BLOCKS
from src.experiment import run_experiment, run_name

REG_MODES = ("none", "attn", "mlp", "attn+mlp")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", default=["beauty", "yambda"],
                        choices=list(DATASETS))
    parser.add_argument("--optimizers", nargs="+", default=["adamw", "muon"],
                        choices=["adamw", "muon"])
    parser.add_argument("--blocks", nargs="+", type=int, default=list(NUM_BLOCKS))
    parser.add_argument("--reg", nargs="+", default=["none", "attn"],
                        choices=REG_MODES,
                        help="Lipschitz regularization modes to run")
    parser.add_argument("--stage", default=None,
                        choices=["base", "lipschitz", "all"],
                        help="legacy alias: base=none, lipschitz=attn, "
                             "all=none+attn")
    parser.add_argument("--max-epochs", type=int, default=None)
    parser.add_argument("--patience", type=int, default=None)
    parser.add_argument("--force", action="store_true",
                        help="rerun even if results exist")
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    if args.stage is not None:
        args.reg = (["none"] if args.stage == "base" else
                    ["attn"] if args.stage == "lipschitz" else ["none", "attn"])

    jobs = []
    for dataset in args.datasets:
        for reg in args.reg:
            for optimizer in args.optimizers:
                for blocks in args.blocks:
                    jobs.append((dataset, optimizer, blocks, reg))

    print(f"planned runs ({len(jobs)}):")
    for job in jobs:
        print("  ", run_name(*job))

    failures = []
    for i, (dataset, optimizer, blocks, reg) in enumerate(jobs, 1):
        print(f"\n[{i}/{len(jobs)}] starting {run_name(dataset, optimizer, blocks, reg)}")
        try:
            run_experiment(dataset, optimizer, blocks, lipschitz_mode=reg,
                           max_epochs=args.max_epochs, patience=args.patience,
                           device=args.device, skip_existing=not args.force)
        except Exception as exc:  # keep the sweep alive; report at the end
            print(f"FAILED: {exc}")
            failures.append((run_name(dataset, optimizer, blocks, reg), str(exc)))
        time.sleep(2)

    print("\n=== sweep done ===")
    if failures:
        print("failures:")
        for name, err in failures:
            print(f"  {name}: {err}")
    else:
        print("all runs completed")


if __name__ == "__main__":
    main()
