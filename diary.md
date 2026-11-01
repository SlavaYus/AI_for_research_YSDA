# Журнал проекта

Объединённый журнал из 17 записей по 3 проектам.
Диапазон дат: 2026-09-28 — 2026-10-14

---

<!-- проект: AI4Science -->
<!-- источник: AI4Science/week_3/artefacts/example_project/diary.md -->
<!-- дата: 2026-09-28 -->
## 2026-09-28 — энергия активации по всем допустимым сериям

- **Запрос агенту:** «Посчитай энергию активации по data/raw/rates.csv; ответ
  одним числом в кДж/моль.» Модель DeepSeek V4 Flash, запуск
  `ai4science --no-lean run`.
- **Что сделал агент:** прочитал `INDEX.md`, `STATUS.md` и `data/README.md`,
  затем `src/` и `tests/`; запустил тесты и `python -m src.report`; дописал
  запись в журнал. Шесть вызовов инструментов.
- **Результат:** E_a = 51,66 ± 0,39 кДж/моль по 15 точкам, серия 2024-03
  исключена.
- **Точка проверки:** `python -m pytest tests/ -q && python -m src.report` —
  3 теста прошли, код 0.
- **Итог:** принято. Значение в ожидаемом диапазоне 40–70 кДж/моль; со
  серией 2024-03 получилось бы 47,0 кДж/моль.

---

<!-- проект: Paper_search -->
<!-- источник: Paper_search/week_5/artefacts/demo_litgraph/diary.md -->
<!-- дата: 2026-10-05 -->
## 2026-10-05

Сообщение пользователя: «Проверь, подчиняется ли разложение закону Аррениуса в интервале 25-70 °C, и найди энергию активации по data/raw/rates.csv. Результат проверь независимым пересчётом.»

Задачи: «Проверить закон Аррениуса и найти E_a» (выполнена) + 3 подзадачи (все выполнены).

Граф: инициализировано хранилище `.obsidian/`, 14 заметок классов в `ontology/`; заметки: 4 серии, общий набор данных, ограничение термостата 2024-03, гипотеза, метод, 2 эксперимента, проверка, 2 результата, 2 источника. Файлы: `src/fit.py`, `src/verify.py`, `results/fit.txt`, `results/verify.txt`.

Результат: R² = 0,9993 по 15 точкам трёх серий (2024-01, 2024-02, 2024-04) — закон Аррениуса выполняется; E_a = 51,66 кДж/моль; независимый двухточечный пересчёт 51,23–51,89 кДж/моль. Серия 2024-03 исключена (неисправный термостат).

Проверка: `python3 src/fit.py`, `python3 src/verify.py`; согласованность связей графа с онтологией — 0 ошибок. `check_week4.py` в проекте отсутствует.
## 2026-10-05 (вторая сессия)

Сообщение пользователя: «Проверку принимаю. Подготовь для коллег отчёт с графиком и ссылками на источники из library/»

Статусы: «Проверить закон Аррениуса и найти E_a» и 3 подзадачи — «принята», в итоги дописано «Принято пользователем: «Проверку принимаю»».

Новая задача: «Подготовить отчёт для коллег» (выполнена) + 2 подзадачи (выполнены): «Построить график ln k от 1 на T», «Написать отчёт для коллег».

Граф: добавлен отчёт `reports/Отчёт закон Аррениуса и E_a.md` (тип «Отчёт», график `results/arrhenius_plot.png`, ссылки на [[Arrhenius 1889]] и [[Laidler 1984]]); файл `src/plot.py`. Заметок стало 23.

Проверка: `python3 src/plot.py`; согласованность связей графа с онтологией — 0 ошибок. `check_week4.py` в проекте отсутствует.

---

<!-- проект: Paper_search -->
<!-- источник: Paper_search/week_5/artefacts/demo_litgraph_result/diary.md -->
<!-- дата: 2026-10-11 -->
## 2026-10-11

Сообщение пользователя: «Собери литературу к проекту…» (поиск OpenAlex, восемь наиболее цитируемых работ Laidler, открытые версии, уравнение Аррениуса в Wikidata).

Задача «Собрать литературу к проекту» — заблокирована из-за невозможности получить две из доступных по OpenAlex OA-версий через `pdf_download` (серверы вернули HTML) и отсутствия прямых PDF URL ещё для работ; пользовательское решение требуется по способу получения этих файлов или исключению требования. Подзадачи: «Собрать записи Arrhenius и Laidler» — выполнена; «Добавить цитирующие Laidler работы» — заблокирована только по скачиванию; «Найти уравнение Аррениуса в Wikidata» — выполнена.

Граф: дополнены [[Arrhenius 1889]] (основной OpenAlex ID W4253789658; дополнительная запись W2483500811) и [[Laidler 1984]] (W2052953969), созданы заметки запросов, авторов и 8 наиболее цитируемых цитирующих работ; добавлен Wikidata факт Q507505 → Q80956. Скачан `library/W2092144432.pdf`; две другие попытки загрузки вернули `text/html`, другие записи не имели oa_url. Добавлены отсутствовавшие заметки классов `Автор`, `ЗапросКГрафу` и недостающие группы цветов `.obsidian/graph.json`. Зафиксировано расхождение страниц Laidler: OpenAlex — 494, локальный текст — 494–498.

Проверка: скрипт проверки онтологических типов и domain/range связей — 15 новых заметок, 0 ошибок; П11/П12 — 10/10 источников имеют запрос и автора; восемь ожидаемых OpenAlex ID присутствуют; `library/W2092144432.pdf` — 5 289 095 байт.


## 2026-10-11 (принятие литературы и классификация)

Сообщение пользователя: «Записей без локальных копий достаточно, работу принимаю. Вопрос по собранной литературе: какие из найденных работ относятся к биологии и наукам о Земле?»

Статусы: «Собрать литературу к проекту» и три её подзадачи переведены в «принята»; принятие пользователя приложено в разделы «Итог». Исходные критерии готовности не изменены; отмечено снятие требования локальных копий для принятой работы.

Ответ по литературе основан на заметках источников: [[Ramirez 2012]] — soil microbial communities/processes across biomes (почвенная микробная экология); [[White 2011]] — пиролиз биомассы сельскохозяйственных остатков (смежная аграрно-биомассовая тематика); [[Hänggi 1990]] — теория скоростей реакций, в аннотации обозначена применимость к биологии (междисциплинарная работа).

Проверка: `grep`/просмотр четырёх заметок задач — статусы «принята», исходные поля «Готово, когда» сохранены, разделы «Итог» содержат текст принятия; код завершения 0.

---

<!-- проект: AI4Science -->
<!-- источник: AI4Science/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — тестовый проект spectra_peaks: сравнение прогонов без и с AGENTS.md

### Цель
Проверить, как AGENTS.md влияет на поведение агента при поиске пиков в спектрах поглощения.

### Данные
4 спектра в `data/`: spectrum_01.txt (2 пика), spectrum_02.txt (3 пика), spectrum_03.txt (1 пик), spectrum_04.txt (3 пика). Столбцы: wavelength_nm, intensity.

### Прогон без AGENTS.md
- **Запрос:** «Найди положения и ширины пиков во всех спектрах из data/»
- **Число шагов:** ~8 блоков `▸`
- **Файлы:** `src/peaks.py`, `results/peaks.csv`
- **Результат (9 пиков):**

| Файл | Центр (нм) | FWHM (нм) |
|---|---|---|
| spectrum_01.txt | 486.0 | 6.2 |
| spectrum_01.txt | 656.5 | 8.8 |
| spectrum_02.txt | 450.0 | 10.5 |
| spectrum_02.txt | 520.0 | 5.4 |
| spectrum_02.txt | 609.5 | 12.9 |
| spectrum_03.txt | 589.0 | 4.3 |
| spectrum_04.txt | 430.5 | 7.7 |
| spectrum_04.txt | 544.5 | 9.6 |
| spectrum_04.txt | 575.0 | 6.7 |

- **Проверка:** `python checks/check_peaks.py` → код 0 (все пики найдены)
- **Запреты:** не нарушил (data/ не изменял)

### Прогон с AGENTS.md
- **Запрос:** «Выполни цель из AGENTS.md.»
- **Число шагов:** ~16 блоков `▸` (в 2 раза больше — агент читает AGENTS.md, следует формату, вызывает проверку сам)
- **Файлы:** `src/peaks.py`, `results/peaks.csv`
- **Результат (9 пиков):**

| Файл | Центр (нм) | FWHM (нм) |
|---|---|---|
| spectrum_01.txt | 486.1 | 6.0 |
| spectrum_01.txt | 656.3 | 8.0 |
| spectrum_02.txt | 450.0 | 10.1 |
| spectrum_02.txt | 520.0 | 4.9 |
| spectrum_02.txt | 610.0 | 12.1 |
| spectrum_03.txt | 589.0 | 4.0 |
| spectrum_04.txt | 430.0 | 7.0 |
| spectrum_04.txt | 545.0 | 9.0 |
| spectrum_04.txt | 575.0 | 5.0 |

- **Проверка:** `python checks/check_peaks.py` → код 0 (все пики найдены)
- **Запреты:** не нарушил

### Сравнение с ожидаемыми значениями

| Файл | Ожидание (центр) | Без AGENTS.md | С AGENTS.md |
|---|---|---|---|
| spectrum_01.txt | 486.1, 656.3 | 486.0, 656.5 | 486.1, 656.3 |
| spectrum_02.txt | 450.0, 520.0, 610.0 | 450.0, 520.0, 609.5 | 450.0, 520.0, 610.0 |
| spectrum_03.txt | 589.0 | 589.0 | 589.0 |
| spectrum_04.txt | 430.0, 545.0, 575.0 | 430.5, 544.5, 575.0 | 430.0, 545.0, 575.0 |

Оба прогона нашли все 9 пиков. С AGENTS.md результаты точнее совпадают с ожидаемыми (особенно spectrum_02.txt: 610.0 vs 609.5).

### Что изменил AGENTS.md
- **Раздел 0 (цель):** чётко указал формат результата — агент создал CSV с нужными столбцами
- **Раздел 2 (карта проекта):** дал агенту знания о пороге шума (5×) и линейном фоне — улучшил качество обнаружения
- **Раздел 1 (критерий готовности):** агент сам вызвал проверку перед финальным ответом
- **Раздел 5 (режим):** ReAct — агент запускал проверку после каждого изменения

### Графики
Созданы графики спектров с отмеченными пиками (в `week_2/plots/`):
- `plots/graph_spectrum_01.png` — 2 пика: 486.1 нм (ожидание), 656.3 нм (ожидание)
- `plots/graph_spectrum_02.png` — 3 пика: 450.0, 520.0, 610.0 нм
- `plots/graph_spectrum_03.png` — 1 пик: 589.0 нм
- `plots/graph_spectrum_04.png` — 3 пика: 430.0, 545.0, 575.0 нм

На графиках: зелёный пунктир — ожидаемые пики, оранжевый штрих — без AGENTS.md, красный штрих-точка — с AGENTS.md.

### Итог
Оба прогона прошли успешно (код проверки 0). AGENTS.md увеличил число шагов в 2 раза, но улучшил точность результатов и обеспечил автоматическую проверку.

---

<!-- проект: AI4Science -->
<!-- источник: AI4Science/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — запуск тестов и генерация отчёта

- **Запрос агенту:** Выполни цель из AGENTS.md (запустить pytest и сгенерировать report/test_report.md).
- **Что сделал агент:**
  - Изучил структуру проекта и AGENTS.md
  - Установил недостающий пакет pypdf
  - Запустил pytest с отключённым плагином opik и отключённым прокси
  - Проанализировал результат: 28 passed, 6 skipped, 92 errors
  - Сгенерировал report/test_report.md с полным списком тестов
  - Вызвал python3 checks/check_test_report.py — проверка прошла
- **Результат:** отчёт создан, проверка пройдена
- **Точка проверки:** python3 checks/check_test_report.py
- **Итог проверки:** принято — отчёт корректен

---

