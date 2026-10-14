"""Построение графа проекта из заметок demo_graph_test."""
import os
import re
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

ROOT = Path("/home/yusupov/Agent_shad/AI4Science/week_4/artefacts/demo_graph_test")
NOTES_DIR = ROOT / "notes"
TASKS_DIR = ROOT / "tasks"
ONTOLOGY_DIR = ROOT / "ontology"
PLOTS_DIR = Path("/home/yusupov/Agent_shad/AI4Science/week_4/plots")
PLOTS_DIR.mkdir(exist_ok=True)

# Собираем все узлы и связи
G = nx.DiGraph()

# Добавляем узлы из заметок
note_files = list(NOTES_DIR.glob("*.md")) + list(TASKS_DIR.glob("*.md"))

for nf in note_files:
    name = nf.stem
    G.add_node(name, source='note' if 'notes' in str(nf) else 'task')
    
    # Читаем связи
    content = nf.read_text(encoding='utf-8')
    
    # Ищем ссылки вида [[Название]]
    links = re.findall(r'\[\[(.+?)\]\]', content)
    
    for link in links:
        # Пропускаем ссылки на классы в поле type
        if 'тип:' in content.split('## Связи')[0] if '## Связи' in content else '':
            continue
        
        # Проверяем, существует ли целевой узел
        target_exists = False
        for other_nf in note_files:
            if other_nf.stem == link:
                target_exists = True
                break
        
        if target_exists:
            G.add_edge(name, link)

# Добавляем узлы из ontology/
for of in ONTOLOGY_DIR.glob("*.md"):
    name = of.stem
    G.add_node(name, source='ontology')

# Добавляем узлы из файлов проекта (data, src, results, library)
for subdir in ['data', 'src', 'results', 'library']:
    subdir_path = ROOT / subdir
    if subdir_path.exists():
        for fp in subdir_path.rglob("*"):
            if fp.is_file():
                rel_path = fp.relative_to(ROOT)
                name = str(rel_path)
                G.add_node(name, source='file')

# Строим граф
plt.figure(figsize=(20, 16))

# Определяем цвета по типу узла
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# Цвета для разных типов узлов
colors = {
    'note': '#4CAF50',  # зелёный
    'task': '#FF9800',  # оранжевый
    'ontology': '#9E9E9E',  # серый
    'file': '#2196F3',  # синий
}

# Рисуем узлы
for node_type, color in colors.items():
    nodes = [n for n, d in G.nodes(data=True) if d.get('source') == node_type]
    if nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=color, 
                              node_size=800, alpha=0.8, edgecolors='black', linewidths=1)

# Рисуем рёбра
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, arrows=True, arrowsize=15)

# Рисуем подписи
labels = {node: node[:30] + '...' if len(node) > 30 else node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_weight='bold')

plt.title("Граф проекта demo_graph_test", fontsize=16, fontweight='bold')
plt.axis('off')
plt.tight_layout()

# Сохраняем
out_path = PLOTS_DIR / "graph_demo_graph_test.png"
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Граф сохранён: {out_path}")
print(f"Узлов: {G.number_of_nodes()}, Рёбер: {G.number_of_edges()}")

# Печатаем статистику
print("\nСтатистика:")
print(f"  Узлов типа 'note': {sum(1 for n, d in G.nodes(data=True) if d.get('source') == 'note')}")
print(f"  Узлов типа 'task': {sum(1 for n, d in G.nodes(data=True) if d.get('source') == 'task')}")
print(f"  Узлов типа 'ontology': {sum(1 for n, d in G.nodes(data=True) if d.get('source') == 'ontology')}")
print(f"  Узлов типа 'file': {sum(1 for n, d in G.nodes(data=True) if d.get('source') == 'file')}")