# AI4Science — курс ШАД «ИИ-ассистенты для исследователя»

Репозиторий студента Юупова Вячеслава курса ШАД «ИИ-ассистенты для исследователя. AI4Science» (осень 2026).

## Структура

| Папка | Описание |
|---|---|
| [AI4Science/](AI4Science/) | Учебный проект: консольный агент AI4Science — обёртка над Goose с MCP-инструментами для научного рабочего процесса (код, PDF, поиск, Lean 4) |
| [Paper_search/](Paper_search/) | Исследование: поиск научных статей по оптимизаторам с аппроксимацией гессиана для трансформерных рекомендательных систем |
| [SASRec_exp/](SASRec_exp/) | Исследование: сравнение оптимизаторов (AdamW vs Muon), глубины SASRec и Lipschitz-регуляризации на датасетах Beauty и Yambda |

## AI4Science

Консольный агент для курса ШАД. Инференс через Yandex AI Studio, инструменты через MCP:

- **Lean 4** — проверка доказательств (`lean_check`), поиск лемм в Mathlib (4 движка)
- **Сеть** — веб-поиск (Brave / DuckDuckGo), скачивание и чтение PDF
- **Skills** — модульные руководства по темам (python, latex, lean, literature, debug-loop)
- **Бюджет** — учёт токенов, суточный лимит, авто-сжатие истории

Установка: `setup.sh` (Linux/macOS) или `setup.bat` (Windows). Документация — в [AI4Science/README.md](AI4Science/README.md) и [AI4Science/docs/ARCHITECTURE.md](AI4Science/docs/ARCHITECTURE.md).

## Paper_search

Поиск и отбор статей по оптимизаторам с использованием аппроксимации гессиана для рекомендательных систем.

- **Отправные статьи**: AdamW, Shampoo, Muon, Hessian Structure, MuonRec
- **Найдены**: K-FAC, Sophia, SOAP, Dissecting Hessian, KF-QN
- **Код**: `src/find_hessian_papers.py`, `src/select_hessian_five.py`, `src/plot_paper_graph.py`
- **Данные**: `data/` (JSON-метаданные), `papers/` (PDF)

## SASRec_exp

Эксперименты с рекомендательной моделью SASRec:

- **Оптимизаторы**: AdamW (1D веса) vs Muon (2D веса attention/FFN) vs HybridMuonAdamW
- **Глубина**: 2 / 4 / 6 трансформерных блоков
- **Регуляризация**: Lipschitz-ограничение attention-слоев (spectral norm)
- **Датасеты**: Beauty (SemantID), Yambda
- **Метрики**: HR@10, NDCG@10, Coverage@10 (общие и по бакетам)
- **Код**: `src/` — модель, оптимизаторы, метрики, тренировка, эксперименты, визуализация

## Запуск

```bash
# AI4Science
cd AI4Science && ./setup.sh          # или setup.bat на Windows
ai4science                            # интерактивная сессия

# Paper_search
cd Paper_search && python src/find_hessian_papers.py

# SASRec_exp
cd SASRec_exp && CUDA_VISIBLE_DEVICES=5 python -m src.run_experiments --stage all
```