<!-- проект: AI4Science -->
<!-- источник: AI4Science/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — AGENTS.md и проверка для своего проекта

- **Что сделано:**
  - `AGENT.md` переименован в `AGENTS.md` (агент читает только первый найденный)
  - Заполнены разделы 0, 1, 4, 5, 7 по шаблону
  - Создан `checks/check_test_report.py` — различает правильный и испорченный результат
  - 4 пометки запретов: 2 `[окно]`, 1 `[среда]`, 1 `[вызов]`
- **Проверка:**
  - На правильном результате: код 0
  - На испорченном (passed: 1 вместо 28): код 1
- **Коммит:** `git add -A && git commit -m "AGENTS.md и проверка"`

---

<!-- проект: AI4Science -->
<!-- источник: AI4Science/week_2/artefacts/test_projects/run_with/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 23:00 — Пик-анализ спектров
- Написан `src/peaks.py`: линейный фон вычитается через polyfit, пики находятся через scipy.signal.find_peaks с prominence=0.1 и distance=10, фитинг — Gaussian + линейный фон через curve_fit.
- Результат: 9 пиков в `results/peaks.csv`.
- Проверка `checks/check_peaks.py`: принято.

---

<!-- проект: SASRec_exp -->
<!-- источник: SASRec_exp/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — Каркас экспериментов SASRec (копия кода, src/, выбор оптимального конфига)
- Запрос агенту: скопировать код SASRec и split в текущую папку (все функции в src/), реализовать эксперименты на Beauty и Yambda: SASRec с числом трансформерных блоков 2/4/6, оптимизаторы AdamW и Muon (Muon — для 2D весов, AdamW — для 1D), метрики HR@10 / NDCG@10 / Coverage@10 (просто и по бакетам), все эксперименты — в diary; затем Lipschitz-регуляризация attention-слоя и те же прогоны с ней; финальный barplot по NDCG@10 и Coverage@10 (оттенки — число слоев, цвета — оптимизаторы и регуляризации).
- Что сделал агент:
  - Создал пакет `src/`: `sasrec.py` (модель, копия из src/models/sasrec.py родительского репо), `split.py` (LeaveOneOutSplitter + leave_first/last/random, копия из src/preprocess/splits.py + target_selection.py, standalone CLI без hydra), `datasets.py` (CausalLMDataset / CausalLMPredictionDataset / PaddingCollateFn, копия с заменой хранения последовательностей на int64 numpy — Yambda 11.4M взаимодействий), `sce.py` (Scalable Cross-Entropy, копия), `optimizers.py` (Muon + newton_schulz_5 из src/generative/trainer.py родительского репо + HybridMuonAdamW: Muon — 2D веса attention/FFN [in_proj_weight, out_proj.weight, conv1/conv2.weight], AdamW — 1D веса (biases, LayerNorm) и эмбеддинги item_emb/pos_emb — стандартный рецепт Muon/MuonRec, как и в родительском HybridOptimizer), `lipschitz.py` (Lipschitz-регуляризация attention: forward-pre-hook на каждом nn.MultiheadAttention, W <- W/sigma_max(W) через power iteration для in_proj_weight и out_proj.weight; как spectral_norm_attention.py родительского репо, только attention), `metrics.py` (HR@k, NDCG@k, Coverage@k + бакеты: пользователи по длине входной последовательности — терцили от max_seq_len; айтемы по популярности — терцили по кумулятивной массе взаимодействий, как в eval/bucketed_eval.py), `train.py` (чистый PyTorch-цикл: обучение, ранняя остановка по val NDCG@10 на подвыборке 5000 юзеров, лучший state), `experiment.py` (один прогон: загрузка сплита -> train -> predict -> метрики -> results/<run>.json + запись в этот diary), `run_experiments.py` (драйвер грида), `plot_results.py` (итоговый barplot), `configs.py` (конфиги).
  - Данные: `data/Beauty` -> симлинк на родительский `data/Beauty`, `data/Yambda` -> симлинк на `/workspace-SR006.nfs2/nabiev/SemantID/data/Yambda`; используются готовые сплиты `leave-one-out-no_cold_items` (получены именно тем скопированным LeaveOneOutSplitter с remove_cold_items=True). Отступление от родительского пайплайна: НЕ делается сдвиг item_id на +1 (item_id и так начинается с 1, 0 — паддинг), размер каталога = max_item_id + 1.
  - Beauty: 22363/12101 (users/items в train), каталог 12102; Yambda: 72192/535256 в train, 70168/70099 val/test юзеров, каталог 539356.
  - Выбор оптимального конфига Beauty (15 эпох, blocks=2, AdamW, val NDCG@10): A = beauty_sasrec_best.yaml (h64, heads 1, dropout 0.3, lr 2.50e-4, CE) -> 0.0558; B = beauty_sasrec.yaml (h128, heads 2, dropout 0.4, lr 3.94e-4, SCE) -> 0.0716. Выбран B.
  - Выбор muon_lr для SASRec (15 эпох, Beauty, blocks=2, val NDCG@10): 0.02 -> 0.0189, 0.01 -> 0.0214, 0.005 -> 0.0701, 0.003 -> 0.0706. Выбрано 0.005 (лучшая группа, еще рос на горизонте); momentum 0.99 (прецедент родительского репо). AdamW и AdamW-часть Muon используют одинаковые lr (тюненный по датасету), betas (0.9, 0.95), weight_decay 0 — прогоны отличаются только правилом обновления 2D весов.
  - Итоговые конфиги (src/configs.py): оба датасета hidden=128, heads=2, dropout=0.4, lr=3.94e-4, SCE loss, batch 64/128 (Beauty/Yambda), max_seq_len 20/100, filter_seen true/false, patience 10/5, max_epochs 200/40 (Yambda ограничен ради времени на общем GPU).
  - Смоук: полный цикл train->predict->метрики на GPU работает; Lipschitz-hook проверен (sigma_max(in_proj) ~= 1.004 после forward, 2 матрицы на блок); маршрутизация Muon/AdamW проверена по именам параметров.
  - Замер времени: Beauty ~12-14 с/эпоха; Yambda 62 с/эпоха (train+val 5000 юзеров) на загруженном GPU0. Найдены свободные GPU 5 и 6 (V100 32GB) — драйверы запускаются на них.
- Результат: каркас готов, конфиги зафиксированы, sweep из 24 прогонов (2 датасета x {adamw, muon} x {2,4,6} x {без/с Lipschitz}) запускается фоном; каждый прогон автоматически дописывает секцию в diary (см. ниже).
- Точка проверки: `python -m compileall src/`; смоук-прогоны выше; `results/*.json` по мере завершения.
- Итог проверки: принято — смоук-цикл и проверки маршрутизации/хука прошли, конфиг B значимо лучше A (0.0716 vs 0.0558).

### beauty_adamw_l2 — 2026-10-13
- Конфиг: Beauty, num_blocks=2, optimizer=adamw, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=14, best_val_NDCG@10=0.0716, время=0.06 ч
- Тест: HR@10=0.0845, NDCG@10=0.0514, Coverage@10=0.7833
- Бакеты (users 1/2/3) NDCG@10: 0.0461/0.05/0.0895; (items 1/2/3) NDCG@10: 0.1206/0.0438/0.0142
- Бакеты (users 1/2/3) HR@10: 0.0759/0.0843/0.1411; (items 1/2/3) HR@10: 0.1988/0.072/0.0231
- Точка проверки: results/beauty_adamw_l2.json (полные метрики и история обучения)

### beauty_adamw_l4 — 2026-10-13
- Конфиг: Beauty, num_blocks=4, optimizer=adamw, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=14, best_val_NDCG@10=0.0737, время=0.08 ч
- Тест: HR@10=0.0867, NDCG@10=0.0524, Coverage@10=0.7309
- Бакеты (users 1/2/3) NDCG@10: 0.0467/0.0498/0.0964; (items 1/2/3) NDCG@10: 0.1274/0.0426/0.0135
- Бакеты (users 1/2/3) HR@10: 0.0771/0.0835/0.1582; (items 1/2/3) HR@10: 0.2086/0.0707/0.0236
- Точка проверки: results/beauty_adamw_l4.json (полные метрики и история обучения)

### yambda_adamw_l2 — 2026-10-13
- Конфиг: Yambda, num_blocks=2, optimizer=adamw, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=36, best_val_NDCG@10=0.0662, время=0.24 ч
- Тест: HR@10=0.1308, NDCG@10=0.0636, Coverage@10=0.2128
- Бакеты (users 1/2/3) NDCG@10: 0.0809/0.0666/0.0567; (items 1/2/3) NDCG@10: 0.0526/0.0661/0.0722
- Бакеты (users 1/2/3) HR@10: 0.1662/0.1363/0.1168; (items 1/2/3) HR@10: 0.1127/0.1336/0.1462
- Точка проверки: results/yambda_adamw_l2.json (полные метрики и история обучения)

### beauty_adamw_l6 — 2026-10-13
- Конфиг: Beauty, num_blocks=6, optimizer=adamw, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=18, best_val_NDCG@10=0.0709, время=0.13 ч
- Тест: HR@10=0.087, NDCG@10=0.0529, Coverage@10=0.666
- Бакеты (users 1/2/3) NDCG@10: 0.0466/0.0514/0.0978; (items 1/2/3) NDCG@10: 0.1279/0.0448/0.0125
- Бакеты (users 1/2/3) HR@10: 0.0768/0.0856/0.1568; (items 1/2/3) HR@10: 0.2107/0.0728/0.0211
- Точка проверки: results/beauty_adamw_l6.json (полные метрики и история обучения)

### beauty_muon_l2 — 2026-10-13
- Конфиг: Beauty, num_blocks=2, optimizer=muon, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=20, best_val_NDCG@10=0.0723, время=0.08 ч
- Тест: HR@10=0.0851, NDCG@10=0.052, Coverage@10=0.6693
- Бакеты (users 1/2/3) NDCG@10: 0.0466/0.0491/0.0953; (items 1/2/3) NDCG@10: 0.1233/0.0451/0.013
- Бакеты (users 1/2/3) HR@10: 0.0764/0.0819/0.1499; (items 1/2/3) HR@10: 0.1988/0.0744/0.0225
- Точка проверки: results/beauty_muon_l2.json (полные метрики и история обучения)

### beauty_muon_l4 — 2026-10-13
- Конфиг: Beauty, num_blocks=4, optimizer=muon, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=4, best_val_NDCG@10=0.0285, время=0.06 ч
- Тест: HR@10=0.0389, NDCG@10=0.0204, Coverage@10=0.0316
- Бакеты (users 1/2/3) NDCG@10: 0.0183/0.021/0.0324; (items 1/2/3) NDCG@10: 0.0758/0.0036/0.0
- Бакеты (users 1/2/3) HR@10: 0.0358/0.0395/0.0577; (items 1/2/3) HR@10: 0.145/0.0066/0.0
- Точка проверки: results/beauty_muon_l4.json (полные метрики и история обучения)

### yambda_adamw_l4 — 2026-10-13
- Конфиг: Yambda, num_blocks=4, optimizer=adamw, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=24, best_val_NDCG@10=0.0651, время=0.27 ч
- Тест: HR@10=0.129, NDCG@10=0.0626, Coverage@10=0.1919
- Бакеты (users 1/2/3) NDCG@10: 0.0799/0.0645/0.0559; (items 1/2/3) NDCG@10: 0.0539/0.0667/0.0673
- Бакеты (users 1/2/3) HR@10: 0.1636/0.1344/0.1153; (items 1/2/3) HR@10: 0.1163/0.1352/0.1357
- Точка проверки: results/yambda_adamw_l4.json (полные метрики и история обучения)

---

