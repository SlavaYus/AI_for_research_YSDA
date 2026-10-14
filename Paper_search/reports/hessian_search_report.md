# Отчёт: 5 статей arXiv по аппроксимации гессиана в оптимизации

Дата: 2026-10-14
Инструменты: расширение `research` недели 5 (`openalex_search`, `openalex_work`,
`openalex_links`), обвязка недели 4 (заметки-источники). Все записи — arXiv-only
(фильтр OpenAlex `primary_location.source.id:S4306400194`).

## Отправная точка (papers/)

| arXiv | Работа | Роль |
|---|---|---|
| 1711.05101 | Loshchilov, Hutter. Decoupled Weight Decay Regularization (AdamW) | базовый адаптивный оптимизатор |
| 1802.09568 | Gupta, Koren, Singer. Shampoo: Preconditioned Stochastic Tensor Optimization | Кронекеровский предобусловливатель |
| 2502.16982 | Liu et al. Muon is Scalable for LLM Training | ортогонализующий оптимизатор для LLM |
| 2505.02809 | Dong, Zhang, Yao, Sun. Towards Quantifying the Hessian Structure of NN | структура гессиана |
| 2603.00416 | Shan et al. MuonRec | оптимизатор для генеративной рекомендации |

## Метод поиска

Запросы к `openalex_search` (английский), ограничение — источник arXiv:

1. `Hessian approximation optimizer neural network`
2. `second-order optimization neural network Hessian`
3. `Kronecker-factored approximate curvature K-FAC`
4. `diagonal Hessian adaptive optimizer language model`
5. `quasi-Newton deep learning optimizer`
6. `preconditioned stochastic optimization Shampoo`

Найдено 77 уникальных статей arXiv; полный список — `data/hessian_arxiv_candidates.json`.
Отобрано 5 — по тематической близости к отправным статьям и охвату разных способов
аппроксимации гессиана (полный Кронекер, диагональ, Кронекер+Adam, структура, квазиньютон).

## 5 найденных статей

### 1. K-FAC — arXiv:1503.05671
*Martens, Grosse. Optimizing Neural Networks with Kronecker-factored Approximate Curvature, 2015. Цит. 414.*
- OpenAlex: W2155894447, DOI 10.48550/arxiv.1503.05671, oa_status green.
- Аппроксимирует матрицу Фишера/гессиан Кронекеровским произведением блочных матриц и обращает её эффективно.
- **Связь:** классический предшественник Shampoo (1802.09568) — обе работы заменяют полный гессиан/Фишер произведением Кронекера; объясняет блочно-Кронекеровский взгляд, который эмпирически проверяет 2505.02809.
- Файл: `papers/1503.05671.pdf`.

### 2. Sophia — arXiv:2305.14342
*Liu, Li, Hall, Liang, Ma. Sophia: A Scalable Stochastic Second-order Optimizer for LM Pre-training, 2023. Цит. 28.*
- OpenAlex: W4378509498, DOI 10.48550/arxiv.2305.14342, oa_status green.
- Диагональная аппроксимация гессиана (оценка Гаусса–Ньютона–Гессиана с клиппингом) для предобучения LLM.
- **Связь:** второй порядок для трансформеров — конкурирует с AdamW (1711.05101) и предвосхищает мотивацию Muon (2502.16982); прямо опирается на наблюдения о структуре гессиана LLM (2505.02809).
- Файл: `papers/2305.14342.pdf`.

### 3. SOAP — arXiv:2409.11321
*Vyas et al. SOAP: Improving and Stabilizing Shampoo using Adam, 2024. Цит. 2.*
- OpenAlex: W4403707245, DOI 10.48550/arxiv.2409.11321, oa_status green.
- Запускает Shampoo-предобусловливание в eigenbasis и применяет Adam в этом базисе; снижает разрыв Shampoo↔Adam.
- **Связь:** прямое развитие Shampoo (1802.09568) и мост к AdamW (1711.05101); идея ортогонального/спектрального предобусловливания роднит его с Muon (2502.16982).
- Файл: `papers/2409.11321.pdf`.

### 4. Dissecting Hessian — arXiv:2010.04261
*Wu, Zhu, Wu, Wang, Ge. Dissecting Hessian: Understanding Common Structure of Hessian in NN, 2020. Цит. 9.*
- OpenAlex: W3092641135, DOI 10.48550/arxiv.2010.04261, oa_status green.
- Эмпирически показывает, что послойные гессианы разлагаются как Кронекерово произведение двух меньших матриц, и объясняет низкий ранг.
- **Связь:** эмпирическая основа для статьи-отправной точки 2505.02809, которая даёт теоретическое объяснение блочно-диагональной структуры гессиана; мотивирует Кронекеровские методы K-FAC и Shampoo.
- Файл: `papers/2010.04261.pdf`.

### 5. KF-QN — arXiv:2102.06737
*Ren, Bahamou, Goldfarb. Kronecker-factored Quasi-Newton Methods for Deep Learning, 2021. Цит. 1.*
- OpenAlex: W4287329019, DOI 10.48550/arxiv.2102.06737, oa_status green.
- Строит квазиньютоновское обновление в Кронекеровском базисе — сочетает L-BFGS с аппроксимацией гессиана по слоям.
- **Связь:** соединяет квазиньютоновскую (гессиановую) линию с Кронекеровским предобусловливанием Shampoo (1802.09568); его родственник по цитированию (KF-QN для CNN, W3132846247) прямо ссылается на Shampoo через `openalex_links`.
- Файл: `papers/2102.06737.pdf`.

## Как связаны (сводка)

- **Кронекеровская аппроксимация гессиана:** K-FAC (1503.05671) → Shampoo (seed) → KF-QN (2102.06737) → SOAP (2409.11321).
- **Структура гессиана:** Dissecting Hessian (2010.04261) даёт эмпирику, Hessian Structure (seed 2505.02809) — теорию; обе мотивируют K-FAC и Shampoo.
- **Диагональная аппроксимация / второй порядок для LLM:** Sophia (2305.14342) рядом с AdamW (seed) и Muon (seed).

## Проверка

1. Запуск поиска и отбора:
   - `python3 src/find_hessian_papers.py` — список кандидатов arXiv и `data/hessian_arxiv_candidates.json`;
   - `python3 src/select_hessian_five.py` — 5 записей и `data/hessian_five.json`.
2. Независимая сверка заголовков PDF:
   `for id in 1503.05671 2305.14342 2409.11321 2010.04261 2102.06737; do pdftotext -f 1 -l 1 papers/$id.pdf - | head -3; done`
   — совпадают с названиями из OpenAlex.
3. Идентификаторы: `jq -r '.[] | "\(.arxiv_id) \(.openalex_id) \(.doi)"' data/hessian_five.json`.
4. Связь KF-QN↔Shampoo: `openalex_links` для Shampoo (W2788190072), relation `cited_by`.

## Ограничения

- OpenAlex неполно индексирует ссылки свежих arXiv-препринтов (у 2505.02809 — 0 цитирований),
  поэтому связи установлены по тематике и проверены по аннотациям/заголовкам, а не по графу цитирований.
- Числа `cited_by` — из OpenAlex на 2026-10-14 и занижены для препринтов.
