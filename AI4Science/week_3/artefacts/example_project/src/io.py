"""Чтение и запись файлов проекта: действия, результат зависит от файлов на диске.

Используется в: src/report.py::make_table(), tests/test_physics.py.
"""
import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BAD_SERIES = {"2024-03"}  # неисправный термостат, см. data/README.md


def load_rates(path=ROOT / "data" / "raw" / "rates.csv", exclude=BAD_SERIES):
    """Измерения k(T) из data/raw/rates.csv; температура переводится в кельвины.

    Возвращает: (series, T_K, k) — массивы numpy одной длины.
    Данные: столбцы и единицы описаны в data/README.md.
    Проверка: tests/test_physics.py::test_load_rates_kelvin_and_exclusion.
    """
    series, T, k = [], [], []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["series"] in exclude:
                continue
            series.append(row["series"])
            T.append(float(row["T_C"]) + 273.15)
            k.append(float(row["k_s"]))
    return np.array(series), np.array(T), np.array(k)


def save_table(path, header, rows):
    """Запись таблицы CSV; папка создаётся при необходимости.

    Используется в: src/report.py::make_table().
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