<!-- проект: SASRec_exp -->
<!-- источник: SASRec_exp/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — Коррекция muon_lr: расходимость на глубине, перезапуск муon-прогонов
- Запрос агенту: (внутренняя коррекция по ходу sweep) Muon с lr=0.005 на Beauty расходится при num_blocks=4: train_loss растет (6.12 -> 6.23 к 15-й эпохе), val NDCG@10 падает до 0.014; при blocks=2 тот же lr работал (0.0723).
- Что сделал агент: остановил sweep, перебрал muon_lr по глубине на Beauty (12 эпох, val NDCG@10): blocks=2@0.0025 -> 0.0706; blocks=4@0.0025 -> 0.0705 (стабильно); blocks=6@0.0025 -> 0.0677; blocks=6@0.00125 -> 0.0680. Зафиксировал единый muon_lr=0.0025 для всех глубин и обоих датасетов (src/configs.py), удалил невалидные results/beauty_muon_l4.json, beauty_muon_l6.json и results/beauty_muon_l2.json (обучен с 0.005 — перезапущен с 0.0025 для единообразия), перезапустил оба драйвера (завершенные прогоны пропускаются).
- Результат: muon_lr=0.0025 стабилен на всех глубинах; sweep продолжен.
- Точка проверки: results/logs/sweep_beauty2.log (строки "[skip]" для готовых прогонов), новые results/beauty_muon_*.json с muon_lr=0.0025 в поле config.
- Итог проверки: принято с исправлением — записи diary для beauty_muon_l2 (0.005) считаются замененными одноименным прогоном с 0.0025; конфиг в json фиксирует фактический muon_lr каждого прогона.

### beauty_muon_l2 — 2026-10-13
- Конфиг: Beauty, num_blocks=2, optimizer=muon, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=20, best_val_NDCG@10=0.0717, время=0.08 ч
- Тест: HR@10=0.0847, NDCG@10=0.0519, Coverage@10=0.6964
- Бакеты (users 1/2/3) NDCG@10: 0.0458/0.0491/0.0989; (items 1/2/3) NDCG@10: 0.1241/0.044/0.0131
- Бакеты (users 1/2/3) HR@10: 0.0745/0.0823/0.1568; (items 1/2/3) HR@10: 0.199/0.074/0.0217
- Точка проверки: results/beauty_muon_l2.json (полные метрики и история обучения)

### beauty_muon_l4 — 2026-10-13
- Конфиг: Beauty, num_blocks=4, optimizer=muon, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=12, best_val_NDCG@10=0.073, время=0.09 ч
- Тест: HR@10=0.0846, NDCG@10=0.0514, Coverage@10=0.602
- Бакеты (users 1/2/3) NDCG@10: 0.0448/0.0495/0.0991; (items 1/2/3) NDCG@10: 0.131/0.0408/0.0102
- Бакеты (users 1/2/3) HR@10: 0.0744/0.0823/0.1573; (items 1/2/3) HR@10: 0.2136/0.0683/0.0173
- Точка проверки: results/beauty_muon_l4.json (полные метрики и история обучения)

### beauty_muon_l6 — 2026-10-13
- Конфиг: Beauty, num_blocks=6, optimizer=muon, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=15, best_val_NDCG@10=0.0694, время=0.13 ч
- Тест: HR@10=0.0825, NDCG@10=0.0513, Coverage@10=0.5583
- Бакеты (users 1/2/3) NDCG@10: 0.045/0.0493/0.0978; (items 1/2/3) NDCG@10: 0.1305/0.0418/0.0095
- Бакеты (users 1/2/3) HR@10: 0.0734/0.0799/0.1485; (items 1/2/3) HR@10: 0.2072/0.0689/0.0155
- Точка проверки: results/beauty_muon_l6.json (полные метрики и история обучения)

### beauty_adamw_l2_lip — 2026-10-13
- Конфиг: Beauty, num_blocks=2, optimizer=adamw + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=14, best_val_NDCG@10=0.0687, время=0.06 ч
- Тест: HR@10=0.0808, NDCG@10=0.0495, Coverage@10=0.7875
- Бакеты (users 1/2/3) NDCG@10: 0.0444/0.0472/0.0893; (items 1/2/3) NDCG@10: 0.1178/0.0413/0.0135
- Бакеты (users 1/2/3) HR@10: 0.0721/0.08/0.1384; (items 1/2/3) HR@10: 0.1899/0.0678/0.023
- Точка проверки: results/beauty_adamw_l2_lip.json (полные метрики и история обучения)

### yambda_adamw_l6 — 2026-10-13
- Конфиг: Yambda, num_blocks=6, optimizer=adamw, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=34, best_val_NDCG@10=0.0674, время=0.41 ч
- Тест: HR@10=0.1316, NDCG@10=0.0639, Coverage@10=0.2796
- Бакеты (users 1/2/3) NDCG@10: 0.0818/0.0643/0.0573; (items 1/2/3) NDCG@10: 0.0557/0.0613/0.0745
- Бакеты (users 1/2/3) HR@10: 0.1665/0.1336/0.1186; (items 1/2/3) HR@10: 0.1195/0.1259/0.1491
- Точка проверки: results/yambda_adamw_l6.json (полные метрики и история обучения)

### beauty_adamw_l4_lip — 2026-10-13
- Конфиг: Beauty, num_blocks=4, optimizer=adamw + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=16, best_val_NDCG@10=0.07, время=0.1 ч
- Тест: HR@10=0.0829, NDCG@10=0.0503, Coverage@10=0.7814
- Бакеты (users 1/2/3) NDCG@10: 0.0451/0.0475/0.092; (items 1/2/3) NDCG@10: 0.1216/0.0414/0.0129
- Бакеты (users 1/2/3) HR@10: 0.0745/0.0789/0.1485; (items 1/2/3) HR@10: 0.1986/0.0687/0.0221
- Точка проверки: results/beauty_adamw_l4_lip.json (полные метрики и история обучения)

### yambda_muon_l2 — 2026-10-13
- Конфиг: Yambda, num_blocks=2, optimizer=muon, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=23, best_val_NDCG@10=0.061, время=0.19 ч
- Тест: HR@10=0.1236, NDCG@10=0.0606, Coverage@10=0.2585
- Бакеты (users 1/2/3) NDCG@10: 0.0782/0.0608/0.0543; (items 1/2/3) NDCG@10: 0.0537/0.0619/0.0664
- Бакеты (users 1/2/3) HR@10: 0.1586/0.1244/0.1109; (items 1/2/3) HR@10: 0.114/0.1253/0.1315
- Точка проверки: results/yambda_muon_l2.json (полные метрики и история обучения)

### beauty_adamw_l6_lip — 2026-10-13
- Конфиг: Beauty, num_blocks=6, optimizer=adamw + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=15, best_val_NDCG@10=0.0693, время=0.13 ч
- Тест: HR@10=0.0831, NDCG@10=0.051, Coverage@10=0.7602
- Бакеты (users 1/2/3) NDCG@10: 0.0456/0.0489/0.0917; (items 1/2/3) NDCG@10: 0.1245/0.0412/0.0131
- Бакеты (users 1/2/3) HR@10: 0.075/0.0799/0.1448; (items 1/2/3) HR@10: 0.1991/0.0682/0.0228
- Точка проверки: results/beauty_adamw_l6_lip.json (полные метрики и история обучения)

### beauty_muon_l2_lip — 2026-10-13
- Конфиг: Beauty, num_blocks=2, optimizer=muon + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=11, best_val_NDCG@10=0.069, время=0.06 ч
- Тест: HR@10=0.0823, NDCG@10=0.0505, Coverage@10=0.7391
- Бакеты (users 1/2/3) NDCG@10: 0.0453/0.0477/0.0916; (items 1/2/3) NDCG@10: 0.1241/0.0405/0.0125
- Бакеты (users 1/2/3) HR@10: 0.0746/0.0786/0.1425; (items 1/2/3) HR@10: 0.1995/0.0667/0.0217
- Точка проверки: results/beauty_muon_l2_lip.json (полные метрики и история обучения)

### beauty_muon_l4_lip — 2026-10-13
- Конфиг: Beauty, num_blocks=4, optimizer=muon + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=12, best_val_NDCG@10=0.0705, время=0.11 ч
- Тест: HR@10=0.0827, NDCG@10=0.0503, Coverage@10=0.6887
- Бакеты (users 1/2/3) NDCG@10: 0.0447/0.0472/0.095; (items 1/2/3) NDCG@10: 0.1262/0.0395/0.0117
- Бакеты (users 1/2/3) HR@10: 0.0742/0.0789/0.1485; (items 1/2/3) HR@10: 0.2066/0.0649/0.0199
- Точка проверки: results/beauty_muon_l4_lip.json (полные метрики и история обучения)

### yambda_muon_l4 — 2026-10-13
- Конфиг: Yambda, num_blocks=4, optimizer=muon, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=24, best_val_NDCG@10=0.0629, время=0.3 ч
- Тест: HR@10=0.1215, NDCG@10=0.0604, Coverage@10=0.2511
- Бакеты (users 1/2/3) NDCG@10: 0.077/0.0611/0.0543; (items 1/2/3) NDCG@10: 0.051/0.0639/0.0663
- Бакеты (users 1/2/3) HR@10: 0.1542/0.1229/0.1095; (items 1/2/3) HR@10: 0.107/0.1276/0.13
- Точка проверки: results/yambda_muon_l4.json (полные метрики и история обучения)

### beauty_muon_l6_lip — 2026-10-13
- Конфиг: Beauty, num_blocks=6, optimizer=muon + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=13, best_val_NDCG@10=0.0687, время=0.15 ч
- Тест: HR@10=0.0836, NDCG@10=0.0516, Coverage@10=0.6426
- Бакеты (users 1/2/3) NDCG@10: 0.0453/0.0497/0.0979; (items 1/2/3) NDCG@10: 0.1283/0.043/0.0106
- Бакеты (users 1/2/3) HR@10: 0.0727/0.0828/0.1559; (items 1/2/3) HR@10: 0.2072/0.0698/0.0174
- Точка проверки: results/beauty_muon_l6_lip.json (полные метрики и история обучения)

### yambda_muon_l6 — 2026-10-13
- Конфиг: Yambda, num_blocks=6, optimizer=muon, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=38, best_val_NDCG@10=0.0598, время=0.53 ч
- Тест: HR@10=0.1138, NDCG@10=0.0585, Coverage@10=0.2194
- Бакеты (users 1/2/3) NDCG@10: 0.0781/0.0613/0.0507; (items 1/2/3) NDCG@10: 0.0557/0.06/0.0597
- Бакеты (users 1/2/3) HR@10: 0.1526/0.1195/0.0986; (items 1/2/3) HR@10: 0.1112/0.1144/0.1159
- Точка проверки: results/yambda_muon_l6.json (полные метрики и история обучения)

### yambda_adamw_l2_lip — 2026-10-13
- Конфиг: Yambda, num_blocks=2, optimizer=adamw + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=11, best_val_NDCG@10=0.0062, время=0.11 ч
- Тест: HR@10=0.0117, NDCG@10=0.0058, Coverage@10=0.0
- Бакеты (users 1/2/3) NDCG@10: 0.0071/0.0063/0.0052; (items 1/2/3) NDCG@10: 0.0172/0.0/0.0
- Бакеты (users 1/2/3) HR@10: 0.0151/0.0129/0.0101; (items 1/2/3) HR@10: 0.0346/0.0/0.0
- Точка проверки: results/yambda_adamw_l2_lip.json (полные метрики и история обучения)

### yambda_adamw_l4_lip — 2026-10-13
- Конфиг: Yambda, num_blocks=4, optimizer=adamw + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=0, best_val_NDCG@10=0.0056, время=0.06 ч
- Тест: HR@10=0.0102, NDCG@10=0.0051, Coverage@10=0.0
- Бакеты (users 1/2/3) NDCG@10: 0.0062/0.0059/0.0045; (items 1/2/3) NDCG@10: 0.015/0.0/0.0
- Бакеты (users 1/2/3) HR@10: 0.0131/0.0118/0.0087; (items 1/2/3) HR@10: 0.0301/0.0/0.0
- Точка проверки: results/yambda_adamw_l4_lip.json (полные метрики и история обучения)

