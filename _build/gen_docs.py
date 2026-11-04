"""Generates the FICTIONAL Word documents for the Copilot labs from story.py."""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Inches

import story as S

ROOT = Path(__file__).resolve().parents[1]
OUT1 = ROOT / "data" / "session-1"
OUT2 = ROOT / "data" / "session-2"
RED = RGBColor(0xC6, 0x01, 0x1F)
INK = RGBColor(0x1B, 0x1B, 0x1F)
GREY = RGBColor(0x6B, 0x6B, 0x6B)


def shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def new_doc(title, subtitle):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    for s in d.sections:
        s.left_margin = s.right_margin = Inches(0.9)
        s.top_margin = s.bottom_margin = Inches(0.8)
        hp = s.header.paragraphs[0]
        hp.text = "FICTIONAL TRAINING MATERIAL | Microsoft 365 Copilot Level 2 | Riverfront Rally Weekend"
        hp.runs[0].font.size = Pt(8)
        hp.runs[0].font.color.rgb = GREY
    p = d.add_paragraph()
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(24)
    r.font.color.rgb = RED
    p = d.add_paragraph()
    r = p.add_run(subtitle)
    r.italic = True
    r.font.size = Pt(11)
    r.font.color.rgb = GREY
    return d


def h(d, text, level=1):
    p = d.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(15 if level == 1 else 12.5)
    r.font.color.rgb = RED if level == 1 else INK
    p.paragraph_format.space_before = Pt(12)
    return p


def table(d, headers, rows, widths=None):
    t = d.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, hd in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        run = c.paragraphs[0].add_run(hd)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.size = Pt(10)
        shade(c, "C6011F")
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(v))
            run.font.size = Pt(10)
            if ri % 2 == 1:
                shade(cells[i], "F7F3EA")
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
    d.add_paragraph()
    return t


def email_export():
    d = new_doc("Email Thread Export - Riverfront Rally Weekend",
                "Exported from the Promo Task Force mailboxes | May 10 - June 15, 2027 | 16 messages")
    for e in S.EMAILS:
        eid, when, frm, to, cc, subj, body, _ = e
        p = d.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        r = p.add_run(f"[{eid}]  {subj}")
        r.bold = True
        r.font.size = Pt(12.5)
        r.font.color.rgb = INK
        meta = d.add_paragraph()
        mr = meta.add_run(
            f"From: {frm} <{S.addr(frm)}>\nTo: {'; '.join(f'{x} <{S.addr(x)}>' for x in to)}"
            + (f"\nCc: {'; '.join(f'{x} <{S.addr(x)}>' for x in cc)}" if cc else "")
            + f"\nSent: {when}")
        mr.font.size = Pt(9)
        mr.font.color.rgb = GREY
        for para in body:
            bp = d.add_paragraph(para)
            bp.paragraph_format.space_after = Pt(2)
        line = d.add_paragraph()
        lr = line.add_run("_" * 90)
        lr.font.color.rgb = RGBColor(0xD9, 0xD4, 0xC7)
    d.save(OUT1 / "01_Email_Thread_Export.docx")


def transcript_doc():
    m = S.TRANSCRIPT_META
    d = new_doc(m["title"] + " - Transcript & Recap", m["when"] + " | Microsoft Teams meeting")
    table(d, ["Organizer", "Attendees", "Not present"],
          [[m["organizer"], ", ".join(m["attendees"]), ", ".join(m["absent"])]], [1.4, 3.6, 1.8])
    h(d, "Meeting recap (auto-generated - not reviewed)")
    note = d.add_paragraph()
    nr = note.add_run("AI-generated content may be incorrect. Check the transcript before acting on this recap.")
    nr.italic = True
    nr.font.size = Pt(9)
    nr.font.color.rgb = GREY
    for claim, _, _ in S.RECAP:
        d.add_paragraph(claim, style="List Bullet")
    h(d, "Transcript")
    for ts, who, text in S.TRANSCRIPT:
        p = d.add_paragraph()
        r1 = p.add_run(f"{ts}  ")
        r1.font.color.rgb = GREY
        r1.font.size = Pt(9)
        r2 = p.add_run(f"{who}: ")
        r2.bold = True
        p.add_run(text)
    d.save(OUT1 / "02_Teams_Ops_Huddle_Transcript.docx")


