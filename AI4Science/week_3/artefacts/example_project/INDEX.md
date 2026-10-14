# INDEX.md — где что лежит

- `AGENTS.md` — правила работы агента в проекте.
- `STATUS.md` — где работа сейчас; читать в начале сессии.
- `diary.md` — журнал проекта; только дописывается.
- `data/README.md` — описание данных: столбцы, единицы, известные дефекты.
- `data/raw/rates.csv` — измерения k(T) по сериям; только чтение.
- `src/io.py` — чтение и запись файлов: `load_rates()`, `save_table()`.
- `src/physics.py` — формулы: `arrhenius()`, `fit_arrhenius()`.
- `src/report.py` — расчёт целиком, `make_table()`; пишет `results/arrhenius_fit.csv`.
- `tests/test_physics.py` — проверки формул и чтения данных.
- `results/` — результаты; каждый файл пишет один скрипт из `src/`.
