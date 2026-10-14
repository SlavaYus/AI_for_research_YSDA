"""Linear Arrhenius fit: ln k = ln A - E_a/(R T) over series 2024-01, 2024-02, 2024-04.

Excludes series 2024-03 (faulty thermostat). Writes results/fit_arrhenius.csv.
"""
from pathlib import Path
import csv

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "rates.csv"
OUT = ROOT / "results"
R = 8.314462618  # J/(mol K)

INCLUDE = {"2024-01", "2024-02", "2024-04"}


def load_series() -> list[tuple[float, float]]:
    """Return (T_K, k) pairs for included series."""
    points: list[tuple[float, float]] = []
    with RAW.open() as f:
        for row in csv.DictReader(f):
            if row["series"] in INCLUDE:
                t_c = float(row["T_C"])
                k = float(row["k_s"])
                points.append((t_c + 273.15, k))
    return points


def main() -> None:
    points = load_series()
    x = np.array([1.0 / t for t, _ in points])
    y = np.array([np.log(k) for _, k in points])

    # least squares: y = a + b*x, b = -E_a/R
    n = len(x)
    sx, sy = x.sum(), y.sum()
    sxx = (x * x).sum()
    sxy = (x * y).sum()
    b = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    a = (sy - b * sx) / n

    y_pred = a + b * x
    ss_res = ((y - y_pred) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1.0 - ss_res / ss_tot

    e_a_kj = -b * R / 1000.0

    OUT.mkdir(exist_ok=True)
    with (OUT / "fit_arrhenius.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quantity", "value", "unit"])
        w.writerow(["E_a", f"{e_a_kj:.3f}", "kJ/mol"])
        w.writerow(["ln A", f"{a:.3f}", "ln(1/s)"])
        w.writerow(["R2", f"{r2:.6f}", "-"])
        w.writerow(["n_points", str(n), "-"])

    print(f"E_a = {e_a_kj:.3f} kJ/mol")
    print(f"ln A = {a:.3f}")
    print(f"R^2 = {r2:.6f}")
    print(f"n = {n} points (series {sorted(INCLUDE)})")


if __name__ == "__main__":
    main()