def event_plan():
    e = S.EVENT_PLAN
    d = new_doc(e["title"], e["subtitle"])
    h(d, "Weekend overview")
    d.add_paragraph("Three home games vs. the Allegheny Ironmen, Friday June 18 - Sunday June 20, 2027. "
                    "Objective: weekend net contribution of at least $2.4M and full delivery of every sponsor commitment.")
    table(d, ["Game", "First pitch", "Gates open", "Promotion", "Presenting sponsor"], e["games"],
          [0.8, 0.9, 0.9, 2.8, 1.6])
    h(d, "Giveaway distribution by gate (units)")
    table(d, ["Gate", "Fri - Towel", "Sat - Bobblehead", "Sun - Mini Bat"], e["distribution"])
    h(d, "Staffing")
    d.add_paragraph(e["staffing"])
    h(d, "Fireworks")
    d.add_paragraph("Postgame fireworks Friday by Skyburst Pyrotechnics (vendor service, $65,000). Permit filed 6/1. "
                    "Weather call by Ops at 6:00 PM.")
    h(d, "Key dates")
    table(d, ["When", "Milestone"], e["key_dates"], [1.8, 4.8])
    h(d, "Revision history")
    table(d, ["Version", "Date", "Change"], e["revisions"], [0.8, 0.9, 4.9])
    d.save(OUT1 / "03_Event_Plan_v3_Riverfront_Rally_Weekend.docx")


def sponsor_doc(out):
    d = new_doc("Sponsor Requirements Summary", "Riverfront Rally Weekend & June homestand | Sponsorship team | as of June 15, 2027")
    for name, promo, status, fee, guarantee, makegood, extras in S.SPONSORS:
        h(d, name, 2)
        table(d, ["Promotion", "Contract status", "Fee", "Guaranteed delivery", "Make-good"],
              [[promo, status, fee, guarantee, makegood]], [1.6, 1.6, 0.8, 1.3, 1.5])
        for x in extras:
            d.add_paragraph(x, style="List Bullet")
    d.save(out / "04_Sponsor_Requirements_Summary.docx")


def ops_doc(out):
    d = new_doc("Ballpark Operations Playbook - Giveaway Rules", "Excerpt | Owner: Marcus Bell, Ballpark Operations | rev. March 2027")
    table(d, ["Rule", "Standard"], S.OPS_RULES, [1.6, 5.0])
    d.save(out / "05_Operations_Playbook_Giveaway_Rules.docx")


def plot_twist():
    p = S.PLOT_TWIST
    d = new_doc(p["title"], f"From: {p['from']} | To: {p['to']} | {p['when']}")
    d.add_paragraph(p["intro"])
    for head, body in p["changes"]:
        h(d, head, 2)
        d.add_paragraph(body)
    h(d, "What I need by 3:00 PM")
    for a in p["ask"]:
        d.add_paragraph(a, style="List Number")
    d.add_paragraph("- Elena")
    d.save(OUT2 / "06_Plot_Twist_Memo_June17.docx")


def checklist():
    d = new_doc("Promotional Readiness Checklist", "Standard for every sponsored promotion | Promotions & Marketing | v2.1")
    d.add_paragraph("Use this checklist to rate each promotional element GREEN, YELLOW or RED. Every rating must cite evidence. "
                    "If evidence is missing, the check is NOT met.")
    for sec, items in S.CHECKLIST:
        h(d, sec, 2)
        for it in items:
            d.add_paragraph(it, style="List Bullet")
    d.save(OUT2 / "07_Promotional_Readiness_Checklist.docx")


def standards():
    d = new_doc("Game-Day Event Standards", "Fan Experience & Ballpark Operations | rev. January 2027")
    table(d, ["Standard", "Requirement"], S.STANDARDS, [1.7, 4.9])
    d.save(OUT2 / "08_Event_Standards.docx")


def findings():
    d = new_doc("Task Force Investigation Findings", "Session 1 output | Readiness assessment as of Wed June 16, 2027 11:00 AM")
    d.add_paragraph("Reference version of the Session 1 deliverable. Use your own findings if you completed Session 1; "
                    "use this file if you did not.")
    table(d, ["Element", "Rating", "Finding & evidence"], [list(f) for f in S.FINDINGS_S1], [1.6, 0.8, 4.2])
    h(d, "Recommendation")
    d.add_paragraph("Proceed with conditions: Friday GREEN; Saturday proceeds with a bobblehead shortfall plan; Sunday "
                    "proceeds once the Right Field pallet is rescheduled; bucket hats DELAYED - remove from the fan email.")
    d.save(OUT2 / "09_Task_Force_Findings_Session1.docx")


if __name__ == "__main__":
    email_export()
    transcript_doc()
    event_plan()
    sponsor_doc(OUT1)
    ops_doc(OUT1)
    plot_twist()
    checklist()
    standards()
    findings()
    print("docs ok")
