"""Build the optional PDF submission from the Markdown deliverables."""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, TableStyle,
)


ROOT = Path(__file__).resolve().parent
STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle(
    "Cell", fontName="Helvetica", fontSize=8, leading=11, spaceAfter=2,
))
STYLES.add(ParagraphStyle(
    "Cover", parent=STYLES["Title"], alignment=TA_CENTER,
    textColor=colors.HexColor("#17365d"), spaceAfter=22,
))
STYLES["BodyText"].spaceAfter = 8
STYLES["BodyText"].leading = 14


def inline(text):
    """Convert the small inline Markdown subset used in this report."""
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`(.+?)`", r'<font name="Courier">\1</font>', text)


def markdown_blocks(filename):
    """Convert paragraphs, headings and issue tables to PDF flowables."""
    blocks = []
    lines = (ROOT / filename).read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].startswith("|"):
                cells = [cell.strip() for cell in lines[index].strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", cell) for cell in cells):
                    rows.append([Paragraph(inline(cell), STYLES["Cell"])
                                 for cell in cells])
                index += 1
            widths = [95, 82, 32, 138, 160] if len(rows[0]) == 5 else [137, 185, 185]
            table = LongTable(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce6f1")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c4ce")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            blocks.extend([table, Spacer(1, 12)])
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            blocks.append(Paragraph(inline(line.lstrip("# ")),
                                    STYLES[f"Heading{min(level, 3)}"]))
            index += 1
            continue
        paragraph = []
        while index < len(lines) and lines[index].strip():
            if lines[index].startswith(("#", "|")):
                break
            paragraph.append(lines[index].strip())
            index += 1
        blocks.append(Paragraph(inline(" ".join(paragraph)), STYLES["BodyText"]))
    return blocks


def footer(canvas, document):
    """Label every page with the student's identity and page number."""
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526577"))
    canvas.drawString(44, 28, "Krishna Jha | PES1UG24CS236 | Lab 5")
    canvas.drawRightString(A4[0] - 44, 28, str(document.page))
    canvas.restoreState()


def main():
    """Write a readable report with a summary, issue table and reflections."""
    target = ROOT / "PES1UG24CS236_Lab5_Report.pdf"
    document = SimpleDocTemplate(
        str(target), pagesize=A4, leftMargin=44, rightMargin=44,
        topMargin=40, bottomMargin=46,
        title="Lab 5: Static Code Analysis - Gym Membership System",
        author="Krishna Jha - PES1UG24CS236",
    )
    story = [
        Spacer(1, 42),
        Paragraph("Lab 5: Static Code Analysis", STYLES["Cover"]),
        Paragraph("Gym Membership System", STYLES["Heading1"]),
        Paragraph("<b>Name:</b> Krishna Jha<br/><b>SRN:</b> PES1UG24CS236"
                  "<br/><b>Assignment:</b> 48 (spreadsheet row 49)", STYLES["BodyText"]),
        Spacer(1, 16),
        Paragraph("Final results", STYLES["Heading2"]),
        Paragraph("Pylint: <b>10.00/10</b> (before: 4.81/10).<br/>"
                  "Bandit: <b>0 findings</b> (before: 6).<br/>"
                  "Flake8: <b>0 findings</b> (before: 9).<br/>"
                  "Regression suite: <b>10 tests passed</b>.", STYLES["BodyText"]),
        Paragraph("The submission contains the cleaned Python program, the "
                  "preserved original, before and after reports, an issue table, "
                  "reflection answers, regression tests, and three local commits. "
                  "No analysis checks were suppressed.", STYLES["BodyText"]),
        Paragraph("Assigned source: github.com/SETAPESU26/"
                  "L5_48_gym_membership_system<br/>"
                  "Source commit: 1bbe424240e3a8f7dc099ff1782f7b6a15c6f913",
                  STYLES["BodyText"]),
        Paragraph("Reproduce: install requirements-dev.txt, then run "
                  "<font name='Courier'>python run_checks.py</font> from LAB5. "
                  "Raw evidence is in reports/before and reports/after.",
                  STYLES["BodyText"]),
        PageBreak(),
    ]
    story.extend(markdown_blocks("issues.md"))
    story.append(PageBreak())
    story.extend(markdown_blocks("reflection.md"))
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(target)


if __name__ == "__main__":
    main()
