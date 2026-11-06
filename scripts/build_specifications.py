"""Render controlled spec revisions and append their unchanged baseline PDFs."""

from pathlib import Path
import html
import json
import re
import hashlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "docs/specifications"
QA = ROOT / "tmp/specification-qa"
QA.mkdir(parents=True, exist_ok=True)
STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle(name="DocTitle", fontName="Helvetica-Bold", fontSize=23,
                          leading=27, textColor=colors.black, spaceAfter=14))
STYLES.add(ParagraphStyle(name="Section", fontName="Helvetica-Bold", fontSize=15,
                          leading=19, textColor=colors.HexColor("#173c50"), spaceAfter=12))
STYLES.add(ParagraphStyle(name="Subsection", fontName="Helvetica-Bold", fontSize=11,
                          leading=14, spaceBefore=6, spaceAfter=6))
STYLES.add(ParagraphStyle(name="Text", fontName="Helvetica", fontSize=9.5, leading=13,
                          spaceAfter=8, splitLongWords=True))
STYLES.add(ParagraphStyle(name="CellText", fontName="Helvetica", fontSize=8.4,
                          leading=11, splitLongWords=True))
STYLES.add(ParagraphStyle(name="CellHead", parent=STYLES["CellText"], fontName="Helvetica-Bold",
                          textColor=colors.white))
STYLES.add(ParagraphStyle(name="CodeLine", fontName="Courier", fontSize=8.5,
                          leading=11, leftIndent=12, spaceAfter=1))


def inline(text):
    escaped = html.escape(text)
    return re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', escaped)


def render_markdown(path, out, label):
    lines = path.read_text().splitlines()
    story = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line == "<!-- page -->":
            story.append(PageBreak())
            index += 1
            continue
        if line.startswith("```"):
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code = html.escape(lines[index]).replace(" ", "&#160;")
                story.append(Paragraph(code or "&#160;", STYLES["CodeLine"]))
                index += 1
            story.append(Spacer(1, 9))
            index += 1
            continue
        if line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [value.strip() for value in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                    style = STYLES["CellHead"] if not rows else STYLES["CellText"]
                    rows.append([Paragraph(inline(value), style) for value in cells])
                index += 1
            count = len(rows[0])
            widths = [118, 192, 194] if count == 3 else [170, 334]
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173c50")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f1f5f6"), colors.white]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            story.extend([table, Spacer(1, 10)])
            continue
        if line.startswith("#"):
            depth = len(line) - len(line.lstrip("#"))
            style = {1: "DocTitle", 2: "Section"}.get(depth, "Subsection")
            story.append(Paragraph(inline(line.lstrip("# ")), STYLES[style]))
            index += 1
            continue
        para = [line]
        index += 1
        while index < len(lines) and lines[index].strip() and not lines[index].startswith(("#", "|", "```", "<!--")):
            para.append(lines[index].strip())
            index += 1
        story.append(Paragraph(inline(" ".join(para)), STYLES["Text"]))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#52616a"))
        canvas.drawString(54, 30, f"{label} | Controlling revision | Research prototype")
        canvas.drawRightString(558, 30, str(doc.page))
        canvas.restoreState()
    doc = SimpleDocTemplate(str(out), pagesize=letter, rightMargin=54, leftMargin=54,
                            topMargin=42, bottomMargin=48,
                            title=label, author="Lakshmi Sindhu Pulugundla")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def build(stem, baseline, label):
    revision = QA / (stem + "_revision.pdf")
    render_markdown(SPECS / (stem + ".md"), revision, label)
    output = SPECS / (stem + ".pdf")
    writer = PdfWriter()
    writer.append(str(revision), outline_item="Part A Controlling revision")
    writer.append(str(SPECS / baseline), outline_item="Part B Retained baseline")
    writer.add_metadata({"/Title": label, "/Author": "Lakshmi Sindhu Pulugundla",
                         "/Subject": "Expanded research component requirements with retained baseline"})
    with output.open("wb") as handle:
        writer.write(handle)
    result = PdfReader(output)
    old = PdfReader(SPECS / baseline)
    prefix = len(PdfReader(revision).pages)
    assert len(result.pages) == prefix + len(old.pages)
    # Verify the baseline text and page content streams were preserved verbatim.
    for index, page in enumerate(old.pages):
        appended = result.pages[prefix + index]
        assert page.extract_text() == appended.extract_text()
        assert page.get_contents().get_data() == appended.get_contents().get_data()
    return {"file": output.name, "revision_pages": prefix, "baseline_pages": len(old.pages),
            "total_pages": len(result.pages), "baseline_content_verified": True,
            "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}


if __name__ == "__main__":
    results = [build("BioSynvia_PRD_v1.2", "BioSynvia_PRD_v1.1_Problem_First.pdf", "BioSynvia PRD v1.2"),
               build("BioSynvia_SRD_v0.2", "BioSynvia_System_Requirements_Document_v0.1.pdf", "BioSynvia SRD v0.2")]
    (QA / "document_checks.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
