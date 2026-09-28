"""
Ultra-Visual SAT-SA Presentation Deck Builder for SIH 2026 (12 Slides).
60% Visual Content + 40% Text.
Constructs rich flowcharts, decision trees, distribution charts, architecture stacks, 
before/after models, evidence chains, dashboard mockups, and validation flows.
"""

import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Color Palette
C_NAVY_DARK = RGBColor(10, 25, 47)       # #0A192F (Dark Navy)
C_NAVY = RGBColor(15, 30, 60)            # #0F1E3C (Primary Navy)
C_NAVY_LIGHT = RGBColor(24, 43, 73)      # #182B49 (Card Dark Navy)
C_SIH_BLUE = RGBColor(0, 112, 192)       # #0070C0 (Official SIH Template Accent)
C_ACCENT_BLUE = RGBColor(2, 132, 199)    # #0284C7 (Vibrant Cyan Blue)
C_SLATE_DARK = RGBColor(30, 41, 59)      # #1E293B (Dark Slate Header)
C_SLATE_TEXT = RGBColor(51, 65, 85)      # #334155 (Legible Body)
C_MUTED = RGBColor(100, 116, 139)        # #64748B (Muted)
C_BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC (Light Canvas)
C_BG_CARD = RGBColor(241, 245, 249)      # #F1F5F9 (Card Surface)
C_BORDER = RGBColor(203, 213, 225)       # #CBD5E1 (Border Gray)
C_BORDER_LIGHT = RGBColor(226, 232, 240) # #E2E8F0 (Soft Border)
C_WHITE = RGBColor(255, 255, 255)
C_AMBER = RGBColor(217, 119, 6)          # #D97706 (Warning Amber)
C_AMBER_BG = RGBColor(254, 243, 199)     # #FEF3C7 (Amber Container)
C_RED = RGBColor(220, 38, 38)            # #DC2626 (Critical Red)
C_RED_BG = RGBColor(254, 226, 226)       # #FEE2E2 (Red Container)
C_GREEN = RGBColor(5, 150, 105)          # #059669 (Healthy Green)
C_GREEN_BG = RGBColor(209, 250, 229)     # #D1FAE5 (Green Container)
C_BLUE_BG = RGBColor(224, 242, 254)      # #E0F2FE (Blue Container)
C_GRAY_BG = RGBColor(229, 231, 235)      # #E5E7EB (Bar Track Gray)

FONT_TITLE = "Arial"
FONT_BODY = "Arial"

def set_shape_style(shape, fill_color, border_color=None, border_width=1):
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()

def add_header(slide, slide_num, total_slides, title_text, category_text="SECURITY AUDIT & SUPERVISORY ANALYTICS"):
    # Top-right SIH Logo
    logo_path = 'scratch/template_images/slide2_Picture 10_3.png'
    if os.path.exists(logo_path):
        slide.shapes.add_picture(logo_path, Inches(10.70), Inches(0.00), width=Inches(2.46), height=Inches(1.16))
    
    # Top-left Pill: Team ID & PS ID
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.50), Inches(0.18), Inches(2.20), Inches(0.32))
    set_shape_style(pill, C_SIH_BLUE, None)
    tf = pill.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "SIH 2026 | PS 26157"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER
    
    # Category tag next to pill
    cat_box = slide.shapes.add_textbox(Inches(2.80), Inches(0.18), Inches(7.50), Inches(0.32))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = f"SAT-SA • {category_text.upper()}"
    p_cat.font.name = FONT_BODY
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_MUTED

    # Title text
    if title_text:
        title_box = slide.shapes.add_textbox(Inches(0.50), Inches(0.58), Inches(10.00), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

    # Bottom blue ribbon
    ribbon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.00), Inches(6.95), Inches(13.333), Inches(0.55))
    set_shape_style(ribbon, C_SIH_BLUE, None)
    
    # Footer text left
    foot_left = slide.shapes.add_textbox(Inches(0.50), Inches(7.02), Inches(5.20), Inches(0.40))
    tf_fl = foot_left.text_frame
    tf_fl.margin_left = tf_fl.margin_top = tf_fl.margin_right = tf_fl.margin_bottom = 0
    p_fl = tf_fl.paragraphs[0]
    p_fl.text = "SAT-SA: Security Audit & Supervisory Analytics"
    p_fl.font.name = FONT_BODY
    p_fl.font.size = Pt(11)
    p_fl.font.color.rgb = C_WHITE

    # Footer text center
    foot_mid = slide.shapes.add_textbox(Inches(5.08), Inches(7.02), Inches(4.50), Inches(0.40))
    tf_fm = foot_mid.text_frame
    tf_fm.margin_left = tf_fm.margin_top = tf_fm.margin_right = tf_fm.margin_bottom = 0
    p_fm = tf_fm.paragraphs[0]
    p_fm.text = "@SIH Idea submission- Template | NCIIPC / NTRO"
    p_fm.font.name = FONT_BODY
    p_fm.font.size = Pt(11)
    p_fm.font.color.rgb = C_WHITE
    p_fm.alignment = PP_ALIGN.CENTER

    # Slide number right
    foot_right = slide.shapes.add_textbox(Inches(11.50), Inches(7.02), Inches(1.33), Inches(0.40))
    tf_fr = foot_right.text_frame
    tf_fr.margin_left = tf_fr.margin_top = tf_fr.margin_right = tf_fr.margin_bottom = 0
    p_fr = tf_fr.paragraphs[0]
    p_fr.text = f"Slide {slide_num} of {total_slides}"
    p_fr.font.name = FONT_BODY
    p_fr.font.size = Pt(11)
    p_fr.font.bold = True
    p_fr.font.color.rgb = C_WHITE
    p_fr.alignment = PP_ALIGN.RIGHT

def add_card(slide, left, top, width, height, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
    card = slide.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
    set_shape_style(card, bg_color, border_color, border_width)
    return card

def add_callout(slide, left, top, width, height, text, icon="💡", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True):
    box = add_card(slide, left, top, width, height, bg_color, border_color, border_width=1.5)
    tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.08), Inches(width - 0.30), Inches(height - 0.16))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"{icon}  {text}"
    p.font.name = FONT_BODY
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = text_color
    p.alignment = PP_ALIGN.CENTER
    return box

def add_down_arrow(slide, left, top, width=0.25, height=0.28, color=C_SIH_BLUE):
    shape = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(left), Inches(top), Inches(width), Inches(height))
    set_shape_style(shape, color, None)
    return shape

def add_right_arrow(slide, left, top, width=0.28, height=0.22, color=C_SIH_BLUE):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(left), Inches(top), Inches(width), Inches(height))
    set_shape_style(shape, color, None)
    return shape

def add_kpi_card(slide, left, top, width, height, val_text, label_text, sublabel="", val_color=C_SIH_BLUE, bg_color=C_WHITE, border_color=C_BORDER):
    card = add_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(Inches(left + 0.08), Inches(top + 0.08), Inches(width - 0.16), Inches(height - 0.16))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p1 = tf.paragraphs[0]
    p1.text = val_text
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = val_color
    p1.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = label_text
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.0)
    p2.font.bold = True
    p2.font.color.rgb = C_SLATE_DARK
    p2.alignment = PP_ALIGN.CENTER
    
    if sublabel:
        p3 = tf.add_paragraph()
        p3.text = sublabel
        p3.font.name = FONT_BODY
        p3.font.size = Pt(8.0)
        p3.font.color.rgb = C_MUTED
        p3.alignment = PP_ALIGN.CENTER
    return card

