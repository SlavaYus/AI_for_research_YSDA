"""Plot for the parameter-scaling experiments (sqrt-K lr rule).

One figure: rows = datasets, columns = metrics (HR@10, NDCG@10, Coverage@10).
X axis: total trainable parameters (millions, log scale — the three widths).
Lines: solid = const-lr control, dashed = sqrt(K)-scaled lr.
Colors: AdamW (blue), Muon (orange).
The h=128 point (K=1) is shared by both arms.

Usage: python -m src.plot_param_scaling [--out figures/param_scaling.png]
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.configs import FIGURES_DIR, RESULTS_DIR

OUT_DIR = RESULTS_DIR / "param_scaling"
METRICS = [("HR@10", "HR@10"), ("NDCG@10", "NDCG@10"), ("Coverage@10", "Coverage@10")]
OPT_COLORS = {"adamw": "#4C72B0", "muon": "#DD8452"}
ARM_STYLE = {"constlr": {"linestyle": "-", "label": "lr = const"},
             "scaled": {"linestyle": "--", "label": "lr = base/sqrt(K)"}}


def load_results():
    rows = []
    for path in sorted(OUT_DIR.glob("*.json")):
        with open(path) as f:
            rows.append(json.load(f))
    if not rows:
        raise SystemExit("no results in results/param_scaling/")
    return rows


def plot(out_path):
    rows = load_results()
    datasets = sorted({r["dataset"] for r in rows})

    fig, axes = plt.subplots(len(datasets), len(METRICS),
                             figsize=(5 * len(METRICS), 4 * len(datasets)),
                             squeeze=False)

    for r_i, dataset in enumerate(datasets):
        ds_rows = [x for x in rows if x["dataset"] == dataset]
        dataset_name = ds_rows[0]["dataset_name"]
        for m_i, (metric_key, metric_title) in enumerate(METRICS):
            ax = axes[r_i][m_i]
            for optimizer, color in OPT_COLORS.items():
                opt_rows = [x for x in ds_rows if x["optimizer"] == optimizer]
                base_row = next((x for x in opt_rows if x["hidden_units"] == 128), None)
                if base_row is None:
                    continue
                for arm, style in ARM_STYLE.items():
                    arm_rows = [x for x in opt_rows
                                if x["arm"] in (arm, "base") and x["arm"] != "base"]
                    arm_rows.append(base_row)  # shared K=1 point
                    arm_rows.sort(key=lambda x: x["n_params"])
                    xs = [x["n_params"] / 1e6 for x in arm_rows]
                    ys = [x["metrics"][metric_key] for x in arm_rows]
                    ax.plot(xs, ys, marker="o", color=color,
                            linestyle=style["linestyle"], linewidth=1.8,
                            markersize=5,
                            label=f"{optimizer.upper()} {style['label']}")
                    for x, y in zip(xs, ys):
                        ax.annotate(f"{y:.4f}", (x, y), textcoords="offset points",
                                    xytext=(0, 5), ha="center", fontsize=6.5)
            ax.set_xscale("log")
            xs_all = sorted({x["n_params"] / 1e6 for x in ds_rows})
            ax.set_xticks(xs_all)
            ax.set_xticklabels([f"{x:.2f}M" for x in xs_all], fontsize=8)
            if m_i == 0:
                ax.set_ylabel(metric_title)
            ax.set_title(f"{dataset_name}: {metric_title} vs params", fontsize=11)
            ax.grid(alpha=0.3, linestyle="--")
            ymax = max(x["metrics"][metric_key] for x in ds_rows)
            ymin = min(x["metrics"][metric_key] for x in ds_rows)
            pad = (ymax - ymin) * 0.25 + 1e-4
            ax.set_ylim(ymin - pad, ymax + pad)

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, fontsize=9,
               frameon=False, bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    print(f"saved: {out_path}")

    csv_path = out_path.with_suffix(".csv")
    flat = []
    for x in rows:
        rec = {
            "dataset": x["dataset_name"], "optimizer": x["optimizer"],
            "hidden_units": x["hidden_units"], "arm": x["arm"],
            "n_params": x["n_params"], "K": round(x["k"], 4),
            "lr": x["lr"], "muon_lr": x["muon_lr"],
            "HR@10": x["metrics"]["HR@10"],
            "NDCG@10": x["metrics"]["NDCG@10"],
            "Coverage@10": x["metrics"]["Coverage@10"],
            "best_epoch": x["training"].get("best_epoch"),
            "n_epochs": len(x["training"]["history"]),
            "train_time_h": x["training"].get("train_time_h"),
        }
        for b in (1, 2, 3):
            for m in ("HR@10", "NDCG@10", "Coverage@10"):
                rec[f"ubucket{b}_{m}"] = x["metrics"].get(f"ubucket{b}_{m}")
                rec[f"ibucket{b}_{m}"] = x["metrics"].get(f"ibucket{b}_{m}")
        flat.append(rec)
    pd.DataFrame(flat).sort_values(
        ["dataset", "optimizer", "hidden_units", "arm"]).to_csv(csv_path, index=False)
    print(f"saved: {csv_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=FIGURES_DIR / "param_scaling.png")
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    plot(args.out)


if __name__ == "__main__":
    main()
