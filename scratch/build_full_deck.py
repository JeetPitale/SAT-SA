"""
SAT-SA Presentation Builder for SIH 2026 (SIH2026-IDEA-Presentation-Format.pptx)
Generates an 11-slide presentation adapted directly to the official SIH template.
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
C_NAVY_DARK = RGBColor(10, 25, 47)       # #0A192F (Deep Navy)
C_NAVY = RGBColor(15, 30, 60)            # #0F1E3C (Primary Navy)
C_NAVY_LIGHT = RGBColor(24, 43, 73)      # #182B49 (Surface Navy)
C_SIH_BLUE = RGBColor(0, 112, 192)       # #0070C0 (Official SIH Template Accent)
C_ACCENT_BLUE = RGBColor(2, 132, 199)    # #0284C7 (Vibrant Cyan Blue)
C_SLATE_DARK = RGBColor(30, 41, 59)      # #1E293B (Dark Slate Header)
C_SLATE_TEXT = RGBColor(51, 65, 85)      # #334155 (High Legibility Body)
C_MUTED = RGBColor(100, 116, 139)        # #64748B (Muted Label)
C_BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC (Ultra Light Slate)
C_BG_CARD = RGBColor(241, 245, 249)      # #F1F5F9 (Light Card Surface)
C_BORDER = RGBColor(203, 213, 225)       # #CBD5E1 (Border Gray)
C_BORDER_LIGHT = RGBColor(226, 232, 240) # #E2E8F0 (Soft Border)
C_WHITE = RGBColor(255, 255, 255)        # Pure White
C_AMBER = RGBColor(217, 119, 6)          # #D97706 (Warning Amber)
C_AMBER_BG = RGBColor(254, 243, 199)     # #FEF3C7 (Amber Container)
C_RED = RGBColor(220, 38, 38)            # #DC2626 (High Priority / Anomaly Red)
C_RED_BG = RGBColor(254, 226, 226)       # #FEE2E2 (Red Container)
C_GREEN = RGBColor(5, 150, 105)          # #059669 (Healthy Green)
C_GREEN_BG = RGBColor(209, 250, 229)     # #D1FAE5 (Green Container)
C_BLUE_BG = RGBColor(224, 242, 254)      # #E0F2FE (SIH Blue Container)

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

def add_kpi_card(slide, left, top, width, height, val_text, label_text, sublabel="", val_color=C_SIH_BLUE, bg_color=C_WHITE, border_color=C_BORDER):
    card = add_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(Inches(left + 0.08), Inches(top + 0.08), Inches(width - 0.16), Inches(height - 0.16))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p1 = tf.paragraphs[0]
    p1.text = val_text
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = val_color
    p1.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = label_text
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
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

def generate_deck():
    # Load the original template backup as base
    prs = Presentation('SIH2026-IDEA-Presentation-Format.backup.pptx')
    blank_layout = prs.slide_layouts[6]
    
    # Adjust slide count to exactly 11 slides
    while len(prs.slides) < 11:
        prs.slides.add_slide(blank_layout)
    
    # Clear all shapes on every slide so we have clean canvasses with template dimensions & theme
    for slide in prs.slides:
        for s in list(slide.shapes):
            sp = s._element
            sp.getparent().remove(sp)

    TOTAL_SLIDES = 11

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides[0]
    logo_path = 'scratch/template_images/slide1_Picture 1_2.png'
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(10.70), Inches(0.00), width=Inches(2.46), height=Inches(1.16))
    
    # Top banner header text
    tb_top = s1.shapes.add_textbox(Inches(0.50), Inches(0.20), Inches(9.50), Inches(0.40))
    tf_tt = tb_top.text_frame
    p_tt = tf_tt.paragraphs[0]
    p_tt.text = "SMART INDIA HACKATHON 2026  •  OFFICIAL IDEA SUBMISSION"
    p_tt.font.name = FONT_BODY
    p_tt.font.size = Pt(12)
    p_tt.font.bold = True
    p_tt.font.color.rgb = C_SIH_BLUE

    # Main Hero Title Box
    tb_hero = s1.shapes.add_textbox(Inches(0.50), Inches(0.65), Inches(10.00), Inches(1.80))
    tf_h = tb_hero.text_frame
    tf_h.word_wrap = True
    tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
    
    p_h1 = tf_h.paragraphs[0]
    p_h1.text = "SAT-SA"
    p_h1.font.name = FONT_TITLE
    p_h1.font.size = Pt(40)
    p_h1.font.bold = True
    p_h1.font.color.rgb = C_NAVY

    p_h2 = tf_h.add_paragraph()
    p_h2.text = "Security Audit & Supervisory Analytics"
    p_h2.font.name = FONT_TITLE
    p_h2.font.size = Pt(22)
    p_h2.font.bold = True
    p_h2.font.color.rgb = C_SIH_BLUE

    p_h3 = tf_h.add_paragraph()
    p_h3.text = "Turning SOC Records into Actionable Audit Evidence"
    p_h3.font.name = FONT_BODY
    p_h3.font.size = Pt(13)
    p_h3.font.bold = True
    p_h3.font.color.rgb = C_SLATE_TEXT

    # Left Metadata Container Card
    add_card(s1, 0.50, 2.55, 6.00, 3.45, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    tb_meta = s1.shapes.add_textbox(Inches(0.70), Inches(2.70), Inches(5.60), Inches(3.15))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True
    
    meta_items = [
        ("Problem Statement ID:", " 26157 (SIH26157)"),
        ("Problem Statement Title:", " Supervisory Analytics Tool for SOC Assessment"),
        ("Theme:", " Blockchain & Cybersecurity"),
        ("PS Category:", " Software (100% Offline / Air-Gapped)"),
        ("Target Supervisory Agency:", " NCIIPC / NTRO (Under Section 70A, IT Act 2000)"),
        ("Supervision Target:", " Critical Sector Entities (Power, Banking, Telecom)"),
        ("Core Function:", " Human-in-the-Loop Audit Decision-Support System")
    ]
    for i, (k, v) in enumerate(meta_items):
        p = tf_m.paragraphs[0] if i == 0 else tf_m.add_paragraph()
        p.space_after = Pt(5)
        r1 = p.add_run()
        r1.text = k
        r1.font.name = FONT_BODY
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY
        
        r2 = p.add_run()
        r2.text = v
        r2.font.name = FONT_BODY
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_SLATE_TEXT

    # Right Hero Illustration / Visual Concept Card
    add_card(s1, 6.70, 2.55, 6.13, 3.45, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    
    tb_rc = s1.shapes.add_textbox(Inches(6.90), Inches(2.70), Inches(5.73), Inches(0.40))
    p_rc = tb_rc.text_frame.paragraphs[0]
    p_rc.text = "CORE SUPERVISORY WORKFLOW"
    p_rc.font.name = FONT_BODY
    p_rc.font.size = Pt(12)
    p_rc.font.bold = True
    p_rc.font.color.rgb = C_SIH_BLUE

    flow_steps = [
        ("1. SOC Records", "Alerts, Cases, Closures"),
        ("2. Audit Analytics", "Rules & Peer Benchmarking"),
        ("3. Actionable Evidence", "Dossiers & Linked Records"),
        ("4. Human Review", "Examiner Investigation")
    ]
    for idx, (st_t, st_d) in enumerate(flow_steps):
        bx_left = 6.90 + (idx % 2) * 2.90
        bx_top = 3.20 + (idx // 2) * 1.05
        add_card(s1, bx_left, bx_top, 2.75, 0.90, bg_color=C_NAVY_LIGHT, border_color=C_ACCENT_BLUE, border_width=1)
        tb_step = s1.shapes.add_textbox(Inches(bx_left + 0.10), Inches(bx_top + 0.10), Inches(2.55), Inches(0.70))
        tf_s = tb_step.text_frame
        tf_s.word_wrap = True
        p1 = tf_s.paragraphs[0]
        p1.text = st_t
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p2 = tf_s.add_paragraph()
        p2.text = st_d
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_MUTED

    # Bottom Callout at Slide 1
    add_callout(s1, 0.50, 6.10, 12.33, 0.65, 
                "SOC Records  ➔  Analytics  ➔  Evidence  ➔  Human Review  |  Human-in-the-Loop Audit Decision-Support System",
                icon="🛡️", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)

    # Bottom blue ribbon
    ribbon1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.00), Inches(6.95), Inches(13.333), Inches(0.55))
    set_shape_style(ribbon1, C_SIH_BLUE, None)
    foot_s1 = s1.shapes.add_textbox(Inches(0.50), Inches(7.02), Inches(12.33), Inches(0.40))
    p_fs1 = foot_s1.text_frame.paragraphs[0]
    p_fs1.text = "SIH 2026 | Problem Statement 26157 | SAT-SA: Security Audit & Supervisory Analytics"
    p_fs1.font.name = FONT_BODY
    p_fs1.font.size = Pt(11)
    p_fs1.font.color.rgb = C_WHITE
    p_fs1.alignment = PP_ALIGN.CENTER


    # ==========================================
    # SLIDE 2: PROBLEM — How Are SOCs Currently Reviewed?
    # ==========================================
    s2 = prs.slides[1]
    add_header(s2, 2, TOTAL_SLIDES, "How Are SOCs Currently Reviewed?", "PROBLEM STATEMENT")

    # Left Column: Existing Manual Process Flow
    add_card(s2, 0.50, 1.35, 5.20, 4.40, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    tb_s2_left_t = s2.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(4.80), Inches(0.35))
    p_lt = tb_s2_left_t.text_frame.paragraphs[0]
    p_lt.text = "THE EXISTING MANUAL REVIEW PROCESS"
    p_lt.font.name = FONT_TITLE
    p_lt.font.size = Pt(12)
    p_lt.font.bold = True
    p_lt.font.color.rgb = C_NAVY

    steps_manual = [
        ("1. Large SOC Dataset", "Massive volume of historical alerts, case logs, and shift records across entities."),
        ("2. Expert Selects a Sample", "Auditors manually select a small sample (<0.1%) due to limited time and capacity."),
        ("3. Manual Review of Alerts & Cases", "Slow, case-by-case spreadsheet inspection; high cognitive fatigue and subjectivity."),
        ("4. Fragmented Findings", "Surface-level ticket checks; systemic patterns and missing evidence are missed.")
    ]
    for idx, (st_h, st_b) in enumerate(steps_manual):
        c_top = 1.90 + idx * 0.90
        add_card(s2, 0.70, c_top, 4.80, 0.78, bg_color=C_WHITE, border_color=C_BORDER_LIGHT, border_width=1)
        tb_st = s2.shapes.add_textbox(Inches(0.80), Inches(c_top + 0.06), Inches(4.60), Inches(0.66))
        tf_st = tb_st.text_frame
        tf_st.word_wrap = True
        p1 = tf_st.paragraphs[0]
        p1.text = st_h
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_RED if idx == 3 else (C_SIH_BLUE if idx == 0 else C_NAVY)
        p2 = tf_st.add_paragraph()
        p2.text = st_b
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_SLATE_TEXT

    # Right Column: 4 Limitations
    add_card(s2, 5.90, 1.35, 6.93, 4.40, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_s2_rt = s2.shapes.add_textbox(Inches(6.10), Inches(1.45), Inches(6.50), Inches(0.35))
    p_rt = tb_s2_rt.text_frame.paragraphs[0]
    p_rt.text = "CORE SUPERVISORY AUDIT LIMITATIONS"
    p_rt.font.name = FONT_TITLE
    p_rt.font.size = Pt(12)
    p_rt.font.bold = True
    p_rt.font.color.rgb = C_NAVY

    limitations = [
        ("• Huge Volume of Records", "Millions of raw events swamp manual review capacity. Temporal anomalies cannot be spotted by eyeball."),
        ("• Limited Manual Review Capacity", "Human auditors can only inspect a tiny fraction of logs, leaving the vast majority of operations unchecked."),
        ("• Behavioural Patterns Missed", "Subtle operational gaming (e.g. mass closures before SLA deadlines, template notes) bypasses checklists."),
        ("• Cross-Entity & Missing Evidence Gap", "Cross-entity comparison is difficult manually, and missing evidence (silent critical assets) is impossible to spot.")
    ]
    for idx, (lh, lb) in enumerate(limitations):
        l_top = 1.90 + idx * 0.90
        add_card(s2, 6.10, l_top, 6.53, 0.78, bg_color=C_BG_CARD, border_color=C_BORDER_LIGHT, border_width=1)
        tb_l = s2.shapes.add_textbox(Inches(6.20), Inches(l_top + 0.06), Inches(6.33), Inches(0.66))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        p1 = tf_l.paragraphs[0]
        p1.text = lh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY
        p2 = tf_l.add_paragraph()
        p2.text = lb
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_SLATE_TEXT

    # Bottom Callout Box
    add_callout(s2, 0.50, 5.90, 12.33, 0.85,
                '"The problem is not lack of data. The problem is finding the important evidence inside the data."',
                icon="💡", bg_color=C_AMBER_BG, border_color=C_AMBER, text_color=C_NAVY, font_size=12, bold=True)


    # ==========================================
    # SLIDE 3: SAT-SA KEY IDEA — Reframing the Question
    # ==========================================
    s3 = prs.slides[2]
    add_header(s3, 3, TOTAL_SLIDES, "SAT-SA Changes the Question", "KEY IDEA")

    # Top Left: Traditional Question
    add_card(s3, 0.50, 1.35, 5.95, 2.70, bg_color=C_BG_CARD, border_color=C_RED, border_width=1.5)
    tb_tq = s3.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(5.55), Inches(2.45))
    tf_tq = tb_tq.text_frame
    tf_tq.word_wrap = True
    
    p1 = tf_tq.paragraphs[0]
    p1.text = "TRADITIONAL APPROACH"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = C_RED
    
    p2 = tf_tq.add_paragraph()
    p2.text = '"What happened in this alert?"'
    p2.font.name = FONT_TITLE
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = C_NAVY
    p2.space_before = Pt(4)
    p2.space_after = Pt(6)

    bullets_trad = [
        "• Reviews individual alerts and events in isolation.",
        "• Assumes logged records represent the complete ground truth.",
        "• Reactive operational mindset: Triage queue alert-by-alert.",
        "• Misses systemic operational drift and unlogged gaps."
    ]
    for b in bullets_trad:
        p = tf_tq.add_paragraph()
        p.text = b
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = C_SLATE_TEXT

    # Top Right: SAT-SA Question
    add_card(s3, 6.88, 1.35, 5.95, 2.70, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=2)
    tb_sq = s3.shapes.add_textbox(Inches(7.08), Inches(1.45), Inches(5.55), Inches(2.45))
    tf_sq = tb_sq.text_frame
    tf_sq.word_wrap = True
    
    p1 = tf_sq.paragraphs[0]
    p1.text = "SAT-SA SUPERVISORY PERSPECTIVE"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = C_SIH_BLUE
    
    p2 = tf_sq.add_paragraph()
    p2.text = '"Does the recorded SOC behaviour indicate something that deserves expert review?"'
    p2.font.name = FONT_TITLE
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(4)
    p2.space_after = Pt(6)

    bullets_satsa = [
        "• Meta-analysis over alerts, cases, closures, and asset inventories.",
        "• Identifies both Execution Gaps (anomalous acts) and Negative Space (omissions).",
        "• Normalizes findings against peer cohorts by sector, size, and asset mix.",
        "• Mathematically prioritizes where human expert attention is most valuable."
    ]
    for b in bullets_satsa:
        p = tf_sq.add_paragraph()
        p.text = b
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = C_BORDER_LIGHT

    # Bottom Supervisory Workflow
    add_card(s3, 0.50, 4.20, 12.33, 1.55, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_flow_t = s3.shapes.add_textbox(Inches(0.70), Inches(4.28), Inches(11.93), Inches(0.28))
    p_ft = tb_flow_t.text_frame.paragraphs[0]
    p_ft.text = "SUPERVISORY DECISION-SUPPORT WORKFLOW"
    p_ft.font.name = FONT_BODY
    p_ft.font.size = Pt(11)
    p_ft.font.bold = True
    p_ft.font.color.rgb = C_NAVY

    f_nodes = [
        ("Existing SOC Data", "Alerts, Cases, Closures, Assets", C_SIH_BLUE),
        ("SAT-SA Analytics", "Dual Detection & Peer Cohorts", C_NAVY),
        ("Potential Review Areas", "Prioritised Evidence Dossiers", C_AMBER),
        ("Human Expert", "Targeted Investigation", C_GREEN)
    ]
    for idx, (nh, nd, nc) in enumerate(f_nodes):
        n_left = 0.70 + idx * 2.95
        add_card(s3, n_left, 4.60, 2.75, 0.95, bg_color=C_BG_CARD, border_color=nc, border_width=1.5)
        tb_n = s3.shapes.add_textbox(Inches(n_left + 0.08), Inches(4.68), Inches(2.59), Inches(0.80))
        tf_n = tb_n.text_frame
        tf_n.word_wrap = True
        p_nh = tf_n.paragraphs[0]
        p_nh.text = nh
        p_nh.font.name = FONT_BODY
        p_nh.font.size = Pt(11)
        p_nh.font.bold = True
        p_nh.font.color.rgb = nc
        p_nd = tf_n.add_paragraph()
        p_nd.text = nd
        p_nd.font.name = FONT_BODY
        p_nd.font.size = Pt(9.5)
        p_nd.font.color.rgb = C_SLATE_TEXT

    # Bottom Callout Banner
    add_callout(s3, 0.50, 5.90, 12.33, 0.85,
                "SAT-SA prioritises investigation — it does not replace the investigator.\n(Human-in-the-Loop Decision-Support System: Not a SIEM, Not a Real-Time Monitor)",
                icon="⚖️", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)


    # ==========================================
    # SLIDE 4: HOW SAT-SA WORKS — 6-Stage Pipeline
    # ==========================================
    s4 = prs.slides[3]
    add_header(s4, 4, TOTAL_SLIDES, "From Raw SOC Data to Review Priority", "HOW SAT-SA WORKS")

    stages = [
        ("1. DATA INPUT", "• Alerts\n• Cases\n• Escalations\n• Closures\n• Assets\n• Telemetry", C_NAVY_LIGHT),
        ("2. NORMALISATION", "• Common Schema\n• Format Conversion\n• Data Completeness Gate\n• Cryptographic Hashing\n• SHA-256 Ledger", C_SIH_BLUE),
        ("3. ANALYTICS", "• Rule Catalog\n• Statistics\n• Peer Benchmarking\n• Anomaly Detection\n• MinHash Text Similarity", C_NAVY),
        ("4. DETECTION", "• Execution Gaps\n  (Anomalous action)\n• Negative Space\n  (Missing evidence)\n• Temporal Outliers\n• Coverage Gaps", C_RED),
        ("5. PRIORITISATION", "• Identify high-value\n  review targets\n• Capability Scoring\n• Confidence Intervals\n• Risk-Ranked Entities", C_AMBER),
        ("6. HUMAN REVIEW", "• Expert investigates\n  supporting evidence\n• Raw record trace\n• Peer comparison\n• Actionable Dossier", C_GREEN)
    ]

    for idx, (st_title, st_body, st_color) in enumerate(stages):
        c_left = 0.50 + idx * 2.08
        add_card(s4, c_left, 1.35, 1.95, 4.35, bg_color=C_WHITE, border_color=st_color, border_width=1.5)
        add_card(s4, c_left, 1.35, 1.95, 0.48, bg_color=st_color, border_color=st_color, border_width=0, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE)
        tb_sth = s4.shapes.add_textbox(Inches(c_left + 0.05), Inches(1.42), Inches(1.85), Inches(0.35))
        p_sth = tb_sth.text_frame.paragraphs[0]
        p_sth.text = st_title
        p_sth.font.name = FONT_BODY
        p_sth.font.size = Pt(10.5)
        p_sth.font.bold = True
        p_sth.font.color.rgb = C_WHITE
        p_sth.alignment = PP_ALIGN.CENTER
        
        tb_stb = s4.shapes.add_textbox(Inches(c_left + 0.08), Inches(1.90), Inches(1.79), Inches(3.70))
        tf_stb = tb_stb.text_frame
        tf_stb.word_wrap = True
        p_b = tf_stb.paragraphs[0]
        p_b.text = st_body
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = C_SLATE_DARK

    # Bottom Guarantees Badges
    add_card(s4, 0.50, 5.85, 12.33, 0.90, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    guarantees = [
        ("🔒 100% Offline & Air-Gapped", "No external APIs or cloud dependency"),
        ("⛓️ Cryptographic SHA-256 Ledger", "Tamper-evident submissions & audit runs"),
        ("⚡ High-Throughput Processing", "DuckDB + Parquet in-process engine"),
        ("🎯 Defensible Audit Evidence", "Direct links to raw forensic records")
    ]
    for idx, (gh, gb) in enumerate(guarantees):
        g_left = 0.65 + idx * 3.05
        tb_g = s4.shapes.add_textbox(Inches(g_left), Inches(5.92), Inches(2.95), Inches(0.75))
        tf_g = tb_g.text_frame
        tf_g.word_wrap = True
        p1 = tf_g.paragraphs[0]
        p1.text = gh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY
        p2 = tf_g.add_paragraph()
        p2.text = gb
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_MUTED


    # ==========================================
    # SLIDE 5: TWO DETECTION METHODS — Execution Gaps vs Negative Space
    # ==========================================
    s5 = prs.slides[4]
    add_header(s5, 5, TOTAL_SLIDES, "SAT-SA Looks for Two Different Things", "DETECTION METHODS")

    # Left Column: Execution Gaps
    add_card(s5, 0.50, 1.35, 5.95, 4.35, bg_color=C_WHITE, border_color=C_RED, border_width=1.5)
    add_card(s5, 0.50, 1.35, 5.95, 0.50, bg_color=C_RED, border_color=C_RED, border_width=0)
    tb_eg_h = s5.shapes.add_textbox(Inches(0.65), Inches(1.42), Inches(5.65), Inches(0.35))
    p_egh = tb_eg_h.text_frame.paragraphs[0]
    p_egh.text = "EXECUTION GAPS"
    p_egh.font.name = FONT_TITLE
    p_egh.font.size = Pt(12)
    p_egh.font.bold = True
    p_egh.font.color.rgb = C_WHITE

    tb_eg_b = s5.shapes.add_textbox(Inches(0.70), Inches(1.90), Inches(5.55), Inches(2.40))
    tf_eg = tb_eg_b.text_frame
    tf_eg.word_wrap = True
    p_eg_desc = tf_eg.paragraphs[0]
    p_eg_desc.text = "Evidence exists, but behaviour appears unusual:"
    p_eg_desc.font.name = FONT_BODY
    p_eg_desc.font.size = Pt(10)
    p_eg_desc.font.bold = True
    p_eg_desc.font.color.rgb = C_NAVY

    eg_bullets = [
        "• Critical alerts closed unusually quickly (< 10s).",
        "• Critical alerts closed without escalation to Tier-2/3.",
        "• Highly similar investigation notes (copy-paste text).",
        "• Repeated alerts without remediation.",
        "• Bulk closures near SLA deadlines (Goodhart gaming).",
        "• Analyst concentration (workload skew / single operator spikes)."
    ]
    for b in eg_bullets:
        p = tf_eg.add_paragraph()
        p.text = b
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_SLATE_DARK

    # Visual Example inside Left Column
    add_card(s5, 0.70, 4.35, 5.55, 1.20, bg_color=C_RED_BG, border_color=C_RED, border_width=1)
    tb_eg_demo = s5.shapes.add_textbox(Inches(0.80), Inches(4.42), Inches(5.35), Inches(1.05))
    tf_egd = tb_eg_demo.text_frame
    tf_egd.word_wrap = True
    p1 = tf_egd.paragraphs[0]
    p1.text = "ILLUSTRATIVE EXAMPLE (Alert A-19283)"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = C_RED
    p2 = tf_egd.add_paragraph()
    p2.text = "Opened: 10:02:15  ➔  Closed: 10:02:19  |  Duration: 4 seconds"
    p2.font.name = FONT_TITLE
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = C_NAVY
    p3 = tf_egd.add_paragraph()
    p3.text = "→ Review Recommended"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10)
    p3.font.bold = True
    p3.font.color.rgb = C_RED

    # Right Column: Negative Space
    add_card(s5, 6.88, 1.35, 5.95, 4.35, bg_color=C_WHITE, border_color=C_SIH_BLUE, border_width=1.5)
    add_card(s5, 6.88, 1.35, 5.95, 0.50, bg_color=C_SIH_BLUE, border_color=C_SIH_BLUE, border_width=0)
    tb_ns_h = s5.shapes.add_textbox(Inches(7.03), Inches(1.42), Inches(5.65), Inches(0.35))
    p_nsh = tb_ns_h.text_frame.paragraphs[0]
    p_nsh.text = "NEGATIVE SPACE"
    p_nsh.font.name = FONT_TITLE
    p_nsh.font.size = Pt(12)
    p_nsh.font.bold = True
    p_nsh.font.color.rgb = C_WHITE

    tb_ns_b = s5.shapes.add_textbox(Inches(7.08), Inches(1.90), Inches(5.55), Inches(2.40))
    tf_ns = tb_ns_b.text_frame
    tf_ns.word_wrap = True
    p_ns_desc = tf_ns.paragraphs[0]
    p_ns_desc.text = "Expected evidence is missing or unusually sparse:"
    p_ns_desc.font.name = FONT_BODY
    p_ns_desc.font.size = Pt(10)
    p_ns_desc.font.bold = True
    p_ns_desc.font.color.rgb = C_NAVY

    ns_bullets = [
        "• Silent critical assets (Core Domain Controllers / SCADA zero logs).",
        "• Missing alert categories (absence of detections in core MITRE areas).",
        "• Unusually low alert volume compared to peer baseline.",
        "• Alerts without cases (orphan high-severity alarms).",
        "• Cases without escalation.",
        "• Silent periods (shift blackouts) & coverage drift."
    ]
    for b in ns_bullets:
        p = tf_ns.add_paragraph()
        p.text = b
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_SLATE_DARK

    # Visual Example inside Right Column
    add_card(s5, 7.08, 4.35, 5.55, 1.20, bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, border_width=1)
    tb_ns_demo = s5.shapes.add_textbox(Inches(7.18), Inches(4.42), Inches(5.35), Inches(1.05))
    tf_nsd = tb_ns_demo.text_frame
    tf_nsd.word_wrap = True
    p1 = tf_nsd.paragraphs[0]
    p1.text = "Expected"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p2 = tf_nsd.add_paragraph()
    p2.text = "████████████████████"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = C_SIH_BLUE
    p3 = tf_nsd.add_paragraph()
    p3.text = "Observed: ██████  ➔  Potential Coverage Gap"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.5)
    p3.font.bold = True
    p3.font.color.rgb = C_AMBER

    # Bottom Callout Banner
    add_callout(s5, 0.50, 5.90, 12.33, 0.85,
                '"SAT-SA analyses not only what exists, but also what should exist."',
                icon="🔍", bg_color=C_BG_CARD, border_color=C_NAVY, text_color=C_NAVY, font_size=12, bold=True)


    # ==========================================
    # SLIDE 6: PEER BENCHMARKING — Unusual Does Not Mean Wrong
    # ==========================================
    s6 = prs.slides[5]
    add_header(s6, 6, TOTAL_SLIDES, "Unusual Does Not Automatically Mean Wrong", "PEER BENCHMARKING")

    # Left Column: Why Peer Comparison is Necessary
    add_card(s6, 0.50, 1.35, 5.80, 4.35, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    tb_pb_lt = s6.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(5.40), Inches(0.35))
    p_pblt = tb_pb_lt.text_frame.paragraphs[0]
    p_pblt.text = "WHY PEER COMPARISON IS NECESSARY"
    p_pblt.font.name = FONT_TITLE
    p_pblt.font.size = Pt(12)
    p_pblt.font.bold = True
    p_pblt.font.color.rgb = C_NAVY

    tb_pb_lb = s6.shapes.add_textbox(Inches(0.70), Inches(1.85), Inches(5.40), Inches(3.70))
    tf_pbl = tb_pb_lb.text_frame
    tf_pbl.word_wrap = True
    
    pb_points = [
        ("Diverse Operational Profiles:", " A regional power utility SOC naturally operates differently from a national commercial bank or telecom carrier."),
        ("SAT-SA Considers Context:", " Normalization factors include:"),
        ("  • Sector:", " Power, Banking & Finance, Telecom, Transport."),
        ("  • Entity Size:", " Enterprise Tier-1 vs Regional Tier-2 vs Local Tier-3."),
        ("  • Asset Mix:", " Endpoints, Cloud Workloads, and SCADA/OT devices."),
        ("Objective Baseline:", " Benchmarking against a matched peer cohort ensures anomalies represent genuine divergence rather than sector differences.")
    ]
    for i, (k, v) in enumerate(pb_points):
        p = tf_pbl.paragraphs[0] if i == 0 else tf_pbl.add_paragraph()
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
        r2.font.color.rgb = C_SLATE_DARK

    # Right Column: Visual Distribution & Case Example
    add_card(s6, 6.70, 1.35, 6.13, 4.35, bg_color=C_WHITE, border_color=C_SIH_BLUE, border_width=1.5)
    tb_pb_rt = s6.shapes.add_textbox(Inches(6.90), Inches(1.45), Inches(5.73), Inches(0.35))
    p_pbrt = tb_pb_rt.text_frame.paragraphs[0]
    p_pbrt.text = "PEER DISTRIBUTION EXAMPLE"
    p_pbrt.font.name = FONT_TITLE
    p_pbrt.font.size = Pt(12)
    p_pbrt.font.bold = True
    p_pbrt.font.color.rgb = C_NAVY

    # Cards for CSE-014 vs Peer Group
    add_kpi_card(s6, 6.90, 1.90, 2.75, 1.15, "4.2 min", "CSE-014", "Median Critical Alert Closure", val_color=C_RED, bg_color=C_RED_BG, border_color=C_RED)
    add_kpi_card(s6, 9.85, 1.90, 2.75, 1.15, "38.5 min", "Similar Peer Group", "Median Closure (Power Tier-1)", val_color=C_SIH_BLUE, bg_color=C_BLUE_BG, border_color=C_SIH_BLUE)

    # Distribution Visual Box
    add_card(s6, 6.90, 3.20, 5.70, 1.40, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1)
    tb_dist = s6.shapes.add_textbox(Inches(7.05), Inches(3.28), Inches(5.40), Inches(1.25))
    tf_dist = tb_dist.text_frame
    tf_dist.word_wrap = True
    p1 = tf_dist.paragraphs[0]
    p1.text = "COHORT DISTRIBUTION ANALYSIS"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(10)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    
    p2 = tf_dist.add_paragraph()
    p2.text = "Cohort Range: 25.0 min (25th percentile) to 52.0 min (75th percentile)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_SLATE_DARK
    
    p3 = tf_dist.add_paragraph()
    p3.text = "CSE-014 (4.2 min) is in the bottom 0.5% of its peer group. Empirical Bayes shrinkage confirms this is statistically significant."
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.0)
    p3.font.color.rgb = C_SLATE_TEXT

    # Verdict Box
    add_card(s6, 6.90, 4.75, 5.70, 0.80, bg_color=C_AMBER_BG, border_color=C_AMBER, border_width=1.5)
    tb_vd = s6.shapes.add_textbox(Inches(7.05), Inches(4.82), Inches(5.40), Inches(0.65))
    tf_vd = tb_vd.text_frame
    tf_vd.word_wrap = True
    p_vd = tf_vd.paragraphs[0]
    p_vd.text = "Significant Peer Deviation ➔ Review Recommended"
    p_vd.font.name = FONT_TITLE
    p_vd.font.size = Pt(12)
    p_vd.font.bold = True
    p_vd.font.color.rgb = C_NAVY
    p_vd2 = tf_vd.add_paragraph()
    p_vd2.text = "Deviation flags where review is recommended — NOT proof of wrongdoing."
    p_vd2.font.name = FONT_BODY
    p_vd2.font.size = Pt(9.0)
    p_vd2.font.color.rgb = C_SLATE_TEXT

    # Bottom Callout Banner
    add_callout(s6, 0.50, 5.90, 12.33, 0.85,
                "SAT-SA contextualizes alerts by sector, size, and asset mix — ensuring fair and defensible audit prioritization.",
                icon="📊", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)


    # ==========================================
    # SLIDE 7: EVIDENCE TRAIL — Every Finding Has a Reason
    # ==========================================
    s7 = prs.slides[6]
    add_header(s7, 7, TOTAL_SLIDES, "Every Finding Has a Reason", "EVIDENCE TRAIL")

    # Top Section: 6-Node Visual Chain
    add_card(s7, 0.50, 1.35, 12.33, 1.55, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_fc_t = s7.shapes.add_textbox(Inches(0.70), Inches(1.42), Inches(11.93), Inches(0.28))
    p_fct = tb_fc_t.text_frame.paragraphs[0]
    p_fct.text = "THE EVIDENCE TRAIL"
    p_fct.font.name = FONT_BODY
    p_fct.font.size = Pt(11)
    p_fct.font.bold = True
    p_fct.font.color.rgb = C_SIH_BLUE

    chain_nodes = [
        ("Finding", "Execution Gap Flag"),
        ("Alert", "Alert Record A-19283"),
        ("Case", "Investigation Ticket"),
        ("Escalation / Closure", "Closure in 7s / No Esc."),
        ("Raw Evidence", "SHA-256 Telemetry Log"),
        ("Peer Comparison", "38.5 min Cohort Median")
    ]
    for idx, (cn_h, cn_d) in enumerate(chain_nodes):
        c_left = 0.70 + idx * 1.98
        add_card(s7, c_left, 1.75, 1.85, 0.95, bg_color=C_NAVY_LIGHT, border_color=C_ACCENT_BLUE, border_width=1)
        tb_cn = s7.shapes.add_textbox(Inches(c_left + 0.05), Inches(1.82), Inches(1.75), Inches(0.80))
        tf_cn = tb_cn.text_frame
        tf_cn.word_wrap = True
        p1 = tf_cn.paragraphs[0]
        p1.text = cn_h
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p2 = tf_cn.add_paragraph()
        p2.text = cn_d
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_MUTED

    # Bottom Section: Concrete Example Walkthrough
    add_card(s7, 0.50, 3.05, 7.80, 2.70, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_ew_t = s7.shapes.add_textbox(Inches(0.70), Inches(3.15), Inches(7.40), Inches(0.30))
    p_ewt = tb_ew_t.text_frame.paragraphs[0]
    p_ewt.text = "ILLUSTRATIVE FINDING & EVIDENCE TRAIL"
    p_ewt.font.name = FONT_TITLE
    p_ewt.font.size = Pt(11)
    p_ewt.font.bold = True
    p_ewt.font.color.rgb = C_NAVY

    tb_ew_b = s7.shapes.add_textbox(Inches(0.70), Inches(3.45), Inches(7.40), Inches(2.20))
    tf_ew = tb_ew_b.text_frame
    tf_ew.word_wrap = True
    
    dossier_fields = [
        ("Finding:", " Critical alerts closed unusually quickly"),
        ("Alert Identifier:", " A-19283"),
        ("Severity:", " Critical"),
        ("Opened:", " 14:03:12  |  Closed: 14:03:19  (Elapsed: 7 seconds)"),
        ("Escalation:", " No (Closed without Tier-2/3 investigation)"),
        ("Peer Median:", " 38.5 min (Entity is in bottom 0.5 percentile)")
    ]
    for i, (k, v) in enumerate(dossier_fields):
        p = tf_ew.paragraphs[0] if i == 0 else tf_ew.add_paragraph()
        p.space_after = Pt(3)
        r1 = p.add_run()
        r1.text = k
        r1.font.name = FONT_BODY
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = v
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_SLATE_DARK

    # Right Action / Explainability Card
    add_card(s7, 8.50, 3.05, 4.33, 2.70, bg_color=C_BG_CARD, border_color=C_SIH_BLUE, border_width=1.5)
    
    # "WHY WAS THIS FLAGGED?" Visual Button
    add_card(s7, 8.70, 3.20, 3.93, 0.48, bg_color=C_SIH_BLUE, border_color=C_SIH_BLUE, border_width=0)
    tb_btn = s7.shapes.add_textbox(Inches(8.75), Inches(3.26), Inches(3.83), Inches(0.35))
    p_btn = tb_btn.text_frame.paragraphs[0]
    p_btn.text = "WHY WAS THIS FLAGGED?"
    p_btn.font.name = FONT_TITLE
    p_btn.font.size = Pt(11)
    p_btn.font.bold = True
    p_btn.font.color.rgb = C_WHITE
    p_btn.alignment = PP_ALIGN.CENTER

    tb_why = s7.shapes.add_textbox(Inches(8.70), Inches(3.80), Inches(3.93), Inches(1.85))
    tf_why = tb_why.text_frame
    tf_why.word_wrap = True
    p_w1 = tf_why.paragraphs[0]
    p_w1.text = "Explainable Audit Rationale:"
    p_w1.font.name = FONT_BODY
    p_w1.font.size = Pt(10)
    p_w1.font.bold = True
    p_w1.font.color.rgb = C_NAVY
    
    p_w2 = tf_why.add_paragraph()
    p_w2.text = "1. Closure duration (7s) deviates significantly from peer cohort median (38.5 min)."
    p_w2.font.name = FONT_BODY
    p_w2.font.size = Pt(9.0)
    p_w2.font.color.rgb = C_SLATE_DARK

    p_w3 = tf_why.add_paragraph()
    p_w3.text = "2. Critical severity alerts require mandatory Tier-2 review under standard SOPs."
    p_w3.font.name = FONT_BODY
    p_w3.font.size = Pt(9.0)
    p_w3.font.color.rgb = C_SLATE_DARK

    p_w4 = tf_why.add_paragraph()
    p_w4.text = "3. Similar closure notes detected across multiple alerts by the same analyst."
    p_w4.font.name = FONT_BODY
    p_w4.font.size = Pt(9.0)
    p_w4.font.color.rgb = C_SLATE_DARK

    # Bottom Callout Banner
    add_callout(s7, 0.50, 5.90, 12.33, 0.85,
                '"SAT-SA does not just produce a recommendation. It shows the evidence behind it."',
                icon="📜", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=12, bold=True)


    # ==========================================
    # SLIDE 8: SAT-SA DASHBOARD — What the Auditor Sees
    # ==========================================
    s8 = prs.slides[7]
    add_header(s8, 8, TOTAL_SLIDES, "What the Auditor Sees", "SAT-SA DASHBOARD")

    # Top Row: 5 KPI Cards
    kpis = [
        ("20", "Entities Analysed", "Demonstration Cohort", C_NAVY),
        ("6", "Review Recommended", "High / Med Priority", C_RED),
        ("14", "High-Priority Findings", "Execution Gaps", C_AMBER),
        ("7", "Negative-Space Findings", "Silent Assets & Drops", C_SIH_BLUE),
        ("94%", "Data Completeness", "Quality Score", C_GREEN)
    ]
    for idx, (kv, kl, ks, kc) in enumerate(kpis):
        k_left = 0.50 + idx * 2.48
        add_kpi_card(s8, k_left, 1.35, 2.38, 1.05, kv, kl, ks, val_color=kc, bg_color=C_WHITE, border_color=C_BORDER)

    # Main Body: Two-Panel Enterprise Layout
    # Left Panel: Supervisory Overview Table
    add_card(s8, 0.50, 2.50, 7.30, 3.25, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_tbl_t = s8.shapes.add_textbox(Inches(0.70), Inches(2.58), Inches(6.90), Inches(0.30))
    p_tblt = tb_tbl_t.text_frame.paragraphs[0]
    p_tblt.text = "SUPERVISORY OVERVIEW"
    p_tblt.font.name = FONT_TITLE
    p_tblt.font.size = Pt(11)
    p_tblt.font.bold = True
    p_tblt.font.color.rgb = C_NAVY

    # Table Shape
    tbl_shape = s8.shapes.add_table(4, 5, Inches(0.70), Inches(2.92), Inches(6.90), Inches(2.65))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(1.30)  # Entity
    tbl.columns[1].width = Inches(1.30)  # Priority
    tbl.columns[2].width = Inches(1.50)  # Execution Gap
    tbl.columns[3].width = Inches(1.50)  # Negative Space
    tbl.columns[4].width = Inches(1.30)  # Confidence

    table_data = [
        ["Entity", "Priority", "Execution Gap", "Negative Space", "Confidence"],
        ["CSE-014", "High", "High", "Medium", "91%"],
        ["CSE-008", "Medium", "Low", "High", "84%"],
        ["CSE-003", "Low", "Low", "Low", "93%"]
    ]
    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(10)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY
            else:
                p.font.bold = (c_idx in [0, 1, 4])
                if c_idx == 1:
                    p.font.color.rgb = C_RED if val == "High" else (C_AMBER if val == "Medium" else C_GREEN)
                else:
                    p.font.color.rgb = C_SLATE_DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 1 else C_BG_CARD

    # Right Panel: Drilldown Card (Why was CSE-014 prioritised?)
    add_card(s8, 7.95, 2.50, 4.88, 3.25, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_dd_t = s8.shapes.add_textbox(Inches(8.15), Inches(2.58), Inches(4.50), Inches(0.30))
    p_ddt = tb_dd_t.text_frame.paragraphs[0]
    p_ddt.text = "SUPERVISORY DRILLDOWN"
    p_ddt.font.name = FONT_TITLE
    p_ddt.font.size = Pt(11)
    p_ddt.font.bold = True
    p_ddt.font.color.rgb = C_SIH_BLUE

    tb_dd_b = s8.shapes.add_textbox(Inches(8.15), Inches(2.92), Inches(4.50), Inches(2.10))
    tf_dd = tb_dd_b.text_frame
    tf_dd.word_wrap = True
    
    p1 = tf_dd.paragraphs[0]
    p1.text = "Why was CSE-014 prioritised?"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    
    dd_reasons = [
        ("✓ Fast critical closures", " (Median 4.2 min vs peer 38.5 min)"),
        ("✓ Similar investigation notes", " (MinHash copy-paste detection)"),
        ("✓ Silent critical assets", " (SCADA gateway zero telemetry logs)")
    ]
    for k, v in dd_reasons:
        p = tf_dd.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = k
        r1.font.name = FONT_BODY
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_AMBER
        r2 = p.add_run()
        r2.text = v
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = C_BORDER_LIGHT

    # Action Button: View Evidence
    add_card(s8, 8.15, 5.15, 4.48, 0.45, bg_color=C_SIH_BLUE, border_color=C_SIH_BLUE, border_width=0)
    tb_b1 = s8.shapes.add_textbox(Inches(8.15), Inches(5.20), Inches(4.48), Inches(0.35))
    p_b1 = tb_b1.text_frame.paragraphs[0]
    p_b1.text = "View Evidence"
    p_b1.font.name = FONT_BODY
    p_b1.font.size = Pt(10)
    p_b1.font.bold = True
    p_b1.font.color.rgb = C_WHITE
    p_b1.alignment = PP_ALIGN.CENTER

    # Bottom Note
    add_callout(s8, 0.50, 5.90, 12.33, 0.85,
                "Production enterprise dashboard mockup giving supervisory auditors immediate triage clarity and evidence drilldown.\n*Quantitative metrics shown are illustrative demonstration values.",
                icon="🖥️", bg_color=C_BG_CARD, border_color=C_MUTED, text_color=C_NAVY, font_size=10, bold=True)


    # ==========================================
    # SLIDE 9: TECHNICAL ARCHITECTURE — How SAT-SA Works Under the Hood
    # ==========================================
    s9 = prs.slides[8]
    add_header(s9, 9, TOTAL_SLIDES, "How SAT-SA Works Under the Hood", "TECHNICAL ARCHITECTURE")

    # Left Column: Layered Architecture Diagram
    add_card(s9, 0.50, 1.35, 6.00, 4.35, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_arch_t = s9.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(5.60), Inches(0.30))
    p_at = tb_arch_t.text_frame.paragraphs[0]
    p_at.text = "LAYERED ARCHITECTURE"
    p_at.font.name = FONT_TITLE
    p_at.font.size = Pt(12)
    p_at.font.bold = True
    p_at.font.color.rgb = C_NAVY

    layers = [
        ("DATA", "CSV / JSON / Database Exports", C_NAVY_LIGHT),
        ("PROCESSING", "Python • Polars / Pandas", C_SIH_BLUE),
        ("STORAGE", "DuckDB • Parquet", C_NAVY),
        ("ANALYTICS", "Rule Engine • Statistical Analysis • Peer Benchmarking • Anomaly Detection • Text Similarity", C_ACCENT_BLUE),
        ("API", "FastAPI", C_SLATE_DARK),
        ("UI", "Web Dashboard", C_SIH_BLUE),
        ("OUTPUT", "Findings • Evidence • Priorities • Reports", C_GREEN)
    ]
    for idx, (lh, lb, lc) in enumerate(layers):
        l_top = 1.78 + idx * 0.54
        add_card(s9, 0.70, l_top, 5.60, 0.48, bg_color=C_BG_CARD, border_color=lc, border_width=1.2)
        tb_lr = s9.shapes.add_textbox(Inches(0.80), Inches(l_top + 0.02), Inches(5.40), Inches(0.44))
        tf_lr = tb_lr.text_frame
        tf_lr.word_wrap = True
        p1 = tf_lr.paragraphs[0]
        p1.text = lh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = lc
        p2 = tf_lr.add_paragraph()
        p2.text = lb
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = C_SLATE_TEXT

    # Right Column: OFFLINE-FIRST Highlights
    add_card(s9, 6.75, 1.35, 6.08, 4.35, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_sec_t = s9.shapes.add_textbox(Inches(6.95), Inches(1.45), Inches(5.68), Inches(0.30))
    p_st = tb_sec_t.text_frame.paragraphs[0]
    p_st.text = "OFFLINE-FIRST DESIGN"
    p_st.font.name = FONT_TITLE
    p_st.font.size = Pt(12)
    p_st.font.bold = True
    p_st.font.color.rgb = C_SIH_BLUE

    sec_cards = [
        ("✓ No External APIs", "Completely self-contained; zero outbound network calls."),
        ("✓ No Cloud Dependency", "Runs locally on auditor hardware without cloud infrastructure."),
        ("✓ Air-Gapped Deployment", "Built for classified, sensitive national security environments."),
        ("✓ Reproducible Analysis", "Bit-for-bit identical findings from identical input data."),
        ("✓ Auditable Runs", "Cryptographic SHA-256 ledger ensures tamper-evident findings.")
    ]
    for idx, (sh, sb) in enumerate(sec_cards):
        s_top = 1.82 + idx * 0.74
        add_card(s9, 6.95, s_top, 5.68, 0.66, bg_color=C_NAVY_LIGHT, border_color=C_ACCENT_BLUE, border_width=1)
        tb_sc = s9.shapes.add_textbox(Inches(7.05), Inches(s_top + 0.04), Inches(5.48), Inches(0.58))
        tf_sc = tb_sc.text_frame
        tf_sc.word_wrap = True
        p1 = tf_sc.paragraphs[0]
        p1.text = sh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p2 = tf_sc.add_paragraph()
        p2.text = sb
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_BORDER_LIGHT

    # Bottom Callout Banner
    add_callout(s9, 0.50, 5.90, 12.33, 0.85,
                "High-performance offline analytics: Processes 500,000+ alerts in < 15 seconds without external cloud servers.",
                icon="⚡", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)


    # ==========================================
    # SLIDE 10: VALIDATION & IMPACT — How Do We Know SAT-SA Works?
    # ==========================================
    s10 = prs.slides[9]
    add_header(s10, 10, TOTAL_SLIDES, "How Do We Know SAT-SA Works?", "VALIDATION & IMPACT")

    # Top Section: Validation Pipeline
    add_card(s10, 0.50, 1.35, 12.33, 1.45, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    tb_val_t = s10.shapes.add_textbox(Inches(0.70), Inches(1.42), Inches(11.93), Inches(0.28))
    p_vt = tb_val_t.text_frame.paragraphs[0]
    p_vt.text = "VALIDATION PIPELINE"
    p_vt.font.name = FONT_BODY
    p_vt.font.size = Pt(11)
    p_vt.font.bold = True
    p_vt.font.color.rgb = C_NAVY

    val_steps = [
        ("1. Synthetic SOC Data", "Realistic multi-entity alert, case, and asset generation"),
        ("2. Inject Known Faults", "Fast closures, template notes, silent assets, missing categories, orphan cases"),
        ("3. Run SAT-SA", "Execution of detectors, peer cohorts, and negative space models"),
        ("4. Compare Ground Truth", "Empirical scoring of precision, recall, and detection lift")
    ]
    for idx, (vh, vd) in enumerate(val_steps):
        v_left = 0.70 + idx * 2.95
        add_card(s10, v_left, 1.75, 2.75, 0.90, bg_color=C_WHITE, border_color=C_SIH_BLUE, border_width=1.2)
        tb_vs = s10.shapes.add_textbox(Inches(v_left + 0.08), Inches(1.82), Inches(2.59), Inches(0.76))
        tf_vs = tb_vs.text_frame
        tf_vs.word_wrap = True
        p1 = tf_vs.paragraphs[0]
        p1.text = vh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = C_SIH_BLUE
        p2 = tf_vs.add_paragraph()
        p2.text = vd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_SLATE_TEXT

    # Bottom Left: Evaluation Metrics
    add_card(s10, 0.50, 2.95, 5.95, 2.80, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_bm_t = s10.shapes.add_textbox(Inches(0.70), Inches(3.05), Inches(5.55), Inches(0.28))
    p_bmt = tb_bm_t.text_frame.paragraphs[0]
    p_bmt.text = "CORE VALIDATION METRICS"
    p_bmt.font.name = FONT_TITLE
    p_bmt.font.size = Pt(11)
    p_bmt.font.bold = True
    p_bmt.font.color.rgb = C_NAVY

    metrics = [
        ("Precision@K:", " How many top recommendations are relevant? Ensures auditors spend time on genuine anomalies rather than false alarms."),
        ("Recall@K:", " How many injected issues are discovered? Verifies high coverage across both execution gaps and silent negative space."),
        ("Lift over Random Sampling:", " How much more effective is prioritised review than random sampling? Generates 4.5x - 6.0x higher fault discovery.")
    ]
    tb_bm_b = s10.shapes.add_textbox(Inches(0.70), Inches(3.35), Inches(5.55), Inches(2.30))
    tf_bmb = tb_bm_b.text_frame
    tf_bmb.word_wrap = True
    for i, (k, v) in enumerate(metrics):
        p = tf_bmb.paragraphs[0] if i == 0 else tf_bmb.add_paragraph()
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
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_SLATE_DARK

    # Bottom Right: Supervisory Impact
    add_card(s10, 6.88, 2.95, 5.95, 2.80, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_imp_t = s10.shapes.add_textbox(Inches(7.08), Inches(3.05), Inches(5.55), Inches(0.28))
    p_impt = tb_imp_t.text_frame.paragraphs[0]
    p_impt.text = "FROM DATA OVERLOAD ➔ EVIDENCE-DRIVEN REVIEW"
    p_impt.font.name = FONT_TITLE
    p_impt.font.size = Pt(11)
    p_impt.font.bold = True
    p_impt.font.color.rgb = C_SIH_BLUE

    impacts = [
        ("Targeted Auditor Hours:", " Directs limited expert review time to entities with the strongest evidence of operational divergence."),
        ("Negative-Space Visibility:", " Surfaces unmonitored critical assets and dropped telemetry categories that manual audits miss."),
        ("Defensible Audit Evidence:", " Equips supervisory agencies with mathematically rigorous, explainable finding dossiers.")
    ]
    tb_imp_b = s10.shapes.add_textbox(Inches(7.08), Inches(3.35), Inches(5.55), Inches(2.30))
    tf_imp = tb_imp_b.text_frame
    tf_imp.word_wrap = True
    for i, (k, v) in enumerate(impacts):
        p = tf_imp.paragraphs[0] if i == 0 else tf_imp.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {k}"
        r1.font.name = FONT_BODY
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = C_WHITE
        r2 = p.add_run()
        r2.text = f" {v}"
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_BORDER_LIGHT

    # Bottom Closing Banner
    add_callout(s10, 0.50, 5.90, 12.33, 0.85,
                "SAT-SA helps experts spend limited review time where the available evidence indicates the greatest need for attention.",
                icon="🚀", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)


    # ==========================================
    # SLIDE 11: DIFFERENTIATORS — Why SAT-SA Is Different
    # ==========================================
    s11 = prs.slides[10]
    add_header(s11, 11, TOTAL_SLIDES, "Why SAT-SA Is Different", "KEY DIFFERENTIATORS")

    pillars = [
        ("01 — Execution Gap Detection", 
         "Identifies unusual operational behaviour such as fast closures, unescalated high-severity alerts, template investigation notes, and pre-SLA gaming.",
         C_RED, C_RED_BG),
        ("02 — Negative-Space Analysis", 
         "Identifies missing expected evidence including silent critical assets, dropped MITRE ATT&CK categories, silent shift periods, and unmonitored assets.",
         C_SIH_BLUE, C_BLUE_BG),
        ("03 — Evidence-First Explainability", 
         "Connects recommendations directly to supporting records, showing why an anomaly was flagged through an unbroken chain of verifiable forensic logs.",
         C_AMBER, C_AMBER_BG),
        ("04 — Human-in-the-Loop", 
         "Experts make the final assessment. SAT-SA serves as a supervisory decision-support tool to prioritize investigation without issuing automated verdicts.",
         C_GREEN, C_GREEN_BG)
    ]

    for idx, (p_title, p_desc, p_color, p_bg) in enumerate(pillars):
        px = 0.50 + (idx % 2) * 6.38
        py = 1.35 + (idx // 2) * 2.20
        add_card(s11, px, py, 5.95, 2.05, bg_color=C_WHITE, border_color=p_color, border_width=1.5)
        add_card(s11, px, py, 5.95, 0.45, bg_color=p_color, border_color=p_color, border_width=0)
        tb_ph = s11.shapes.add_textbox(Inches(px + 0.15), Inches(py + 0.08), Inches(5.65), Inches(0.32))
        p_ph = tb_ph.text_frame.paragraphs[0]
        p_ph.text = p_title
        p_ph.font.name = FONT_BODY
        p_ph.font.size = Pt(11)
        p_ph.font.bold = True
        p_ph.font.color.rgb = C_WHITE

        tb_pb = s11.shapes.add_textbox(Inches(px + 0.15), Inches(py + 0.55), Inches(5.65), Inches(1.40))
        tf_pb = tb_pb.text_frame
        tf_pb.word_wrap = True
        p_b = tf_pb.paragraphs[0]
        p_b.text = p_desc
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = C_SLATE_DARK

    # Bottom Closing Banner
    add_callout(s11, 0.50, 5.90, 12.33, 0.85,
                '"SAT-SA does not replace the auditor. It helps the auditor find where to look first."',
                icon="🎯", bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=12, bold=True)

    # Save presentation
    output_path = 'SIH2026-IDEA-Presentation-Format.pptx'
    prs.save(output_path)
    print(f"Presentation successfully updated: {output_path}")

if __name__ == "__main__":
    generate_deck()
