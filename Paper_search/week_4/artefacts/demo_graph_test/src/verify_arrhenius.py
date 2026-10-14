"""Independent E_a estimate: nonlinear fit k = A*exp(-E_a/(R*T)) by Gauss-Newton.

Uses the same three series (2024-01, 2024-02, 2024-04), excludes 2024-03.
Writes results/verify_arrhenius.csv.
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
    points: list[tuple[float, float]] = []
    with RAW.open() as f:
        for row in csv.DictReader(f):
            if row["series"] in INCLUDE:
                t_c = float(row["T_C"])
                k = float(row["k_s"])
                points.append((t_c + 273.15, k))
    return points


def gauss_newton(t: np.ndarray, k: np.ndarray, p0: np.ndarray,
                 max_iter: int = 100, tol: float = 1e-12) -> np.ndarray:
    """Fit p=[lnA, Ea] to k=A*exp(-Ea/(R*T)) by Gauss-Newton."""
    p = p0.copy()
    for _ in range(max_iter):
        lnA, Ea = p
        k_pred = np.exp(lnA - Ea / (R * t))
        r = k - k_pred
        # Jacobian of residual wrt [lnA, Ea]
        J = np.column_stack([-k_pred, k_pred / (R * t)])
        JtJ = J.T @ J
        Jtr = J.T @ r
        try:
            delta = np.linalg.solve(JtJ, -Jtr)
        except np.linalg.LinAlgError:
            delta = np.linalg.lstsq(JtJ, -Jtr, rcond=None)[0]
        p = p + delta
        if np.linalg.norm(delta) < tol:
            break
    return p


def main() -> None:
    points = load_series()
    t = np.array([t for t, _ in points])
    k = np.array([k for _, k in points])

    # initial guess from linear fit slope/intercept
    x = 1.0 / t
    y = np.log(k)
    b, a = np.polyfit(x, y, 1)
    p0 = np.array([a, -b * R])

    p = gauss_newton(t, k, p0)
    lnA, Ea = p

    # standard error from covariance (J^T J)^-1 * s^2
    k_pred = np.exp(lnA - Ea / (R * t))
    r = k - k_pred
    n = len(k)
    s2 = (r @ r) / (n - 2)
    J = np.column_stack([-k_pred, k_pred / (R * t)])
    cov = np.linalg.inv(J.T @ J) * s2
    e_a_err = np.sqrt(cov[1, 1]) / 1000.0  # kJ/mol

    e_a_kj = Ea / 1000.0

    OUT.mkdir(exist_ok=True)
    with (OUT / "verify_arrhenius.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quantity", "value", "unit"])
        w.writerow(["E_a", f"{e_a_kj:.3f}", "kJ/mol"])
        w.writerow(["E_a_err", f"{e_a_err:.3f}", "kJ/mol"])
        w.writerow(["ln A", f"{lnA:.3f}", "ln(1/s)"])
        w.writerow(["n_points", str(n), "-"])

    print(f"E_a = {e_a_kj:.3f} +/- {e_a_err:.3f} kJ/mol")
    print(f"ln A = {lnA:.3f}")
    print(f"n = {n} points")


if __name__ == "__main__":
    main()