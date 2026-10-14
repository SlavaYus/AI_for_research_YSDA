"""Расчёт целиком: данные -> аппроксимация -> results/arrhenius_fit.csv.

Запуск из корня проекта: python -m src.report
"""
from src.io import ROOT, load_rates, save_table
from src.physics import fit_arrhenius

HEADER = ["Ea_kJ_mol", "Ea_err", "lnA", "lnA_err", "n_points"]


def make_table(out=ROOT / "results" / "arrhenius_fit.csv"):
    """Одна строка результата по всем допустимым сериям.

    Данные: src/io.py::load_rates() — серия 2024-03 исключена.
    Формула: src/physics.py::fit_arrhenius().
    Результат: results/arrhenius_fit.csv со столбцами HEADER.
    """
    _, T, k = load_rates()
    Ea, Ea_err, lnA, lnA_err, n = fit_arrhenius(T, k)
    row = [f"{Ea / 1000:.2f}", f"{Ea_err / 1000:.2f}", f"{lnA:.3f}", f"{lnA_err:.3f}", n]
    save_table(out, HEADER, [row])
    return dict(zip(HEADER, row))


if __name__ == "__main__":
    print(make_table())
