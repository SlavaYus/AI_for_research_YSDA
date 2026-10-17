#!/usr/bin/env python3
"""Генерация PDF-отчёта по diary.md (reportlab)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = "/home/yusupov/Agent_shad/AI_for_research_YSDA/report.pdf"

_FDIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DejaVu", _FDIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", _FDIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Oblique",
                               _FDIR + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-BoldOblique",
                               _FDIR + "DejaVuSans-BoldOblique.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuMono",
                               _FDIR + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily(
    "DejaVu", normal="DejaVu", bold="DejaVu-Bold",
    italic="DejaVu-Oblique", boldItalic="DejaVu-BoldOblique")
pdfmetrics.registerFontFamily(
    "DejaVu-Bold", normal="DejaVu-Bold", bold="DejaVu-Bold",
    italic="DejaVu-Bold", boldItalic="DejaVu-Bold")

styles = getSampleStyleSheet()

for _s in styles.byName.values():
    if not hasattr(_s, "fontName"):
        continue
    _s.fontName = {
        "Helvetica": "DejaVu", "Helvetica-Bold": "DejaVu-Bold",
        "Helvetica-Oblique": "DejaVu-Oblique",
        "Helvetica-BoldOblique": "DejaVu-BoldOblique",
        "Times-Roman": "DejaVu", "Times-Bold": "DejaVu-Bold",
        "Times-Italic": "DejaVu-Oblique",
        "Times-BoldItalic": "DejaVu-BoldOblique",
        "Courier": "DejaVu", "Courier-Bold": "DejaVu-Bold",
        "Courier-Oblique": "DejaVu-Oblique",
        "Courier-BoldOblique": "DejaVu-BoldOblique",
    }.get(_s.fontName, "DejaVu")

title_s = ParagraphStyle(
    "T", parent=styles["Title"], fontSize=15, spaceAfter=2 * mm,
    textColor=HexColor("#1a1a2e"),
)
sub_s = ParagraphStyle(
    "Sub", parent=styles["Normal"], fontSize=9, alignment=TA_CENTER,
    textColor=HexColor("#555555"), spaceAfter=4 * mm,
)
h1 = ParagraphStyle(
    "H1", parent=styles["Heading1"], fontSize=11.5, spaceBefore=4 * mm,
    spaceAfter=2 * mm, textColor=HexColor("#16324f"),
)
h2 = ParagraphStyle(
    "H2", parent=styles["Heading2"], fontSize=10, spaceBefore=2.5 * mm,
    spaceAfter=1 * mm, textColor=HexColor("#234e70"),
)
body = ParagraphStyle(
    "B", parent=styles["Normal"], fontSize=9, leading=11.5,
    alignment=TA_JUSTIFY, spaceAfter=1.5 * mm,
)
quote = ParagraphStyle(
    "Q", parent=styles["Normal"], fontSize=8.5, leading=10.5,
    leftIndent=6 * mm, rightIndent=3 * mm, fontName="DejaVu-Oblique",
    textColor=HexColor("#333333"), spaceBefore=1 * mm, spaceAfter=1 * mm,
)
bul = ParagraphStyle(
    "Bu", parent=body, leftIndent=5 * mm, bulletIndent=1 * mm,
    spaceAfter=0.8 * mm,
)

story = []


def hr():
    story.append(Spacer(1, 1 * mm))
    story.append(HRFlowable(width="100%", thickness=0.4,
                            color=HexColor("#bbbbbb")))


story.append(Paragraph("Отчёт о проделанной работе", title_s))
story.append(Paragraph(
    "Курс ШАД «ИИ-ассистенты для исследователя. AI4Science» · "
    "Юупов Вячеслав · 17 записей журнала · 3 проекта · "
    "28.09.2026 — 14.10.2026", sub_s))
hr()

# ---------------------------------------------------------------- 1
story.append(Paragraph("1. Структура репозитория", h1))
story.append(Paragraph(
    "<b>AI4Science/</b> — учебный проект: консольный агент (обёртка над "
    "Goose с MCP-инструментами: Lean 4, веб-поиск, чтение PDF, skills). "
    "Задачи недель: расчёт энергии активации, запуск pytest и генерация "
    "отчёта о тестах, эксперимент с AGENTS.md (поиск пиков в спектрах "
    "до/после), построение графа знаний проекта.", body))
story.append(Paragraph(
    "<b>Paper_search/</b> — исследовательский трек: проверка закона "
    "Аррениуса с построением графа знаний в Obsidian (онтология, задачи, "
    "эксперименты, источники); сбор литературы через OpenAlex (Arrhenius, "
    "Laidler + 8 цитирующих работ, связь с Wikidata); поиск 5 статей "
    "arXiv по аппроксимации гессиана (K-FAC, Sophia, SOAP и др.).", body))
story.append(Paragraph(
    "<b>SASRec_exp/</b> — эксперименты с рекомендательной моделью SASRec "
    "на датасетах Beauty и Yambda: сравнение оптимизаторов AdamW vs "
    "Muon (гибридный: 2D-веса attention/FFN — Muon, 1D — AdamW), глубины "
    "2/4/6 блоков, Lipschitz-регуляризации attention и MLP (spectral "
    "norm через power-итерацию), масштабирование lr ~ 1/√K при росте "
    "числа параметров. Итого 70+ прогонов с автоматической записью "
    "метрик в diary.", body))
story.append(Paragraph(
    "<b>diary.md</b> — объединённый журнал (958 строк) из трёх проектов; "
    "каждая сессия/прогон дописывает в него секцию с конфигом, "
    "метриками и точкой проверки. <b>AGENT.md</b>, <b>README.md</b> — "
    "конфигурация агента и описание репозитория.", body))

# ---------------------------------------------------------------- 2
story.append(Paragraph("2. Примеры запросов агенту", h1))

examples = [
    ("2.1 Энергия активации (AI4Science, 28.09)",
     "«Посчитай энергию активации по data/raw/rates.csv; ответ одним "
     "числом в кДж/моль.»",
     "Агент прочитал INDEX.md/STATUS.md/src/tests, запустил тесты и "
     "<font face='DejaVuMono'>python -m src.report</font>. Результат: "
     "<b>E_a = 51,66 ± 0,39 кДж/моль</b> по 15 точкам; серия 2024-03 "
     "исключена. Проверка <font face='DejaVuMono'>pytest && src.report</font> — код 0."),
    ("2.2 Закон Аррениуса + граф знаний (Paper_search, 05.10)",
     "«Проверь, подчиняется ли разложение закону Аррениуса в интервале "
     "25–70 °C, и найди энергию активации по data/raw/rates.csv. "
     "Результат проверь независимым пересчётом.»",
     "R² = 0,9993, E_a = 51,66 кДж/моль; независимый двухточечный "
     "пересчёт 51,23–51,89. Инициализирован граф Obsidian (онтология, "
     "задачи, эксперименты, результаты, источники). Позже: «Подготовь для "
     "коллег отчёт с графиком и ссылками на источники из library/» — "
     "создан отчёт + график ln k vs 1/T."),
    ("2.3 Сбор литературы (Paper_search, 11.10)",
     "«Собери литературу к проекту…» (поиск OpenAlex, 8 наиболее "
     "цитируемых работ Laidler, открытые версии, уравнение Аррениуса в "
     "Wikidata).",
     "Добавлены записи OpenAlex (W4253789658, W2052953969), созданы "
     "заметки авторов и цитирующих работ, скачан PDF. Задача частично "
     "заблокирована (серверы вернули HTML вместо PDF) — агент корректно "
     "эскалировал блокировку пользователю."),
    ("2.4 Влияние AGENTS.md (AI4Science, 13.10)",
     "«Найди положения и ширины пиков во всех спектрах из data/» — "
     "затем тот же запрос: «Выполни цель из AGENTS.md.»",
     "Оба прогона нашли 9 пиков. Без AGENTS.md — 8 шагов; с ним — 16 "
     "шагов, но результаты точнее совпали с ожидаемыми, агент сам "
     "вызвал проверку перед финальным ответом (ReAct-режим)."),
    ("2.5 Каркас SASRec-экспериментов (SASRec_exp, 13.10)",
     "«Скопировать код SASRec и split в текущую папку, реализовать "
     "эксперименты на Beauty и Yambda: SASRec с числом трансформерных "
     "блоков 2/4/6, оптимизаторы AdamW и Muon, метрики HR@10 / NDCG@10 / "
     "Coverage@10; затем Lipschitz-регуляризация attention-слоя и те же "
     "прогоны с ней; финальный barplot.»",
     "Создан пакет src/ (модель, сплиты, датасеты, SCE-loss, "
     "HybridMuonAdamW, метрики, тренировка, драйвер грида, plot). "
     "Подобран оптимальный конфиг (B: h=128, SCE) и muon_lr. Sweep из "
     "24 прогонов запущен фоном, каждый прогон сам дописывал секцию в "
     "diary."),
    ("2.6 Коррекция по ходу (SASRec_exp, 13.10)",
     "(внутренняя коррекция) «Muon с lr=0.005 на Beauty расходится при "
     "num_blocks=4: train_loss растёт, val NDCG@10 падает до 0.014.»",
     "Агент остановил sweep, перебрал muon_lr по глубине, зафиксировал "
     "единый muon_lr=0.0025, удалил невалидные json и перезапустил "
     "драйверы (готовые прогоны пропускались)."),
    ("2.7 Масштабирование lr ~ 1/√K (SASRec_exp, 13.10)",
     "«Запустить эксперименты, в которых при увеличении числа параметров "
     "модели в K раз learning rate уменьшается в √K раз.»",
     "20 прогонов (hidden 64/128/256, оба оптимизатора, 2 датасета). "
     "Правило подтверждено в 4/4 сравнениях при K≈2; обратная "
     "экстраполяция (K<1) вредит. Попутно найден и исправлен баг "
     "arm='base' в src/param_scaling.py."),
    ("2.8 Поиск статей по гессиану (Paper_search, 14.10)",
     "«Найди в Arxiv 5 статей по оптимизации с использованием "
     "аппроксимации гессиана. Для отправной точки используй статьи из "
     "papers/; для поиска используй инструменты из week4 и week5.»",
     "Определены отправные статьи (AdamW, Shampoo, Muon, MuonRec), "
     "через OpenAlex-инструменты отобрано 5 работ: K-FAC, Sophia, SOAP, "
     "Dissecting Hessian, KF-QN; PDF скачаны, отчёт "
     "reports/hessian_search_report.md."),
]

for head, req, res in examples:
    story.append(Paragraph(head, h2))
    story.append(Paragraph(req, quote))
    story.append(Paragraph(res, body))

# ---------------------------------------------------------------- 3
story.append(Paragraph("3. Ключевые результаты и выводы", h1))

tbl_data = [
    ["Блок", "Итог"],
    ["Энергия активации", "E_a = 51,66 ± 0,39 кДж/моль; R² = 0,9993"],
    ["SASRec, оптимизаторы",
     "AdamW ≥ Muon по NDCG; Muon даёт больший Coverage на Yambda"],
    ["Lipschitz-регуляризация",
     "Сохраняет Coverage при росте глубины; на Yambda нестабильна с "
     "AdamW, стабильна с Muon"],
    ["Масштабирование lr",
     "lr ~ 1/√K подтверждено при K≈2 (4/4 сравнения)"],
    ["Графы знаний",
     "Граф Obsidian (23 заметки) + граф проекта (46 узлов, 27 рёбер)"],
]

tbl = Table(tbl_data, colWidths=[45 * mm, 115 * mm])
tbl.setStyle(TableStyle([
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("LEADING", (0, 0), (-1, -1), 10),
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#dce6f1")),
    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#16324f")),
    ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "DejaVu-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#999999")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 1.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
]))
story.append(tbl)
story.append(Spacer(1, 2 * mm))

for b in [
    "Агент последовательно решает задачи разного уровня — от одного "
    "числа в ответе до многодневных свипов на GPU с автоматическим "
    "ведением журнала.",
    "AGENTS.md повышает качество и добавляет автопроверку ценой "
    "удвоения числа шагов; без него агент также справляется, но менее "
    "точно.",
    "Агент корректно эскалирует блокировки (недоступные PDF) и сам "
    "находит баги в собственном коде (arm='base', расходимость Muon).",
    "diary.md — единая точка правды: каждая сессия оставляет запрос, "
    "результат, точку проверки и статус приёмки.",
]:
    story.append(Paragraph(b, bul, bulletText="•"))

hr()
story.append(Paragraph(
    "Отчёт сгенерирован на основе diary.md · reportlab · 2026-10-17",
    ParagraphStyle("F", parent=styles["Normal"], fontSize=7.5,
                   alignment=TA_CENTER, textColor=HexColor("#888888"))))

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    topMargin=1.5 * cm, bottomMargin=1.5 * cm,
    leftMargin=1.8 * cm, rightMargin=1.8 * cm,
)
doc.build(story)
print("OK:", OUT)