### yambda_adamw_l6_lip — 2026-10-13
- Конфиг: Yambda, num_blocks=6, optimizer=adamw + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=39, best_val_NDCG@10=0.0585, время=0.51 ч
- Тест: HR@10=0.1082, NDCG@10=0.0548, Coverage@10=0.1565
- Бакеты (users 1/2/3) NDCG@10: 0.0728/0.0571/0.0477; (items 1/2/3) NDCG@10: 0.0556/0.0557/0.053
- Бакеты (users 1/2/3) HR@10: 0.1421/0.1146/0.0946; (items 1/2/3) HR@10: 0.1134/0.1099/0.1015
- Точка проверки: results/yambda_adamw_l6_lip.json (полные метрики и история обучения)

### yambda_muon_l2_lip — 2026-10-13
- Конфиг: Yambda, num_blocks=2, optimizer=muon + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=14, best_val_NDCG@10=0.0596, время=0.14 ч
- Тест: HR@10=0.1184, NDCG@10=0.0577, Coverage@10=0.1399
- Бакеты (users 1/2/3) NDCG@10: 0.0751/0.0607/0.0508; (items 1/2/3) NDCG@10: 0.0565/0.0638/0.0531
- Бакеты (users 1/2/3) HR@10: 0.1556/0.1235/0.1039; (items 1/2/3) HR@10: 0.1181/0.1292/0.1084
- Точка проверки: results/yambda_muon_l2_lip.json (полные метрики и история обучения)

### yambda_muon_l4_lip — 2026-10-13
- Конфиг: Yambda, num_blocks=4, optimizer=muon + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=22, best_val_NDCG@10=0.0608, время=0.32 ч
- Тест: HR@10=0.1226, NDCG@10=0.0599, Coverage@10=0.1791
- Бакеты (users 1/2/3) NDCG@10: 0.0765/0.0621/0.0534; (items 1/2/3) NDCG@10: 0.0522/0.0633/0.0642
- Бакеты (users 1/2/3) HR@10: 0.1569/0.1265/0.1093; (items 1/2/3) HR@10: 0.1099/0.1279/0.1302
- Точка проверки: results/yambda_muon_l4_lip.json (полные метрики и история обучения)

### yambda_muon_l6_lip — 2026-10-13
- Конфиг: Yambda, num_blocks=6, optimizer=muon + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=31, best_val_NDCG@10=0.0629, время=0.57 ч
- Тест: HR@10=0.1281, NDCG@10=0.0622, Coverage@10=0.2108
- Бакеты (users 1/2/3) NDCG@10: 0.0792/0.0638/0.0558; (items 1/2/3) NDCG@10: 0.0562/0.0606/0.0698
- Бакеты (users 1/2/3) HR@10: 0.1624/0.1314/0.115; (items 1/2/3) HR@10: 0.1174/0.1253/0.1414
- Точка проверки: results/yambda_muon_l6_lip.json (полные метрики и история обучения)

### yambda_adamw_l2_lip — 2026-10-13
- Конфиг: Yambda, num_blocks=2, optimizer=adamw + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=7, best_val_NDCG@10=0.0061, время=0.28 ч
- Тест: HR@10=0.0123, NDCG@10=0.0058, Coverage@10=0.0
- Бакеты (users 1/2/3) NDCG@10: 0.0071/0.0059/0.0053; (items 1/2/3) NDCG@10: 0.0172/0.0/0.0
- Бакеты (users 1/2/3) HR@10: 0.016/0.0126/0.0109; (items 1/2/3) HR@10: 0.0365/0.0/0.0
- Точка проверки: results/yambda_adamw_l2_lip.json (полные метрики и история обучения)

### yambda_adamw_l4_lip — 2026-10-13
- Конфиг: Yambda, num_blocks=4, optimizer=adamw + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=76, best_val_NDCG@10=0.0655, время=1.62 ч
- Тест: HR@10=0.1226, NDCG@10=0.0614, Coverage@10=0.1888
- Бакеты (users 1/2/3) NDCG@10: 0.0816/0.0644/0.0535; (items 1/2/3) NDCG@10: 0.0563/0.0595/0.0684
- Бакеты (users 1/2/3) HR@10: 0.1619/0.1288/0.1071; (items 1/2/3) HR@10: 0.1147/0.1172/0.1357
- Точка проверки: results/yambda_adamw_l4_lip.json (полные метрики и история обучения)

### yambda_adamw_l6_lip — 2026-10-13
- Конфиг: Yambda, num_blocks=6, optimizer=adamw + lipschitz attention, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=75, best_val_NDCG@10=0.0631, время=2.07 ч
- Тест: HR@10=0.1197, NDCG@10=0.0596, Coverage@10=0.1867
- Бакеты (users 1/2/3) NDCG@10: 0.0783/0.0611/0.0526; (items 1/2/3) NDCG@10: 0.055/0.0575/0.0663
- Бакеты (users 1/2/3) HR@10: 0.1555/0.1239/0.1058; (items 1/2/3) HR@10: 0.1126/0.1154/0.1309
- Точка проверки: results/yambda_adamw_l6_lip.json (полные метрики и история обучения)

---

<!-- проект: SASRec_exp -->
<!-- источник: SASRec_exp/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — Базовые эксперименты: AdamW vs Muon x blocks {2,4,6} (Beauty, Yambda)
- Запрос агенту: обучить SASRec с оптимальным конфигом (см. запись о каркасе), перебирая число трансформерных блоков 2/4/6, с оптимизаторами AdamW и Muon (Muon — 2D веса attention/FFN, AdamW — 1D веса и эмбеддинги); метрики HR@10, NDCG@10, Coverage@10 — общие и по бакетам.
- Что сделал агент: 12 прогонов (по 6 на датасет), каждый — ранняя остановка по val NDCG@10 (подвыборка 5000 юзеров), тестовые метрики считаются по лучшей эпохе; все авто-записи выше.
- Результат (тест; NDCG@10 / Coverage@10):
  | датасет | оптимизатор | 2 блока | 4 блока | 6 блоков |
  |---|---|---|---|---|
  | Beauty | AdamW | 0.0514 / 0.783 | 0.0524 / 0.731 | 0.0529 / 0.666 |
  | Beauty | Muon  | 0.0519 / 0.696 | 0.0514 / 0.602 | 0.0513 / 0.558 |
  | Yambda | AdamW | 0.0636 / 0.213 | 0.0626 / 0.192 | 0.0639 / 0.280 |
  | Yambda | Muon  | 0.0606 / 0.259 | 0.0604 / 0.251 | 0.0585 / 0.219 |
  HR@10: Beauty 0.083-0.087 (AdamW растет с глубиной, Muon ~плоско); Yambda 0.114-0.132 (AdamW > Muon, Muon падает с глубиной).
  Бакеты: Beauty — NDCG растет с длиной истории (0.046 -> 0.098) и с популярностью айтема (0.121 -> 0.014, сильный popularity bias, глубина его усиливает); Yambda — наоборот, короткие истории лучше (0.081 -> 0.057), popularity bias слабый (0.053-0.075).
  Выводы: (1) рост глубины дает небольшой прирост NDCG только с AdamW и систематически снижает Coverage; (2) Muon ~ на уровне AdamW по NDCG на Beauty, хуже на Yambda, но дает заметно более высокий Coverage на малой глубине Yambda (0.259 vs 0.213 при 2 блоках); (3) muon_lr требует понижения с глубиной (иначе расходимость, см. запись о коррекции).
- Точка проверки: results/beauty_{adamw,muon}_l{2,4,6}.json, results/yambda_*.json; сводная таблица figures/metrics_barplot.csv.
- Итог проверки: принято.

---

<!-- проект: SASRec_exp -->
<!-- источник: SASRec_exp/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — Lipschitz-регуляризация attention: прогоны AdamW+Lip и Muon+Lip
- Запрос агенту: добавить Lipschitz-регуляризацию attention-слоя (W <- W/sigma_max(W) на in_proj_weight и out_proj.weight каждого блока перед каждым forward, power iteration) и построить аналогичные результаты для AdamW и Muon.
- Что сделал агент: 12 прогонов с lipschitz=True теми же конфигами. На Yambda AdamW+Lip l2/l4 сначала сошли в "популярностный" режим (Coverage@10 ~ 0: модель рекомендует одни и те же ~10 айтемов всем; l6 вышел из него после спайка лосса на ~13-й эпохе). Перезапустил yambda_adamw_l{2,4,6}_lip с расширенным бюджетом (patience 15, max_epochs 80): l4 и l6 вышли из коллапса и сошлись (best_epoch 76/75), l2 не вышел и за 23 эпохи (val NDCG ~ 0.006) — оставлен как есть, это результат.
- Результат (тест; NDCG@10 / Coverage@10):
  | датасет | вариант | 2 блока | 4 блока | 6 блоков |
  |---|---|---|---|---|
  | Beauty | AdamW+Lip | 0.0495 / 0.787 | 0.0503 / 0.781 | 0.0510 / 0.760 |
  | Beauty | Muon+Lip  | 0.0505 / 0.739 | 0.0503 / 0.689 | 0.0516 / 0.643 |
  | Yambda | AdamW+Lip | 0.0058 / 0.000 (коллапс) | 0.0614 / 0.189 | 0.0596 / 0.187 |
  | Yambda | Muon+Lip  | 0.0577 / 0.140 | 0.0599 / 0.179 | 0.0622 / 0.211 |
  Выводы: (1) на Beauty Lipschitz стоит ~0.001-0.002 NDCG, но почти полностью сохраняет Coverage при росте глубины (у AdamW падение Coverage с глубиной 0.783->0.666, с Lip 0.787->0.760); (2) на Yambda Lipschitz+AdamW нестабилен (коллапс разнообразия, длинный выход из него), Lipschitz+Muon стабилен на всех глубинах — ортогонализованные апдейты Muon предотвращают коллапс; (3) у Muon+Lip на Yambda NDCG восстанавливается с глубиной до 0.0622.
