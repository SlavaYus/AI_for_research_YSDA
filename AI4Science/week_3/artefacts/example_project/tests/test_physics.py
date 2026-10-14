"""Проверки формул и чтения данных; ответ известен заранее.

Запуск из корня проекта: python -m pytest tests/ -q
"""
import numpy as np

from src.io import load_rates
from src.physics import arrhenius, fit_arrhenius


def test_arrhenius_known_value():
    # при Ea = 0 константа скорости равна A при любой температуре
    assert np.allclose(arrhenius([300.0, 400.0], 5.0, 0.0), 5.0)


def test_known_activation_energy():
    # синтетические данные без шума: аппроксимация возвращает заданные параметры
    T = np.linspace(290.0, 350.0, 7)
    k = arrhenius(T, 3.0e6, 52_000.0)
    Ea, _, lnA, _, n = fit_arrhenius(T, k)
    assert abs(Ea - 52_000.0) < 1.0
    assert abs(lnA - np.log(3.0e6)) < 1e-6
    assert n == 7


def test_load_rates_kelvin_and_exclusion():
    series, T, k = load_rates()
    assert "2024-03" not in set(series)
    assert T.min() > 273.15  # кельвины, не градусы Цельсия
    assert len(series) == len(T) == len(k) > 0
