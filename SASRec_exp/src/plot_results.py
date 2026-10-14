"""Final barplot: NDCG@10 and Coverage@10.

One figure, 2 rows (datasets) x 2 columns (metrics). Within each panel the
x-axis groups are the optimizer/regularization combos — none, Lipschitz on
attention, Lipschitz on MLP, Lipschitz on both — shown in distinct colors;
the three bars inside each group are the transformer block counts (2/4/6)
shown in increasingly darker shades of the group color.

Older result files (attention-only era) carry a boolean `lipschitz` field and
are mapped to mode 'attn'; newer files carry `lipschitz_mode`.

Usage: python -m src.plot_results [--out figures/metrics_barplot.png]
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.configs import FIGURES_DIR, NUM_BLOCKS, RESULTS_DIR

REG_LABELS = {
    "none": "",
    "attn": " + Lip(attn)",
    "mlp": " + Lip(MLP)",
    "attn+mlp": " + Lip(attn+MLP)",
}
COMBOS = [
    ("adamw", "none", "AdamW"),
    ("muon", "none", "Muon"),
    ("adamw", "attn", "AdamW + Lip(attn)"),
    ("muon", "attn", "Muon + Lip(attn)"),
    ("adamw", "mlp", "AdamW + Lip(MLP)"),
    ("muon", "mlp", "Muon + Lip(MLP)"),
    ("adamw", "attn+mlp", "AdamW + Lip(attn+MLP)"),
    ("muon", "attn+mlp", "Muon + Lip(attn+MLP)"),
]
COMBO_COLORS = {
    "AdamW": "#4C72B0",
    "Muon": "#DD8452",
    "AdamW + Lip(attn)": "#55A868",
    "Muon + Lip(attn)": "#C44E52",
    "AdamW + Lip(MLP)": "#8172B3",
    "Muon + Lip(MLP)": "#937860",
    "AdamW + Lip(attn+MLP)": "#45A29E",
    "Muon + Lip(attn+MLP)": "#CCB974",
}
BLOCK_SHADES = {2: 0.55, 4: 0.3, 6: 0.0}  # light -> full color


def _lighten(color, amount):
    """Blend color towards white by `amount` in [0, 1] (0 = unchanged)."""
    rgb = matplotlib.colors.to_rgb(color)
    return tuple(c + (1 - c) * amount for c in rgb)


def reg_mode_of(record):
    mode = record.get("lipschitz_mode")
    if mode:
        return mode
    return "attn" if record.get("lipschitz") else "none"


def load_results():
    rows = []
    for path in sorted(RESULTS_DIR.glob("*.json")):
        with open(path) as f:
            data = json.load(f)
        if not data.get("metrics"):
            continue
        data["reg_mode"] = reg_mode_of(data)
        rows.append(data)
    return rows


def plot(out_path):
    rows = load_results()
    datasets = sorted({r["dataset"] for r in rows})
    metrics = [("NDCG@10", "NDCG@10"), ("Coverage@10", "Coverage@10")]

    if not rows:
        raise SystemExit("no results found in results/")

    fig, axes = plt.subplots(len(datasets), len(metrics),
                             figsize=(18, 4.8 * len(datasets)),
                             squeeze=False)

    for r, row in enumerate(datasets):
        for c, (metric_key, metric_title) in enumerate(metrics):
            ax = axes[r][c]
            group_width = 0.78
            n_blocks = len(NUM_BLOCKS)
            bar_w = group_width / n_blocks
            xs = np.arange(len(COMBOS))

            for b_i, blocks in enumerate(NUM_BLOCKS):
                heights, labels = [], []
                for optimizer, reg, label in COMBOS:
                    match = [x for x in rows
                             if x["dataset"] == row and x["optimizer"] == optimizer
                             and x["num_blocks"] == blocks
                             and x["reg_mode"] == reg]
                    if match:
                        heights.append(match[0]["metrics"][metric_key])
                        labels.append(f"{match[0]['metrics'][metric_key]:.4f}")
                    else:
                        heights.append(None)
                        labels.append("")
                offsets = (b_i - (n_blocks - 1) / 2) * bar_w
                for g_i, (optimizer, reg, label) in enumerate(COMBOS):
                    h = heights[g_i]
                    if h is None:
                        continue
                    color = _lighten(COMBO_COLORS[label], BLOCK_SHADES[blocks])
                    x = xs[g_i] + offsets
                    ax.bar(x, h, width=bar_w * 0.92, color=color,
                           edgecolor="black", linewidth=0.4)
                    ax.text(x, h, labels[g_i], ha="center", va="bottom",
                            fontsize=6.5, rotation=90)

            ax.set_xticks(xs)
            ax.set_xticklabels([lbl for _, _, lbl in COMBOS], fontsize=8,
                               rotation=20, ha="right")
            dataset_name = next(x["dataset_name"] for x in rows if x["dataset"] == row)
            ax.set_title(f"{dataset_name}: {metric_title}", fontsize=11)
            ax.set_ylabel(metric_title)
            ax.grid(axis="y", alpha=0.3, linestyle="--")
            vals = [x["metrics"][metric_key] for x in rows if x["dataset"] == row]
            ymax = max(vals) if vals else 0.0
            ax.set_ylim(0, ymax * 1.18 if ymax else 1.0)

    handles = []
    for blocks in NUM_BLOCKS:
        handles.append(plt.Rectangle((0, 0), 1, 1,
                                     facecolor="white", edgecolor="black",
                                     label=f"{blocks} blocks"))
    for _, _, label in COMBOS:
        handles.append(plt.Rectangle((0, 0), 1, 1, facecolor=COMBO_COLORS[label],
                                     edgecolor="black", label=label))
    fig.legend(handles=handles, loc="upper center", ncol=11, fontsize=8.5,
               frameon=False, bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.96 if len(datasets) > 1 else 0.93))
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    print(f"saved: {out_path}")

    csv_path = out_path.with_suffix(".csv")
    flat = []
    for x in rows:
        rec = {
            "dataset": x["dataset_name"], "optimizer": x["optimizer"],
            "num_blocks": x["num_blocks"], "lipschitz_mode": x["reg_mode"],
            "HR@10": x["metrics"]["HR@10"],
            "NDCG@10": x["metrics"]["NDCG@10"],
            "Coverage@10": x["metrics"]["Coverage@10"],
            "best_epoch": x["training"].get("best_epoch"),
            "n_epochs": len(x["training"].get("history", [])),
            "train_time_h": x["training"].get("train_time_h"),
        }
        for b in (1, 2, 3):
            for m in ("HR@10", "NDCG@10", "Coverage@10"):
                rec[f"ubucket{b}_{m}"] = x["metrics"].get(f"ubucket{b}_{m}")
                rec[f"ibucket{b}_{m}"] = x["metrics"].get(f"ibucket{b}_{m}")
        flat.append(rec)
    pd.DataFrame(flat).sort_values(
        ["dataset", "optimizer", "lipschitz_mode", "num_blocks"]).to_csv(csv_path, index=False)
    print(f"saved: {csv_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=FIGURES_DIR / "metrics_barplot.png")
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    plot(args.out)


if __name__ == "__main__":
    main()