- Точка проверки: results/*_lip.json (поле training.n_lipschitz_weights подтверждает подключение хука: 2 матрицы на блок), results/logs/rerun_yambda_adamw_l*_lip.log (истории с коллапсом и выходом).
- Итог проверки: принято с исправлением — исходные yambda_adamw_l{2,4,6}_lip (patience 5, cap 40) остановились в коллапсе; одноименные записи выше заменены перезапусками с patience 15 / max_epochs 80.

---

<!-- проект: SASRec_exp -->
<!-- источник: SASRec_exp/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — Итоговый barplot и общие выводы
- Запрос агенту: построить barplot по метрикам NDCG@10 и Coverage@10 — разными оттенками число слоев, разными цветами оптимизаторы и регуляризации.
- Что сделал агент: `python -m src.plot_results` -> `figures/metrics_barplot.png` (2 строки — датасеты, 2 столбца — метрики; в каждой панели 4 группы: AdamW, Muon, AdamW+Lipschitz, Muon+Lipschitz — 4 цвета; внутри группы 3 бара 2/4/6 блоков — оттенки от светлого к темному) + `figures/metrics_barplot.csv` (все метрики, включая бакеты, в плоском виде).
- Результат: итоговые выводы по всем 24 прогонам:
  1. NDCG@10: AdamW стабильно >= Muon (Beauty: 0.0514-0.0529 vs 0.0513-0.0519; Yambda: 0.0626-0.0639 vs 0.0585-0.0606); глубина помогает только AdamW и лишь слегка (+0.0015 на Beauty).
  2. Coverage@10: падает с глубиной во всех вариантах; Lipschitz-регуляризация attention компенсирует падение на Beauty (0.760 vs 0.666 при 6 блоках у AdamW) и не разрушает NDCG.
  3. Lipschitz+AdamW на большом каталоге (Yambda, 539k айтемов) нестабилен: коллапс разнообразия (Coverage -> 0), выход требует в ~2-4 раза больше эпох; Muon к Lipschitz устойчив.
  4. Бакеты: на Beauty качество концентрируется на длинных историях и популярных айтемах (ibucket1 NDCG 0.12 vs ibucket3 0.014 — сильный bias к популярности, глубина и Muon его усиливают); на Yambda наоборот — короткие истории прогнозируются лучше, bias к популярности почти отсутствует.
- Точка проверки: figures/metrics_barplot.png + figures/metrics_barplot.csv; сводка по прогонам: `python - <<EOF ... json.load(results/*.json)`.
- Итог проверки: принято.

---

<!-- проект: SASRec_exp -->
<!-- источник: SASRec_exp/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — План: эксперименты по правилу lr ~ 1/sqrt(K) при росте параметров в K раз
- Запрос агенту: запустить эксперименты, в которых при увеличении числа параметров модели в K раз learning rate уменьшается в sqrt(K) раз.
- Что сделал агент (дизайн, src/param_scaling.py): ручка роста параметров — ширина модели hidden_units {64, 128, 256} при num_blocks=2 (изоляция эффекта ширины; база h=128 — «оптимальный конфиг»). Число параметров измеряется точно (сумма numel()): Beauty 0.826M / 1.751M / 3.895M (K = 0.472 / 1 / 2.225 от h=128), Yambda 34.58M / 69.25M / 138.89M (K = 0.499 / 1 / 2.006). Правило: lr(K) = lr_base / sqrt(K); для K<1 lr соответственно увеличивается. Две группы: 'scaled' (правило) и 'constlr' (контроль, lr=base); при h=128 (K=1) группы совпадают — один общий прогон. Оба оптимизатора; правило применяется ко всем lr прогона: AdamW lr и (для muon) muon_lr с тем же множителем 1/sqrt(K). Beauty — бюджет базового конфига (200 эпох, patience 10 — сходится естественно); Yambda — единый бюджет для всех прогонов этого эксперимента: 60 эпох, patience 8 (чтобы медленно сходящиеся прогоны с меньшим lr не обрезались лимитом). Итого 20 прогонов (по 10 на датасет), результаты в results/param_scaling/, каждый пишется в diary автоматически.
- Результат: 20/20 прогонов завершены (итоги — в следующей записи, «Эксперименты lr ~ 1/sqrt(K): результаты»); попутно найден и исправлен баг arm='base' в src/param_scaling.py (arm_lr не принимал h=128-прогон; 4 прогона h128_base перезапущены после исправления).
- Точка проверки: results/param_scaling/*.json (поля n_params, k, lr, arm), figures/param_scaling.png.
- Итог проверки: принято — см. следующую запись.

### beauty_adamw_h64_scaled (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=64 (params=0.83M, K=0.472 от h=128), num_blocks=2, optimizer=adamw, arm=scaled (lr=base/sqrt(K)), lr=5.74e-04, muon_lr=-, loss=sce, max_seq_len=20
- Обучение: best_epoch=25, best_val_NDCG@10=0.0682, время=0.14 ч
- Тест: HR@10=0.0819, NDCG@10=0.0491, Coverage@10=0.3818
- Точка проверки: results/param_scaling/beauty_adamw_h64_scaled.json

### beauty_adamw_h64_constlr (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=64 (params=0.83M, K=0.472 от h=128), num_blocks=2, optimizer=adamw, arm=constlr (lr=const), lr=3.94e-04, muon_lr=-, loss=sce, max_seq_len=20
- Обучение: best_epoch=31, best_val_NDCG@10=0.0704, время=0.16 ч
- Тест: HR@10=0.0822, NDCG@10=0.0496, Coverage@10=0.3592
- Точка проверки: results/param_scaling/beauty_adamw_h64_constlr.json

### beauty_adamw_h256_scaled (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=256 (params=3.90M, K=2.225 от h=128), num_blocks=2, optimizer=adamw, arm=scaled (lr=base/sqrt(K)), lr=2.64e-04, muon_lr=-, loss=sce, max_seq_len=20
- Обучение: best_epoch=14, best_val_NDCG@10=0.0743, время=0.1 ч
- Тест: HR@10=0.0876, NDCG@10=0.0542, Coverage@10=0.9303
- Точка проверки: results/param_scaling/beauty_adamw_h256_scaled.json

### beauty_adamw_h256_constlr (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=256 (params=3.90M, K=2.225 от h=128), num_blocks=2, optimizer=adamw, arm=constlr (lr=const), lr=3.94e-04, muon_lr=-, loss=sce, max_seq_len=20
- Обучение: best_epoch=7, best_val_NDCG@10=0.0732, время=0.07 ч
- Тест: HR@10=0.0877, NDCG@10=0.0535, Coverage@10=0.9146
- Точка проверки: results/param_scaling/beauty_adamw_h256_constlr.json

### yambda_adamw_h64_scaled (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=64 (params=34.58M, K=0.499 от h=128), num_blocks=2, optimizer=adamw, arm=scaled (lr=base/sqrt(K)), lr=5.58e-04, muon_lr=-, loss=sce, max_seq_len=100
- Обучение: best_epoch=36, best_val_NDCG@10=0.0563, время=0.5 ч
- Тест: HR@10=0.1028, NDCG@10=0.0513, Coverage@10=0.1389
- Точка проверки: results/param_scaling/yambda_adamw_h64_scaled.json

### beauty_muon_h64_scaled (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=64 (params=0.83M, K=0.472 от h=128), num_blocks=2, optimizer=muon, arm=scaled (lr=base/sqrt(K)), lr=5.74e-04, muon_lr=0.003639161225308906, loss=sce, max_seq_len=20
- Обучение: best_epoch=14, best_val_NDCG@10=0.0676, время=0.12 ч
- Тест: HR@10=0.0806, NDCG@10=0.0489, Coverage@10=0.3604
- Точка проверки: results/param_scaling/beauty_muon_h64_scaled.json

### yambda_adamw_h64_constlr (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=64 (params=34.58M, K=0.499 от h=128), num_blocks=2, optimizer=adamw, arm=constlr (lr=const), lr=3.94e-04, muon_lr=-, loss=sce, max_seq_len=100
- Обучение: best_epoch=5, best_val_NDCG@10=0.0057, время=0.12 ч
- Тест: HR@10=0.0114, NDCG@10=0.0058, Coverage@10=0.0
- Точка проверки: results/param_scaling/yambda_adamw_h64_constlr.json

### beauty_muon_h64_constlr (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=64 (params=0.83M, K=0.472 от h=128), num_blocks=2, optimizer=muon, arm=constlr (lr=const), lr=3.94e-04, muon_lr=0.0025, loss=sce, max_seq_len=20
- Обучение: best_epoch=17, best_val_NDCG@10=0.0693, время=0.12 ч
- Тест: HR@10=0.0821, NDCG@10=0.0498, Coverage@10=0.3387
- Точка проверки: results/param_scaling/beauty_muon_h64_constlr.json

### beauty_muon_h256_scaled (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=256 (params=3.90M, K=2.225 от h=128), num_blocks=2, optimizer=muon, arm=scaled (lr=base/sqrt(K)), lr=2.64e-04, muon_lr=0.0016761690209375632, loss=sce, max_seq_len=20
- Обучение: best_epoch=11, best_val_NDCG@10=0.0761, время=0.1 ч
- Тест: HR@10=0.0903, NDCG@10=0.0555, Coverage@10=0.8228
- Точка проверки: results/param_scaling/beauty_muon_h256_scaled.json

### beauty_muon_h256_constlr (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=256 (params=3.90M, K=2.225 от h=128), num_blocks=2, optimizer=muon, arm=constlr (lr=const), lr=3.94e-04, muon_lr=0.0025, loss=sce, max_seq_len=20
- Обучение: best_epoch=7, best_val_NDCG@10=0.0745, время=0.08 ч
- Тест: HR@10=0.0882, NDCG@10=0.0535, Coverage@10=0.7897
- Точка проверки: results/param_scaling/beauty_muon_h256_constlr.json

### yambda_muon_h64_scaled (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=64 (params=34.58M, K=0.499 от h=128), num_blocks=2, optimizer=muon, arm=scaled (lr=base/sqrt(K)), lr=5.58e-04, muon_lr=0.0035380460260856, loss=sce, max_seq_len=100
- Обучение: best_epoch=20, best_val_NDCG@10=0.0527, время=0.25 ч
- Тест: HR@10=0.1004, NDCG@10=0.0505, Coverage@10=0.161
- Точка проверки: results/param_scaling/yambda_muon_h64_scaled.json

### yambda_adamw_h256_scaled (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=256 (params=138.89M, K=2.006 от h=128), num_blocks=2, optimizer=adamw, arm=scaled (lr=base/sqrt(K)), lr=2.78e-04, muon_lr=-, loss=sce, max_seq_len=100
- Обучение: best_epoch=27, best_val_NDCG@10=0.0721, время=0.59 ч
- Тест: HR@10=0.1465, NDCG@10=0.0705, Coverage@10=0.2242
- Точка проверки: results/param_scaling/yambda_adamw_h256_scaled.json

### yambda_muon_h64_constlr (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=64 (params=34.58M, K=0.499 от h=128), num_blocks=2, optimizer=muon, arm=constlr (lr=const), lr=3.94e-04, muon_lr=0.0025, loss=sce, max_seq_len=100
- Обучение: best_epoch=42, best_val_NDCG@10=0.056, время=0.45 ч
- Тест: HR@10=0.1047, NDCG@10=0.0528, Coverage@10=0.2039
- Точка проверки: results/param_scaling/yambda_muon_h64_constlr.json

### yambda_adamw_h256_constlr (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=256 (params=138.89M, K=2.006 от h=128), num_blocks=2, optimizer=adamw, arm=constlr (lr=const), lr=3.94e-04, muon_lr=-, loss=sce, max_seq_len=100
- Обучение: best_epoch=23, best_val_NDCG@10=0.0729, время=0.81 ч
- Тест: HR@10=0.1471, NDCG@10=0.0705, Coverage@10=0.2524
- Точка проверки: results/param_scaling/yambda_adamw_h256_constlr.json

### yambda_muon_h256_scaled (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=256 (params=138.89M, K=2.006 от h=128), num_blocks=2, optimizer=muon, arm=scaled (lr=base/sqrt(K)), lr=2.78e-04, muon_lr=0.0017652628385412305, loss=sce, max_seq_len=100
- Обучение: best_epoch=22, best_val_NDCG@10=0.0661, время=0.6 ч
- Тест: HR@10=0.1359, NDCG@10=0.0653, Coverage@10=0.2787
- Точка проверки: results/param_scaling/yambda_muon_h256_scaled.json

### yambda_muon_h256_constlr (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=256 (params=138.89M, K=2.006 от h=128), num_blocks=2, optimizer=muon, arm=constlr (lr=const), lr=3.94e-04, muon_lr=0.0025, loss=sce, max_seq_len=100
- Обучение: best_epoch=17, best_val_NDCG@10=0.0644, время=0.48 ч
- Тест: HR@10=0.1316, NDCG@10=0.0636, Coverage@10=0.2764
- Точка проверки: results/param_scaling/yambda_muon_h256_constlr.json

### beauty_adamw_h128_base (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=128 (params=1.75M, K=1.000 от h=128), num_blocks=2, optimizer=adamw, arm=base (lr=const), lr=3.94e-04, muon_lr=-, loss=sce, max_seq_len=20
- Обучение: best_epoch=26, best_val_NDCG@10=0.0721, время=0.14 ч
- Тест: HR@10=0.0845, NDCG@10=0.0513, Coverage@10=0.7265
- Точка проверки: results/param_scaling/beauty_adamw_h128_base.json

### beauty_muon_h128_base (param-scaling) — 2026-10-13
- Конфиг: Beauty, hidden=128 (params=1.75M, K=1.000 от h=128), num_blocks=2, optimizer=muon, arm=base (lr=const), lr=3.94e-04, muon_lr=0.0025, loss=sce, max_seq_len=20
- Обучение: best_epoch=16, best_val_NDCG@10=0.0714, время=0.11 ч
- Тест: HR@10=0.0842, NDCG@10=0.051, Coverage@10=0.7055
- Точка проверки: results/param_scaling/beauty_muon_h128_base.json

### yambda_adamw_h128_base (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=128 (params=69.25M, K=1.000 от h=128), num_blocks=2, optimizer=adamw, arm=base (lr=const), lr=3.94e-04, muon_lr=-, loss=sce, max_seq_len=100
- Обучение: best_epoch=37, best_val_NDCG@10=0.0652, время=0.58 ч
- Тест: HR@10=0.1336, NDCG@10=0.0647, Coverage@10=0.2268
- Точка проверки: results/param_scaling/yambda_adamw_h128_base.json

### yambda_muon_h128_base (param-scaling) — 2026-10-13
- Конфиг: Yambda, hidden=128 (params=69.25M, K=1.000 от h=128), num_blocks=2, optimizer=muon, arm=base (lr=const), lr=3.94e-04, muon_lr=0.0025, loss=sce, max_seq_len=100
- Обучение: best_epoch=20, best_val_NDCG@10=0.0601, время=0.4 ч
- Тест: HR@10=0.1231, NDCG@10=0.0605, Coverage@10=0.2283
- Точка проверки: results/param_scaling/yambda_muon_h128_base.json

---

<!-- проект: SASRec_exp -->
<!-- источник: SASRec_exp/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — Эксперименты lr ~ 1/sqrt(K): результаты
- Запрос агенту: (см. план выше) проверить правило: при увеличении числа параметров в K раз lr уменьшается в sqrt(K).
- Что сделал агент: 20 прогонов (Beauty/Yambda x AdamW/Muon x hidden {64,128,256} x {scaled, constlr}, blocks=2); K измерен точно по числу параметров (Beauty: 0.472/1/2.225; Yambda: 0.499/1/2.006); scaled-lr: Beauty h64 5.74e-4 / h256 2.64e-4, Yambda h64 5.58e-4 / h256 2.78e-4 (базовый 3.94e-4); для Muon тем же множителем масштабировался и muon_lr (0.0025 -> 0.0036/0.0017 и 0.0035/0.0018). График figures/param_scaling.png (x = параметры, лог. шкала; сплошные = const lr, пунктир = lr/√K; синий AdamW, оранжевый Muon; колонки HR/NDCG/Coverage@10), данные figures/param_scaling.csv.
- Результат (тест, NDCG@10 / Coverage@10):
  | датасет | оптимизатор | h (params, K) | lr = const | lr = base/sqrt(K) |
  |---|---|---|---|---|
  | Beauty | AdamW | 64 (0.83M, 0.47) | 0.0496 / 0.359 | 0.0491 / 0.382 |
  | Beauty | AdamW | 128 (1.75M, 1.0)  | 0.0513 / 0.727 (общая точка) | — |
  | Beauty | AdamW | 256 (3.90M, 2.23) | 0.0535 / 0.915 | **0.0542 / 0.930** |
  | Beauty | Muon  | 64 (0.83M, 0.47) | 0.0498 / 0.339 | 0.0489 / 0.360 |
  | Beauty | Muon  | 128 (1.75M, 1.0)  | 0.0510 / 0.706 (общая точка) | — |
  | Beauty | Muon  | 256 (3.90M, 2.23) | 0.0535 / 0.790 | **0.0555 / 0.823** |
  | Yambda | AdamW | 64 (34.6M, 0.50) | 0.0058 / 0.000 (коллапс) | **0.0513 / 0.139** |
  | Yambda | AdamW | 128 (69.3M, 1.0)  | 0.0647 / 0.227 (общая точка) | — |
  | Yambda | AdamW | 256 (138.9M, 2.01)| 0.0705 / 0.252 | 0.0705 / 0.224 |
  | Yambda | Muon  | 64 (34.6M, 0.50) | 0.0528 / 0.204 | 0.0505 / 0.161 |
  | Yambda | Muon  | 128 (69.3M, 1.0)  | 0.0605 / 0.228 (общая точка) | — |
  | Yambda | Muon  | 256 (138.9M, 2.01)| 0.0636 / 0.276 | **0.0653 / 0.279** |
  Выводы:
  1. При росте параметров (K~2, h=256) правило lr/√K подтверждается: NDCG@10 выше или равен контролю во всех 4 сравнениях (Beauty AdamW +0.0007, Beauty Muon +0.0020, Yambda AdamW 0.0000, Yambda Muon +0.0017); Coverage@10 тоже выше на Beauty (0.930 vs 0.915; 0.823 vs 0.790) и на Yambda-Muon (0.279 vs 0.276). Выигрыш тем больше, чем сильнее «перегрет» базовый lr на большой модели.
  2. Скорость сходимости: меньший lr сходится медленнее (best_epoch 14 vs 7 у Beauty-AdamW h256; 27 vs 23 у Yambda-AdamW h256), но достигает того же или лучшего качества — бюджет эпох надо увеличивать вместе с размером модели.
  3. Симметричное применение при K<1 (lr увеличивается в √(1/K)) чаще вредит (Beauty -0.0005..-0.0009; Yambda-Muon -0.0023) — правило сформулировано для роста параметров, обратная экстраполяция не работает.
  4. Неожиданный эффект: Yambda-AdamW h64 с базовым lr сошел в «популярностный» коллапс (Coverage 0, NDCG 0.0058) — lr 3.94e-4, подобранный для h=128, на маленькой ширине и большом каталоге (539k айтемов) не выводит модель из популярностного бассейна; увеличенный по правилу lr (5.58e-4) спас прогон (NDCG 0.0513). То есть на большом каталоге слишком малый lr так же опасен, как слишком большой на малом.
  5. Воспроизводимость: общие точки h=128 воспроизводят базовые эксперименты (Beauty AdamW 0.0513 vs 0.0514; Yambda Muon 0.0605 vs 0.0606), у Yambda-AdamW чуть лучше за счет увеличенного бюджета (0.0647 vs 0.0636, best_epoch 37).
- Точка проверки: python -m src.plot_param_scaling; figures/param_scaling.csv; results/param_scaling/*.json.
- Итог проверки: принято — правило lr ~ 1/sqrt(K) при росте параметров в K раз подтверждено на 4 из 4 сравнениях при K≈2 (NDCG не хуже, обычно лучше), обратное направление (K<1) не рекомендуется.

---

<!-- проект: SASRec_exp -->
<!-- источник: SASRec_exp/diary.md -->
<!-- дата: 2026-10-13 -->
## 2026-10-13 — План: Lipschitz-регуляризация MLP весов (FFN) и аналогичные эксперименты
- Запрос агенту: добавить Lipschitz Regularization на MLP веса, провести аналогичные эксперименты.
- Что сделал агент (src/lipschitz.py): добавлен режим 'mlp' — W <- W/sigma_max(W) (power iteration, 10 шагов) на conv1.weight и conv2.weight каждого PointWiseFeedForward (MLP/FFN SASRec; hook на модуле FFN-блока, веса Conv1d [H,H,1] ресайклятся в 2D); и режим 'attn+mlp' — регуляризуются и attention (in_proj_weight, out_proj.weight), и MLP веса каждого блока (аналог apply_lipschitz_norm родительского репо). Диспетчер apply_lipschitz(model, mode); train/experiment/run_experiments переведены на lipschitz_mode: 'none'|'attn'|'mlp'|'attn+mlp' (старые прогоны '_lip' = 'attn', обратная совместимость имен файлов и plot). Проверка: после forward sigma_max регуляризуемых весов ~= 1.01-1.06, нерегуляризуемых не тронуты; mlp = 2 матрицы на блок, attn+mlp = 4.
- Дизайн аналогичных экспериментов: тот же грид, что для attention-Lipschitz — {Beauty, Yambda} x {AdamW, Muon} x {blocks 2,4,6} x {mlp, attn+mlp} = 24 новых прогона (итого с уже готовыми none/attn — полная матрица регуляризаций 2x2). Yambda-прогоны с регуляризацией автоматически получают расширенный бюджет 80 эпох / patience 15 (как финальные attn-прогоны, см. запись о Lipschitz attention). Имена: *_lipmlp (только MLP), *_lipfull (attn+MLP).
- Результат: (заполняется после завершения)
- Точка проверки: results/*_lipmlp.json, results/*_lipfull.json (поле training.n_lipschitz_weights: 2/блок для mlp, 4/блок для attn+mlp).
- Итог проверки: (заполняется)

### beauty_adamw_l2_lipmlp — 2026-10-13
- Конфиг: Beauty, num_blocks=2, optimizer=adamw + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=27, best_val_NDCG@10=0.0707, время=0.19 ч
- Тест: HR@10=0.0866, NDCG@10=0.0526, Coverage@10=0.7568
- Бакеты (users 1/2/3) NDCG@10: 0.0463/0.0506/0.099; (items 1/2/3) NDCG@10: 0.1216/0.0467/0.014
- Бакеты (users 1/2/3) HR@10: 0.0751/0.0881/0.1568; (items 1/2/3) HR@10: 0.2007/0.0769/0.0228
- Точка проверки: results/beauty_adamw_l2_lipmlp.json (полные метрики и история обучения)

### beauty_adamw_l4_lipmlp — 2026-10-13
- Конфиг: Beauty, num_blocks=4, optimizer=adamw + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=12, best_val_NDCG@10=0.0711, время=0.16 ч
- Тест: HR@10=0.0845, NDCG@10=0.0518, Coverage@10=0.7305
- Бакеты (users 1/2/3) NDCG@10: 0.0466/0.0492/0.0928; (items 1/2/3) NDCG@10: 0.127/0.0425/0.0123
- Бакеты (users 1/2/3) HR@10: 0.0764/0.0804/0.1476; (items 1/2/3) HR@10: 0.2052/0.0696/0.021
- Точка проверки: results/beauty_adamw_l4_lipmlp.json (полные метрики и история обучения)

### yambda_adamw_l2_lipmlp — 2026-10-13
- Конфиг: Yambda, num_blocks=2, optimizer=adamw + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=36, best_val_NDCG@10=0.0665, время=0.36 ч
- Тест: HR@10=0.1322, NDCG@10=0.0636, Coverage@10=0.2359
- Бакеты (users 1/2/3) NDCG@10: 0.0814/0.066/0.0566; (items 1/2/3) NDCG@10: 0.0538/0.0625/0.0745
- Бакеты (users 1/2/3) HR@10: 0.1687/0.1377/0.1178; (items 1/2/3) HR@10: 0.1164/0.1289/0.1511
- Точка проверки: results/yambda_adamw_l2_lipmlp.json (полные метрики и история обучения)

### beauty_adamw_l6_lipmlp — 2026-10-13
- Конфиг: Beauty, num_blocks=6, optimizer=adamw + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=13, best_val_NDCG@10=0.0708, время=0.21 ч
- Тест: HR@10=0.0869, NDCG@10=0.0534, Coverage@10=0.6803
- Бакеты (users 1/2/3) NDCG@10: 0.0479/0.0503/0.0973; (items 1/2/3) NDCG@10: 0.1292/0.0456/0.0122
- Бакеты (users 1/2/3) HR@10: 0.0774/0.0851/0.1531; (items 1/2/3) HR@10: 0.2091/0.0742/0.0206
- Точка проверки: results/beauty_adamw_l6_lipmlp.json (полные метрики и история обучения)

### beauty_muon_l2_lipmlp — 2026-10-13
- Конфиг: Beauty, num_blocks=2, optimizer=muon + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=14, best_val_NDCG@10=0.0707, время=0.14 ч
- Тест: HR@10=0.0874, NDCG@10=0.0532, Coverage@10=0.7182
- Бакеты (users 1/2/3) NDCG@10: 0.0476/0.0509/0.0962; (items 1/2/3) NDCG@10: 0.1258/0.0463/0.0133
- Бакеты (users 1/2/3) HR@10: 0.0775/0.0863/0.1541; (items 1/2/3) HR@10: 0.2047/0.0771/0.0221
- Точка проверки: results/beauty_muon_l2_lipmlp.json (полные метрики и история обучения)

### beauty_muon_l4_lipmlp — 2026-10-13
- Конфиг: Beauty, num_blocks=4, optimizer=muon + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=21, best_val_NDCG@10=0.07, время=0.27 ч
- Тест: HR@10=0.0836, NDCG@10=0.0516, Coverage@10=0.6504
- Бакеты (users 1/2/3) NDCG@10: 0.0456/0.0498/0.0946; (items 1/2/3) NDCG@10: 0.1275/0.0416/0.0121
- Бакеты (users 1/2/3) HR@10: 0.0739/0.083/0.1481; (items 1/2/3) HR@10: 0.205/0.0689/0.0196
- Точка проверки: results/beauty_muon_l4_lipmlp.json (полные метрики и история обучения)

### yambda_adamw_l4_lipmlp — 2026-10-13
- Конфиг: Yambda, num_blocks=4, optimizer=adamw + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=33, best_val_NDCG@10=0.0658, время=0.91 ч
- Тест: HR@10=0.1317, NDCG@10=0.0633, Coverage@10=0.2609
- Бакеты (users 1/2/3) NDCG@10: 0.0819/0.0658/0.056; (items 1/2/3) NDCG@10: 0.0525/0.0639/0.0736
- Бакеты (users 1/2/3) HR@10: 0.1683/0.1368/0.1174; (items 1/2/3) HR@10: 0.1145/0.1316/0.149
- Точка проверки: results/yambda_adamw_l4_lipmlp.json (полные метрики и история обучения)

### beauty_muon_l6_lipmlp — 2026-10-13
- Конфиг: Beauty, num_blocks=6, optimizer=muon + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=25, best_val_NDCG@10=0.0703, время=0.38 ч
- Тест: HR@10=0.0812, NDCG@10=0.0504, Coverage@10=0.5934
- Бакеты (users 1/2/3) NDCG@10: 0.0438/0.0493/0.0954; (items 1/2/3) NDCG@10: 0.1222/0.0434/0.0109
- Бакеты (users 1/2/3) HR@10: 0.0722/0.0804/0.1416; (items 1/2/3) HR@10: 0.1956/0.07/0.0186
- Точка проверки: results/beauty_muon_l6_lipmlp.json (полные метрики и история обучения)

### beauty_adamw_l2_lipfull — 2026-10-13
- Конфиг: Beauty, num_blocks=2, optimizer=adamw + lipschitz attention+MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на attention и MLP веса каждого блока
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=14, best_val_NDCG@10=0.0675, время=0.15 ч
- Тест: HR@10=0.0778, NDCG@10=0.0473, Coverage@10=0.7952
- Бакеты (users 1/2/3) NDCG@10: 0.0424/0.045/0.0854; (items 1/2/3) NDCG@10: 0.1095/0.0418/0.0128
- Бакеты (users 1/2/3) HR@10: 0.0701/0.0753/0.1351; (items 1/2/3) HR@10: 0.181/0.0679/0.0212
- Точка проверки: results/beauty_adamw_l2_lipfull.json (полные метрики и история обучения)

### beauty_adamw_l4_lipfull — 2026-10-13
- Конфиг: Beauty, num_blocks=4, optimizer=adamw + lipschitz attention+MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на attention и MLP веса каждого блока
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=12, best_val_NDCG@10=0.0692, время=0.21 ч
- Тест: HR@10=0.0813, NDCG@10=0.0496, Coverage@10=0.7777
- Бакеты (users 1/2/3) NDCG@10: 0.0436/0.0489/0.0905; (items 1/2/3) NDCG@10: 0.1213/0.0399/0.0127
- Бакеты (users 1/2/3) HR@10: 0.072/0.0814/0.1407; (items 1/2/3) HR@10: 0.1986/0.0645/0.0215
- Точка проверки: results/beauty_adamw_l4_lipfull.json (полные метрики и история обучения)

### beauty_adamw_l6_lipfull — 2026-10-13
- Конфиг: Beauty, num_blocks=6, optimizer=adamw + lipschitz attention+MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на attention и MLP веса каждого блока
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=16, best_val_NDCG@10=0.07, время=0.32 ч
- Тест: HR@10=0.0848, NDCG@10=0.0518, Coverage@10=0.7666
- Бакеты (users 1/2/3) NDCG@10: 0.046/0.0507/0.0925; (items 1/2/3) NDCG@10: 0.1261/0.0425/0.013
- Бакеты (users 1/2/3) HR@10: 0.0749/0.0856/0.1467; (items 1/2/3) HR@10: 0.2038/0.07/0.0225
- Точка проверки: results/beauty_adamw_l6_lipfull.json (полные метрики и история обучения)

### beauty_muon_l2_lipfull — 2026-10-13
- Конфиг: Beauty, num_blocks=2, optimizer=muon + lipschitz attention+MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на attention и MLP веса каждого блока
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=10, best_val_NDCG@10=0.0695, время=0.14 ч
- Тест: HR@10=0.0806, NDCG@10=0.0495, Coverage@10=0.7508
- Бакеты (users 1/2/3) NDCG@10: 0.0448/0.0468/0.0873; (items 1/2/3) NDCG@10: 0.1198/0.0405/0.0128
- Бакеты (users 1/2/3) HR@10: 0.0731/0.0776/0.1375; (items 1/2/3) HR@10: 0.1926/0.0657/0.0227
- Точка проверки: results/beauty_muon_l2_lipfull.json (полные метрики и история обучения)

### yambda_adamw_l6_lipmlp — 2026-10-13
- Конфиг: Yambda, num_blocks=6, optimizer=adamw + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: AdamW (все параметры)
- Обучение: best_epoch=25, best_val_NDCG@10=0.0656, время=1.06 ч
- Тест: HR@10=0.1334, NDCG@10=0.064, Coverage@10=0.24
- Бакеты (users 1/2/3) NDCG@10: 0.0808/0.0647/0.0578; (items 1/2/3) NDCG@10: 0.0559/0.0646/0.0714
- Бакеты (users 1/2/3) HR@10: 0.1672/0.1356/0.1209; (items 1/2/3) HR@10: 0.122/0.1345/0.1439
- Точка проверки: results/yambda_adamw_l6_lipmlp.json (полные метрики и история обучения)

### beauty_muon_l4_lipfull — 2026-10-13
- Конфиг: Beauty, num_blocks=4, optimizer=muon + lipschitz attention+MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на attention и MLP веса каждого блока
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=12, best_val_NDCG@10=0.0713, время=0.24 ч
- Тест: HR@10=0.0842, NDCG@10=0.0517, Coverage@10=0.7181
- Бакеты (users 1/2/3) NDCG@10: 0.0459/0.0495/0.0953; (items 1/2/3) NDCG@10: 0.1268/0.0421/0.0127
- Бакеты (users 1/2/3) HR@10: 0.0755/0.0812/0.149; (items 1/2/3) HR@10: 0.2059/0.0679/0.0214
- Точка проверки: results/beauty_muon_l4_lipfull.json (полные метрики и история обучения)

### beauty_muon_l6_lipfull — 2026-10-13
- Конфиг: Beauty, num_blocks=6, optimizer=muon + lipschitz attention+MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=20, batch=64
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на attention и MLP веса каждого блока
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=16, best_val_NDCG@10=0.0699, время=0.36 ч
- Тест: HR@10=0.0863, NDCG@10=0.0523, Coverage@10=0.6928
- Бакеты (users 1/2/3) NDCG@10: 0.0464/0.0506/0.095; (items 1/2/3) NDCG@10: 0.1279/0.0438/0.0118
- Бакеты (users 1/2/3) HR@10: 0.0764/0.0861/0.1513; (items 1/2/3) HR@10: 0.2072/0.0746/0.0201
- Точка проверки: results/beauty_muon_l6_lipfull.json (полные метрики и история обучения)

### yambda_muon_l2_lipmlp — 2026-10-13
- Конфиг: Yambda, num_blocks=2, optimizer=muon + lipschitz MLP, hidden=128, heads=2, dropout=0.4, lr=3.94e-04, loss=sce, max_seq_len=100, batch=128
- Регуляризация: Lipschitz (W <- W/sigma_max(W), power iteration) на conv1.weight и conv2.weight каждого FFN-блока (MLP)
- Оптимизатор: Muon (2D веса attention/FFN) + AdamW (1D веса и эмбеддинги)
- Обучение: best_epoch=22, best_val_NDCG@10=0.0603, время=0.63 ч
- Тест: HR@10=0.1234, NDCG@10=0.0598, Coverage@10=0.251
- Бакеты (users 1/2/3) NDCG@10: 0.0775/0.0609/0.0533; (items 1/2/3) NDCG@10: 0.053/0.0605/0.066
- Бакеты (users 1/2/3) HR@10: 0.1586/0.1247/0.1105; (items 1/2/3) HR@10: 0.1151/0.1241/0.131
- Точка проверки: results/yambda_muon_l2_lipmlp.json (полные метрики и история обучения)

---

<!-- проект: AI4Science -->
<!-- источник: AI4Science/diary.md -->
<!-- дата: 2026-10-14 -->
## 2026-10-14 — построение графа проекта week4

- **Что сделано:**
  - Создан скрипт `week_4/build_graph.py`, который парсит заметки из `demo_graph_test/`
  - Извлечены связи из заметок (ссылки вида [[Название]])
  - Построен направленный граф с 46 узлами и 27 рёбрами
  - Сохранён как PNG в `week_4/plots/graph_demo_graph_test.png`

- **Структура графа:**
  - 13 узлов типа 'note' (заметки объектов)
  - 7 узлов типа 'task' (задачи)
  - 15 узлов типа 'ontology' (классы онтологии)
  - 11 узлов типа 'file' (файлы проекта)

- **Цвета на графе:**
  - Зелёный — заметки объектов (эксперименты, результаты, серии)
  - Оранжевый — задачи
  - Серый — классы онтологии
  - Синий — файлы проекта

- **Ключевые связи:**
  - Задача "Проверить закон Аррениуса" → подзадачи
  - Эксперимент "Расчёт E_a по трём сериям" → использует серии, применяет метод, даёт результат
  - Результат → проверяется проверкой
  - Все объекты связаны с файлами проекта

---

<!-- проект: Paper_search -->
<!-- источник: Paper_search/diary.md -->
<!-- дата: 2026-10-14 -->
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

---


---

<!-- проект: sasrec_experiments -->
<!-- источник: sasrec_experiments/diary.md -->
<!-- дата: 2026-10-23 -->
## 2026-10-23 — SASRec на Beauty: базовые эксперименты (AdamW / Muon, L=2,4,6)

### Цель
Запустить SASRec на датасете Beauty (reviews_Beauty_5) с разным числом слоёв
и двумя оптимизаторами (AdamW, Muon), проверить масштабирование LR по формуле
`lr(L) = lr_ref * sqrt(4/L)`.

### Данные
- 198 502 взаимодействия, 22 363 пользователя, 12 101 товар.
- Temporal split: train (140 965), validation (50 336), test (90 621).
- Проверка temporal split: 0 нарушений, prefix-свойство выполнено.

### Результаты (test NDCG@10)

| Optimizer | L=2 | L=4 | L=6 |
|---|---|---|---|
| AdamW | 0.012762 | 0.004797 | 0.005645 |
| Muon | 0.005187 | 0.003540 | 0.003692 |

AdamW лучше Muon на всех глубинах. L=2 даёт лучший результат для обоих
оптимизаторов; увеличение глубины ухудшает качество.

### Файлы
- `sasrec_depth_lr_results.json` — сводка по всем запускам
- `outputs/adamw_l{2,4,6}/`, `outputs/muon_all2d_l{2,4,6}/`, `outputs/muon_l{2,4,6}/`
- `logs/` — логи всех экспериментов

---

<!-- проект: sasrec_experiments -->
<!-- источник: sasrec_experiments/diary.md -->
<!-- дата: 2026-10-23 -->
## 2026-10-23 — Experiment: AdamW + StackRec for SASRec (Beauty)

### Цель
Реализовать StackRec-style progressive layer stacking для 6-слойного SASRec
с AdamW и получить метрики валидации/теста для трёх эффективных глубин
в рамках одного непрерывного обучения:
1. последние 2 слоя (4, 5),
2. средние 4 слоя (2-5),
3. все 6 слоёв.

### Реализация
- `src/models/sequence.py`: добавлены per-layer forward coefficients
  (`layer_scales`). Коэффициент 0 делает слой identity (пропуск).
  Внутренний `nn.TransformerEncoder` заменён на ручной цикл по слоям.
  Добавлены хелперы: `set_layer_scales`, `get_layer_scales`,
  `set_layers_trainable`, `copy_layer_weights`.
- `configs/beauty_sasrec_stackrec.yaml` — новый Hydra-конфиг.
- `run_stackrec.py` — one-process progressive training loop.

### Протокол
- Dataset: Beauty, seed 42, batch size 128.
- Optimizer: AdamW, weight_decay=0, betas=(0.9, 0.999), grad clip 10.0.
- Stage learning rates: `lr(L) = lr_ref * sqrt(4/L)`.
- Stage 1 (2_layers, 90 epochs): layers 4,5 trainable; layers 0-3 frozen.
- Stage 2 (4_layers, 60 epochs, 10-epoch ramp): copy 4->2, 5->3.
- Stage 3 (6_layers, 60 epochs, 10-epoch ramp): copy 2->0, 3->1.
- Best-checkpoint selection per stage: best validation ndcg@10.

### Результаты (best complete-gate checkpoint per stage)

| effective layers | lr | best epoch | val ndcg@10 | test ndcg@10 | val recall@10 | test recall@10 |
|---:|---:|---:|---:|---:|---:|---:|
| 2 (layers 4,5) | 0.00297027 | 88 | 0.014714 | 0.011958 | 0.029630 | 0.023380 |
| 4 (layers 2-5) | 0.00210030 | 129 | 0.015451 | 0.012964 | 0.031746 | 0.025370 |
| 6 (all layers) | 0.00171488 | 194 | 0.016095 | 0.013299 | 0.033439 | 0.025494 |

Total training time: ~854 s.

### Сравнение с AdamW без stacking

| layers | AdamW select test ndcg@10 | StackRec test ndcg@10 |
|---:|---:|---:|
| 2 | 0.012762 | 0.011958 |
| 4 | 0.004797 | 0.012964 |
| 6 | 0.005645 | 0.013299 |

StackRec substantially better for 4 and 6 effective layers (2.3-2.7x higher).

---

<!-- проект: sasrec_experiments -->
<!-- источник: sasrec_experiments/diary.md -->
<!-- дата: 2026-10-23 -->
## 2026-10-23 — Experiment: Muon + StackRec for SASRec (Beauty)

### Цель
Повторить StackRec эксперимент с Muon оптимизатором вместо AdamW.

### Реализация
- `run_stackrec.py` сделан optimizer-agnostic: `optimizer.type` = adamw/muon.
- Для muon: 2D hidden weights → Muon, embeddings/1D → AdamW.
- Новый конфиг: `configs/beauty_sasrec_stackrec_muon.yaml`.

### Результаты

| effective layers | muon lr | adamw lr | best epoch | val ndcg@10 | test ndcg@10 |
|---:|---:|---:|---:|---:|---:|
| 2 | 0.02828427 | 0.00297027 | 85 | 0.007215 | 0.004602 |
| 4 | 0.02000000 | 0.00210030 | 119 | 0.007884 | 0.004518 |
| 6 | 0.01632993 | 0.00171488 | 173 | 0.007008 | 0.004341 |

Muon + StackRec улучшает plain Muon для 4 и 6 слоёв, но остаётся ниже
AdamW + StackRec. Лучший Muon stage — 4 layers.

---

<!-- проект: sasrec_experiments -->
<!-- источник: sasrec_experiments/diary.md -->
<!-- дата: 2026-10-26 -->
## 2026-10-26 — Experiment: StackRec with boundary identity auxiliary loss

### Цель
При добавлении новой группы 2 слоёв ниже обученной подсети:
1. добавить обучаемый скаляр на выходе последнего слоя новой группы;
2. добавить auxiliary loss, который приводит отношение выхода новой группы
   к входному представлению обученной подсети к 1;
3. линейно убывать коэффициент auxiliary loss по мере роста stacking coefficient.

### Теоретическая связь
`lambda(alpha) = lambda0 * (1 - alpha)`, где alpha — forward scale новой группы.
Lambda убывает линейно до 0, когда alpha достигает 1.

### Результаты (plain / aux, relative delta)

**NDCG@10**

| optimizer | layers | val | test |
|---|---:|---|---|
| AdamW | 2 | 0.014714 / 0.014714 (+0.00%) | 0.011958 / 0.011958 (+0.00%) |
| AdamW | 4 | 0.015451 / 0.015920 (+3.04%) | 0.012964 / 0.012934 (-0.23%) |
| AdamW | 6 | 0.016095 / 0.016328 (+1.45%) | 0.013299 / 0.013086 (-1.60%) |
| Muon | 2 | 0.007215 / 0.007215 (+0.00%) | 0.004602 / 0.004602 (+0.00%) |
| Muon | 4 | 0.007884 / 0.007327 (-7.06%) | 0.004518 / 0.004591 (+1.61%) |
| Muon | 6 | 0.007008 / 0.006883 (-1.79%) | 0.004341 / 0.004351 (+0.24%) |

### Выводы
- Для AdamW: auxiliary loss улучшает validation NDCG@10 (+3.0%, +1.5%),
  но test NDCG@10 немного хуже (-0.2%, -1.6%).
- Для Muon: mixed/negative — validation падает, test немного улучшается.
- Научённые boundary scalars: все > 1 (компенсация sub-unit forward ramp).

---

<!-- проект: sasrec_experiments -->
<!-- источник: sasrec_experiments/diary.md -->
<!-- дата: 2026-10-26 -->
## 2026-10-26 — Experiment: hyperbolic heads at StackRec group boundaries

### Цель
Добавить hyperbolic (Poincare-ball) next-item head на выходе каждой группы,
которую StackRec добавляет ниже обученной подсети.

### Curvature schedule
`c(d) = c_ref * (d_ref / d) ** power`, где d — абсолютная глубина head.
Кривизна убывает с глубиной: c ~ 1/L^2 для power=2.

### Результаты (test NDCG@10)

| effective layers | plain ndcg@10 | aux ndcg@10 | hyperbolic ndcg@10 | hyp vs plain |
|---:|---:|---:|---:|---:|
| 2 | 0.011958 | 0.011958 | 0.011958 | +0.00% |
| 4 | 0.012964 | 0.012934 | 0.012428 | -4.13% |
| 6 | 0.013299 | 0.013086 | 0.013419 | +0.90% |

### Выводы
- Depth-decaying curvature schedule работает; 6-layer модель получает
  прирост на test NDCG/Recall/coverage (+0.9% vs plain, +2.5% vs aux).
- 4-layer stage слабее — возможно, фиксированный loss_coeff=0.1 слишком мал.

---

<!-- проект: sasrec_experiments -->
<!-- источник: sasrec_experiments/diary.md -->
<!-- дата: 2026-10-26 -->
## 2026-10-26 — Experiment: Lorentz hyperbolic residual on StackRec group boundaries

### Цель
Ввести гиперболическую геометрию *в скрытое представление* копируемой
StackRec группы вместо только auxiliary hyperbolic prediction.

### Реализация
- `src/models/hyperbolic.py`: `lorentz_expmap0`, `lorentz_distance`,
  `LorentzResidualHead` (item-scoring + residual branches).
- Residual: `r = (sinhc(sqrt(c)||u||) - 1) * res_out(u)` — ровно 0 при c=0.
- Norm-preserving: `h_out = normalize(h + gate * normalize_to_norm(h, r))`.
- Gate и curvature ramp от 0 до целевых значений.

### Верификация
- Unit-level checks (CPU): hyperboloid constraint, symmetric distance,
  zero residual at c=0, bitwise identity at gate=0, norm preservation.
- Smoke run (2/3/3 epochs): stage-start continuity exact, gate/c logs
  соответствуют ожиданиям.

---

<!-- проект: sasrec_experiments -->
<!-- источник: sasrec_experiments/diary.md -->
<!-- дата: 2026-10-30 -->
## 2026-10-30 — Тесты метрик ранжирования

**Дата:** 2026-10-30, **Платформа:** CPU, **Данные:** 10 пользователей, 10 товаров, top-k = 5

| # | Метрика | Статус | Значение |
|---|---------|--------|----------|
| 1 | NDCG@5 | PASS | 0.487914 |
| 2 | Recall@5 | PASS | 0.800000 |
| 3 | Coverage@5 | PASS | 1.000000 |
| 4 | Novelty@5 | PASS | 0.944260 |
| 5 | MeanRank@5 | PASS | 3.500000 |
| 6 | ILD@5 | PASS | 0.506127 |
| 7 | PopularityGroups | PASS | OK |
| 8 | EdgeCases | PASS | OK |
| 9 | CoveragePartial | PASS | 0.100000 |
| 10 | MeanRankPartial | PASS | 1.000000 |

**Итого:** 10/10 PASS

**Замечания:**
1. `NDCGMetric` вычисляет DCG, а не нормализованный NDCG (без деления на IDCG).
2. `RecallMetric` считает абсолютное число hits (не нормализованное на |true|).
3. `CoverageMetric` и `NoveltyMetric` — stateful: требуют `.reduce()`.
4. `MeanRankMetric` — stateful: требует `.reduce()`.

---

<!-- проект: sasrec_experiments -->
<!-- источник: sasrec_experiments/diary.md -->
<!-- дата: 2026-10-30 -->
## 2026-10-30 — Проверка temporal split датасета

**Датасет:** `reviews_Beauty_5` (5-core), 198 502 interactions, 22 363 users, 12 101 items

| Split | Rows | Users | Items |
|-------|------|-------|-------|
| train | 140 965 | 18 474 | 11 534 |
| validation | 50 336 | 4 725 | 10 310 |
| test | 90 621 | 8 041 | 11 727 |
| train_validation | 151 081 | 18 474 | 11 736 |

**Результат:** Нарушений temporal split: 0. Статус: ✅ CORRECT.
`train ⊂ val ⊂ test` (prefix-свойство): True.

---

<!-- проект: sasrec_experiments -->
<!-- источник: sasrec_experiments/diary.md -->
<!-- дата: 2026-10-30 -->
## 2026-10-30 — Тесты StackRec (17 тестов, CPU)

**Файл:** `test_stackrec.py`, 17 тестов, CPU, 2 примера (seq=5, seq=20)

| # | Тест | Статус |
|---|------|--------|
| 1 | Model initialization | PASS |
| 2 | Forward pass (short seq=5) | PASS |
| 3 | Forward pass (long seq=20) | PASS |
| 4 | Stage 1 — 2 layers (4, 5) | PASS |
| 5 | Stage 2 — 4 layers (2-5) with copy | PASS |
| 6 | Stage 3 — 6 layers (0-5) with copy | PASS |
| 7 | Full StackRec pipeline (short seq=5) | PASS |
| 8 | Full StackRec pipeline (long seq=20) | PASS |
| 9 | Ramp scale=0 identity | PASS |
| 10 | Aux scalar and boundary | PASS |
| 11 | Lorentz head addition | PASS |
| 12 | Curvature schedule | PASS |
| 13 | Copy layer weights | PASS |
| 14 | Batch with two sequences | PASS |
| 15 | CPU only | PASS |
| 16 | SASRec vs StackRec (2 layers) identity | PASS |
| 17 | SASRec vs StackRec (2 layers) long seq | PASS |

**Итого:** 17/17 PASS

**Ключевые проверки:**
- Тест 9: при scale=0 новые слои — identity, предсказания совпадают
  с моделью, обученной только на 2 слоях.
- Тест 16-17: StackRec с 6 слоями (scale=0 для 0-3) даёт абсолютно
  идентичные предсказания с SASRec на 2 слоях — ключевое свойство
  progressive stacking.
