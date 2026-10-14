"""Формулы проекта: вычисления, результат зависит только от аргументов."""
import numpy as np

R = 8.314462618  # Дж/(моль·К)


def arrhenius(T, A, Ea):
    """Константа скорости по закону Аррениуса: k = A·exp(-Ea/(R·T)).

    T в кельвинах, Ea в Дж/моль, A и k в с^-1.
    Проверка: tests/test_physics.py::test_arrhenius_known_value.
    """
    return A * np.exp(-Ea / (R * np.asarray(T, dtype=float)))


def fit_arrhenius(T, k):
    """Аппроксимация k(T) законом Аррениуса: линейная регрессия ln k по 1/T; T в кельвинах.

    Возвращает: Ea (Дж/моль), погрешность Ea, ln A, погрешность ln A, число точек.
    Данные: массивы из src/io.py::load_rates().
    Проверка: tests/test_physics.py::test_known_activation_energy.
    Используется в: src/report.py::make_table().
    """
    x = 1.0 / np.asarray(T, dtype=float)
    y = np.log(np.asarray(k, dtype=float))
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    cov = (resid @ resid / (n - 2)) * np.linalg.inv(X.T @ X)
    lnA, slope = coef
    lnA_err, slope_err = np.sqrt(np.diag(cov))
    return -slope * R, slope_err * R, lnA, lnA_err, n
