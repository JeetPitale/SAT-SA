"""
SAT-SA: Official Smart India Hackathon (SIH) 2026 Presentation & PDF Generator
Problem Statement ID: 26157
Problem Statement Title: Supervisory Analytics Tool for SOC Assessment
Theme: Blockchain & Cybersecurity | Category: Software (Offline / Air-Gapped)

Generates:
1. SAT-SA_SIH2026_FINAL.pptx / SAT-SA_SIH2026_Final.pptx (Editable PPTX using the official 6-slide SIH template)
2. SAT-SA_SIH2026_FINAL.pdf / SAT-SA_SIH2026_Final.pdf (Official 6-page submission PDF)
"""

import os
import sys
import shutil
from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# ReportLab for PDF generation
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# -------------------------------------------------------------------------
# CONSTANTS & PALETTE
# -------------------------------------------------------------------------
C_NAVY_DARK = RGBColor(10, 25, 47)       # #0A192F (Deep Navy)
C_NAVY = RGBColor(15, 30, 60)            # #0F1E3C (Primary Navy)
C_NAVY_LIGHT = RGBColor(24, 43, 73)      # #182B49 (Surface Navy)
C_SIH_BLUE = RGBColor(0, 112, 192)       # #0070C0 (Official SIH Blue)
C_ACCENT_BLUE = RGBColor(2, 132, 199)    # #0284C7 (Cyan Blue)
C_SLATE_DARK = RGBColor(30, 41, 59)      # #1E293B (Dark Slate)
C_SLATE_TEXT = RGBColor(51, 65, 85)      # #334155 (Body Text)
C_MUTED = RGBColor(100, 116, 139)        # #64748B (Muted Text)
C_BG_CARD = RGBColor(241, 245, 249)      # #F1F5F9 (Light Card)
C_BORDER = RGBColor(203, 213, 225)       # #CBD5E1 (Border)
C_BORDER_LIGHT = RGBColor(226, 232, 240) # #E2E8F0 (Soft Border)
C_WHITE = RGBColor(255, 255, 255)
C_AMBER = RGBColor(217, 119, 6)          # #D97706 (Warning Amber)
C_AMBER_BG = RGBColor(254, 243, 199)     # #FEF3C7 (Amber Container)
C_RED = RGBColor(220, 38, 38)            # #DC2626 (Critical Red)
C_RED_BG = RGBColor(254, 226, 226)       # #FEE2E2 (Red Container)
C_GREEN = RGBColor(5, 150, 105)          # #059669 (Healthy Green)
C_GREEN_BG = RGBColor(209, 250, 229)     # #D1FAE5 (Green Container)
C_BLUE_BG = RGBColor(224, 242, 254)      # #E0F2FE (Blue Container)

FONT_TITLE = "Arial"
FONT_BODY = "Arial"
FONT_SERIF = "Times New Roman"

def set_shape_style(shape, fill_color, border_color=None, border_width=1):
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()

def add_header(slide, slide_num, total_slides, sih_title, subhead=""):
    logo_path = 'scratch/template_images/slide2_Picture 10_3.png'
    if os.path.exists(logo_path):
        slide.shapes.add_picture(logo_path, Inches(10.70), Inches(0.00), width=Inches(2.46), height=Inches(1.16))
    
    # Top-left Pill
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
    
    # Header Title
    title_box = slide.shapes.add_textbox(Inches(0.50), Inches(0.55), Inches(10.00), Inches(0.68))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    
    p_title = tf_title.paragraphs[0]
    p_title.text = sih_title
    p_title.font.name = FONT_SERIF
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = C_NAVY

    if subhead:
        p_sub = tf_title.add_paragraph()
        p_sub.text = subhead
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(10.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_SIH_BLUE

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

def add_callout(slide, left, top, width, height, text, bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True):
    box = add_card(slide, left, top, width, height, bg_color, border_color, border_width=1.5)
    tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.08), Inches(width - 0.30), Inches(height - 0.16))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = FONT_BODY
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = text_color
    p.alignment = PP_ALIGN.CENTER
    return box

def add_down_arrow(slide, left, top, width=0.22, height=0.22, color=C_SIH_BLUE):
    shape = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(left), Inches(top), Inches(width), Inches(height))
    set_shape_style(shape, color, None)
    return shape

