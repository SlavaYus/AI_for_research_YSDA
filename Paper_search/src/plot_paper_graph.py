"""Граф тематических связей: 5 отправных статей papers/ и 5 найденных arXiv-статей.

Инструмент недели 4 (networkx + matplotlib). Оформление по AGENT.md: толщина
границ узлов и рёбер — 2, штрихи длины 0 (сплошные линии).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
PLOTS = ROOT / "plots"
PLOTS.mkdir(exist_ok=True)

SEED = "#2196F3"    # отправные статьи
FOUND = "#4CAF50"   # найденные статьи

nodes = [
    ("AdamW\n1711.05101", "seed"),
    ("Shampoo\n1802.09568", "seed"),
    ("Muon\n2502.16982", "seed"),
    ("Hessian Structure\n2505.02809", "seed"),
    ("MuonRec\n2603.00416", "seed"),
    ("K-FAC\n1503.05671", "found"),
    ("Sophia\n2305.14342", "found"),
    ("SOAP\n2409.11321", "found"),
    ("Dissecting Hessian\n2010.04261", "found"),
    ("KF-QN\n2102.06737", "found"),
]

edges = [
    ("K-FAC\n1503.05671", "Shampoo\n1802.09568", "Кронекеровский предобусловливатель"),
    ("KF-QN\n2102.06737", "Shampoo\n1802.09568", "квазиньютон на Кронекере"),
    ("SOAP\n2409.11321", "Shampoo\n1802.09568", "Shampoo → Adam-базис"),
    ("SOAP\n2409.11321", "AdamW\n1711.05101", "спектральный предобусловливатель"),
    ("Sophia\n2305.14342", "AdamW\n1711.05101", "второй порядок против Adam"),
    ("Sophia\n2305.14342", "Muon\n2502.16982", "оптимизаторы LLM"),
    ("Dissecting Hessian\n2010.04261", "Hessian Structure\n2505.02809", "структура гессиана"),
    ("Dissecting Hessian\n2010.04261", "K-FAC\n1503.05671", "Кронекер = структура"),
    ("Hessian Structure\n2505.02809", "K-FAC\n1503.05671", "теория Кронекера"),
    ("Hessian Structure\n2505.02809", "KF-QN\n2102.06737", "блочная структура"),
    ("MuonRec\n2603.00416", "Muon\n2502.16982", "Muon для рекомендаций"),
]

G = nx.DiGraph()
for label, kind in nodes:
    G.add_node(label, kind=kind)
G.add_edges_from((s, t) for s, t, _ in edges)

pos = nx.spring_layout(G, k=1.1, iterations=200, seed=42)

fig, ax = plt.subplots(figsize=(13, 10))
colors = [SEED if k == "seed" else FOUND for _, k in nodes]

nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=3200,
                       edgecolors="black", linewidths=2, alpha=0.9)
nx.draw_networkx_edges(G, pos, width=2, arrows=True, arrowsize=18,
                       edge_color="#555555", style="solid", connectionstyle="arc3,rad=0.08")
nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

ax.set_title("Аппроксимация гессиана в оптимизации: отправные статьи и найденные arXiv",
             fontsize=14, fontweight="bold")
ax.axis("off")
plt.tight_layout()

out = PLOTS / "hessian_papers_graph.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
plt.close()
print(f"Граф сохранён: {out}")
print(f"Узлов: {G.number_of_nodes()}, рёбер: {G.number_of_edges()}")
