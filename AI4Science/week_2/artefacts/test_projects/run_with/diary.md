
## 2026-10-13 23:00 — Пик-анализ спектров
- Написан `src/peaks.py`: линейный фон вычитается через polyfit, пики находятся через scipy.signal.find_peaks с prominence=0.1 и distance=10, фитинг — Gaussian + линейный фон через curve_fit.
- Результат: 9 пиков в `results/peaks.csv`.
- Проверка `checks/check_peaks.py`: принято.
