"""Arrhenius plot: ln k vs 1/T for series 2024-01/02/04 with linear fit line.

Excludes series 2024-03 (faulty thermostat). Writes results/arrhenius_plot.png.
"""
from pathlib import Path
import csv

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "rates.csv"
OUT = ROOT / "results"
R = 8.314462618  # J/(mol K)

INCLUDE = {"2024-01", "2024-02", "2024-04"}
COLORS = {"2024-01": "#1f77b4", "2024-02": "#2ca02c", "2024-04": "#d62728"}


def load_series() -> dict[str, list[tuple[float, float]]]:
    """Return {series: [(T_K, k), ...]} for included series."""
    data: dict[str, list[tuple[float, float]]] = {}
    with RAW.open() as f:
        for row in csv.DictReader(f):
            if row["series"] in INCLUDE:
                t_c = float(row["T_C"])
                k = float(row["k_s"])
                data.setdefault(row["series"], []).append((t_c + 273.15, k))
    return data


def main() -> None:
    data = load_series()
    x_all = np.array([1.0 / t for pts in data.values() for t, _ in pts])
    y_all = np.array([np.log(k) for pts in data.values() for _, k in pts])

    # linear fit ln k = a + b*(1/T), b = -E_a/R
    b, a = np.polyfit(x_all, y_all, 1)

    x_fit = np.linspace(x_all.min(), x_all.max(), 200)
    y_fit = a + b * x_fit

    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    for series, pts in data.items():
        xs = [1.0 / t for t, _ in pts]
        ys = [np.log(k) for _, k in pts]
        ax.scatter(xs, ys, s=42, color=COLORS[series], label=f"серия {series}",
                   zorder=3, edgecolors="white", linewidths=0.5)
    ax.plot(x_fit, y_fit, color="black", lw=1.6, ls="--",
            label="линейный фит ln k = ln A − E_a/(RT)")

    ax.set_xlabel(r"$1/T$, K$^{-1}$")
    ax.set_ylabel(r"$\ln k$")
    ax.set_title("Закон Аррениуса: ln k от 1/T (25–70 °C)")
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=False)

    # secondary axis: temperature in °C
    ax2 = ax.secondary_xaxis("top", functions=(lambda x: 1.0 / x - 273.15,
                                               lambda t: 1.0 / (t + 273.15)))
    ax2.set_xlabel("T, °C")

    fig.tight_layout()
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "arrhenius_plot.png", dpi=150)
    print(f"saved {OUT / 'arrhenius_plot.png'}")
    print(f"fit: ln k = {a:.3f} + ({b:.3f})*(1/T), E_a = {-b*R/1000:.3f} kJ/mol")


if __name__ == "__main__":
    main()