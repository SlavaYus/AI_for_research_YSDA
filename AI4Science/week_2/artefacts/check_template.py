"""Проверка результата для своего проекта: заготовка.

Положите файл в проект как checks/check.py и запускайте из корня проекта:
    python checks/check.py
Код возврата 0 — результат принят, 1 — нет. Эта команда записывается
в раздел 1 «Критерий готовности» файла AGENTS.md.

Ниже три вида проверок. Оставьте те, что подходят вашей задаче, и
подставьте свои имена файлов и числа. Правило: проверка считает эталон
сама или берёт его из источника, который агент не меняет, — и никогда
не доверяет словам агента о результате.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # корень проекта
RESULT = ROOT / "results" / "result.csv"            # файл, который должен создать агент
errors = []

# 1. Результат существует и имеет нужную форму.
if not RESULT.is_file():
    print(f"нет файла {RESULT.relative_to(ROOT)}")
    sys.exit(1)
rows = list(csv.DictReader(open(RESULT, encoding="utf-8")))
need = {"sample", "value"}                          # нужные столбцы
if not rows or not need <= set(rows[0]):
    errors.append(f"в результате нужны столбцы {sorted(need)}")

# 2. Число строк согласовано с исходными данными.
DATA = ROOT / "data" / "measurements.csv"           # исходные данные
if DATA.is_file():
    n_data = sum(1 for _ in open(DATA, encoding="utf-8")) - 1
    if len(rows) != n_data:
        errors.append(f"строк в результате {len(rows)}, в данных {n_data}")

# 3. Несколько значений совпадают с независимым пересчётом.
#    Эталон — ваш ручной расчёт, справочник или другой способ счёта.
REFERENCE = {"s1": 10.62, "s2": 3.14}               # образец: эталонные значения
TOL = 0.01                                          # допуск
got = {r.get("sample"): r.get("value") for r in rows}
for sample, ref in REFERENCE.items():
    try:
        if abs(float(got[sample]) - ref) > TOL:
            errors.append(f"{sample}: {got[sample]} вместо {ref} ± {TOL}")
    except (KeyError, TypeError, ValueError):
        errors.append(f"{sample}: нет числового значения в результате")

print("\n".join(errors) if errors else "принято")
sys.exit(1 if errors else 0)
