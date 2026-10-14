#!/usr/bin/env python3
"""Линейная регрессия ln k от 1/T по трём сериям (2024-01, 2024-02, 2024-04).
Серия 2024-03 исключена (неисправный термостат).
Выводит коэффициенты, R^2 и E_a в кДж/моль."""
import numpy as np
import csv

R = 8.314462618  # Дж/(моль·К)

rows = []
with open('data/raw/rates.csv') as f:
    for r in csv.DictReader(f):
        rows.append(r)

# исключаем серию 2024-03
sel = [r for r in rows if r['series'] != '2024-03']
T = np.array([float(r['T_C']) + 273.15 for r in sel])   # К
k = np.array([float(r['k_s']) for r in sel])             # с^-1

x = 1.0 / T
y = np.log(k)

# МНК: y = a + b*x
n = len(x)
b = (n*np.sum(x*y) - np.sum(x)*np.sum(y)) / (n*np.sum(x*x) - np.sum(x)**2)
a = (np.sum(y) - b*np.sum(x)) / n

yhat = a + b*x
ss_res = np.sum((y - yhat)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - ss_res/ss_tot

Ea = -b * R / 1000.0  # кДж/моль

print(f"точек: {n}")
print(f"a (ln A) = {a:.6f}")
print(f"b (наклон) = {b:.6f} K")
print(f"R^2 = {r2:.6f}")
print(f"E_a = {Ea:.3f} кДж/моль")

with open('results/fit.txt', 'w') as f:
    f.write(f"точек: {n}\n")
    f.write(f"a (ln A) = {a:.6f}\n")
    f.write(f"b (наклон) = {b:.6f} K\n")
    f.write(f"R^2 = {r2:.6f}\n")
    f.write(f"E_a = {Ea:.3f} кДж/моль\n")