def build_presentation():
    prs = Presentation('SIH2026-IDEA-Presentation-Format.backup.pptx')
    blank_layout = prs.slide_layouts[6]
    
    TOTAL_SLIDES = 12
    while len(prs.slides) < TOTAL_SLIDES:
        prs.slides.add_slide(blank_layout)
    
    # Clear shapes
    for slide in prs.slides:
        for s in list(slide.shapes):
            sp = s._element
            sp.getparent().remove(sp)

    # =========================================================================
    # SLIDE 1: SAT-SA OVERVIEW (Large Central Hero Workflow)
    # =========================================================================
    s1 = prs.slides[0]
    logo_path = 'scratch/template_images/slide1_Picture 1_2.png'
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(10.70), Inches(0.00), width=Inches(2.46), height=Inches(1.16))
    
    tb_top = s1.shapes.add_textbox(Inches(0.50), Inches(0.20), Inches(9.50), Inches(0.40))
    p_tt = tb_top.text_frame.paragraphs[0]
    p_tt.text = "SMART INDIA HACKATHON 2026  •  OFFICIAL IDEA SUBMISSION"
    p_tt.font.name = FONT_BODY
    p_tt.font.size = Pt(12)
    p_tt.font.bold = True
    p_tt.font.color.rgb = C_SIH_BLUE

    tb_hero = s1.shapes.add_textbox(Inches(0.50), Inches(0.60), Inches(10.00), Inches(1.70))
    tf_h = tb_hero.text_frame
    tf_h.word_wrap = True
    tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
    
    p_h1 = tf_h.paragraphs[0]
    p_h1.text = "SAT-SA"
    p_h1.font.name = FONT_TITLE
    p_h1.font.size = Pt(38)
    p_h1.font.bold = True
    p_h1.font.color.rgb = C_NAVY

    p_h2 = tf_h.add_paragraph()
    p_h2.text = "Security Audit & Supervisory Analytics"
    p_h2.font.name = FONT_TITLE
    p_h2.font.size = Pt(20)
    p_h2.font.bold = True
    p_h2.font.color.rgb = C_SIH_BLUE

    p_h3 = tf_h.add_paragraph()
    p_h3.text = "Turning SOC Records into Actionable Audit Evidence  |  Problem Statement 26157"
    p_h3.font.name = FONT_BODY
    p_h3.font.size = Pt(12.5)
    p_h3.font.bold = True
    p_h3.font.color.rgb = C_SLATE_TEXT

    # Left Container: Metadata Card
    add_card(s1, 0.50, 2.45, 4.40, 3.55, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    tb_meta = s1.shapes.add_textbox(Inches(0.65), Inches(2.55), Inches(4.10), Inches(3.35))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True
    
    meta_items = [
        ("PS ID:", " 26157 (SIH26157)"),
        ("PS Title:", " Supervisory Analytics Tool for SOC Assessment"),
        ("Theme:", " Blockchain & Cybersecurity"),
        ("Category:", " Software (100% Offline / Air-Gapped)"),
        ("Target Agency:", " NCIIPC / NTRO (Section 70A, IT Act)"),
        ("Entities:", " Critical Sector Entities (Power, Banking, Telecom)"),
        ("System Type:", " Human-in-the-Loop Audit Decision-Support")
    ]
    for i, (k, v) in enumerate(meta_items):
        p = tf_m.paragraphs[0] if i == 0 else tf_m.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = k
        r1.font.name = FONT_BODY
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = f" {v}"
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_SLATE_TEXT

    # Right Container: Large Hero Workflow Diagram
    add_card(s1, 5.10, 2.45, 7.73, 3.55, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_w_title = s1.shapes.add_textbox(Inches(5.30), Inches(2.55), Inches(7.33), Inches(0.30))
    p_wt = tb_w_title.text_frame.paragraphs[0]
    p_wt.text = "CORE SYSTEM WORKFLOW (FROM DATA TO AUDIT DECISION)"
    p_wt.font.name = FONT_BODY
    p_wt.font.size = Pt(11)
    p_wt.font.bold = True
    p_wt.font.color.rgb = C_SIH_BLUE

    # 5 Sequential Workflow Nodes with Down Arrows
    nodes_s1 = [
        ("🗄️  1. SOC DATA", "Historical Alerts, Cases, Closures, Assets, Telemetry", C_NAVY_LIGHT, C_WHITE),
        ("⚙️  2. SAT-SA AUDIT ANALYTICS", "Offline Rule Engine, Statistical Shrinkage & Peer Benchmarking", C_SIH_BLUE, C_WHITE),
        ("🔍  3. DETECT PATTERNS", "Dual Detection: Execution Gaps (anomalies) & Negative Space (omissions)", C_NAVY_LIGHT, C_WHITE),
        ("📜  4. EXPLAIN WITH EVIDENCE", "Unbroken Forensic Dossier, Record Timestamps & Peer Comparison", C_ACCENT_BLUE, C_WHITE),
        ("👨‍💻  5. HUMAN EXPERT REVIEW", "Supervisory Examiner Conducts Targeted, Defensible Investigation", C_GREEN, C_WHITE)
    ]
    
    y_start = 2.90
    for idx, (nh, nd, n_bg, n_fg) in enumerate(nodes_s1):
        c_top = y_start + idx * 0.60
        add_card(s1, 5.30, c_top, 7.33, 0.44, bg_color=n_bg, border_color=C_ACCENT_BLUE, border_width=1)
        tb_node = s1.shapes.add_textbox(Inches(5.45), Inches(c_top + 0.02), Inches(7.03), Inches(0.40))
        tf_node = tb_node.text_frame
        tf_node.word_wrap = True
        p = tf_node.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{nh}  —  "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = n_fg
        r2 = p.add_run()
        r2.text = nd
        r2.font.name = FONT_BODY
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = C_BORDER_LIGHT if n_bg in [C_NAVY_LIGHT, C_NAVY_DARK] else C_WHITE

    # Bottom Callout at Slide 1
    add_callout(s1, 0.50, 6.10, 12.33, 0.65, 
                "Database ➔ Analytics ➔ Evidence ➔ Auditor  |  Human-in-the-Loop Audit Decision-Support System",
                icon="🛡️", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)

    ribbon1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.00), Inches(6.95), Inches(13.333), Inches(0.55))
    set_shape_style(ribbon1, C_SIH_BLUE, None)
    foot_s1 = s1.shapes.add_textbox(Inches(0.50), Inches(7.02), Inches(12.33), Inches(0.40))
    p_fs1 = foot_s1.text_frame.paragraphs[0]
    p_fs1.text = "SIH 2026 | Problem Statement 26157 | SAT-SA: Security Audit & Supervisory Analytics"
    p_fs1.font.name = FONT_BODY
    p_fs1.font.size = Pt(11)
    p_fs1.font.color.rgb = C_WHITE
    p_fs1.alignment = PP_ALIGN.CENTER


    # =========================================================================
    # SLIDE 2: THE CURRENT PROBLEM (Manual Review Bottleneck)
    # =========================================================================
    s2 = prs.slides[1]
    add_header(s2, 2, TOTAL_SLIDES, "The Current Problem: Manual Review Bottleneck", "PROBLEM STATEMENT")

    # Central Workflow: 4 Stage Vertical Bottleneck
    add_card(s2, 0.50, 1.35, 5.00, 4.40, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    tb_bw_t = s2.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(4.60), Inches(0.30))
    p_bwt = tb_bw_t.text_frame.paragraphs[0]
    p_bwt.text = "MANUAL AUDIT WORKFLOW"
    p_bwt.font.name = FONT_TITLE
    p_bwt.font.size = Pt(11)
    p_bwt.font.bold = True
    p_bwt.font.color.rgb = C_NAVY

    wf_steps_s2 = [
        ("LARGE SOC DATA", "Millions of Records & Event Logs", C_SIH_BLUE),
        ("MANUAL SAMPLING", "Auditor Samples < 0.1% Randomly", C_AMBER),
        ("MANUAL REVIEW", "Slow, Subjective Ticket Inspection", C_NAVY),
        ("LIMITED FINDINGS", "Systemic Gaps & Omissions Missed", C_RED)
    ]
    for idx, (sh, sd, sc) in enumerate(wf_steps_s2):
        s_top = 1.85 + idx * 0.95
        add_card(s2, 0.70, s_top, 4.60, 0.65, bg_color=C_WHITE, border_color=sc, border_width=1.5)
        tb_ws = s2.shapes.add_textbox(Inches(0.80), Inches(s_top + 0.05), Inches(4.40), Inches(0.55))
        tf_ws = tb_ws.text_frame
        tf_ws.word_wrap = True
        p1 = tf_ws.paragraphs[0]
        p1.text = sh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = sc
        p2 = tf_ws.add_paragraph()
        p2.text = sd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_SLATE_TEXT
        
        if idx < 3:
            add_down_arrow(s2, 2.90, s_top + 0.68, width=0.20, height=0.22, color=sc)

    # Right Side: 4 Problem Bubbles / Cards
    add_card(s2, 5.70, 1.35, 7.13, 4.40, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_pb_t = s2.shapes.add_textbox(Inches(5.90), Inches(1.45), Inches(6.70), Inches(0.30))
    p_pbt = tb_pb_t.text_frame.paragraphs[0]
    p_pbt.text = "SURROUNDING AUDIT CHALLENGES"
    p_pbt.font.name = FONT_TITLE
    p_pbt.font.size = Pt(11)
    p_pbt.font.bold = True
    p_pbt.font.color.rgb = C_NAVY

    problems_s2 = [
        ("1. High Data Volume", "Millions of historical records generated across dozens of critical entities swamp manual inspection capacity.", C_RED_BG, C_RED),
        ("2. Limited Review Capacity", "Supervisory teams have limited auditor hours to assess compliance across entire national sectors.", C_AMBER_BG, C_AMBER),
        ("3. Hidden Behavioural Patterns", "Operational gaming (fast closures, template copy-paste notes, SLA deadline rushes) bypasses checklists.", C_BLUE_BG, C_SIH_BLUE),
        ("4. Missing Evidence Blindspot", "Silent critical assets and dropped telemetry categories produce ZERO logs for random sampling to catch.", C_BG_CARD, C_NAVY)
    ]
    for idx, (ph, pd, p_bg, p_col) in enumerate(problems_s2):
        p_top = 1.85 + idx * 0.95
        add_card(s2, 5.90, p_top, 6.73, 0.80, bg_color=p_bg, border_color=p_col, border_width=1.2)
        tb_p = s2.shapes.add_textbox(Inches(6.05), Inches(p_top + 0.05), Inches(6.43), Inches(0.70))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        p1 = tf_p.paragraphs[0]
        p1.text = ph
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = p_col
        p2 = tf_p.add_paragraph()
        p2.text = pd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_SLATE_TEXT

    # Bottom Callout Box
    add_callout(s2, 0.50, 5.90, 12.33, 0.85,
                '"Too much data. Limited expert review time."\nThe problem is not lack of data. The problem is finding the important evidence inside the data.',
                icon="⚠️", bg_color=C_AMBER_BG, border_color=C_AMBER, text_color=C_NAVY, font_size=11, bold=True)


    # =========================================================================
    # SLIDE 3: SAT-SA REFRAMES THE PROBLEM (Before vs After)
    # =========================================================================
    s3 = prs.slides[2]
    add_header(s3, 3, TOTAL_SLIDES, "SAT-SA Reframes the Problem: Before vs After", "PARADIGM SHIFT")

    # Left Box: BEFORE (Traditional Model)
    add_card(s3, 0.50, 1.35, 5.40, 4.40, bg_color=C_BG_CARD, border_color=C_RED, border_width=1.5)
    tb_bef_t = s3.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(5.00), Inches(0.30))
    p_bt = tb_bef_t.text_frame.paragraphs[0]
    p_bt.text = "BEFORE: MANUAL / RANDOM SAMPLING"
    p_bt.font.name = FONT_BODY
    p_bt.font.size = Pt(11)
    p_bt.font.bold = True
    p_bt.font.color.rgb = C_RED

    before_flow = [
        ("SOC Records", "Raw unstructured event dumps"),
        ("Random / Manual Sampling", "Auditor picks arbitrary <0.1%"),
        ("Expert Review", "Slow manual ticket triage"),
        ("Fragmented Findings", "Systemic operational drift missed")
    ]
    for idx, (bh, bd) in enumerate(before_flow):
        b_top = 1.90 + idx * 0.90
        add_card(s3, 0.70, b_top, 5.00, 0.65, bg_color=C_WHITE, border_color=C_BORDER, border_width=1)
        tb_bf = s3.shapes.add_textbox(Inches(0.80), Inches(b_top + 0.05), Inches(4.80), Inches(0.55))
        tf_bf = tb_bf.text_frame
        tf_bf.word_wrap = True
        p1 = tf_bf.paragraphs[0]
        p1.text = bh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = C_RED if idx == 3 else C_NAVY
        p2 = tf_bf.add_paragraph()
        p2.text = bd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_SLATE_TEXT
        if idx < 3:
            add_down_arrow(s3, 3.10, b_top + 0.68, width=0.18, height=0.18, color=C_RED)

    # Center Big Arrow
    add_right_arrow(s3, 6.05, 3.15, width=0.50, height=0.45, color=C_SIH_BLUE)

    # Right Box: WITH SAT-SA
    add_card(s3, 6.70, 1.35, 6.13, 4.40, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_aft_t = s3.shapes.add_textbox(Inches(6.90), Inches(1.45), Inches(5.73), Inches(0.30))
    p_at = tb_aft_t.text_frame.paragraphs[0]
    p_at.text = "WITH SAT-SA: EVIDENCE-DRIVEN SUPERVISION"
    p_at.font.name = FONT_BODY
    p_at.font.size = Pt(11)
    p_at.font.bold = True
    p_at.font.color.rgb = C_SIH_BLUE

    satsa_flow = [
        ("1. SOC Records", "Normalized into canonical schemas"),
        ("2. Analytics Engine", "Parallel Rules • Peer Benchmarks • Anomaly ML"),
        ("3. Dual Detection", "Execution Gaps + Negative Space Analysis"),
        ("4. Prioritisation & Evidence", "Ranked Entity Dossiers + Unbroken Evidence Chain"),
        ("5. Human Expert Review", "Targeted, defensible supervisory investigation")
    ]
    for idx, (sh, sd) in enumerate(satsa_flow):
        s_top = 1.85 + idx * 0.72
        add_card(s3, 6.90, s_top, 5.73, 0.54, bg_color=C_NAVY_LIGHT, border_color=C_ACCENT_BLUE, border_width=1)
        tb_sf = s3.shapes.add_textbox(Inches(7.05), Inches(s_top + 0.04), Inches(5.43), Inches(0.46))
        tf_sf = tb_sf.text_frame
        tf_sf.word_wrap = True
        p1 = tf_sf.paragraphs[0]
        p1.text = sh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p2 = tf_sf.add_paragraph()
        p2.text = sd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = C_BORDER_LIGHT
        if idx < 4:
            add_down_arrow(s3, 9.65, s_top + 0.56, width=0.15, height=0.14, color=C_SIH_BLUE)

    # Bottom Callout Banner
    add_callout(s3, 0.50, 5.90, 12.33, 0.85,
                '"SAT-SA does not replace expert review — it makes expert review more targeted."',
                icon="🎯", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=12, bold=True)


    # =========================================================================
    # SLIDE 4: COMPLETE SAT-SA WORKFLOW (6-Stage Horizontal Pipeline)
    # =========================================================================
    s4 = prs.slides[3]
    add_header(s4, 4, TOTAL_SLIDES, "How SAT-SA Works: Complete 6-Stage Pipeline", "END-TO-END WORKFLOW")

    pipe_stages = [
        ("STAGE 1", "DATA INPUT", "• Alerts\n• Cases\n• Assets\n• Escalations\n• Closures\n• Telemetry", C_NAVY_LIGHT),
        ("STAGE 2", "NORMALISATION", "• CSV / JSON / DB\n• Schema Validator\n• Data Quality Gate\n• SHA-256 Ledger\n• DuckDB Lake", C_SIH_BLUE),
        ("STAGE 3", "ANALYTICS", "• Rules\n• Statistics\n• Peer Benchmarks\n• Anomaly ML\n• MinHash Notes", C_NAVY),
        ("STAGE 4", "DETECTION", "• Execution Gaps\n  (Anomalous action)\n• Negative Space\n  (Missing evidence)\n• Temporal Outliers", C_RED),
        ("STAGE 5", "PRIORITISATION", "• Multiple Signals\n• Evidence Strength\n• Peer Deviation\n• Review Priority\n• Budget Optimizer", C_AMBER),
        ("STAGE 6", "HUMAN REVIEW", "• Recommendation\n• Evidence Dossier\n• Expert Decision\n• Defensible Log\n• Compliance Pack", C_GREEN)
    ]

    for idx, (st_num, st_name, st_desc, st_col) in enumerate(pipe_stages):
        c_left = 0.50 + idx * 2.08
        # Container
        add_card(s4, c_left, 1.35, 1.95, 4.35, bg_color=C_WHITE, border_color=st_col, border_width=1.5)
        # Header Badge
        add_card(s4, c_left, 1.35, 1.95, 0.52, bg_color=st_col, border_color=st_col, border_width=0)
        tb_h = s4.shapes.add_textbox(Inches(c_left + 0.05), Inches(1.39), Inches(1.85), Inches(0.45))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        p1 = tf_h.paragraphs[0]
        p1.text = st_num
        p1.font.name = FONT_BODY
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = C_BORDER_LIGHT
        p1.alignment = PP_ALIGN.CENTER
        p2 = tf_h.add_paragraph()
        p2.text = st_name
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p2.alignment = PP_ALIGN.CENTER

        # Body
        tb_b = s4.shapes.add_textbox(Inches(c_left + 0.08), Inches(1.95), Inches(1.79), Inches(3.65))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        p_desc = tf_b.paragraphs[0]
        p_desc.text = st_desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(9.0)
        p_desc.font.color.rgb = C_SLATE_DARK

        if idx < 5:
            add_right_arrow(s4, c_left + 1.97, 3.20, width=0.10, height=0.18, color=C_SIH_BLUE)

    # Bottom Guarantees Badges
    add_callout(s4, 0.50, 5.90, 12.33, 0.85,
                "100% Offline & Air-Gapped • No External APIs • Cryptographic SHA-256 Tamper Ledger • In-Process DuckDB",
                icon="🔒", bg_color=C_BG_CARD, border_color=C_NAVY, text_color=C_NAVY, font_size=11, bold=True)


    # =========================================================================
    # SLIDE 5: DETECTION METHOD 1 — EXECUTION GAPS
    # =========================================================================
    s5 = prs.slides[4]
    add_header(s5, 5, TOTAL_SLIDES, "Detection Method 1: Execution Gaps Workflow", "EXECUTION GAPS")

    # Left Side: Visual Decision Flow
    add_card(s5, 0.50, 1.35, 5.40, 4.40, bg_color=C_NAVY_DARK, border_color=C_RED, border_width=1.5)
    tb_df_t = s5.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(5.00), Inches(0.30))
    p_dft = tb_df_t.text_frame.paragraphs[0]
    p_dft.text = "EXECUTION GAP DECISION FLOW"
    p_dft.font.name = FONT_TITLE
    p_dft.font.size = Pt(11)
    p_dft.font.bold = True
    p_dft.font.color.rgb = C_RED

    df_steps = [
        ("1. SOC Record Exists", "Alert, case, or closure logged in data dump", C_NAVY_LIGHT),
        ("2. Analyse Operational Behaviour", "Evaluate timestamps, escalation path & note text", C_NAVY_LIGHT),
        ("3. Compare: Own History + Peer Group", "Benchmark against entity historical mean & peer cohort", C_NAVY_LIGHT),
        ("4. Is Behaviour Unusual? ➔ YES", "Statistically significant velocity or note anomaly", C_AMBER),
        ("5. Review Recommended ➔ Evidence Trail", "Flag prioritized for human expert verification", C_RED)
    ]
    for idx, (dh, dd, dc) in enumerate(df_steps):
        d_top = 1.85 + idx * 0.72
        add_card(s5, 0.70, d_top, 5.00, 0.54, bg_color=dc, border_color=C_ACCENT_BLUE if dc == C_NAVY_LIGHT else dc, border_width=1)
        tb_ds = s5.shapes.add_textbox(Inches(0.85), Inches(d_top + 0.04), Inches(4.70), Inches(0.46))
        tf_ds = tb_ds.text_frame
        tf_ds.word_wrap = True
        p1 = tf_ds.paragraphs[0]
        p1.text = dh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE if dc in [C_NAVY_LIGHT, C_RED] else C_NAVY
        p2 = tf_ds.add_paragraph()
        p2.text = dd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = C_BORDER_LIGHT if dc in [C_NAVY_LIGHT, C_RED] else C_SLATE_DARK
        if idx < 4:
            add_down_arrow(s5, 3.10, d_top + 0.56, width=0.15, height=0.14, color=C_SIH_BLUE)

    # Right Side: 5 Detector Cards
    add_card(s5, 6.10, 1.35, 6.73, 4.40, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_dt_t = s5.shapes.add_textbox(Inches(6.30), Inches(1.45), Inches(6.33), Inches(0.30))
    p_dtt = tb_dt_t.text_frame.paragraphs[0]
    p_dtt.text = "CORE DETECTOR MODULES"
    p_dtt.font.name = FONT_TITLE
    p_dtt.font.size = Pt(11)
    p_dtt.font.bold = True
    p_dtt.font.color.rgb = C_NAVY

    detectors_eg = [
        ("⚡ Fast Critical Closures", "Critical severity alerts closed in < 10 seconds without investigation.", C_RED_BG, C_RED),
        ("🚫 Missing Escalation", "Critical & high alarms closed at Tier-1 without Tier-2/3 investigation.", C_AMBER_BG, C_AMBER),
        ("📋 Template Notes", "MinHash LSH identifies identical copy-pasted resolution text across tickets.", C_BLUE_BG, C_SIH_BLUE),
        ("🔄 Repeat Alerts", "Identical alerts firing continuously without remediation or ticket escalation.", C_BG_CARD, C_NAVY),
        ("⏱️ SLA Clustering", "Abnormal surge of bulk closures 5 minutes prior to SLA breach deadline.", C_AMBER_BG, C_AMBER)
    ]
    for idx, (dh, dd, d_bg, d_col) in enumerate(detectors_eg):
        d_top = 1.85 + idx * 0.74
        add_card(s5, 6.30, d_top, 6.33, 0.62, bg_color=d_bg, border_color=d_col, border_width=1)
        tb_d = s5.shapes.add_textbox(Inches(6.45), Inches(d_top + 0.04), Inches(6.03), Inches(0.54))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        p1 = tf_d.paragraphs[0]
        p1.text = dh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = d_col
        p2 = tf_d.add_paragraph()
        p2.text = dd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = C_SLATE_TEXT

    # Bottom Callout Box
    add_callout(s5, 0.50, 5.90, 12.33, 0.85,
                "Execution Gaps: Evidence exists, but recorded operational behaviour appears anomalous or gamed.\nExample: Opened 10:02:15  ➔  Closed 10:02:19 (4 seconds)  ➔  [ Review Recommended ]",
                icon="⚡", bg_color=C_RED_BG, border_color=C_RED, text_color=C_NAVY, font_size=10.5, bold=True)


    # =========================================================================
    # SLIDE 6: DETECTION METHOD 2 — NEGATIVE SPACE
    # =========================================================================
    s6 = prs.slides[5]
    add_header(s6, 6, TOTAL_SLIDES, "Detection Method 2: Negative Space Workflow", "NEGATIVE SPACE")

    # Left Side: Expectation vs Observation Diagram
    add_card(s6, 0.50, 1.35, 5.40, 4.40, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_ns_t = s6.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(5.00), Inches(0.30))
    p_nst = tb_ns_t.text_frame.paragraphs[0]
    p_nst.text = "EXPECTATION VS OBSERVATION MODEL"
    p_nst.font.name = FONT_TITLE
    p_nst.font.size = Pt(11)
    p_nst.font.bold = True
    p_nst.font.color.rgb = C_SIH_BLUE

    ns_model_steps = [
        ("1. ENTITY PROFILE", "Assets + Sector + Entity Scale", C_NAVY_LIGHT),
        ("2. EXPECTED BEHAVIOUR", "Model normal alert baseline & active assets", C_NAVY_LIGHT),
        ("3. COMPARE EXPECTED VS OBSERVED", "Compare expected telemetry vs actual logs", C_SIH_BLUE),
        ("4. MISSING / UNUSUALLY SPARSE?", "Evaluate silent periods, dropped categories & orphan alerts", C_AMBER),
        ("5. YES ➔ REVIEW RECOMMENDED", "Negative space signal flagged for auditor drilldown", C_RED)
    ]
    for idx, (nh, nd, nc) in enumerate(ns_model_steps):
        n_top = 1.85 + idx * 0.72
        add_card(s6, 0.70, n_top, 5.00, 0.54, bg_color=nc, border_color=C_ACCENT_BLUE if nc == C_NAVY_LIGHT else nc, border_width=1)
        tb_n = s6.shapes.add_textbox(Inches(0.85), Inches(n_top + 0.04), Inches(4.70), Inches(0.46))
        tf_n = tb_n.text_frame
        tf_n.word_wrap = True
        p1 = tf_n.paragraphs[0]
        p1.text = nh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE if nc in [C_NAVY_LIGHT, C_RED, C_SIH_BLUE] else C_NAVY
        p2 = tf_n.add_paragraph()
        p2.text = nd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = C_BORDER_LIGHT if nc in [C_NAVY_LIGHT, C_RED, C_SIH_BLUE] else C_SLATE_DARK
        if idx < 4:
            add_down_arrow(s6, 3.10, n_top + 0.56, width=0.15, height=0.14, color=C_SIH_BLUE)

    # Right Side: Visual Bar Graphics (Expected vs Observed)
    add_card(s6, 6.10, 1.35, 6.73, 4.40, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_cmp_t = s6.shapes.add_textbox(Inches(6.30), Inches(1.45), Inches(6.33), Inches(0.30))
    p_cmpt = tb_cmp_t.text_frame.paragraphs[0]
    p_cmpt.text = "VISUAL EVIDENCE OF NEGATIVE SPACE"
    p_cmpt.font.name = FONT_TITLE
    p_cmpt.font.size = Pt(11)
    p_cmpt.font.bold = True
    p_cmpt.font.color.rgb = C_NAVY

    # Bar 1: Alert Volume Comparison
    add_card(s6, 6.30, 1.85, 6.33, 1.05, bg_color=C_BG_CARD, border_color=C_BORDER_LIGHT, border_width=1)
    tb_b1 = s6.shapes.add_textbox(Inches(6.45), Inches(1.90), Inches(6.03), Inches(0.95))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True
    p1 = tf_b1.paragraphs[0]
    p1.text = "1. Alert Volume Density (Expected vs Observed)"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p2 = tf_b1.add_paragraph()
    p2.text = "Expected:  ████████████████████  (100% Peer Baseline)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = C_SIH_BLUE
    p3 = tf_b1.add_paragraph()
    p3.text = "Observed:  ██████  (28%)  ➔  [ Potential Coverage Gap ]"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.0)
    p3.font.bold = True
    p3.font.color.rgb = C_RED

    # Bar 2: Asset Telemetry Coverage
    add_card(s6, 6.30, 3.00, 6.33, 1.05, bg_color=C_BG_CARD, border_color=C_BORDER_LIGHT, border_width=1)
    tb_b2 = s6.shapes.add_textbox(Inches(6.45), Inches(3.05), Inches(6.03), Inches(0.95))
    tf_b2 = tb_b2.text_frame
    tf_b2.word_wrap = True
    p1 = tf_b2.paragraphs[0]
    p1.text = "2. Asset Telemetry Reporting (Registered vs Active Logs)"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p2 = tf_b2.add_paragraph()
    p2.text = "Registered: ████████████████████  (50 Critical Tier-1 Assets)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = C_SIH_BLUE
    p3 = tf_b2.add_paragraph()
    p3.text = "Reporting:  █████████  (41 Active)  ➔  [ 9 Silent SCADA Gateways ]"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.0)
    p3.font.bold = True
    p3.font.color.rgb = C_AMBER

    # Bar 3: Shift Window Blackout
    add_card(s6, 6.30, 4.15, 6.33, 1.05, bg_color=C_BG_CARD, border_color=C_BORDER_LIGHT, border_width=1)
    tb_b3 = s6.shapes.add_textbox(Inches(6.45), Inches(4.20), Inches(6.03), Inches(0.95))
    tf_b3 = tb_b3.text_frame
    tf_b3.word_wrap = True
    p1 = tf_b3.paragraphs[0]
    p1.text = "3. Shift Window Coverage (24/7 Roster Monitoring)"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p2 = tf_b3.add_paragraph()
    p2.text = "Day Shifts:   ████████████████████  (Normal Triage)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = C_SIH_BLUE
    p3 = tf_b3.add_paragraph()
    p3.text = "Night Shifts: █  (4%)  ➔  [ Shift Blackout Anomaly ]"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.0)
    p3.font.bold = True
    p3.font.color.rgb = C_RED

    # Bottom Callout Box
    add_callout(s6, 0.50, 5.90, 12.33, 0.85,
                '"The absence of evidence can itself be evidence for review."\nSAT-SA analyses not only what exists, but also what should exist.',
                icon="🕳️", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11.5, bold=True)


    # =========================================================================
    # SLIDE 7: PEER BENCHMARKING (Distribution & Baseline)
    # =========================================================================
    s7 = prs.slides[6]
    add_header(s7, 7, TOTAL_SLIDES, "Peer Benchmarking: Distribution & Context", "PEER BENCHMARKING")

    # Top Visual: Distribution Benchmark Scale
    add_card(s7, 0.50, 1.35, 12.33, 2.30, bg_color=C_WHITE, border_color=C_SIH_BLUE, border_width=1.5)
    tb_scale_t = s7.shapes.add_textbox(Inches(0.70), Inches(1.42), Inches(11.93), Inches(0.28))
    p_sct = tb_scale_t.text_frame.paragraphs[0]
    p_sct.text = "CRITICAL ALERT CLOSURE TIME DISTRIBUTION (POWER SECTOR TIER-1 COHORT)"
    p_sct.font.name = FONT_TITLE
    p_sct.font.size = Pt(11)
    p_sct.font.bold = True
    p_sct.font.color.rgb = C_NAVY

    # Timeline Scale Line Shape
    scale_bar = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.00), Inches(2.20), Inches(11.33), Inches(0.08))
    set_shape_style(scale_bar, C_BORDER)
    
    # Peer Range Track
    peer_range = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.72), Inches(2.10), Inches(5.10), Inches(0.28))
    set_shape_style(peer_range, C_BLUE_BG, C_SIH_BLUE, 1)
    
    # Scale Ticks & Labels
    scale_marks = [
        ("0 min", 1.00), ("10 min", 2.88), ("20 min", 4.76), 
        ("30 min", 6.64), ("40 min", 8.52), ("50 min", 10.40), ("60 min", 12.28)
    ]
    for lbl, x_pos in scale_marks:
        tb_m = s7.shapes.add_textbox(Inches(x_pos - 0.40), Inches(2.35), Inches(0.80), Inches(0.30))
        p = tb_m.text_frame.paragraphs[0]
        p.text = lbl
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED
        p.alignment = PP_ALIGN.CENTER

    # Peer Median Marker (38.5 min at x = 8.24)
    med_marker = s7.shapes.add_shape(MSO_SHAPE.OVAL, Inches(8.14), Inches(2.04), Inches(0.40), Inches(0.40))
    set_shape_style(med_marker, C_SIH_BLUE, C_WHITE, 1.5)
    tb_med_lbl = s7.shapes.add_textbox(Inches(7.24), Inches(1.70), Inches(2.20), Inches(0.35))
    p_ml = tb_med_lbl.text_frame.paragraphs[0]
    p_ml.text = "● Peer Median: 38.5 min"
    p_ml.font.name = FONT_BODY
    p_ml.font.size = Pt(9.5)
    p_ml.font.bold = True
    p_ml.font.color.rgb = C_SIH_BLUE
    p_ml.alignment = PP_ALIGN.CENTER

    # Outlier Marker CSE-014 (4.2 min at x = 1.79)
    out_marker = s7.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.69), Inches(2.04), Inches(0.40), Inches(0.40))
    set_shape_style(out_marker, C_RED, C_WHITE, 1.5)
    tb_out_lbl = s7.shapes.add_textbox(Inches(0.80), Inches(1.70), Inches(2.20), Inches(0.35))
    p_ol = tb_out_lbl.text_frame.paragraphs[0]
    p_ol.text = "🔴 CSE-014: 4.2 min"
    p_ol.font.name = FONT_BODY
    p_ol.font.size = Pt(9.5)
    p_ol.font.bold = True
    p_ol.font.color.rgb = C_RED
    p_ol.alignment = PP_ALIGN.CENTER

    # Bottom Left: 5-Stage Benchmarking Process Flow
    add_card(s7, 0.50, 3.80, 6.00, 1.95, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    tb_pf_t = s7.shapes.add_textbox(Inches(0.70), Inches(3.88), Inches(5.60), Inches(0.28))
    p_pft = tb_pf_t.text_frame.paragraphs[0]
    p_pft.text = "5-STAGE BENCHMARKING PROCESS"
    p_pft.font.name = FONT_TITLE
    p_pft.font.size = Pt(10.5)
    p_pft.font.bold = True
    p_pft.font.color.rgb = C_NAVY

    bm_steps = [
        ("1. Entity Profile", "Extract sector, scale & asset mix"),
        ("2. Identify Peer Group", "Match with homogenous cohort"),
        ("3. Calculate Baseline", "Robust median & IQR bounds"),
        ("4. Measure Deviation", "Empirical Bayes shrinkage Z-score"),
        ("5. Generate Signal", "Flag review priority if > 3σ outlier")
    ]
    for idx, (bh, bd) in enumerate(bm_steps):
        b_top = 4.20 + idx * 0.28
        tb_b = s7.shapes.add_textbox(Inches(0.70), Inches(b_top), Inches(5.60), Inches(0.26))
        tf_b = tb_b.text_frame
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        p = tf_b.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"• {bh}: "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = C_SIH_BLUE
        r2 = p.add_run()
        r2.text = bd
        r2.font.name = FONT_BODY
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = C_SLATE_DARK

    # Bottom Right: Normalization Dimensions Card
    add_card(s7, 6.70, 3.80, 6.13, 1.95, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_cd_t = s7.shapes.add_textbox(Inches(6.90), Inches(3.88), Inches(5.73), Inches(0.28))
    p_cdt = tb_cd_t.text_frame.paragraphs[0]
    p_cdt.text = "PEER CONTEXT FACTORS & STATISTICAL GUARDRAILS"
    p_cdt.font.name = FONT_TITLE
    p_cdt.font.size = Pt(10.5)
    p_cdt.font.bold = True
    p_cdt.font.color.rgb = C_SIH_BLUE

    context_bullets = [
        ("• Sector Normalization: ", "Power Grid vs Banking vs Telecom baselines"),
        ("• Entity Size Scaling: ", "Accounts for 50k alerts/day enterprise vs Tier-3 entities"),
        ("• Asset Mix Diversity: ", "Differentiates IT endpoints from OT/SCADA devices"),
        ("• Empirical Bayes: ", "Prevents noisy small-sample bias from triggering false alarms")
    ]
    for idx, (ch, cd) in enumerate(context_bullets):
        c_top = 4.20 + idx * 0.35
        tb_c = s7.shapes.add_textbox(Inches(6.90), Inches(c_top), Inches(5.73), Inches(0.32))
        tf_c = tb_c.text_frame
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p = tf_c.paragraphs[0]
        r1 = p.add_run()
        r1.text = ch
        r1.font.name = FONT_BODY
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = C_AMBER
        r2 = p.add_run()
        r2.text = cd
        r2.font.name = FONT_BODY
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = C_BORDER_LIGHT

    # Bottom Callout Banner
    add_callout(s7, 0.50, 5.90, 12.33, 0.85,
                '"Peer deviation is a review signal — not a conclusion."\nSAT-SA ensures anomalies reflect genuine operational divergence, not differences in entity scale or sector.',
                icon="📊", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)


    # =========================================================================
    # SLIDE 8: EVIDENCE TRAIL (From Finding to Evidence)
    # =========================================================================
    s8 = prs.slides[7]
    add_header(s8, 8, TOTAL_SLIDES, "From Finding to Evidence: Forensic Traceability", "EVIDENCE TRAIL")

    # Left Side: Connected Chain Diagram (6 Nodes)
    add_card(s8, 0.50, 1.35, 5.80, 4.40, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_ec_t = s8.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(5.40), Inches(0.30))
    p_ect = tb_ec_t.text_frame.paragraphs[0]
    p_ect.text = "THE EVIDENCE CHAIN"
    p_ect.font.name = FONT_TITLE
    p_ect.font.size = Pt(11)
    p_ect.font.bold = True
    p_ect.font.color.rgb = C_SIH_BLUE

    chain_nodes_s8 = [
        ("FINDING", "Critical alerts closed unusually quickly", C_RED),
        ("ALERT", "A-19283 (Severity 5: Mimikatz Memory Dump)", C_NAVY_LIGHT),
        ("CASE", "Ticket #C-8821", C_NAVY_LIGHT),
        ("ESCALATION", "NONE (Closed at Tier-1 triage)", C_AMBER),
        ("RAW RECORD", "Timestamp: 14:03:12 ➔ 14:03:19 (7s) | Analyst #11", C_NAVY_LIGHT),
        ("PEER BASELINE", "Power Sector Tier-1 Median: 38.5 minutes", C_SIH_BLUE)
    ]
    for idx, (nh, nd, nc) in enumerate(chain_nodes_s8):
        c_top = 1.85 + idx * 0.62
        add_card(s8, 0.70, c_top, 5.40, 0.48, bg_color=nc if nc != C_NAVY_LIGHT else C_NAVY_LIGHT, border_color=C_ACCENT_BLUE if nc == C_NAVY_LIGHT else nc, border_width=1)
        tb_cn = s8.shapes.add_textbox(Inches(0.85), Inches(c_top + 0.02), Inches(5.10), Inches(0.44))
        tf_cn = tb_cn.text_frame
        tf_cn.word_wrap = True
        p = tf_cn.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{nh}: "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(9.0)
        r1.font.bold = True
        r1.font.color.rgb = C_WHITE if nc in [C_RED, C_SIH_BLUE, C_NAVY_LIGHT] else C_NAVY
        r2 = p.add_run()
        r2.text = nd
        r2.font.name = FONT_BODY
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = C_BORDER_LIGHT if nc in [C_RED, C_SIH_BLUE, C_NAVY_LIGHT] else C_SLATE_DARK
        if idx < 5:
            add_down_arrow(s8, 3.30, c_top + 0.50, width=0.14, height=0.12, color=C_SIH_BLUE)

    # Right Side: Supervisory Explainability Card
    add_card(s8, 6.50, 1.35, 6.33, 4.40, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    
    # "WHY WAS THIS FLAGGED?" Button Box
    add_card(s8, 6.70, 1.50, 5.93, 0.48, bg_color=C_SIH_BLUE, border_color=C_SIH_BLUE, border_width=0)
    tb_btn = s8.shapes.add_textbox(Inches(6.75), Inches(1.56), Inches(5.83), Inches(0.35))
    p_btn = tb_btn.text_frame.paragraphs[0]
    p_btn.text = "🔍  WHY WAS THIS FLAGGED?"
    p_btn.font.name = FONT_TITLE
    p_btn.font.size = Pt(11)
    p_btn.font.bold = True
    p_btn.font.color.rgb = C_WHITE
    p_btn.alignment = PP_ALIGN.CENTER

    tb_why = s8.shapes.add_textbox(Inches(6.70), Inches(2.15), Inches(5.93), Inches(3.40))
    tf_why = tb_why.text_frame
    tf_why.word_wrap = True
    
    reasons_s8 = [
        ("• Closure Velocity Outlier:", " Closure duration (7 seconds) is significantly below the peer cohort median (38.5 minutes) and entity own historical baseline."),
        ("• Critical Severity Rule:", " Severity 5 (Credential Dumping) mandates Tier-2 escalation under NCIIPC guidelines; alert was dismissed without investigation."),
        ("• MinHash Template Note:", ' Resolution note "Routine system noise - verified" has 98.4% Jaccard similarity to 42 other tickets resolved by Analyst #11.'),
        ("• Defensible Custody:", " SHA-256 hash-chain confirms raw log timestamp integrity with zero tampering.")
    ]
    for i, (k, v) in enumerate(reasons_s8):
        p = tf_why.paragraphs[0] if i == 0 else tf_why.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = k
        r1.font.name = FONT_BODY
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = f" {v}"
        r2.font.name = FONT_BODY
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = C_SLATE_DARK

    # Bottom Callout Box
    add_callout(s8, 0.50, 5.90, 12.33, 0.85,
                '"SAT-SA does not just produce a recommendation. It shows the evidence behind it."',
                icon="📜", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=12, bold=True)


    # =========================================================================
    # SLIDE 9: SAT-SA SYSTEM ARCHITECTURE (Layered Stack)
    # =========================================================================
    s9 = prs.slides[8]
    add_header(s9, 9, TOTAL_SLIDES, "SAT-SA System Architecture: Layered Pipeline", "SYSTEM ARCHITECTURE")

    # Left Column: Layered Architecture Diagram
    add_card(s9, 0.50, 1.35, 6.80, 4.40, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_sa_t = s9.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(6.40), Inches(0.30))
    p_sat = tb_sa_t.text_frame.paragraphs[0]
    p_sat.text = "LAYERED SYSTEM ARCHITECTURE"
    p_sat.font.name = FONT_TITLE
    p_sat.font.size = Pt(11)
    p_sat.font.bold = True
    p_sat.font.color.rgb = C_NAVY

    arch_layers = [
        ("DATA SOURCES", "CSV | JSON | DB EXPORTS | SOC RECORDS", C_NAVY_LIGHT),
        ("INGESTION & NORMALISATION", "Schema Validation | Data Quality Gate | SHA-256 Ledger", C_SIH_BLUE),
        ("FEATURE LAYER", "Entity | Asset | Alert | Case Behavioral Feature Vectors", C_NAVY),
        ("ANALYTICS ENGINE", "Rule Engine (20+)  |  Statistics (EB)  |  Anomaly ML (Isolation Forest)", C_ACCENT_BLUE),
        ("PRIORITISATION", "NCIIPC Capability Scoring  |  Budget Optimizer (Knapsack)", C_AMBER),
        ("EVIDENCE LAYER", "Forensic Dossier Generator  |  Explainable Chain Links", C_SLATE_DARK),
        ("LOCAL DASHBOARD", "Air-Gapped Streamlit + Plotly Visual Interface", C_GREEN)
    ]
    for idx, (lh, lb, lc) in enumerate(arch_layers):
        l_top = 1.82 + idx * 0.53
        add_card(s9, 0.70, l_top, 6.40, 0.46, bg_color=C_BG_CARD, border_color=lc, border_width=1.2)
        tb_l = s9.shapes.add_textbox(Inches(0.85), Inches(l_top + 0.02), Inches(6.10), Inches(0.42))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        p1 = tf_l.paragraphs[0]
        p1.text = lh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.0)
        p1.font.bold = True
        p1.font.color.rgb = lc
        p2 = tf_l.add_paragraph()
        p2.text = lb
        p2.font.name = FONT_BODY
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = C_SLATE_TEXT
        if idx < 6:
            add_down_arrow(s9, 3.80, l_top + 0.47, width=0.12, height=0.10, color=C_SIH_BLUE)

    # Right Column: OFFLINE-FIRST Highlights
    add_card(s9, 7.50, 1.35, 5.33, 4.40, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    
    # Offline-First Badge
    add_card(s9, 7.70, 1.50, 4.93, 0.48, bg_color=C_SIH_BLUE, border_color=C_SIH_BLUE, border_width=0)
    tb_of = s9.shapes.add_textbox(Inches(7.75), Inches(1.56), Inches(4.83), Inches(0.35))
    p_of = tb_of.text_frame.paragraphs[0]
    p_of.text = "🔒  OFFLINE-FIRST GUARANTEES"
    p_of.font.name = FONT_TITLE
    p_of.font.size = Pt(11)
    p_of.font.bold = True
    p_of.font.color.rgb = C_WHITE
    p_of.alignment = PP_ALIGN.CENTER

    tb_of_b = s9.shapes.add_textbox(Inches(7.70), Inches(2.15), Inches(4.93), Inches(3.40))
    tf_ofb = tb_of_b.text_frame
    tf_ofb.word_wrap = True
    
    of_points = [
        ("• Air-Gapped Deployment:", " Runs 100% locally inside classified premises with zero network access."),
        ("• No External Cloud APIs:", " No LLM cloud dependencies, no external telemetry, no data leakage."),
        ("• In-Process High Speed:", " Apache Parquet + DuckDB processes 500k+ alerts in <15s on commodity laptops."),
        ("• Reproducible Runs:", " Bit-for-bit identical results from identical input datasets."),
        ("• Cryptographic Integrity:", " SHA-256 hash chain ensures tamper-evident audit submissions.")
    ]
    for i, (k, v) in enumerate(of_points):
        p = tf_ofb.paragraphs[0] if i == 0 else tf_ofb.add_paragraph()
        p.space_after = Pt(5)
        r1 = p.add_run()
        r1.text = k
        r1.font.name = FONT_BODY
        r1.font.size = Pt(9.0)
        r1.font.bold = True
        r1.font.color.rgb = C_AMBER
        r2 = p.add_run()
        r2.text = f" {v}"
        r2.font.name = FONT_BODY
        r2.font.size = Pt(8.0)
        r2.font.color.rgb = C_BORDER_LIGHT

    # Bottom Callout Box
    add_callout(s9, 0.50, 5.90, 12.33, 0.85,
                "Air-Gapped • No External APIs • Reproducible • Auditable • High Performance DuckDB Engine",
                icon="🛡️", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)


    # =========================================================================
    # SLIDE 10: DASHBOARD + REVIEW WORKFLOW
    # =========================================================================
    s10 = prs.slides[9]
    add_header(s10, 10, TOTAL_SLIDES, "Dashboard & Reviewer Workflow", "USER JOURNEY")

    # Left Side: Dashboard Mockup
    add_card(s10, 0.50, 1.35, 6.20, 4.40, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_db_t = s10.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(5.80), Inches(0.28))
    p_dbt = tb_db_t.text_frame.paragraphs[0]
    p_dbt.text = "SUPERVISORY AUDIT DASHBOARD MOCKUP"
    p_dbt.font.name = FONT_TITLE
    p_dbt.font.size = Pt(10.5)
    p_dbt.font.bold = True
    p_dbt.font.color.rgb = C_NAVY

    # 4 KPI Tiles
    kpi_d = [
        ("20", "Entities", C_NAVY),
        ("6", "Review Rec.", C_RED),
        ("14", "High Findings", C_AMBER),
        ("94%", "Data Quality", C_GREEN)
    ]
    for idx, (kv, kl, kc) in enumerate(kpi_d):
        k_left = 0.70 + idx * 1.45
        add_kpi_card(s10, k_left, 1.80, 1.35, 0.85, kv, kl, val_color=kc, bg_color=C_BG_CARD, border_color=C_BORDER_LIGHT)

    # Small Entity Table
    tbl_shape = s10.shapes.add_table(4, 4, Inches(0.70), Inches(2.80), Inches(5.80), Inches(2.75))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(1.40)  # Entity
    tbl.columns[1].width = Inches(1.50)  # Sector
    tbl.columns[2].width = Inches(1.40)  # Priority
    tbl.columns[3].width = Inches(1.50)  # Confidence

    table_data_s10 = [
        ["Entity", "Sector", "Priority", "Confidence"],
        ["CSE-014", "Power Grid", "HIGH", "91%"],
        ["CSE-008", "Banking", "MEDIUM", "84%"],
        ["CSE-003", "Telecom", "LOW", "93%"]
    ]
    for r_idx, row in enumerate(table_data_s10):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(9.0)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY
            else:
                p.font.bold = (c_idx in [0, 2, 3])
                if c_idx == 2:
                    p.font.color.rgb = C_RED if val == "HIGH" else (C_AMBER if val == "MEDIUM" else C_GREEN)
                else:
                    p.font.color.rgb = C_SLATE_DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 1 else C_BG_CARD

    # Right Side: Reviewer Workflow
    add_card(s10, 6.90, 1.35, 5.93, 4.40, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_rw_t = s10.shapes.add_textbox(Inches(7.10), Inches(1.45), Inches(5.53), Inches(0.28))
    p_rwt = tb_rw_t.text_frame.paragraphs[0]
    p_rwt.text = "REVIEWER WORKFLOW (USER JOURNEY)"
    p_rwt.font.name = FONT_TITLE
    p_rwt.font.size = Pt(10.5)
    p_rwt.font.bold = True
    p_rwt.font.color.rgb = C_SIH_BLUE

    user_journey = [
        ("1. Dashboard Portfolio", "View entity priority rankings & quality gate"),
        ("2. Select Entity (CSE-014)", "Open entity supervisory profile"),
        ("3. View Finding", "Inspect flagged Execution Gaps & Negative Space"),
        ("4. 'Why Was This Flagged?'", "Examine statistical deviation & rule rationale"),
        ("5. Open Evidence Dossier", "Review linked alerts, cases & raw record timestamps"),
        ("6. Compare With Peers", "Verify sector cohort baseline distribution"),
        ("7. Expert Decision", "Confirm, Reject, or Request Targeted Inspection")
    ]
    for idx, (jh, jd) in enumerate(user_journey):
        j_top = 1.82 + idx * 0.53
        add_card(s10, 7.10, j_top, 5.53, 0.46, bg_color=C_NAVY_LIGHT, border_color=C_ACCENT_BLUE, border_width=1)
        tb_j = s10.shapes.add_textbox(Inches(7.25), Inches(j_top + 0.02), Inches(5.23), Inches(0.42))
        tf_j = tb_j.text_frame
        tf_j.word_wrap = True
        p1 = tf_j.paragraphs[0]
        p1.text = f"{jh} — "
        p1.font.name = FONT_BODY
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p2 = tf_j.add_paragraph()
        p2.text = jd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = C_BORDER_LIGHT
        if idx < 6:
            add_down_arrow(s10, 9.85, j_top + 0.47, width=0.10, height=0.09, color=C_SIH_BLUE)

    # Bottom Callout Box
    add_callout(s10, 0.50, 5.90, 12.33, 0.85,
                "A seamless user journey from high-level portfolio oversight to deep forensic record verification.\n*All quantitative metrics shown are illustrative demonstration values.",
                icon="🖥️", bg_color=C_BG_CARD, border_color=C_MUTED, text_color=C_NAVY, font_size=10, bold=True)


    # =========================================================================
    # SLIDE 11: VALIDATION (Ground-Truth Benchmark)
    # =========================================================================
    s11 = prs.slides[10]
    add_header(s11, 11, TOTAL_SLIDES, "How Do We Validate SAT-SA?", "EMPIRICAL VALIDATION")

    # Top Section: Ground-Truth Validation Workflow
    add_card(s11, 0.50, 1.35, 12.33, 1.45, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    tb_vw_t = s11.shapes.add_textbox(Inches(0.70), Inches(1.42), Inches(11.93), Inches(0.28))
    p_vwt = tb_vw_t.text_frame.paragraphs[0]
    p_vwt.text = "GROUND-TRUTH VALIDATION WORKFLOW"
    p_vwt.font.name = FONT_BODY
    p_vwt.font.size = Pt(11)
    p_vwt.font.bold = True
    p_vwt.font.color.rgb = C_NAVY

    val_pipe_s11 = [
        ("1. Synthetic SOC Data", "Multi-entity generator with realistic MITRE alerts"),
        ("2. Inject Known Faults", "Fast closures, template notes, silent assets, drops"),
        ("3. Run SAT-SA Engine", "Offline execution of rules, shrinkage & negative space"),
        ("4. Compare Ground Truth", "Measure Precision@K, Recall@K & Detection Lift")
    ]
    for idx, (vh, vd) in enumerate(val_pipe_s11):
        v_left = 0.70 + idx * 2.95
        add_card(s11, v_left, 1.75, 2.75, 0.90, bg_color=C_WHITE, border_color=C_SIH_BLUE, border_width=1.2)
        tb_v = s11.shapes.add_textbox(Inches(v_left + 0.08), Inches(1.82), Inches(2.59), Inches(0.76))
        tf_v = tb_v.text_frame
        tf_v.word_wrap = True
        p1 = tf_v.paragraphs[0]
        p1.text = vh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = C_SIH_BLUE
        p2 = tf_v.add_paragraph()
        p2.text = vd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_SLATE_TEXT

    # Bottom Left: 3 Core Validation Metrics
    add_card(s11, 0.50, 2.95, 5.95, 2.80, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_vm_t = s11.shapes.add_textbox(Inches(0.70), Inches(3.05), Inches(5.55), Inches(0.28))
    p_vmt = tb_vm_t.text_frame.paragraphs[0]
    p_vmt.text = "CORE VALIDATION METRICS"
    p_vmt.font.name = FONT_TITLE
    p_vmt.font.size = Pt(11)
    p_vmt.font.bold = True
    p_vmt.font.color.rgb = C_NAVY

    v_metrics = [
        ("Precision@K:", " How many top recommendations are relevant? Ensures auditors spend inspection hours on genuine operational anomalies."),
        ("Recall@K:", " How many injected issues are discovered? Verifies high coverage across both execution gaps and silent negative space."),
        ("Lift over Random:", " 4.5x - 6.0x higher fault discovery rate compared to traditional manual sampling methods.")
    ]
    tb_vm_b = s11.shapes.add_textbox(Inches(0.70), Inches(3.35), Inches(5.55), Inches(2.30))
    tf_vmb = tb_vm_b.text_frame
    tf_vmb.word_wrap = True
    for i, (k, v) in enumerate(v_metrics):
        p = tf_vmb.paragraphs[0] if i == 0 else tf_vmb.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {k}"
        r1.font.name = FONT_BODY
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = C_SIH_BLUE
        r2 = p.add_run()
        r2.text = f" {v}"
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = C_SLATE_DARK

    # Bottom Right: Conceptual Lift Bar Chart
    add_card(s11, 6.88, 2.95, 5.95, 2.80, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_lc_t = s11.shapes.add_textbox(Inches(7.08), Inches(3.05), Inches(5.55), Inches(0.28))
    p_lct = tb_lc_t.text_frame.paragraphs[0]
    p_lct.text = "DETECTION LIFT (SAT-SA VS RANDOM SAMPLING)"
    p_lct.font.name = FONT_TITLE
    p_lct.font.size = Pt(11)
    p_lct.font.bold = True
    p_lct.font.color.rgb = C_SIH_BLUE

    tb_lc_b = s11.shapes.add_textbox(Inches(7.08), Inches(3.40), Inches(5.55), Inches(2.25))
    tf_lcb = tb_lc_b.text_frame
    tf_lcb.word_wrap = True
    
    p1 = tf_lcb.paragraphs[0]
    p1.text = "Random Sampling (Baseline Manual Review):"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    
    p2 = tf_lcb.add_paragraph()
    p2.text = "████  (1.0x Baseline Fault Discovery)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = C_MUTED
    p2.space_after = Pt(8)

    p3 = tf_lcb.add_paragraph()
    p3.text = "SAT-SA Prioritisation (Evidence-Driven):"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.5)
    p3.font.bold = True
    p3.font.color.rgb = C_WHITE

    p4 = tf_lcb.add_paragraph()
    p4.text = "████████████████████  (4.5x – 6.0x Lift)"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(9.5)
    p4.font.bold = True
    p4.font.color.rgb = C_AMBER
    p4.space_after = Pt(8)

    p5 = tf_lcb.add_paragraph()
    p5.text = "*Illustrative validation concept — not actual measured results."
    p5.font.name = FONT_BODY
    p5.font.size = Pt(8.0)
    p5.font.italic = True
    p5.font.color.rgb = C_BORDER_LIGHT

    # Bottom Callout Box
    add_callout(s11, 0.50, 5.90, 12.33, 0.85,
                "Empirical validation guarantees that supervisory examiners spend limited inspection budgets on genuine anomalies.",
                icon="🔬", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)


    # =========================================================================
    # SLIDE 12: FINAL IMPACT (Before ➔ SAT-SA ➔ After)
    # =========================================================================
    s12 = prs.slides[11]
    add_header(s12, 12, TOTAL_SLIDES, "From Data Overload to Evidence-Driven Review", "FINAL IMPACT")

    # Top Box: BEFORE (Red / Gray)
    add_card(s12, 0.50, 1.35, 12.33, 1.80, bg_color=C_RED_BG, border_color=C_RED, border_width=1.5)
    tb_ib_t = s12.shapes.add_textbox(Inches(0.70), Inches(1.42), Inches(11.93), Inches(0.28))
    p_ibt = tb_ib_t.text_frame.paragraphs[0]
    p_ibt.text = "BEFORE: MANUAL DATA OVERLOAD & BLINDSPOTS"
    p_ibt.font.name = FONT_TITLE
    p_ibt.font.size = Pt(11)
    p_ibt.font.bold = True
    p_ibt.font.color.rgb = C_RED

    before_impact_nodes = [
        ("Millions of SOC Records", "Unstructured alert & ticket volume"),
        ("Manual Sampling (<0.1%)", "Arbitrary & unrepresentative inspection"),
        ("Limited Review Capacity", "Auditor fatigue & superficial checks"),
        ("Unchecked Blindspots", "Silent assets & gaming remain hidden")
    ]
    for idx, (bh, bd) in enumerate(before_impact_nodes):
        b_left = 0.70 + idx * 2.95
        add_card(s12, b_left, 1.75, 2.75, 1.25, bg_color=C_WHITE, border_color=C_RED, border_width=1)
        tb_bi = s12.shapes.add_textbox(Inches(b_left + 0.08), Inches(1.82), Inches(2.59), Inches(1.10))
        tf_bi = tb_bi.text_frame
        tf_bi.word_wrap = True
        p1 = tf_bi.paragraphs[0]
        p1.text = bh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_RED
        p2 = tf_bi.add_paragraph()
        p2.text = bd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_SLATE_TEXT

    # Center Transformation Badge
    add_card(s12, 4.60, 3.25, 4.13, 0.40, bg_color=C_SIH_BLUE, border_color=C_SIH_BLUE, border_width=0)
    tb_tb = s12.shapes.add_textbox(Inches(4.65), Inches(3.28), Inches(4.03), Inches(0.32))
    p_t = tb_tb.text_frame.paragraphs[0]
    p_t.text = "▼  TRANSFORMED BY SAT-SA  ▼"
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(10)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE
    p_t.alignment = PP_ALIGN.CENTER

    # Bottom Box: AFTER (Navy / Blue)
    add_card(s12, 0.50, 3.75, 12.33, 2.00, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_ia_t = s12.shapes.add_textbox(Inches(0.70), Inches(3.82), Inches(11.93), Inches(0.28))
    p_iat = tb_ia_t.text_frame.paragraphs[0]
    p_iat.text = "AFTER: EVIDENCE-DRIVEN SUPERVISORY IMPACT"
    p_iat.font.name = FONT_TITLE
    p_iat.font.size = Pt(11)
    p_iat.font.bold = True
    p_iat.font.color.rgb = C_SIH_BLUE

    after_impact_nodes = [
        ("Evidence-Based Priorities", "Mathematical risk ranking of entities"),
        ("Explainable Findings", "Unbroken chain connecting raw logs"),
        ("Focused Expert Review", "Targeted inspection on true anomalies"),
        ("Maximised Audit ROI", "Defensible NCIIPC compliance packs")
    ]
    for idx, (ah, ad) in enumerate(after_impact_nodes):
        a_left = 0.70 + idx * 2.95
        add_card(s12, a_left, 4.15, 2.75, 1.45, bg_color=C_NAVY_LIGHT, border_color=C_ACCENT_BLUE, border_width=1)
        tb_ai = s12.shapes.add_textbox(Inches(a_left + 0.08), Inches(4.22), Inches(2.59), Inches(1.30))
        tf_ai = tb_ai.text_frame
        tf_ai.word_wrap = True
        p1 = tf_ai.paragraphs[0]
        p1.text = ah
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p2 = tf_ai.add_paragraph()
        p2.text = ad
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_BORDER_LIGHT

    # Final Closing Banner
    add_callout(s12, 0.50, 5.90, 12.33, 0.85,
                '"From Data Overload to Evidence-Driven Review."\nSAT-SA does not replace the auditor — it helps the auditor find where to look first.',
                icon="🚀", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=12, bold=True)

    # Save presentation
    output_path = 'SIH2026-IDEA-Presentation-Format.pptx'
    prs.save(output_path)
    print(f"Ultra-visual 12-slide presentation successfully generated and saved to: {output_path}")

if __name__ == "__main__":
    build_presentation()
