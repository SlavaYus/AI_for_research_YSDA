# Журнал

## 2026-10-14

Запрос: «Найди в Arxiv 5 статей по оптимизации с использованием аппроксимации гессиана
или просто статьи по аппроксимации гессиана. Для отправной точки используй статьи из
papers. Для поиска используй инструменты из week4 и week5».

Что сделано:
- определил отправные статьи в `papers/` (AdamW 1711.05101, Shampoo 1802.09568, Muon
  2502.16982, Hessian Structure 2505.02809, MuonRec 2603.00416) чтением PDF (`pdftotext`);
- поиск инструментом недели 5 (`openalex_search`/`openalex_work`/`openalex_links` из
  `week_5/artefacts/research_mcp.py`) с фильтром arXiv (`primary_location.source.id:S4306400194`);
- скрипты: `src/find_hessian_papers.py` (77 кандидатов), `src/select_hessian_five.py`
  (отбор 5 + выгрузка PDF);
- отчёт `reports/hessian_search_report.md`, память `memory/2026-10-14_hessian_search.md`.

Результат: 5 статей arXiv по аппроксимации гессиана, скачаны в `papers/`:
1503.05671 (K-FAC), 2305.14342 (Sophia), 2409.11321 (SOAP), 2010.04261 (Dissecting
Hessian), 2102.06737 (KF-QN). Связи с отправными статьями описаны в отчёте.

Точка проверки: `python3 src/find_hessian_papers.py` и `python3 src/select_hessian_five.py`;
сверка заголовков `pdftotext -f 1 -l 1 papers/<id>.pdf`.

Итог проверки: заголовки в PDF совпали с метаданными OpenAlex; `data/hessian_five.json`
содержит 5 записей с DOI `10.48550/arxiv.*`.
