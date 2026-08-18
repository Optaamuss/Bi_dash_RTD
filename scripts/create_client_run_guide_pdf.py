from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PATH = OUTPUT_DIR / "right_to_dream_dashboard_mvp_run_guide.pdf"

BRAND_GREEN = colors.HexColor("#10a068")
BG_DARK = colors.HexColor("#050706")
TEXT = colors.HexColor("#1d2522")
MUTED = colors.HexColor("#5d6a64")
LIGHT_GREEN = colors.HexColor("#e8f7f0")
LIGHT_GREY = colors.HexColor("#f5f7f6")


def code(text: str) -> Paragraph:
    return Preformatted(
        text,
        ParagraphStyle(
            "Code",
            fontName="Courier",
            fontSize=7.6,
            leading=10.5,
            textColor=colors.HexColor("#101815"),
            backColor=colors.HexColor("#eef2f0"),
            borderColor=colors.HexColor("#d9e0dc"),
            borderWidth=0.5,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=8,
        ),
    )


def bullet(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=8) for item in items],
        bulletType="bullet",
        leftIndent=16,
    )


def build_pdf() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=17 * mm,
        leftMargin=17 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="Right To Dream Dashboard MVP Run Guide",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        alignment=TA_CENTER,
        textColor=colors.white,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#dce8e2"),
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=BRAND_GREEN,
        spaceBefore=12,
        spaceAfter=6,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=TEXT,
        spaceBefore=8,
        spaceAfter=3,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=TEXT,
        spaceAfter=5,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=8.5,
        leading=12,
        textColor=MUTED,
    )
    link = ParagraphStyle(
        "Link",
        parent=body,
        textColor=BRAND_GREEN,
    )

    story = []
    header = Table(
        [
            [Paragraph("RIGHT TO DREAM TALENT INTELLIGENCE", title)],
            [Paragraph("Dashboard MVP - Non-Technical Run Guide", subtitle)],
        ],
        colWidths=[176 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BG_DARK),
                ("BOX", (0, 0), (-1, -1), 1, BRAND_GREEN),
                ("TOPPADDING", (0, 0), (-1, -1), 15),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )
    story.append(header)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Purpose", h1))
    story.append(
        Paragraph(
            "This guide explains how to open the Right To Dream dashboard MVP on a laptop. No coding knowledge is required. The person running it only needs to install Python once, unzip the dashboard package, and copy a few commands into Terminal or Command Prompt.",
            body,
        )
    )

    story.append(Paragraph("Before You Start", h1))
    story.append(
        bullet(
            [
                "Use Python 3.11. Do not use Python 3.14 for this MVP because some dashboard packages may not install smoothly yet.",
                "Keep the Terminal or Command Prompt window open while using the dashboard.",
                "The dashboard runs locally on the user's computer. It is not published to the public internet.",
            ],
            body,
        )
    )

    story.append(Paragraph("1. Download Python 3.11", h1))
    story.append(
        Paragraph(
            'Open this official Python page: <link href="https://www.python.org/downloads/release/python-3119/">https://www.python.org/downloads/release/python-3119/</link>',
            link,
        )
    )
    data = [
        ["Computer", "Download Option"],
        ["Mac", "macOS 64-bit universal2 installer"],
        ["Windows", "Windows installer (64-bit)"],
    ]
    table = Table(data, colWidths=[42 * mm, 126 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BRAND_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREY),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d7ded9")),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(table)
    story.append(Paragraph("Windows users: during installation, tick 'Add Python to PATH' if the option appears.", small))

    story.append(Paragraph("2. Unzip The Dashboard Package", h1))
    story.append(
        Paragraph(
            "Unzip the file named like right_to_dream_talent_intelligence_mvp_YYYYMMDD_HHMMSS.zip. Put the unzipped folder somewhere easy to find, such as the Desktop.",
            body,
        )
    )

    story.append(Paragraph("3. Open Terminal Or Command Prompt", h1))
    story.append(bullet(["Mac: open Terminal.", "Windows: open Command Prompt or PowerShell."], body))

    story.append(Paragraph("4. Go Into The Dashboard Folder", h1))
    story.append(Paragraph("Mac example if the folder is on the Desktop:", body))
    story.append(code("cd ~/Desktop/dashboard-mvp"))
    story.append(Paragraph("Windows example if the folder is on the Desktop:", body))
    story.append(code(r"cd Desktop\dashboard-mvp"))

    story.append(Paragraph("5. Create The App Environment", h1))
    story.append(Paragraph("Mac:", body))
    story.append(code("python3.11 -m venv .venv"))
    story.append(Paragraph("Windows:", body))
    story.append(code("py -3.11 -m venv .venv"))

    story.append(Paragraph("6. Turn The Environment On", h1))
    story.append(Paragraph("Mac:", body))
    story.append(code("source .venv/bin/activate"))
    story.append(Paragraph("Windows:", body))
    story.append(code(r".venv\Scripts\activate"))

    story.append(Paragraph("7. Install Required Packages", h1))
    story.append(code("python -m pip install --upgrade pip\npip install -r requirements.txt"))
    story.append(Paragraph("This may take a few minutes the first time.", small))

    story.append(Paragraph("8. Start The Dashboard", h1))
    story.append(code("streamlit run dashboard/app.py"))
    story.append(
        Paragraph(
            "A browser window should open automatically. If it does not, copy the local link shown in the Terminal. It usually looks like http://localhost:8501.",
            body,
        )
    )

    story.append(Paragraph("Stopping The Dashboard", h1))
    story.append(Paragraph("Click inside the Terminal or Command Prompt window and press Ctrl + C.", body))

    story.append(Paragraph("Opening It Again Later", h1))
    story.append(Paragraph("Mac:", body))
    story.append(code("cd ~/Desktop/dashboard-mvp\nsource .venv/bin/activate\nstreamlit run dashboard/app.py"))
    story.append(Paragraph("Windows:", body))
    story.append(code("cd Desktop\\dashboard-mvp\n.venv\\Scripts\\activate\nstreamlit run dashboard/app.py"))

    story.append(Paragraph("Simple Troubleshooting", h1))
    trouble = Table(
        [
            [Paragraph("Issue", h2), Paragraph("What To Try", h2)],
            [Paragraph("Python command not found", body), Paragraph("Confirm Python 3.11 is installed. On Windows, reinstall and tick Add Python to PATH.", body)],
            [Paragraph("Package install fails", body), Paragraph("Check that Python 3.11 is being used, not Python 3.14.", body)],
            [Paragraph("Dashboard does not open", body), Paragraph("Copy the http://localhost:8501 link from Terminal into a browser.", body)],
            [Paragraph("Terminal looks stuck", body), Paragraph("Some install steps take a few minutes. Wait unless an error message appears.", body)],
        ],
        colWidths=[54 * mm, 114 * mm],
    )
    trouble.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BRAND_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREEN),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c7d8ce")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(KeepTogether([trouble]))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Official Python downloads: https://www.python.org/downloads/",
            small,
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT_PATH)