# =========================================================================
# PPTX BUILDER
# =========================================================================
def build_pptx():
    template_path = 'SIH2026-IDEA-Presentation-Format.backup.pptx'
    prs = Presentation(template_path)
    blank_layout = prs.slide_layouts[6]
    
    TOTAL_SLIDES = 6
    
    # Trim to exactly 6 slides (Deleting Slide 7 Important Instructions)
    while len(prs.slides) > TOTAL_SLIDES:
        rId = prs.slides._sldIdLst[6].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[6]
        
    while len(prs.slides) < TOTAL_SLIDES:
        prs.slides.add_slide(blank_layout)

    # Clear all existing shapes on all 6 slides to guarantee 0 overlapping artifacts
    for slide in prs.slides:
        for s in list(slide.shapes):
            sp = s._element
            sp.getparent().remove(sp)

    # =========================================================================
    # SLIDE 1: TITLE PAGE (Simplified Clean Official Template Layout)
    # =========================================================================
    s1 = prs.slides[0]
    logo_path = 'scratch/template_images/slide1_Picture 1_2.png'
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(10.70), Inches(0.00), width=Inches(2.46), height=Inches(1.16))
    
    tb_top = s1.shapes.add_textbox(Inches(0.50), Inches(0.18), Inches(9.50), Inches(0.40))
    p_tt = tb_top.text_frame.paragraphs[0]
    p_tt.text = "SMART INDIA HACKATHON 2026"
    p_tt.font.name = FONT_SERIF
    p_tt.font.size = Pt(20)
    p_tt.font.bold = True
    p_tt.font.color.rgb = C_SIH_BLUE

    tb_sub = s1.shapes.add_textbox(Inches(0.50), Inches(0.55), Inches(9.50), Inches(0.35))
    p_sub = tb_sub.text_frame.paragraphs[0]
    p_sub.text = "TITLE PAGE"
    p_sub.font.name = FONT_SERIF
    p_sub.font.size = Pt(13)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_NAVY

    # Hero Title Box
    tb_title = s1.shapes.add_textbox(Inches(0.50), Inches(1.05), Inches(12.33), Inches(1.20))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    
    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "SAT-SA: Security Audit & Supervisory Analytics"
    p_t1.font.name = FONT_TITLE
    p_t1.font.size = Pt(25)
    p_t1.font.bold = True
    p_t1.font.color.rgb = C_NAVY

    p_t2 = tf_t.add_paragraph()
    p_t2.text = "Turning SOC Records into Actionable Audit Evidence"
    p_t2.font.name = FONT_BODY
    p_t2.font.size = Pt(13.5)
    p_t2.font.bold = True
    p_t2.font.color.rgb = C_SIH_BLUE

    # Main Metadata Box (Clean 2-Column Official SIH Form)
    add_card(s1, 0.50, 2.35, 12.33, 2.30, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    
    # Left Column Fields
    tb_m_left = s1.shapes.add_textbox(Inches(0.80), Inches(2.55), Inches(5.60), Inches(1.90))
    tf_ml = tb_m_left.text_frame
    tf_ml.word_wrap = True
    
    left_items = [
        ("Problem Statement ID –", " 26157 (SIH26157)"),
        ("Problem Statement Title –", " Supervisory Analytics Tool for SOC Assessment"),
        ("Theme –", " Blockchain & Cybersecurity")
    ]
    for i, (k, v) in enumerate(left_items):
        p = tf_ml.paragraphs[0] if i == 0 else tf_ml.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = k
        r1.font.name = FONT_BODY
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = f" {v}"
        r2.font.name = FONT_BODY
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_SLATE_TEXT

    # Right Column Fields
    tb_m_right = s1.shapes.add_textbox(Inches(6.80), Inches(2.55), Inches(5.70), Inches(1.90))
    tf_mr = tb_m_right.text_frame
    tf_mr.word_wrap = True
    
    right_items = [
        ("PS Category –", " Software (Offline / Air-Gapped)"),
        ("Team ID –", " SIH26157_TEAM"),
        ("Team Name –", " SAT-SA Analytics (Registered on portal)")
    ]
    for i, (k, v) in enumerate(right_items):
        p = tf_mr.paragraphs[0] if i == 0 else tf_mr.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = k
        r1.font.name = FONT_BODY
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = f" {v}"
        r2.font.name = FONT_BODY
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_SLATE_TEXT

    # Sub-card: Solution Role & Architecture Summary
    add_card(s1, 0.50, 4.80, 12.33, 0.95, bg_color=C_WHITE, border_color=C_BORDER, border_width=1)
    tb_role = s1.shapes.add_textbox(Inches(0.70), Inches(4.88), Inches(11.93), Inches(0.80))
    tf_role = tb_role.text_frame
    tf_role.word_wrap = True
    p_r1 = tf_role.paragraphs[0]
    p_r1.text = "SOLUTION SCOPE & HUMAN-IN-THE-LOOP AUDIT OBJECTIVE"
    p_r1.font.name = FONT_BODY
    p_r1.font.size = Pt(9.5)
    p_r1.font.bold = True
    p_r1.font.color.rgb = C_SIH_BLUE
    p_r2 = tf_role.add_paragraph()
    p_r2.text = "An offline supervisory analytics tool that evaluates SOC records, detects behavioural anomalies, execution gaps, and missing evidence, and prioritises high-risk entities to assist human auditors."
    p_r2.font.name = FONT_BODY
    p_r2.font.size = Pt(9.5)
    p_r2.font.color.rgb = C_SLATE_DARK

    # Bottom Callout at Slide 1
    add_callout(s1, 0.50, 5.95, 12.33, 0.80, 
                "Offline-First Supervisory Analytics & Review Prioritisation for Critical Sector Security Operations Centers\nHuman-in-the-loop decision support enabling defensible, evidence-backed supervisory investigations.",
                bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=10.5, bold=True)

    ribbon1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.00), Inches(6.95), Inches(13.333), Inches(0.55))
    set_shape_style(ribbon1, C_SIH_BLUE, None)
    foot_s1 = s1.shapes.add_textbox(Inches(0.50), Inches(7.02), Inches(12.33), Inches(0.40))
    p_fs1 = foot_s1.text_frame.paragraphs[0]
    p_fs1.text = "SIH 2026 | Problem Statement 26157 | SAT-SA: Security Audit & Supervisory Analytics | Slide 1 of 6"
    p_fs1.font.name = FONT_BODY
    p_fs1.font.size = Pt(11)
    p_fs1.font.color.rgb = C_WHITE
    p_fs1.alignment = PP_ALIGN.CENTER


    # =========================================================================
    # SLIDE 2: IDEA TITLE / PROPOSED SOLUTION (3-Part Layout)
    # =========================================================================
    s2 = prs.slides[1]
    add_header(s2, 2, TOTAL_SLIDES, "IDEA TITLE", "SAT-SA: Security Audit & Supervisory Analytics")

    # Column 1: THE PROBLEM
    add_card(s2, 0.50, 1.35, 3.80, 4.45, bg_color=C_WHITE, border_color=C_RED, border_width=1.5)
    tb_p_h = s2.shapes.add_textbox(Inches(0.65), Inches(1.45), Inches(3.50), Inches(0.30))
    p_ph = tb_p_h.text_frame.paragraphs[0]
    p_ph.text = "1. THE PROBLEM"
    p_ph.font.name = FONT_TITLE
    p_ph.font.size = Pt(11)
    p_ph.font.bold = True
    p_ph.font.color.rgb = C_RED

    prob_cards = [
        ("High Data Volume", "SOCs generate millions of alerts, cases, closures, and asset records."),
        ("Limited Expert Review Capacity", "Large SOC datasets make exhaustive manual review difficult."),
        ("Missing Evidence", "Silent critical assets & dropped logs produce zero events to sample.")
    ]
    for idx, (ph, pd) in enumerate(prob_cards):
        p_top = 1.85 + idx * 1.00
        add_card(s2, 0.65, p_top, 3.50, 0.85, bg_color=C_RED_BG, border_color=C_RED, border_width=1)
        tb_p = s2.shapes.add_textbox(Inches(0.75), Inches(p_top + 0.05), Inches(3.30), Inches(0.75))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        p1 = tf_p.paragraphs[0]
        p1.text = ph
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_RED
        p2 = tf_p.add_paragraph()
        p2.text = pd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_SLATE_TEXT

    # Column 2: OUR SOLUTION
    add_card(s2, 4.50, 1.35, 4.33, 4.45, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_s_h = s2.shapes.add_textbox(Inches(4.65), Inches(1.45), Inches(4.03), Inches(0.30))
    p_sh = tb_s_h.text_frame.paragraphs[0]
    p_sh.text = "2. OUR PROPOSED SOLUTION"
    p_sh.font.name = FONT_TITLE
    p_sh.font.size = Pt(11)
    p_sh.font.bold = True
    p_sh.font.color.rgb = C_SIH_BLUE

    sol_nodes = [
        ("SOC Records", "Historical Alerts, Cases, Assets", C_NAVY_LIGHT),
        ("SAT-SA Analytics Engine", "• Rule Analysis  • Statistics (EB)\n• Peer Cohorts  • Anomaly ML", C_SIH_BLUE),
        ("Review Priorities", "Prioritised Entities & Findings", C_AMBER),
        ("Human Expert Auditor", "Targeted Forensic Investigation", C_GREEN)
    ]
    for idx, (sh, sd, sc) in enumerate(sol_nodes):
        s_top = 1.85 + idx * 0.90
        s_hgt = 0.70 if idx == 1 else 0.55
        add_card(s2, 4.65, s_top, 4.03, s_hgt, bg_color=sc if sc != C_NAVY_LIGHT else C_NAVY_LIGHT, border_color=C_ACCENT_BLUE if sc == C_NAVY_LIGHT else sc, border_width=1)
        tb_s = s2.shapes.add_textbox(Inches(4.75), Inches(s_top + 0.04), Inches(3.83), Inches(s_hgt - 0.08))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        p1 = tf_s.paragraphs[0]
        p1.text = sh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE if sc in [C_NAVY_LIGHT, C_SIH_BLUE, C_GREEN] else C_NAVY
        p2 = tf_s.add_paragraph()
        p2.text = sd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = C_BORDER_LIGHT if sc in [C_NAVY_LIGHT, C_SIH_BLUE, C_GREEN] else C_SLATE_DARK
        if idx < 3:
            add_down_arrow(s2, 6.55, s_top + s_hgt + 0.02, width=0.15, height=0.12, color=C_SIH_BLUE)

    # Column 3: INNOVATION
    add_card(s2, 9.03, 1.35, 3.80, 4.45, bg_color=C_WHITE, border_color=C_SIH_BLUE, border_width=1.5)
    tb_i_h = s2.shapes.add_textbox(Inches(9.18), Inches(1.45), Inches(3.50), Inches(0.30))
    p_ih = tb_i_h.text_frame.paragraphs[0]
    p_ih.text = "3. INNOVATION & UNIQUENESS"
    p_ih.font.name = FONT_TITLE
    p_ih.font.size = Pt(11)
    p_ih.font.bold = True
    p_ih.font.color.rgb = C_SIH_BLUE

    innov_cards = [
        ("01 — EXECUTION GAPS", "Evidence exists, but behaviour appears unusual (e.g. 4s fast closures, template notes).", C_RED_BG, C_RED),
        ("02 — NEGATIVE SPACE", "Expected evidence is missing or unexpectedly sparse (e.g. silent SCADA assets, blackout shifts).", C_BLUE_BG, C_SIH_BLUE),
        ("03 — EVIDENCE TRAIL", "Every recommendation links to an unbroken chain of verifiable raw records.", C_GREEN_BG, C_GREEN)
    ]
    for idx, (ih, idesc, i_bg, i_col) in enumerate(innov_cards):
        i_top = 1.85 + idx * 1.00
        add_card(s2, 9.18, i_top, 3.50, 0.85, bg_color=i_bg, border_color=i_col, border_width=1)
        tb_i = s2.shapes.add_textbox(Inches(9.28), Inches(i_top + 0.05), Inches(3.30), Inches(0.75))
        tf_i = tb_i.text_frame
        tf_i.word_wrap = True
        p1 = tf_i.paragraphs[0]
        p1.text = ih
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = i_col
        p2 = tf_i.add_paragraph()
        p2.text = idesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_SLATE_TEXT

    # Bottom Callout Banner
    add_callout(s2, 0.50, 5.90, 12.33, 0.85,
                '"SAT-SA analyses not only what exists — but also what should exist."\nIdentifies where expert review should focus without replacing the human investigator.',
                bg_color=C_BG_CARD, border_color=C_NAVY, text_color=C_NAVY, font_size=11, bold=True)


    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH (Workflow, Detection Engine & Tech Stack)
    # =========================================================================
    s3 = prs.slides[2]
    add_header(s3, 3, TOTAL_SLIDES, "TECHNICAL APPROACH", "Methodology, Workflow & Detection Engine")

    # Top: System Workflow Bar
    add_card(s3, 0.50, 1.35, 12.33, 0.70, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_wf_t = s3.shapes.add_textbox(Inches(0.65), Inches(1.38), Inches(12.03), Inches(0.25))
    p_wft = tb_wf_t.text_frame.paragraphs[0]
    p_wft.text = "COMPLETE SYSTEM WORKFLOW PIPELINE"
    p_wft.font.name = FONT_BODY
    p_wft.font.size = Pt(9.0)
    p_wft.font.bold = True
    p_wft.font.color.rgb = C_SIH_BLUE

    pipe_steps_s3 = ["DATA INPUT", "NORMALISATION", "FEATURE EXTRACTION", "DETECTION ENGINE", "PRIORITISATION", "EVIDENCE TRAIL", "HUMAN REVIEW"]
    for idx, ps in enumerate(pipe_steps_s3):
        p_left = 0.65 + idx * 1.73
        add_card(s3, p_left, 1.62, 1.62, 0.35, bg_color=C_NAVY_LIGHT, border_color=C_ACCENT_BLUE, border_width=1)
        tb_ps = s3.shapes.add_textbox(Inches(p_left), Inches(1.65), Inches(1.62), Inches(0.30))
        p = tb_ps.text_frame.paragraphs[0]
        p.text = ps
        p.font.name = FONT_BODY
        p.font.size = Pt(8.0)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

    # Middle Left: Data Input & Detection Engine
    add_card(s3, 0.50, 2.15, 6.00, 2.70, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_de_t = s3.shapes.add_textbox(Inches(0.65), Inches(2.22), Inches(5.70), Inches(0.25))
    p_det = tb_de_t.text_frame.paragraphs[0]
    p_det.text = "DATA INPUT & DETECTION ENGINE"
    p_det.font.name = FONT_TITLE
    p_det.font.size = Pt(10.5)
    p_det.font.bold = True
    p_det.font.color.rgb = C_NAVY

    tb_de_b = s3.shapes.add_textbox(Inches(0.65), Inches(2.50), Inches(5.70), Inches(2.25))
    tf_deb = tb_de_b.text_frame
    tf_deb.word_wrap = True
    
    de_points = [
        ("• Ingestion Sources:", " CSV | JSON | DB Exports (Alerts, Cases, Closures, Assets, Telemetry)"),
        ("• 4 Parallel Analytics Branches:", " Rules • Statistical Analysis (EB) • Peer Benchmarks • Anomaly ML"),
        ("• Dual-Paradigm Output:", " Splits into Execution Gaps (Faulty actions) + Negative Space (Omissions)")
    ]
    for i, (k, v) in enumerate(de_points):
        p = tf_deb.paragraphs[0] if i == 0 else tf_deb.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = k
        r1.font.name = FONT_BODY
        r1.font.size = Pt(9.0)
        r1.font.bold = True
        r1.font.color.rgb = C_SIH_BLUE
        r2 = p.add_run()
        r2.text = f" {v}"
        r2.font.name = FONT_BODY
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = C_SLATE_DARK

    # Middle Right: Visual Mini-Demos
    add_card(s3, 6.70, 2.15, 6.13, 2.70, bg_color=C_BG_CARD, border_color=C_BORDER, border_width=1.5)
    
    add_card(s3, 6.85, 2.25, 5.83, 1.15, bg_color=C_RED_BG, border_color=C_RED, border_width=1)
    tb_md1 = s3.shapes.add_textbox(Inches(6.95), Inches(2.28), Inches(5.63), Inches(1.05))
    tf_m1 = tb_md1.text_frame
    tf_m1.word_wrap = True
    p1 = tf_m1.paragraphs[0]
    p1.text = "EXECUTION GAP VISUAL (Alert A-19283)"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.0)
    p1.font.bold = True
    p1.font.color.rgb = C_RED
    p2 = tf_m1.add_paragraph()
    p2.text = "Opened: 10:02:15  ➔  Closed: 10:02:19  |  Duration: 4 seconds"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.0)
    p2.font.bold = True
    p2.font.color.rgb = C_NAVY
    p3 = tf_m1.add_paragraph()
    p3.text = "Significant Peer Deviation  ➔  [ Review Recommended ]"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(8.5)
    p3.font.bold = True
    p3.font.color.rgb = C_RED

    add_card(s3, 6.85, 3.55, 5.83, 1.15, bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, border_width=1)
    tb_md2 = s3.shapes.add_textbox(Inches(6.95), Inches(3.58), Inches(5.63), Inches(1.05))
    tf_m2 = tb_md2.text_frame
    tf_m2.word_wrap = True
    p1 = tf_m2.paragraphs[0]
    p1.text = "NEGATIVE SPACE VISUAL (Critical SCADA Gateways)"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.0)
    p1.font.bold = True
    p1.font.color.rgb = C_SIH_BLUE
    p2 = tf_m2.add_paragraph()
    p2.text = "Expected: ████████████████████ (Baseline Activity)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8.0)
    p2.font.color.rgb = C_SLATE_TEXT
    p3 = tf_m2.add_paragraph()
    p3.text = "Observed: ██████ (Low Telemetry)  ➔  [ Potential Coverage Gap ]"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(8.5)
    p3.font.bold = True
    p3.font.color.rgb = C_AMBER

    # Bottom Tech Stack
    add_card(s3, 0.50, 4.95, 12.33, 0.85, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_tech = s3.shapes.add_textbox(Inches(0.65), Inches(5.00), Inches(12.03), Inches(0.75))
    tf_tech = tb_tech.text_frame
    tf_tech.word_wrap = True
    p_t1 = tf_tech.paragraphs[0]
    p_t1.text = "TECHNOLOGY STACK & OFFLINE-FIRST ARCHITECTURE"
    p_t1.font.name = FONT_BODY
    p_t1.font.size = Pt(9.0)
    p_t1.font.bold = True
    p_t1.font.color.rgb = C_SIH_BLUE
    
    p_t2 = tf_tech.add_paragraph()
    p_t2.text = "Python 3  •  Pandas  •  DuckDB + Parquet  •  scikit-learn  •  Streamlit / Plotly  •  Pydantic"
    p_t2.font.name = FONT_BODY
    p_t2.font.size = Pt(8.5)
    p_t2.font.bold = True
    p_t2.font.color.rgb = C_WHITE

    p_t3 = tf_tech.add_paragraph()
    p_t3.text = "OFFLINE-FIRST: Air-Gapped • No External Cloud APIs • Tamper-Evident SHA-256 Ledger"
    p_t3.font.name = FONT_BODY
    p_t3.font.size = Pt(8.0)
    p_t3.font.color.rgb = C_AMBER

    # Bottom Callout Banner
    add_callout(s3, 0.50, 5.90, 12.33, 0.85,
                "Designed for high-volume local analytical processing with zero external cloud API dependencies.",
                bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=10.5, bold=True)


    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # =========================================================================
    s4 = prs.slides[3]
    add_header(s4, 4, TOTAL_SLIDES, "FEASIBILITY AND VIABILITY", "Feasibility Analysis & Risk-Mitigation Matrix")

    # Left: Feasibility Cards
    add_card(s4, 0.50, 1.35, 5.00, 4.45, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_fs_t = s4.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(4.60), Inches(0.30))
    p_fst = tb_fs_t.text_frame.paragraphs[0]
    p_fst.text = "FEASIBILITY ANALYSIS"
    p_fst.font.name = FONT_TITLE
    p_fst.font.size = Pt(11)
    p_fst.font.bold = True
    p_fst.font.color.rgb = C_NAVY

    feas_cards = [
        ("OFFLINE DEPLOYMENT", "Works completely without cloud access, external APIs, or outbound network calls in air-gapped environments."),
        ("SCALABLE ANALYTICS", "Columnar storage (DuckDB/Parquet) and vectorized processing easily handle large operational datasets locally."),
        ("MODULAR DETECTORS", "Detector rules, statistics, and anomaly models can be independently updated and verified."),
        ("HUMAN-IN-THE-LOOP", "System prioritises and recommends review; human experts retain absolute assessment authority.")
    ]
    for idx, (fh, fd) in enumerate(feas_cards):
        f_top = 1.85 + idx * 0.95
        add_card(s4, 0.70, f_top, 4.60, 0.82, bg_color=C_BG_CARD, border_color=C_BORDER_LIGHT, border_width=1)
        tb_f = s4.shapes.add_textbox(Inches(0.80), Inches(f_top + 0.05), Inches(4.40), Inches(0.72))
        tf_f = tb_f.text_frame
        tf_f.word_wrap = True
        p1 = tf_f.paragraphs[0]
        p1.text = fh
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY
        p2 = tf_f.add_paragraph()
        p2.text = fd
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = C_SLATE_TEXT

    # Right: Challenges & Mitigation Table
    add_card(s4, 5.70, 1.35, 7.13, 3.25, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_cm_t = s4.shapes.add_textbox(Inches(5.90), Inches(1.45), Inches(6.70), Inches(0.28))
    p_cmt = tb_cm_t.text_frame.paragraphs[0]
    p_cmt.text = "CHALLENGES & SAT-SA MITIGATION STRATEGIES"
    p_cmt.font.name = FONT_TITLE
    p_cmt.font.size = Pt(11)
    p_cmt.font.bold = True
    p_cmt.font.color.rgb = C_NAVY

    tbl_shape = s4.shapes.add_table(6, 2, Inches(5.90), Inches(1.80), Inches(6.73), Inches(2.65))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.60)
    tbl.columns[1].width = Inches(4.13)

    cm_data = [
        ["Potential Challenge", "SAT-SA Mitigation Strategy"],
        ["Incomplete / Missing data", "Automated data-quality gates & schema validation"],
        ["Different CSE data schemas", "Canonical Pydantic schema maps heterogeneous formats"],
        ["Small sample sizes per entity", "Empirical Bayes Poisson-Gamma statistical shrinkage"],
        ["False alarm fatigue", "Context-aware peer benchmarking + human review"],
        ["Adversarial KPI gaming", "Multi-detector diversity + random audit baseline"]
    ]
    for r_idx, row in enumerate(cm_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5 if r_idx > 0 else 9.0)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY
            else:
                p.font.bold = (c_idx == 0)
                p.font.color.rgb = C_NAVY if c_idx == 0 else C_SLATE_DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 1 else C_BG_CARD

    # Right Bottom: Deployment Workflow
    add_card(s4, 5.70, 4.70, 7.13, 1.10, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_dep = s4.shapes.add_textbox(Inches(5.85), Inches(4.75), Inches(6.83), Inches(0.95))
    tf_dep = tb_dep.text_frame
    tf_dep.word_wrap = True
    p1 = tf_dep.paragraphs[0]
    p1.text = "OFFLINE DEPLOYMENT WORKFLOW"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.0)
    p1.font.bold = True
    p1.font.color.rgb = C_SIH_BLUE
    p2 = tf_dep.add_paragraph()
    p2.text = "Offline Dataset  ➔  SAT-SA Engine  ➔  Local DuckDB  ➔  Local Dashboard  ➔  Expert Review"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8.5)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p3 = tf_dep.add_paragraph()
    p3.text = "✓ Zero dependency on external cloud services or Internet connectivity."
    p3.font.name = FONT_BODY
    p3.font.size = Pt(8.0)
    p3.font.color.rgb = C_AMBER

    # Bottom Callout Box
    add_callout(s4, 0.50, 5.90, 12.33, 0.85,
                "Designed for air-gapped deployment and suitable for further validation in supervisory workflows.",
                bg_color=C_GREEN_BG, border_color=C_GREEN, text_color=C_NAVY, font_size=11, bold=True)


    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS
    # =========================================================================
    s5 = prs.slides[4]
    add_header(s5, 5, TOTAL_SLIDES, "IMPACT AND BENEFITS", "Supervisory Transformation & Strategic Value")

    # Left: Transformation Diagram
    add_card(s5, 0.50, 1.35, 5.40, 4.45, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_tr_t = s5.shapes.add_textbox(Inches(0.70), Inches(1.45), Inches(5.00), Inches(0.28))
    p_trt = tb_tr_t.text_frame.paragraphs[0]
    p_trt.text = "SUPERVISORY TRANSFORMATION"
    p_trt.font.name = FONT_TITLE
    p_trt.font.size = Pt(11)
    p_trt.font.bold = True
    p_trt.font.color.rgb = C_NAVY

    add_card(s5, 0.70, 1.80, 5.00, 1.05, bg_color=C_RED_BG, border_color=C_RED, border_width=1)
    tb_td = s5.shapes.add_textbox(Inches(0.80), Inches(1.85), Inches(4.80), Inches(0.95))
    tf_td = tb_td.text_frame
    tf_td.word_wrap = True
    p1 = tf_td.paragraphs[0]
    p1.text = "TODAY: MANUAL DATA OVERLOAD"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.0)
    p1.font.bold = True
    p1.font.color.rgb = C_RED
    p2 = tf_td.add_paragraph()
    p2.text = "Large SOC Dataset  ➔  Manual Sampling  ➔  Limited Review Capacity"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8.0)
    p2.font.color.rgb = C_SLATE_TEXT

    add_card(s5, 1.70, 2.95, 3.00, 0.35, bg_color=C_SIH_BLUE, border_color=C_SIH_BLUE, border_width=0)
    tb_sc = s5.shapes.add_textbox(Inches(1.70), Inches(2.98), Inches(3.00), Inches(0.30))
    p_sc = tb_sc.text_frame.paragraphs[0]
    p_sc.text = "▼  SAT-SA ANALYTICS  ▼"
    p_sc.font.name = FONT_BODY
    p_sc.font.size = Pt(8.5)
    p_sc.font.bold = True
    p_sc.font.color.rgb = C_WHITE
    p_sc.alignment = PP_ALIGN.CENTER

    add_card(s5, 0.70, 3.40, 5.00, 1.15, bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, border_width=1)
    tb_ft = s5.shapes.add_textbox(Inches(0.80), Inches(3.45), Inches(4.80), Inches(1.05))
    tf_ft = tb_ft.text_frame
    tf_ft.word_wrap = True
    p1 = tf_ft.paragraphs[0]
    p1.text = "WITH SAT-SA: EVIDENCE-DRIVEN REVIEW"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(9.0)
    p1.font.bold = True
    p1.font.color.rgb = C_SIH_BLUE
    p2 = tf_ft.add_paragraph()
    p2.text = "Evidence-Based Priorities  ➔  Explainable Findings  ➔  Focused Expert Review\nEvidence-backed and traceable supervisory assessment"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8.0)
    p2.font.color.rgb = C_NAVY

    # Right Top: 4 Impact Cards
    add_card(s5, 6.10, 1.35, 6.73, 2.30, bg_color=C_WHITE, border_color=C_BORDER, border_width=1.5)
    tb_ic_t = s5.shapes.add_textbox(Inches(6.30), Inches(1.42), Inches(6.33), Inches(0.25))
    p_ict = tb_ic_t.text_frame.paragraphs[0]
    p_ict.text = "FOUR PILLARS OF SUPERVISORY VALUE"
    p_ict.font.name = FONT_TITLE
    p_ict.font.size = Pt(10.5)
    p_ict.font.bold = True
    p_ict.font.color.rgb = C_NAVY

    impact_pillars = [
        ("FOCUSED REVIEW", "Helps experts identify where to investigate first."),
        ("EVIDENCE-DRIVEN", "Links recommendations directly to underlying records."),
        ("BETTER VISIBILITY", "Detects both unusual behaviour and missing evidence."),
        ("EFFICIENT AUDIT", "Reduces dependence on purely manual sampling.")
    ]
    for idx, (ih, idesc) in enumerate(impact_pillars):
        ix = 6.30 + (idx % 2) * 3.20
        iy = 1.72 + (idx // 2) * 0.90
        add_card(s5, ix, iy, 3.05, 0.82, bg_color=C_BG_CARD, border_color=C_BORDER_LIGHT, border_width=1)
        tb_p = s5.shapes.add_textbox(Inches(ix + 0.08), Inches(iy + 0.04), Inches(2.89), Inches(0.74))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        p1 = tf_p.paragraphs[0]
        p1.text = ih
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.0)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY
        p2 = tf_p.add_paragraph()
        p2.text = idesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = C_SLATE_TEXT

    # Right Bottom: Comparison Table
    add_card(s5, 6.10, 3.75, 6.73, 2.05, bg_color=C_NAVY_DARK, border_color=C_SIH_BLUE, border_width=1.5)
    tb_uv_t = s5.shapes.add_textbox(Inches(6.30), Inches(3.82), Inches(6.33), Inches(0.25))
    p_uvt = tb_uv_t.text_frame.paragraphs[0]
    p_uvt.text = "TRADITIONAL MANUAL REVIEW VS SAT-SA"
    p_uvt.font.name = FONT_TITLE
    p_uvt.font.size = Pt(10.5)
    p_uvt.font.bold = True
    p_uvt.font.color.rgb = C_SIH_BLUE

    uv_table_shape = s5.shapes.add_table(5, 2, Inches(6.30), Inches(4.12), Inches(6.33), Inches(1.55))
    tbl_uv = uv_table_shape.table
    tbl_uv.columns[0].width = Inches(3.15)
    tbl_uv.columns[1].width = Inches(3.18)

    uv_data = [
        ["Traditional Manual Review", "SAT-SA Supervisory Analytics"],
        ["Sample-driven manual review", "Priority-driven analysis across the submitted dataset"],
        ["Record-focused in isolation", "Behaviour-focused across time"],
        ["Hard to compare peer entities", "Context-aware peer benchmarking"],
        ["Inspects existing logs only", "Inspects existing + missing evidence"]
    ]
    for r_idx, row in enumerate(uv_data):
        for c_idx, val in enumerate(row):
            cell = tbl_uv.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(8.0 if r_idx > 0 else 8.5)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_SIH_BLUE if c_idx == 1 else C_NAVY_LIGHT
            else:
                p.font.bold = (c_idx == 1)
                p.font.color.rgb = C_AMBER if c_idx == 1 else C_BORDER_LIGHT
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY_LIGHT if r_idx % 2 == 1 else C_NAVY_DARK

    # Bottom Callout Box
    add_callout(s5, 0.50, 5.90, 12.33, 0.85,
                '"From Data Overload → Evidence-Driven Review"\nSAT-SA helps supervisory experts spend limited review time where evidence indicates the greatest need.',
                bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)


    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES (With Verified Clickable Links)
    # =========================================================================
    s6 = prs.slides[5]
    add_header(s6, 6, TOTAL_SLIDES, "RESEARCH  AND REFERENCES", "Regulatory Guidelines, Standards & Scientific References")

    ref_cards_pptx = [
        ("1. NCIIPC & GOVERNMENT GUIDELINES", [
            ("• NCIIPC Guidelines (Sec 70A, IT Act 2000) — ", "Official NCIIPC", "https://nciipc.gov.in"),
            ("• CERT-In Cyber Security Directions — ", "Official CERT-In", "https://www.cert-in.org.in"),
            ("• NCIIPC / QCI Conformity Assessment Framework — ", "Official NCIIPC Guidelines", "https://nciipc.gov.in")
        ], C_SIH_BLUE, C_BLUE_BG),
        ("2. SMART INDIA HACKATHON 2026 SPECIFICATION", [
            ("• Problem Statement 26157: Supervisory Analytics Tool — ", "Official SIH", "https://www.sih.gov.in"),
            ("• Objective: Offline supervisory audit engine for prioritizing human investigation", "", ""),
            ("• Scope: Analysis of historical alerts, case tickets, shift rosters, and asset telemetry", "", "")
        ], C_NAVY, C_BG_CARD),
        ("3. RESEARCH ON SOC ANALYTICS & OPERATIONS", [
            ("• MITRE ATT&CK Enterprise Framework & Detection Taxonomy — ", "Official MITRE", "https://attack.mitre.org"),
            ("• SOC Alert Fatigue & Supervisory Triage Optimization (IEEE/ACM Surveys)", "", ""),
            ("• Empirical Analysis of SOC Workflows: Closure Velocity, Shift Drift & Quality", "", "")
        ], C_SLATE_DARK, C_BG_CARD),
        ("4. STATISTICAL & MACHINE LEARNING REFERENCES", [
            ("• Isolation Forest (Liu, Ting & Zhou) — ", "IEEE ICDM", "https://doi.org/10.1109/ICDM.2008.17"),
            ("• MinHash / LSH (Broder et al.) — ", "IEEE FOCS", "https://doi.org/10.1109/SFCS.1997.646128"),
            ("• Empirical Bayes Poisson-Gamma Shrinkage (Efron & Morris) — ", "JASA", "https://doi.org/10.1080/01621459.1973.10482431")
        ], C_GREEN, C_GREEN_BG)
    ]

    for idx, (rh, r_bullets, r_col, r_bg) in enumerate(ref_cards_pptx):
        rx = 0.50 + (idx % 2) * 6.38
        ry = 1.35 + (idx // 2) * 2.20
        add_card(s6, rx, ry, 5.95, 2.05, bg_color=C_WHITE, border_color=r_col, border_width=1.5)
        add_card(s6, rx, ry, 5.95, 0.40, bg_color=r_col, border_color=r_col, border_width=0)
        tb_rh = s6.shapes.add_textbox(Inches(rx + 0.15), Inches(ry + 0.05), Inches(5.65), Inches(0.30))
        p_rh = tb_rh.text_frame.paragraphs[0]
        p_rh.text = rh
        p_rh.font.name = FONT_BODY
        p_rh.font.size = Pt(9.5)
        p_rh.font.bold = True
        p_rh.font.color.rgb = C_WHITE

        tb_rb = s6.shapes.add_textbox(Inches(rx + 0.15), Inches(ry + 0.45), Inches(5.65), Inches(1.50))
        tf_rb = tb_rb.text_frame
        tf_rb.word_wrap = True
        for i, (b_prefix, b_link_text, b_url) in enumerate(r_bullets):
            p = tf_rb.paragraphs[0] if i == 0 else tf_rb.add_paragraph()
            p.space_after = Pt(2)
            r1 = p.add_run()
            r1.text = b_prefix
            r1.font.name = FONT_BODY
            r1.font.size = Pt(8.0)
            r1.font.color.rgb = C_SLATE_DARK
            if b_url and b_link_text:
                r2 = p.add_run()
                r2.text = b_link_text
                r2.font.name = FONT_BODY
                r2.font.size = Pt(8.0)
                r2.font.bold = True
                r2.font.color.rgb = C_SIH_BLUE
                r2.hyperlink.address = b_url

    # Bottom Callout Banner
    add_callout(s6, 0.50, 5.90, 12.33, 0.85,
                "All methodologies grounded in established supervisory standards, peer-reviewed statistical models, and official regulatory guidelines.",
                bg_color=C_BLUE_BG, border_color=C_SIH_BLUE, text_color=C_NAVY, font_size=11, bold=True)

    # Save final presentation
    output_pptx = 'SAT-SA_SIH2026_FINAL.pptx'
    prs.save(output_pptx)
    print(f"[+] PPTX generated successfully: {output_pptx}")


# =========================================================================
# REPORTLAB PDF GENERATOR (EXACT 6 PAGES WIDESCREEN WITH TEXT WRAPPING)
# =========================================================================
def build_pdf():
    output_pdf = 'SAT-SA_SIH2026_FINAL.pdf'
    
    # 13.333 inches x 7.5 inches in points
    width_pt = 13.333 * 72.0
    height_pt = 7.5 * 72.0
    
    c = canvas.Canvas(output_pdf, pagesize=(width_pt, height_pt))
    
    def rgb(r, g, b):
        return HexColor(f"#{r:02x}{g:02x}{b:02x}")
    
    C_NAVY_DARK_PDF = rgb(10, 25, 47)
    C_NAVY_PDF = rgb(15, 30, 60)
    C_NAVY_LIGHT_PDF = rgb(24, 43, 73)
    C_SIH_BLUE_PDF = rgb(0, 112, 192)
    C_ACCENT_BLUE_PDF = rgb(2, 132, 199)
    C_SLATE_DARK_PDF = rgb(30, 41, 59)
    C_SLATE_TEXT_PDF = rgb(51, 65, 85)
    C_BG_CARD_PDF = rgb(241, 245, 249)
    C_BORDER_PDF = rgb(203, 213, 225)
    C_BORDER_LIGHT_PDF = rgb(226, 232, 240)
    C_WHITE_PDF = rgb(255, 255, 255)
    C_AMBER_PDF = rgb(217, 119, 6)
    C_AMBER_BG_PDF = rgb(254, 243, 199)
    C_RED_PDF = rgb(220, 38, 38)
    C_RED_BG_PDF = rgb(254, 226, 226)
    C_GREEN_PDF = rgb(5, 150, 105)
    C_GREEN_BG_PDF = rgb(209, 250, 229)
    C_BLUE_BG_PDF = rgb(224, 242, 254)
    
    def draw_rounded_rect(c, x_in, y_in, w_in, h_in, fill_color, stroke_color=None, stroke_width=1, r_pt=6):
        x = x_in * 72.0
        y = height_pt - (y_in + h_in) * 72.0
        w = w_in * 72.0
        h = h_in * 72.0
        c.saveState()
        c.setFillColor(fill_color)
        if stroke_color:
            c.setStrokeColor(stroke_color)
            c.setLineWidth(stroke_width)
            c.roundRect(x, y, w, h, r_pt, fill=1, stroke=1)
        else:
            c.roundRect(x, y, w, h, r_pt, fill=1, stroke=0)
        c.restoreState()

    def draw_wrapped_text(c, x_pt, y_pt, max_w_pt, text, font_name, font_size, line_spacing=11, fill_color=C_SLATE_TEXT_PDF):
        c.saveState()
        c.setFont(font_name, font_size)
        c.setFillColor(fill_color)
        words = text.split(" ")
        lines = []
        curr = ""
        for w in words:
            test = curr + (" " if curr else "") + w
            if c.stringWidth(test, font_name, font_size) <= max_w_pt:
                curr = test
            else:
                if curr:
                    lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)
        
        for i, l in enumerate(lines):
            c.drawString(x_pt, y_pt - i * line_spacing, l)
        c.restoreState()
        return len(lines)

    def draw_header_pdf(c, slide_num, title, subhead=""):
        logo_path = 'scratch/template_images/slide2_Picture 10_3.png'
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 10.70 * 72.0, height_pt - 1.16 * 72.0, width=2.46 * 72.0, height=1.16 * 72.0, mask='auto')

        # Top-left pill
        draw_rounded_rect(c, 0.50, 0.18, 2.20, 0.32, C_SIH_BLUE_PDF, None, r_pt=4)
        c.saveState()
        c.setFillColor(C_WHITE_PDF)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString((0.50 + 1.10) * 72.0, height_pt - (0.18 + 0.22) * 72.0, "SIH 2026 | PS 26157")
        c.restoreState()

        # Title
        c.saveState()
        c.setFillColor(C_NAVY_PDF)
        c.setFont("Times-Bold", 22)
        c.drawString(0.50 * 72.0, height_pt - 0.78 * 72.0, title)
        if subhead:
            c.setFillColor(C_SIH_BLUE_PDF)
            c.setFont("Helvetica-Bold", 10.5)
            c.drawString(0.50 * 72.0, height_pt - 0.98 * 72.0, subhead)
        c.restoreState()

        # Bottom ribbon
        c.saveState()
        c.setFillColor(C_SIH_BLUE_PDF)
        c.rect(0, 0, width_pt, 0.55 * 72.0, fill=1, stroke=0)
        c.setFillColor(C_WHITE_PDF)
        c.setFont("Helvetica", 11)
        c.drawString(0.50 * 72.0, 0.20 * 72.0, "SAT-SA: Security Audit & Supervisory Analytics")
        c.drawCentredString(width_pt / 2.0, 0.20 * 72.0, "@SIH Idea submission- Template | NCIIPC / NTRO")
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(width_pt - 0.50 * 72.0, 0.20 * 72.0, f"Slide {slide_num} of 6")
        c.restoreState()

    def draw_callout_pdf(c, x_in, y_in, w_in, h_in, text, bg_color=C_BLUE_BG_PDF, border_color=C_SIH_BLUE_PDF, text_color=C_NAVY_PDF, font_size=10.5):
        draw_rounded_rect(c, x_in, y_in, w_in, h_in, bg_color, border_color, stroke_width=1.5, r_pt=6)
        c.saveState()
        c.setFillColor(text_color)
        c.setFont("Helvetica-Bold", font_size)
        lines = text.split("\n")
        total_h = len(lines) * (font_size + 3)
        start_y = height_pt - (y_in + h_in / 2.0) * 72.0 + total_h / 2.0 - font_size
        for i, l in enumerate(lines):
            c.drawCentredString((x_in + w_in / 2.0) * 72.0, start_y - i * (font_size + 3), l)
        c.restoreState()

    # =========================================================================
    # PAGE 1: TITLE PAGE (Simplified Clean Official Template Layout)
    # =========================================================================
    logo_path = 'scratch/template_images/slide1_Picture 1_2.png'
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 10.70 * 72.0, height_pt - 1.16 * 72.0, width=2.46 * 72.0, height=1.16 * 72.0, mask='auto')

    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Times-Bold", 20)
    c.drawString(0.50 * 72.0, height_pt - 0.40 * 72.0, "SMART INDIA HACKATHON 2026")
    c.setFillColor(C_NAVY_PDF)
    c.setFont("Times-Bold", 13)
    c.drawString(0.50 * 72.0, height_pt - 0.70 * 72.0, "TITLE PAGE")

    c.setFont("Helvetica-Bold", 25)
    c.drawString(0.50 * 72.0, height_pt - 1.25 * 72.0, "SAT-SA: Security Audit & Supervisory Analytics")
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(0.50 * 72.0, height_pt - 1.60 * 72.0, "Turning SOC Records into Actionable Audit Evidence")
    c.restoreState()

    # Main Metadata Box (Clean 2-Column Official SIH Form)
    draw_rounded_rect(c, 0.50, 2.35, 12.33, 2.30, C_BG_CARD_PDF, C_BORDER_PDF, stroke_width=1.5)
    
    # Left Column Fields
    left_meta = [
        ("Problem Statement ID –", "26157 (SIH26157)"),
        ("Problem Statement Title –", "Supervisory Analytics Tool for SOC Assessment"),
        ("Theme –", "Blockchain & Cybersecurity")
    ]
    for i, (k, v) in enumerate(left_meta):
        y_pos = height_pt - (2.75 + i * 0.55) * 72.0
        c.saveState()
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(C_NAVY_PDF)
        c.drawString(0.80 * 72.0, y_pos, k)
        c.setFont("Helvetica", 10.5)
        c.setFillColor(C_SLATE_TEXT_PDF)
        c.drawString(2.95 * 72.0, y_pos, v)
        c.restoreState()

    # Right Column Fields
    right_meta = [
        ("PS Category –", "Software (Offline / Air-Gapped)"),
        ("Team ID –", "SIH26157_TEAM"),
        ("Team Name –", "SAT-SA Analytics (Registered on portal)")
    ]
    for i, (k, v) in enumerate(right_meta):
        y_pos = height_pt - (2.75 + i * 0.55) * 72.0
        c.saveState()
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(C_NAVY_PDF)
        c.drawString(6.80 * 72.0, y_pos, k)
        c.setFont("Helvetica", 10.5)
        c.setFillColor(C_SLATE_TEXT_PDF)
        c.drawString(8.15 * 72.0, y_pos, v)
        c.restoreState()

    # Sub-card: Solution Role & Scope Summary
    draw_rounded_rect(c, 0.50, 4.80, 12.33, 0.95, C_WHITE_PDF, C_BORDER_PDF, stroke_width=1)
    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(0.70 * 72.0, height_pt - 5.05 * 72.0, "SOLUTION SCOPE & HUMAN-IN-THE-LOOP AUDIT OBJECTIVE")
    c.setFillColor(C_SLATE_DARK_PDF)
    c.setFont("Helvetica", 9.5)
    c.drawString(0.70 * 72.0, height_pt - 5.35 * 72.0, "An offline supervisory analytics tool that evaluates SOC records, detects behavioural anomalies, execution gaps, and")
    c.drawString(0.70 * 72.0, height_pt - 5.55 * 72.0, "missing evidence, and prioritises high-risk entities to assist human auditors.")
    c.restoreState()

    draw_callout_pdf(c, 0.50, 5.95, 12.33, 0.80, 
                     "Offline-First Supervisory Analytics & Review Prioritisation for Critical Sector Security Operations Centers\nHuman-in-the-loop decision support enabling defensible, evidence-backed supervisory investigations.",
                     bg_color=C_BLUE_BG_PDF, border_color=C_SIH_BLUE_PDF, text_color=C_NAVY_PDF, font_size=10.5)

    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.rect(0, 0, width_pt, 0.55 * 72.0, fill=1, stroke=0)
    c.setFillColor(C_WHITE_PDF)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width_pt / 2.0, 0.20 * 72.0, "SIH 2026 | Problem Statement 26157 | SAT-SA: Security Audit & Supervisory Analytics | Slide 1 of 6")
    c.restoreState()
    c.showPage()


    # =========================================================================
    # PAGE 2: IDEA TITLE
    # =========================================================================
    draw_header_pdf(c, 2, "IDEA TITLE", "SAT-SA: Security Audit & Supervisory Analytics")
    
    # Col 1: The Problem
    draw_rounded_rect(c, 0.50, 1.35, 3.80, 4.45, C_WHITE_PDF, C_RED_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_RED_PDF)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.65 * 72.0, height_pt - 1.65 * 72.0, "1. THE PROBLEM")
    c.restoreState()
    
    for idx, (ph, pd) in enumerate([
        ("High Data Volume", "SOCs generate millions of alerts, cases, closures, and asset records."),
        ("Limited Expert Review Capacity", "Large SOC datasets make exhaustive manual review difficult."),
        ("Missing Evidence", "Silent critical assets & dropped logs produce zero events to sample.")
    ]):
        p_top = 1.85 + idx * 1.00
        draw_rounded_rect(c, 0.65, p_top, 3.50, 0.85, C_RED_BG_PDF, C_RED_PDF, stroke_width=1)
        c.saveState()
        c.setFillColor(C_RED_PDF)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(0.75 * 72.0, height_pt - (p_top + 0.26) * 72.0, ph)
        c.restoreState()
        draw_wrapped_text(c, 0.75 * 72.0, height_pt - (p_top + 0.46) * 72.0, 3.30 * 72.0, pd, "Helvetica", 8.0, line_spacing=10, fill_color=C_SLATE_TEXT_PDF)

    # Col 2: Our Solution
    draw_rounded_rect(c, 4.50, 1.35, 4.33, 4.45, C_NAVY_DARK_PDF, C_SIH_BLUE_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(4.65 * 72.0, height_pt - 1.65 * 72.0, "2. OUR PROPOSED SOLUTION")
    c.restoreState()
    
    for idx, (sh, sd, sc) in enumerate([
        ("SOC Records", "Historical Alerts, Cases, Assets", C_NAVY_LIGHT_PDF),
        ("SAT-SA Analytics Engine", "• Rule Analysis  • Statistics (EB)\n• Peer Cohorts  • Anomaly ML", C_SIH_BLUE_PDF),
        ("Review Priorities", "Prioritised Entities & Findings", C_AMBER_PDF),
        ("Human Expert Auditor", "Targeted Forensic Investigation", C_GREEN_PDF)
    ]):
        s_top = 1.85 + idx * 0.90
        s_hgt = 0.70 if idx == 1 else 0.55
        draw_rounded_rect(c, 4.65, s_top, 4.03, s_hgt, sc, C_ACCENT_BLUE_PDF if sc == C_NAVY_LIGHT_PDF else sc, stroke_width=1)
        c.saveState()
        c.setFillColor(C_WHITE_PDF)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(4.75 * 72.0, height_pt - (s_top + 0.26) * 72.0, sh)
        c.setFont("Helvetica", 8.0)
        c.setFillColor(C_BORDER_LIGHT_PDF)
        lines = sd.split("\n")
        for l_idx, l in enumerate(lines):
            c.drawString(4.75 * 72.0, height_pt - (s_top + 0.45 + l_idx * 0.18) * 72.0, l)
        c.restoreState()

    # Col 3: Innovation
    draw_rounded_rect(c, 9.03, 1.35, 3.80, 4.45, C_WHITE_PDF, C_SIH_BLUE_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(9.18 * 72.0, height_pt - 1.65 * 72.0, "3. INNOVATION & UNIQUENESS")
    c.restoreState()

    for idx, (ih, idesc, i_bg, i_col) in enumerate([
        ("01 — EXECUTION GAPS", "Evidence exists, but behaviour appears unusual (e.g. 4s fast closures, template notes).", C_RED_BG_PDF, C_RED_PDF),
        ("02 — NEGATIVE SPACE", "Expected evidence is missing or unexpectedly sparse (e.g. silent SCADA assets, blackout shifts).", C_BLUE_BG_PDF, C_SIH_BLUE_PDF),
        ("03 — EVIDENCE TRAIL", "Every recommendation links to an unbroken chain of verifiable raw records.", C_GREEN_BG_PDF, C_GREEN_PDF)
    ]):
        i_top = 1.85 + idx * 1.00
        draw_rounded_rect(c, 9.18, i_top, 3.50, 0.85, i_bg, i_col, stroke_width=1)
        c.saveState()
        c.setFillColor(i_col)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(9.28 * 72.0, height_pt - (i_top + 0.26) * 72.0, ih)
        c.restoreState()
        draw_wrapped_text(c, 9.28 * 72.0, height_pt - (i_top + 0.46) * 72.0, 3.30 * 72.0, idesc, "Helvetica", 8.0, line_spacing=10, fill_color=C_SLATE_TEXT_PDF)

    draw_callout_pdf(c, 0.50, 5.90, 12.33, 0.85,
                     '"SAT-SA analyses not only what exists — but also what should exist."\nIdentifies where expert review should focus without replacing the human investigator.',
                     bg_color=C_BG_CARD_PDF, border_color=C_NAVY_PDF, text_color=C_NAVY_PDF, font_size=11)
    c.showPage()


    # =========================================================================
    # PAGE 3: TECHNICAL APPROACH
    # =========================================================================
    draw_header_pdf(c, 3, "TECHNICAL APPROACH", "Methodology, Workflow & Detection Engine")
    
    # Workflow bar
    draw_rounded_rect(c, 0.50, 1.35, 12.33, 0.70, C_NAVY_DARK_PDF, C_SIH_BLUE_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(0.65 * 72.0, height_pt - 1.55 * 72.0, "COMPLETE SYSTEM WORKFLOW PIPELINE")
    c.restoreState()

    pipe_steps = ["DATA INPUT", "NORMALISATION", "FEATURE EXTRACTION", "DETECTION ENGINE", "PRIORITISATION", "EVIDENCE TRAIL", "HUMAN REVIEW"]
    for idx, ps in enumerate(pipe_steps):
        p_left = 0.65 + idx * 1.73
        draw_rounded_rect(c, p_left, 1.62, 1.62, 0.35, C_NAVY_LIGHT_PDF, C_ACCENT_BLUE_PDF, stroke_width=1)
        c.saveState()
        c.setFillColor(C_WHITE_PDF)
        c.setFont("Helvetica-Bold", 8.0)
        c.drawCentredString((p_left + 0.81) * 72.0, height_pt - (1.62 + 0.22) * 72.0, ps)
        c.restoreState()

    # Left: Detection Engine Box
    draw_rounded_rect(c, 0.50, 2.15, 6.00, 2.70, C_WHITE_PDF, C_BORDER_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_NAVY_PDF)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(0.65 * 72.0, height_pt - 2.40 * 72.0, "DATA INPUT & DETECTION ENGINE")
    c.restoreState()

    for i, (k, v) in enumerate([
        ("• Ingestion Sources:", "CSV | JSON | DB Exports (Alerts, Cases, Closures, Assets, Telemetry)"),
        ("• 4 Parallel Analytics Branches:", "Rules • Statistical Analysis (EB) • Peer Benchmarks • Anomaly ML"),
        ("• Dual-Paradigm Output:", "Splits into Execution Gaps (Faulty actions) + Negative Space (Omissions)")
    ]):
        y_pos = height_pt - (2.75 + i * 0.65) * 72.0
        c.saveState()
        c.setFillColor(C_SIH_BLUE_PDF)
        c.setFont("Helvetica-Bold", 9.0)
        c.drawString(0.65 * 72.0, y_pos, k)
        c.setFillColor(C_SLATE_DARK_PDF)
        c.setFont("Helvetica", 8.0)
        c.drawString(0.65 * 72.0, y_pos - 13, v)
        c.restoreState()

    # Right: Mini Demos
    draw_rounded_rect(c, 6.70, 2.15, 6.13, 2.70, C_BG_CARD_PDF, C_BORDER_PDF, stroke_width=1.5)
    
    draw_rounded_rect(c, 6.85, 2.25, 5.83, 1.15, C_RED_BG_PDF, C_RED_PDF, stroke_width=1)
    c.saveState()
    c.setFillColor(C_RED_PDF)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(6.95 * 72.0, height_pt - 2.50 * 72.0, "EXECUTION GAP VISUAL (Alert A-19283)")
    c.setFillColor(C_NAVY_PDF)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(6.95 * 72.0, height_pt - 2.80 * 72.0, "Opened: 10:02:15  ➔  Closed: 10:02:19  |  Duration: 4 seconds")
    c.setFillColor(C_RED_PDF)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(6.95 * 72.0, height_pt - 3.10 * 72.0, "Significant Peer Deviation  ➔  [ Review Recommended ]")
    c.restoreState()

    draw_rounded_rect(c, 6.85, 3.55, 5.83, 1.15, C_BLUE_BG_PDF, C_SIH_BLUE_PDF, stroke_width=1)
    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(6.95 * 72.0, height_pt - 3.80 * 72.0, "NEGATIVE SPACE VISUAL (Critical SCADA Gateways)")
    c.setFillColor(C_SLATE_TEXT_PDF)
    c.setFont("Helvetica", 8.0)
    c.drawString(6.95 * 72.0, height_pt - 4.10 * 72.0, "Expected: [████████████████████] (Baseline Activity)")
    c.setFillColor(C_AMBER_PDF)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(6.95 * 72.0, height_pt - 4.40 * 72.0, "Observed: [██████] (Low Telemetry)  ➔  [ Potential Coverage Gap ]")
    c.restoreState()

    # Tech stack bottom
    draw_rounded_rect(c, 0.50, 4.95, 12.33, 0.85, C_NAVY_DARK_PDF, C_SIH_BLUE_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(0.65 * 72.0, height_pt - 5.15 * 72.0, "TECHNOLOGY STACK & OFFLINE-FIRST ARCHITECTURE")
    c.setFillColor(C_WHITE_PDF)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(0.65 * 72.0, height_pt - 5.38 * 72.0, "Python 3  •  Pandas  •  DuckDB + Parquet  •  scikit-learn  •  Streamlit / Plotly  •  Pydantic")
    c.setFillColor(C_AMBER_PDF)
    c.setFont("Helvetica", 8.0)
    c.drawString(0.65 * 72.0, height_pt - 5.60 * 72.0, "OFFLINE-FIRST: Air-Gapped • No External Cloud APIs • Tamper-Evident SHA-256 Ledger")
    c.restoreState()

    draw_callout_pdf(c, 0.50, 5.90, 12.33, 0.85,
                     "Designed for high-volume local analytical processing with zero external cloud API dependencies.",
                     bg_color=C_BLUE_BG_PDF, border_color=C_SIH_BLUE_PDF, text_color=C_NAVY_PDF, font_size=10.5)
    c.showPage()


    # =========================================================================
    # PAGE 4: FEASIBILITY AND VIABILITY
    # =========================================================================
    draw_header_pdf(c, 4, "FEASIBILITY AND VIABILITY", "Feasibility Analysis & Risk-Mitigation Matrix")
    
    # Left Feasibility Cards
    draw_rounded_rect(c, 0.50, 1.35, 5.00, 4.45, C_WHITE_PDF, C_BORDER_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_NAVY_PDF)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.70 * 72.0, height_pt - 1.65 * 72.0, "FEASIBILITY ANALYSIS")
    c.restoreState()

    for idx, (fh, fd) in enumerate([
        ("OFFLINE DEPLOYMENT", "Works completely without cloud access, external APIs, or outbound network calls in air-gapped environments."),
        ("SCALABLE ANALYTICS", "Columnar storage (DuckDB/Parquet) and vectorized processing easily handle large operational datasets locally."),
        ("MODULAR DETECTORS", "Detector rules, statistics, and anomaly models can be independently updated and verified."),
        ("HUMAN-IN-THE-LOOP", "System prioritises and recommends review; human experts retain absolute assessment authority.")
    ]):
        f_top = 1.85 + idx * 0.95
        draw_rounded_rect(c, 0.70, f_top, 4.60, 0.82, C_BG_CARD_PDF, C_BORDER_LIGHT_PDF, stroke_width=1)
        c.saveState()
        c.setFillColor(C_NAVY_PDF)
        c.setFont("Helvetica-Bold", 9.0)
        c.drawString(0.80 * 72.0, height_pt - (f_top + 0.26) * 72.0, fh)
        c.restoreState()
        draw_wrapped_text(c, 0.80 * 72.0, height_pt - (f_top + 0.46) * 72.0, 4.40 * 72.0, fd, "Helvetica", 7.5, line_spacing=10, fill_color=C_SLATE_TEXT_PDF)

    # Right Table
    draw_rounded_rect(c, 5.70, 1.35, 7.13, 3.25, C_WHITE_PDF, C_BORDER_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_NAVY_PDF)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(5.90 * 72.0, height_pt - 1.65 * 72.0, "CHALLENGES & SAT-SA MITIGATION STRATEGIES")
    c.restoreState()

    cm_data = [
        ["Potential Challenge", "SAT-SA Mitigation Strategy"],
        ["Incomplete / Missing data", "Automated data-quality gates & schema validation"],
        ["Different CSE data schemas", "Canonical Pydantic schema maps heterogeneous formats"],
        ["Small sample sizes per entity", "Empirical Bayes Poisson-Gamma statistical shrinkage"],
        ["False alarm fatigue", "Context-aware peer benchmarking + human review"],
        ["Adversarial KPI gaming", "Multi-detector diversity + random audit baseline"]
    ]
    for r_idx, row in enumerate(cm_data):
        row_y = 1.80 + r_idx * 0.44
        bg_col = C_NAVY_PDF if r_idx == 0 else (C_WHITE_PDF if r_idx % 2 == 1 else C_BG_CARD_PDF)
        draw_rounded_rect(c, 5.90, row_y, 6.73, 0.42, bg_col, None, r_pt=2)
        c.saveState()
        if r_idx == 0:
            c.setFillColor(C_WHITE_PDF)
            c.setFont("Helvetica-Bold", 9.0)
        else:
            c.setFillColor(C_NAVY_PDF)
            c.setFont("Helvetica-Bold", 8.5)
        c.drawString(6.00 * 72.0, height_pt - (row_y + 0.26) * 72.0, row[0])
        if r_idx == 0:
            c.setFillColor(C_WHITE_PDF)
            c.setFont("Helvetica-Bold", 9.0)
        else:
            c.setFillColor(C_SLATE_DARK_PDF)
            c.setFont("Helvetica", 8.0)
        c.drawString(8.60 * 72.0, height_pt - (row_y + 0.26) * 72.0, row[1])
        c.restoreState()

    # Right Bottom: Deployment
    draw_rounded_rect(c, 5.70, 4.70, 7.13, 1.10, C_NAVY_DARK_PDF, C_SIH_BLUE_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(5.85 * 72.0, height_pt - 4.95 * 72.0, "OFFLINE DEPLOYMENT WORKFLOW")
    c.setFillColor(C_WHITE_PDF)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(5.85 * 72.0, height_pt - 5.25 * 72.0, "Offline Dataset  ➔  SAT-SA Engine  ➔  Local DuckDB  ➔  Local Dashboard  ➔  Expert Review")
    c.setFillColor(C_AMBER_PDF)
    c.setFont("Helvetica", 8.0)
    c.drawString(5.85 * 72.0, height_pt - 5.55 * 72.0, "✓ Zero dependency on external cloud services or Internet connectivity.")
    c.restoreState()

    draw_callout_pdf(c, 0.50, 5.90, 12.33, 0.85,
                     "Designed for air-gapped deployment and suitable for further validation in supervisory workflows.",
                     bg_color=C_GREEN_BG_PDF, border_color=C_GREEN_PDF, text_color=C_NAVY_PDF, font_size=11)
    c.showPage()


    # =========================================================================
    # PAGE 5: IMPACT AND BENEFITS
    # =========================================================================
    draw_header_pdf(c, 5, "IMPACT AND BENEFITS", "Supervisory Transformation & Strategic Value")

    # Left: Transformation
    draw_rounded_rect(c, 0.50, 1.35, 5.40, 4.45, C_WHITE_PDF, C_BORDER_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_NAVY_PDF)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.70 * 72.0, height_pt - 1.65 * 72.0, "SUPERVISORY TRANSFORMATION")
    c.restoreState()

    draw_rounded_rect(c, 0.70, 1.80, 5.00, 1.05, C_RED_BG_PDF, C_RED_PDF, stroke_width=1)
    c.saveState()
    c.setFillColor(C_RED_PDF)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(0.80 * 72.0, height_pt - 2.05 * 72.0, "TODAY: MANUAL DATA OVERLOAD")
    c.setFillColor(C_SLATE_TEXT_PDF)
    c.setFont("Helvetica", 8.0)
    c.drawString(0.80 * 72.0, height_pt - 2.35 * 72.0, "Large SOC Dataset  ➔  Manual Sampling  ➔  Limited Review Capacity")
    c.drawString(0.80 * 72.0, height_pt - 2.55 * 72.0, "Potentially Missed Critical Behavioural Patterns & Silent Gaps")
    c.restoreState()

    draw_rounded_rect(c, 1.70, 2.95, 3.00, 0.35, C_SIH_BLUE_PDF, None, r_pt=4)
    c.saveState()
    c.setFillColor(C_WHITE_PDF)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString((1.70 + 1.50) * 72.0, height_pt - (2.95 + 0.22) * 72.0, "▼  SAT-SA ANALYTICS  ▼")
    c.restoreState()

    draw_rounded_rect(c, 0.70, 3.40, 5.00, 1.15, C_BLUE_BG_PDF, C_SIH_BLUE_PDF, stroke_width=1)
    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 9.0)
    c.drawString(0.80 * 72.0, height_pt - 3.65 * 72.0, "WITH SAT-SA: EVIDENCE-DRIVEN REVIEW")
    c.setFillColor(C_NAVY_PDF)
    c.setFont("Helvetica", 8.0)
    c.drawString(0.80 * 72.0, height_pt - 3.95 * 72.0, "Evidence-Based Priorities  ➔  Explainable Findings  ➔  Focused Expert Review")
    c.drawString(0.80 * 72.0, height_pt - 4.15 * 72.0, "Evidence-backed and traceable supervisory assessment")
    c.restoreState()

    # Right Top: 4 Pillars
    draw_rounded_rect(c, 6.10, 1.35, 6.73, 2.30, C_WHITE_PDF, C_BORDER_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_NAVY_PDF)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(6.30 * 72.0, height_pt - 1.62 * 72.0, "FOUR PILLARS OF SUPERVISORY VALUE")
    c.restoreState()

    for idx, (ih, idesc) in enumerate([
        ("FOCUSED REVIEW", "Helps experts identify where to investigate first."),
        ("EVIDENCE-DRIVEN", "Links recommendations directly to underlying records."),
        ("BETTER VISIBILITY", "Detects both unusual behaviour and missing evidence."),
        ("EFFICIENT AUDIT", "Reduces dependence on purely manual sampling.")
    ]):
        ix = 6.30 + (idx % 2) * 3.20
        iy = 1.72 + (idx // 2) * 0.90
        draw_rounded_rect(c, ix, iy, 3.05, 0.82, C_BG_CARD_PDF, C_BORDER_LIGHT_PDF, stroke_width=1)
        c.saveState()
        c.setFillColor(C_NAVY_PDF)
        c.setFont("Helvetica-Bold", 9.0)
        c.drawString((ix + 0.12) * 72.0, height_pt - (iy + 0.26) * 72.0, ih)
        c.restoreState()
        draw_wrapped_text(c, (ix + 0.12) * 72.0, height_pt - (iy + 0.48) * 72.0, 2.80 * 72.0, idesc, "Helvetica", 7.5, line_spacing=10, fill_color=C_SLATE_TEXT_PDF)

    # Right Bottom: Table
    draw_rounded_rect(c, 6.10, 3.75, 6.73, 2.05, C_NAVY_DARK_PDF, C_SIH_BLUE_PDF, stroke_width=1.5)
    c.saveState()
    c.setFillColor(C_SIH_BLUE_PDF)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(6.30 * 72.0, height_pt - 4.00 * 72.0, "TRADITIONAL MANUAL REVIEW VS SAT-SA")
    c.restoreState()

    uv_data = [
        ["Traditional Manual Review", "SAT-SA Supervisory Analytics"],
        ["Sample-driven manual review", "Priority-driven analysis across the submitted dataset"],
        ["Record-focused in isolation", "Behaviour-focused across time"],
        ["Hard to compare peer entities", "Context-aware peer benchmarking"],
        ["Inspects existing logs only", "Inspects existing + missing evidence"]
    ]
    for r_idx, row in enumerate(uv_data):
        row_y = 4.12 + r_idx * 0.31
        bg_col = C_SIH_BLUE_PDF if (r_idx == 0) else (C_NAVY_LIGHT_PDF if r_idx % 2 == 1 else C_NAVY_DARK_PDF)
        draw_rounded_rect(c, 6.30, row_y, 6.33, 0.29, bg_col, None, r_pt=2)
        c.saveState()
        c.setFillColor(C_WHITE_PDF if r_idx == 0 else C_BORDER_LIGHT_PDF)
        c.setFont("Helvetica-Bold" if r_idx == 0 else "Helvetica", 8.0)
        c.drawString(6.40 * 72.0, height_pt - (row_y + 0.19) * 72.0, row[0])
        c.setFillColor(C_WHITE_PDF if r_idx == 0 else C_AMBER_PDF)
        c.setFont("Helvetica-Bold" if r_idx == 0 else "Helvetica-Bold", 8.0)
        c.drawString(9.55 * 72.0, height_pt - (row_y + 0.19) * 72.0, row[1])
        c.restoreState()

    draw_callout_pdf(c, 0.50, 5.90, 12.33, 0.85,
                     '"From Data Overload → Evidence-Driven Review"\nSAT-SA helps supervisory experts spend limited review time where evidence indicates the greatest need.',
                     bg_color=C_BLUE_BG_PDF, border_color=C_SIH_BLUE_PDF, text_color=C_NAVY_PDF, font_size=11)
    c.showPage()


    # =========================================================================
    # PAGE 6: RESEARCH AND REFERENCES (With Verified Clickable Hyperlinks)
    # =========================================================================
    draw_header_pdf(c, 6, "RESEARCH  AND REFERENCES", "Regulatory Guidelines, Standards & Scientific References")

    ref_cards_pdf = [
        ("1. NCIIPC & GOVERNMENT GUIDELINES", [
            ("• NCIIPC Guidelines (Sec 70A, IT Act 2000) — ", "Official NCIIPC", "https://nciipc.gov.in"),
            ("• CERT-In Cyber Security Directions — ", "Official CERT-In", "https://www.cert-in.org.in"),
            ("• NCIIPC / QCI Conformity Assessment Framework — ", "Official NCIIPC Guidelines", "https://nciipc.gov.in")
        ], C_SIH_BLUE_PDF, C_BLUE_BG_PDF),
        ("2. SMART INDIA HACKATHON 2026 SPECIFICATION", [
            ("• Problem Statement 26157: Supervisory Analytics Tool — ", "Official SIH", "https://www.sih.gov.in"),
            ("• Objective: Offline supervisory audit engine for prioritizing human investigation", "", ""),
            ("• Scope: Analysis of historical alerts, case tickets, shift rosters, and asset telemetry", "", "")
        ], C_NAVY_PDF, C_BG_CARD_PDF),
        ("3. RESEARCH ON SOC ANALYTICS & OPERATIONS", [
            ("• MITRE ATT&CK Enterprise Framework & Detection Taxonomy — ", "Official MITRE", "https://attack.mitre.org"),
            ("• SOC Alert Fatigue & Supervisory Triage Optimization (IEEE/ACM Surveys)", "", ""),
            ("• Empirical Analysis of SOC Workflows: Closure Velocity, Shift Drift & Quality", "", "")
        ], C_SLATE_DARK_PDF, C_BG_CARD_PDF),
        ("4. STATISTICAL & MACHINE LEARNING REFERENCES", [
            ("• Isolation Forest (Liu, Ting & Zhou) — ", "IEEE ICDM", "https://doi.org/10.1109/ICDM.2008.17"),
            ("• MinHash / LSH (Broder et al.) — ", "IEEE FOCS", "https://doi.org/10.1109/SFCS.1997.646128"),
            ("• Empirical Bayes Poisson-Gamma Shrinkage (Efron & Morris) — ", "JASA", "https://doi.org/10.1080/01621459.1973.10482431")
        ], C_GREEN_PDF, C_GREEN_BG_PDF)
    ]

    for idx, (rh, r_bullets, r_col, r_bg) in enumerate(ref_cards_pdf):
        rx = 0.50 + (idx % 2) * 6.38
        ry = 1.35 + (idx // 2) * 2.20
        draw_rounded_rect(c, rx, ry, 5.95, 2.05, C_WHITE_PDF, r_col, stroke_width=1.5)
        draw_rounded_rect(c, rx, ry, 5.95, 0.40, r_col, r_col, stroke_width=0, r_pt=4)
        c.saveState()
        c.setFillColor(C_WHITE_PDF)
        c.setFont("Helvetica-Bold", 9.0)
        c.drawString((rx + 0.15) * 72.0, height_pt - (ry + 0.25) * 72.0, rh)
        c.restoreState()
        
        for i, (b_prefix, b_link_text, b_url) in enumerate(r_bullets):
            bullet_y = height_pt - (ry + 0.62 + i * 0.44) * 72.0
            if b_url and b_link_text:
                c.saveState()
                c.setFont("Helvetica", 7.5)
                c.setFillColor(C_SLATE_DARK_PDF)
                c.drawString((rx + 0.15) * 72.0, bullet_y, b_prefix)
                
                # Measure offset for link
                txt_w = c.stringWidth(b_prefix, "Helvetica", 7.5)
                link_x = (rx + 0.15) * 72.0 + txt_w
                c.setFont("Helvetica-Bold", 7.5)
                c.setFillColor(C_SIH_BLUE_PDF)
                c.drawString(link_x, bullet_y, b_link_text)
                link_w = c.stringWidth(b_link_text, "Helvetica-Bold", 7.5)
                
                # Clickable PDF annotation
                c.linkURL(b_url, (link_x, bullet_y - 2, link_x + link_w, bullet_y + 9), relative=0)
                c.restoreState()
            else:
                draw_wrapped_text(c, (rx + 0.15) * 72.0, bullet_y, 5.65 * 72.0, b_prefix, "Helvetica", 7.5, line_spacing=9.5, fill_color=C_SLATE_DARK_PDF)

    draw_callout_pdf(c, 0.50, 5.90, 12.33, 0.85,
                     "All methodologies grounded in established supervisory standards, peer-reviewed statistical models, and official regulatory guidelines.",
                     bg_color=C_BLUE_BG_PDF, border_color=C_SIH_BLUE_PDF, text_color=C_NAVY_PDF, font_size=11)
    c.showPage()
    
    # Save the canvas
    c.save()
    print(f"[+] PDF generated successfully: {output_pdf}")


if __name__ == "__main__":
    build_pptx()
    build_pdf()
