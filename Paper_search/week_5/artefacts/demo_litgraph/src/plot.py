#!/usr/bin/env python3
"""График Аррениуса: ln k от 1/T по трём сериям (2024-01, 2024-02, 2024-04)
и прямая регрессии. Серия 2024-03 исключена."""
import numpy as np
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

rows = []
with open('data/raw/rates.csv') as f:
    for r in csv.DictReader(f):
        rows.append(r)

sel = [r for r in rows if r['series'] != '2024-03']
T = np.array([float(r['T_C']) + 273.15 for r in sel])
k = np.array([float(r['k_s']) for r in sel])
x = 1.0 / T
y = np.log(k)

# регрессия (как в fit.py)
n = len(x)
b = (n*np.sum(x*y) - np.sum(x)*np.sum(y)) / (n*np.sum(x*x) - np.sum(x)**2)
a = (np.sum(y) - b*np.sum(x)) / n

series = sorted(set(r['series'] for r in sel))
colors = {'2024-01': '#1f77b4', '2024-02': '#ff7f0e', '2024-04': '#2ca02c'}
for s in series:
    pts = [r for r in sel if r['series'] == s]
    xs = [1.0/(float(r['T_C'])+273.15) for r in pts]
    ys = [np.log(float(r['k_s'])) for r in pts]
    plt.scatter(xs, ys, label=s, color=colors[s], zorder=3)

xx = np.linspace(x.min(), x.max(), 100)
plt.plot(xx, a + b*xx, 'k--', label=f'регрессия, R² = 0.9993')
plt.xlabel('1/T, K⁻¹')
plt.ylabel('ln k')
plt.title('График Аррениуса: ln k от 1/T')
plt.legend()
plt.tight_layout()
plt.savefig('results/arrhenius_plot.png', dpi=150)
print('saved results/arrhenius_plot.png')