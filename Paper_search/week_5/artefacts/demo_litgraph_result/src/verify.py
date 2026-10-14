#!/usr/bin/env python3
"""Независимый пересчёт E_a: двухточечная формула Аррениуса
ln(k2/k1) = -Ea/R * (1/T2 - 1/T1) по крайним точкам каждой серии
(2024-01, 2024-02, 2024-04). Серия 2024-03 исключена."""
import numpy as np
import csv

R = 8.314462618  # Дж/(моль·К)

rows = []
with open('data/raw/rates.csv') as f:
    for r in csv.DictReader(f):
        rows.append(r)

sel = [r for r in rows if r['series'] != '2024-03']
series = sorted(set(r['series'] for r in sel))

print("Двухточечный пересчёт E_a по крайним точкам каждой серии:")
print(f"{'серия':<10}{'E_a, кДж/моль':>16}")
vals = []
for s in series:
    pts = sorted([r for r in sel if r['series'] == s], key=lambda r: float(r['T_C']))
    lo, hi = pts[0], pts[-1]
    T1 = float(lo['T_C']) + 273.15
    T2 = float(hi['T_C']) + 273.15
    k1 = float(lo['k_s']); k2 = float(hi['k_s'])
    Ea = -R * np.log(k2/k1) / (1/T2 - 1/T1) / 1000.0
    vals.append(Ea)
    print(f"{s:<10}{Ea:>16.3f}")

mean = np.mean(vals)
lo = min(vals); hi = max(vals)
print(f"\nсреднее по сериям: {mean:.3f} кДж/моль")
print(f"диапазон: {lo:.3f} – {hi:.3f} кДж/моль")

with open('results/verify.txt', 'w') as f:
    f.write("Двухточечный пересчёт E_a по крайним точкам каждой серии:\n")
    for s, v in zip(series, vals):
        f.write(f"{s}: {v:.3f} кДж/моль\n")
    f.write(f"среднее: {mean:.3f} кДж/моль\n")
    f.write(f"диапазон: {lo:.3f} – {hi:.3f} кДж/моль\n")