"""Генерация графиков спектров с обнаруженными пиками."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

DATA_DIR = Path("week_2/artefacts/test_projects/spectra_peaks/data")
RESULTS_DIR = Path("week_2/artefacts/test_projects/spectra_peaks/results")
RESULTS_DIR.mkdir(exist_ok=True)

# Загружаем ожидаемые пики
expected = np.genfromtxt(
    "week_2/artefacts/test_projects/spectra_peaks/checks/expected_peaks.csv",
    delimiter=",", skip_header=1, dtype=str
)
expected_dict = {}
for row in expected:
    expected_dict.setdefault(row[0], []).append((float(row[1]), float(row[2])))

# Загружаем результаты без AGENTS.md
without = np.genfromtxt(
    "week_2/artefacts/test_projects/run_without/results/peaks.csv",
    delimiter=",", skip_header=1, dtype=str
)
without_dict = {}
for row in without:
    without_dict.setdefault(row[0], []).append((float(row[1]), float(row[2])))

# Загружаем результаты с AGENTS.md
with_ = np.genfromtxt(
    "week_2/artefacts/test_projects/run_with/results/peaks.csv",
    delimiter=",", skip_header=1, dtype=str
)
with_dict = {}
for row in with_:
    with_dict.setdefault(row[0], []).append((float(row[1]), float(row[2])))

# Генерируем графики для каждого спектра
for sp_file in sorted(DATA_DIR.glob("spectrum_*.txt")):
    data = np.loadtxt(sp_file, skiprows=1)
    wl, intensity = data[:, 0], data[:, 1]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(wl, intensity, 'b-', linewidth=1, label='спектр')
    
    # Ожидаемые пики
    if sp_file.name in expected_dict:
        for center, fwhm in expected_dict[sp_file.name]:
            ax.axvline(center, color='green', linestyle='--', alpha=0.7, linewidth=1.5,
                      label=f'ожидание: {center:.1f} нм' if center == expected_dict[sp_file.name][0][0] else '')
    
    # Результаты без AGENTS.md
    if sp_file.name in without_dict:
        for center, fwhm in without_dict[sp_file.name]:
            ax.axvline(center, color='orange', linestyle=':', alpha=0.7, linewidth=1.5,
                      label=f'без AGENTS.md: {center:.1f} нм' if center == without_dict[sp_file.name][0][0] else '')
    
    # Результаты с AGENTS.md
    if sp_file.name in with_dict:
        for center, fwhm in with_dict[sp_file.name]:
            ax.axvline(center, color='red', linestyle='-.', alpha=0.7, linewidth=1.5,
                      label=f'с AGENTS.md: {center:.1f} нм' if center == with_dict[sp_file.name][0][0] else '')
    
    ax.set_xlabel('Длина волны, нм')
    ax.set_ylabel('Интенсивность')
    ax.set_title(f'{sp_file.name}')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    
    out_path = RESULTS_DIR / f'graph_{sp_file.stem}.png'
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  {out_path}")

# Сводная таблица сравнения
print("\n=== Сводная таблица ===")
print(f"{'Файл':<20} {'Ожидание':<20} {'Без AGENTS.md':<20} {'С AGENTS.md':<20}")
print("-" * 80)
for sp_file in sorted(DATA_DIR.glob("spectrum_*.txt")):
    exp = expected_dict.get(sp_file.name, [])
    w = without_dict.get(sp_file.name, [])
    wi = with_dict.get(sp_file.name, [])
    exp_str = ", ".join(f"{c:.1f}" for c, _ in exp)
    w_str = ", ".join(f"{c:.1f}" for c, _ in w)
    wi_str = ", ".join(f"{c:.1f}" for c, _ in wi)
    print(f"{sp_file.name:<20} {exp_str:<20} {w_str:<20} {wi_str:<20}")

print("\nГрафики сохранены в results/")