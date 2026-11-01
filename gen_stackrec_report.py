#!/usr/bin/env python3
"""Generate StackRec report PDF in English using reportlab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

def build_pdf(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'ReportTitle', parent=styles['Title'],
        fontSize=16, leading=20, spaceAfter=6*mm,
        alignment=TA_CENTER, textColor=HexColor('#1a1a2e')
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=11, leading=14, spaceAfter=10*mm,
        alignment=TA_CENTER, textColor=HexColor('#555555'),
        fontName='Helvetica-Oblique'
    )
    heading_style = ParagraphStyle(
        'Heading2', parent=styles['Heading2'],
        fontSize=13, leading=16, spaceBefore=8*mm, spaceAfter=4*mm,
        textColor=HexColor('#16213e'), fontName='Helvetica-Bold'
    )
    heading3_style = ParagraphStyle(
        'Heading3', parent=styles['Heading3'],
        fontSize=11, leading=14, spaceBefore=6*mm, spaceAfter=3*mm,
        textColor=HexColor('#1a1a2e'), fontName='Helvetica-Bold'
    )
    normal_style = ParagraphStyle(
        'ReportNormal', parent=styles['Normal'],
        fontSize=10, leading=13, spaceAfter=3*mm,
        alignment=TA_JUSTIFY, fontName='Helvetica'
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=normal_style,
        leftIndent=15*mm, fontSize=10, leading=13,
        spaceAfter=1*mm, fontName='Helvetica'
    )
    small_style = ParagraphStyle(
        'Small', parent=normal_style,
        fontSize=9, leading=11, fontName='Helvetica'
    )

    # Title
    story.append(Paragraph(
        "StackRec Report: Progressive Layer Stacking for SASRec",
        title_style
    ))
    story.append(Paragraph(
        "Experiments on Beauty Dataset (reviews_Beauty_5) &mdash; October 2026",
        subtitle_style
    ))
    story.append(Spacer(1, 3*mm))

    # Section 1: Introduction
    story.append(Paragraph("1. Introduction", heading_style))
    story.append(Paragraph(
        "StackRec is a progressive depth-narrowing method adapted for the "
        "SASRec (Sequential Recommendation) model. Instead of training a "
        "deep model from scratch, training starts with the bottom 2 transformer "
        "layers, then weights are copied to new layers and all 6 layers are "
        "gradually activated.",
        normal_style
    ))
    story.append(Paragraph(
        "Key property: when layer scale=0, lower layers act as identity "
        "functions, so a 2-layer subnet inside a 6-layer model produces "
        "<b>identical</b> predictions to a standalone 2-layer SASRec "
        "(tests 16-17, 17/17 PASS).",
        normal_style
    ))

    # Section 2: Architecture
    story.append(Paragraph("2. StackRec Architecture", heading_style))
    story.append(Paragraph(
        "The model always has 6 transformer layers. Per-layer forward "
        "coefficients (<i>layer_scales</i>) control layer activation: "
        "scale=0 means identity (skip), scale=1 means full activation.",
        normal_style
    ))
    story.append(Paragraph("Training stages:", heading3_style))
    story.append(Paragraph(
        "<bullet>&bull;</bullet> <b>Stage 1 (2_layers, 90 epochs):</b> "
        "train layers 4,5; layers 0-3 frozen with scale=0.", bullet_style))
    story.append(Paragraph(
        "<bullet>&bull;</bullet> <b>Stage 2 (4_layers, 60 epochs, "
        "10-epoch ramp):</b> copy weights 4->2, 5->3; train layers 2-5; "
        "scales of layers 2,3 ramp from 0 to 1.", bullet_style))
    story.append(Paragraph(
        "<bullet>&bull;</bullet> <b>Stage 3 (6_layers, 60 epochs, "
        "10-epoch ramp):</b> copy 2->0, 3->1; train all 6 layers; "
        "scales of layers 0,1 ramp from 0 to 1.", bullet_style))
    story.append(Paragraph(
        "Each stage uses a smaller LR: "
        "<i>lr(L) = lr_ref &times; sqrt(4/L)</i>.",
        normal_style
    ))

    # Section 3: Experiments
    story.append(Paragraph("3. Experiments", heading_style))

    # 3.1 Baseline
    story.append(Paragraph("3.1. Baseline SASRec (AdamW / Muon, L=2,4,6)", heading3_style))
    story.append(Paragraph(
        "Increasing depth degrades performance for both optimizers. "
        "AdamW consistently outperforms Muon.", normal_style))

    data = [
        [Paragraph("<b>Optimizer</b>", small_style),
         Paragraph("<b>L=2</b>", small_style),
         Paragraph("<b>L=4</b>", small_style),
         Paragraph("<b>L=6</b>", small_style)],
        [Paragraph("AdamW", normal_style),
         Paragraph("0.012762", normal_style),
         Paragraph("0.004797", normal_style),
         Paragraph("0.005645", normal_style)],
        [Paragraph("Muon", normal_style),
         Paragraph("0.005187", normal_style),
         Paragraph("0.003540", normal_style),
         Paragraph("0.003692", normal_style)],
    ]
    t = Table(data, colWidths=[3*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 2*mm))

    # 3.2 AdamW + StackRec
    story.append(Paragraph("3.2. AdamW + StackRec", heading3_style))
    story.append(Paragraph(
        "StackRec achieves 2.3-2.7x higher test NDCG@10 for 4 and 6 layers "
        "compared to plain AdamW.", normal_style))

    data2 = [
        [Paragraph("<b>Layers</b>", small_style),
         Paragraph("<b>LR</b>", small_style),
         Paragraph("<b>Epoch</b>", small_style),
         Paragraph("<b>Val NDCG@10</b>", small_style),
         Paragraph("<b>Test NDCG@10</b>", small_style),
         Paragraph("<b>Test Rec@10</b>", small_style)],
        [Paragraph("2 (4,5)", normal_style),
         Paragraph("0.00297", normal_style),
         Paragraph("88", normal_style),
         Paragraph("0.014714", normal_style),
         Paragraph("0.011958", normal_style),
         Paragraph("0.023380", normal_style)],
        [Paragraph("4 (2-5)", normal_style),
         Paragraph("0.00210", normal_style),
         Paragraph("129", normal_style),
         Paragraph("0.015451", normal_style),
         Paragraph("0.012964", normal_style),
         Paragraph("0.025370", normal_style)],
        [Paragraph("6 (all)", normal_style),
         Paragraph("0.00171", normal_style),
         Paragraph("194", normal_style),
         Paragraph("0.016095", normal_style),
         Paragraph("0.013299", normal_style),
         Paragraph("0.025494", normal_style)],
    ]
    t2 = Table(data2, colWidths=[2.5*cm, 2*cm, 1.8*cm, 2.8*cm, 2.8*cm, 2.5*cm])
    t2.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t2)
    story.append(Spacer(1, 2*mm))

    # 3.3 Muon + StackRec
    story.append(Paragraph("3.3. Muon + StackRec", heading3_style))
    story.append(Paragraph(
        "Muon + StackRec improves over plain Muon for 4 and 6 layers, "
        "but remains significantly below AdamW + StackRec. "
        "Best Muon stage: 4 layers.", normal_style))

    data3 = [
        [Paragraph("<b>Layers</b>", small_style),
         Paragraph("<b>Muon LR</b>", small_style),
         Paragraph("<b>AdamW LR</b>", small_style),
         Paragraph("<b>Epoch</b>", small_style),
         Paragraph("<b>Val NDCG@10</b>", small_style),
         Paragraph("<b>Test NDCG@10</b>", small_style)],
        [Paragraph("2", normal_style),
         Paragraph("0.02828", normal_style),
         Paragraph("0.00297", normal_style),
         Paragraph("85", normal_style),
         Paragraph("0.007215", normal_style),
         Paragraph("0.004602", normal_style)],
        [Paragraph("4", normal_style),
         Paragraph("0.02000", normal_style),
         Paragraph("0.00210", normal_style),
         Paragraph("119", normal_style),
         Paragraph("0.007884", normal_style),
         Paragraph("0.004518", normal_style)],
        [Paragraph("6", normal_style),
         Paragraph("0.01633", normal_style),
         Paragraph("0.00171", normal_style),
         Paragraph("173", normal_style),
         Paragraph("0.007008", normal_style),
         Paragraph("0.004341", normal_style)],
    ]
    t3 = Table(data3, colWidths=[2*cm, 2.5*cm, 2.5*cm, 1.8*cm, 2.8*cm, 2.8*cm])
    t3.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t3)
    story.append(Spacer(1, 2*mm))

    # 3.4 Auxiliary Identity Loss
    story.append(Paragraph("3.4. Auxiliary Identity Loss", heading3_style))
    story.append(Paragraph(
        "When a new 2-layer group is stacked below the trained subnet, "
        "an auxiliary loss drives the output ratio to 1: "
        "<i>&lambda;(alpha) = &lambda;<sub>0</sub> &times; (1 - alpha)</i>.",
        normal_style))

    data4 = [
        [Paragraph("<b>Opt.</b>", small_style),
         Paragraph("<b>Layers</b>", small_style),
         Paragraph("<b>Val NDCG@10</b>", small_style),
         Paragraph("<b>Test NDCG@10</b>", small_style)],
        [Paragraph("AdamW", normal_style),
         Paragraph("2", normal_style),
         Paragraph("0.014714 / 0.014714 (+0.00%)", small_style),
         Paragraph("0.011958 / 0.011958 (+0.00%)", small_style)],
        [Paragraph("AdamW", normal_style),
         Paragraph("4", normal_style),
         Paragraph("0.015451 / 0.015920 (+3.04%)", small_style),
         Paragraph("0.012964 / 0.012934 (-0.23%)", small_style)],
        [Paragraph("AdamW", normal_style),
         Paragraph("6", normal_style),
         Paragraph("0.016095 / 0.016328 (+1.45%)", small_style),
         Paragraph("0.013299 / 0.013086 (-1.60%)", small_style)],
        [Paragraph("Muon", normal_style),
         Paragraph("2", normal_style),
         Paragraph("0.007215 / 0.007215 (+0.00%)", small_style),
         Paragraph("0.004602 / 0.004602 (+0.00%)", small_style)],
        [Paragraph("Muon", normal_style),
         Paragraph("4", normal_style),
         Paragraph("0.007884 / 0.007327 (-7.06%)", small_style),
         Paragraph("0.004518 / 0.004591 (+1.61%)", small_style)],
        [Paragraph("Muon", normal_style),
         Paragraph("6", normal_style),
         Paragraph("0.007008 / 0.006883 (-1.79%)", small_style),
         Paragraph("0.004341 / 0.004351 (+0.24%)", small_style)],
    ]
    t4 = Table(data4, colWidths=[2*cm, 2*cm, 4.5*cm, 4.5*cm])
    t4.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t4)
    story.append(Spacer(1, 2*mm))

    # 3.5 Hyperbolic Heads
    story.append(Paragraph("3.5. Hyperbolic Heads", heading3_style))
    story.append(Paragraph(
        "Poincare-ball next-item head at each newly stacked group boundary. "
        "Curvature decays with depth: "
        "<i>c(d) = c_ref &times; (d_ref / d)<sup>p</sup></i>.",
        normal_style))

    data5 = [
        [Paragraph("<b>Layers</b>", small_style),
         Paragraph("<b>Plain</b>", small_style),
         Paragraph("<b>Aux</b>", small_style),
         Paragraph("<b>Hyperbolic</b>", small_style)],
        [Paragraph("2", normal_style),
         Paragraph("0.011958", normal_style),
         Paragraph("0.011958", normal_style),
         Paragraph("0.011958", normal_style)],
        [Paragraph("4", normal_style),
         Paragraph("0.012964", normal_style),
         Paragraph("0.012934", normal_style),
         Paragraph("0.012428", normal_style)],
        [Paragraph("6", normal_style),
         Paragraph("0.013299", normal_style),
         Paragraph("0.013086", normal_style),
         Paragraph("0.013419", normal_style)],
    ]
    t5 = Table(data5, colWidths=[2.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    t5.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t5)
    story.append(Paragraph(
        "6-layer model gains +0.9% vs plain, +2.5% vs aux. "
        "4-layer stage is weaker -- loss_coeff=0.1 may be too small.",
        normal_style))
    story.append(Spacer(1, 2*mm))

    # 3.6 Lorentz Residual
    story.append(Paragraph("3.6. Lorentz Hyperbolic Residual", heading3_style))
    story.append(Paragraph(
        "Hyperbolic geometry <i>inside</i> the hidden representation of "
        "copied groups: "
        "<i>h_out = normalize(h + gate &times; normalize_to_norm(h, r))</i>, "
        "where r = (sinhc(sqrt(c)&middot;||u||) - 1) &times; W_out u is the "
        "curvature-induced correction, exactly zero at c=0.",
        normal_style))
    story.append(Paragraph(
        "Verification: unit-level checks (CPU) -- hyperboloid constraint, "
        "symmetric distance, zero residual at c=0, bitwise identity at gate=0, "
        "norm preservation. Full training not yet run.",
        normal_style))

    # Section 4: Testing
    story.append(PageBreak())
    story.append(Paragraph("4. Testing", heading_style))

    # 4.1 Ranking metrics
    story.append(Paragraph("4.1. Ranking Metrics Tests (10/10 PASS)", heading3_style))

    data6 = [
        [Paragraph("<b>#</b>", small_style),
         Paragraph("<b>Metric</b>", small_style),
         Paragraph("<b>Status</b>", small_style),
         Paragraph("<b>Value</b>", small_style)],
        [Paragraph("1", normal_style), Paragraph("NDCG@5", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("0.487914", normal_style)],
        [Paragraph("2", normal_style), Paragraph("Recall@5", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("0.800000", normal_style)],
        [Paragraph("3", normal_style), Paragraph("Coverage@5", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("1.000000", normal_style)],
        [Paragraph("4", normal_style), Paragraph("Novelty@5", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("0.944260", normal_style)],
        [Paragraph("5", normal_style), Paragraph("MeanRank@5", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("3.500000", normal_style)],
        [Paragraph("6", normal_style), Paragraph("ILD@5", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("0.506127", normal_style)],
        [Paragraph("7", normal_style), Paragraph("PopularityGroups", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("OK", normal_style)],
        [Paragraph("8", normal_style), Paragraph("EdgeCases", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("OK", normal_style)],
        [Paragraph("9", normal_style), Paragraph("CoveragePartial", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("0.100000", normal_style)],
        [Paragraph("10", normal_style), Paragraph("MeanRankPartial", normal_style),
         Paragraph("<font color='green'>PASS</font>", normal_style),
         Paragraph("1.000000", normal_style)],
    ]
    t6 = Table(data6, colWidths=[1.2*cm, 3.5*cm, 2.5*cm, 3*cm])
    t6.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t6)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<b>Notes:</b> NDCGMetric computes DCG (no IDCG normalization). "
        "RecallMetric counts absolute hits. "
        "CoverageMetric and NoveltyMetric are stateful: require .reduce().",
        small_style))
    story.append(Spacer(1, 3*mm))

    # 4.2 Temporal split
    story.append(Paragraph("4.2. Temporal Split Validation", heading3_style))

    data7 = [
        [Paragraph("<b>Split</b>", small_style),
         Paragraph("<b>Rows</b>", small_style),
         Paragraph("<b>Users</b>", small_style),
         Paragraph("<b>Items</b>", small_style)],
        [Paragraph("train", normal_style),
         Paragraph("140,965", normal_style),
         Paragraph("18,474", normal_style),
         Paragraph("11,534", normal_style)],
        [Paragraph("validation", normal_style),
         Paragraph("50,336", normal_style),
         Paragraph("4,725", normal_style),
         Paragraph("10,310", normal_style)],
        [Paragraph("test", normal_style),
         Paragraph("90,621", normal_style),
         Paragraph("8,041", normal_style),
         Paragraph("11,727", normal_style)],
        [Paragraph("train_validation", normal_style),
         Paragraph("151,081", normal_style),
         Paragraph("18,474", normal_style),
         Paragraph("11,736", normal_style)],
    ]
    t7 = Table(data7, colWidths=[3.5*cm, 3*cm, 3*cm, 3*cm])
    t7.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t7)
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Temporal split violations: <b>0</b>. Prefix property "
        "<i>train &sub; val &sub; test</i>: <b>True</b>.",
        normal_style))
    story.append(Spacer(1, 3*mm))

    # 4.3 StackRec tests
    story.append(Paragraph("4.3. StackRec Unit Tests (17/17 PASS)", heading3_style))

    tests = [
        ("1", "Model initialization", "PASS"),
        ("2", "Forward pass (short seq=5)", "PASS"),
        ("3", "Forward pass (long seq=20)", "PASS"),
        ("4", "Stage 1 -- 2 layers (4, 5)", "PASS"),
        ("5", "Stage 2 -- 4 layers (2-5) with copy", "PASS"),
        ("6", "Stage 3 -- 6 layers (0-5) with copy", "PASS"),
        ("7", "Full StackRec pipeline (short seq=5)", "PASS"),
        ("8", "Full StackRec pipeline (long seq=20)", "PASS"),
        ("9", "Ramp scale=0 identity", "PASS"),
        ("10", "Aux scalar and boundary", "PASS"),
        ("11", "Lorentz head addition", "PASS"),
        ("12", "Curvature schedule", "PASS"),
        ("13", "Copy layer weights", "PASS"),
        ("14", "Batch with two sequences", "PASS"),
        ("15", "CPU only", "PASS"),
        ("16", "SASRec vs StackRec (2 layers) identity", "PASS"),
        ("17", "SASRec vs StackRec (2 layers) long seq", "PASS"),
    ]

    test_data = []
    for i, (num, name, status) in enumerate(tests):
        test_data.append([
            Paragraph(num, small_style),
            Paragraph(name, small_style),
            Paragraph(f"<font color='green'>{status}</font>", small_style),
        ])

    t8 = Table(test_data, colWidths=[1.2*cm, 7*cm, 2*cm])
    style_list = [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]
    for i in range(1, len(test_data)):
        if i % 2 == 0:
            style_list.append(('BACKGROUND', (0, i), (-1, i), HexColor('#f0f4f8')))
    t8.setStyle(TableStyle(style_list))
    story.append(t8)
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        "<b>Key checks:</b> Ramp scale=0 -- new layers as identity; "
        "SASRec vs StackRec identity -- identical predictions; "
        "Copy layer weights -- correct copying and trainability switching.",
        small_style))

    # Section 5: Conclusions
    story.append(PageBreak())
    story.append(Paragraph("5. Conclusions", heading_style))

    conclusions = [
        ("StackRec is effective:",
         "AdamW + StackRec achieves 2.3-2.7x higher test NDCG@10 "
         "for 4 and 6 layers vs. plain AdamW."),
        ("Muon + StackRec:",
         "Improves over plain Muon for 4 and 6 layers, but remains "
         "below AdamW. Best stage: 4 layers."),
        ("Auxiliary identity loss:",
         "Improves validation for AdamW, but test NDCG slightly worse. "
         "For Muon: mixed/negative results."),
        ("Hyperbolic heads:",
         "Depth-decaying curvature helps at 6 layers (+0.9% vs plain), "
         "but 4-layer stage is weaker."),
        ("Lorentz residual:",
         "Verified at unit level; full training not yet run."),
        ("Testing:",
         "10/10 metrics PASS, 17/17 StackRec tests PASS."),
    ]

    for title, text in conclusions:
        story.append(Paragraph(
            f"<b>&bull; {title}</b> {text}", normal_style))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "<i>Project files: sasrec_experiments/</i>", small_style))
    story.append(Paragraph(
        "<i>Sources: diary.md, test_stackrec.py, test_metrics.py, "
        "sasrec_stackrec_results.json, sasrec_stackrec_muon_results.json, "
        "sasrec_stackrec_aux_results.json, sasrec_stackrec_hyperbolic_results.json</i>",
        small_style))

    doc.build(story)
    print(f"PDF written to {path}")

if __name__ == "__main__":
    build_pdf("/home/yusupov/Agent_shad/AI_for_research_YSDA/stackrec_report.pdf")