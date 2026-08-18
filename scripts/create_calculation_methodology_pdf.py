from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PATH = OUTPUT_DIR / "right_to_dream_core_calculations_methodology.pdf"

BRAND_GREEN = colors.HexColor("#10a068")
BG_DARK = colors.HexColor("#050706")
TEXT = colors.HexColor("#1d2522")
MUTED = colors.HexColor("#5d6a64")
LIGHT_GREEN = colors.HexColor("#e8f7f0")
LIGHT_GREY = colors.HexColor("#f5f7f6")


def p(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=8) for item in items],
        bulletType="bullet",
        leftIndent=15,
        spaceAfter=6,
    )


def methodology_table(rows, col_widths):
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BRAND_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREY),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cfdbd5")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def build_pdf():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title="Right To Dream Core Calculations Methodology",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title", parent=styles["Title"], fontSize=21, leading=26, alignment=TA_CENTER, textColor=colors.white)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#dce8e2"))
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=14, leading=18, textColor=BRAND_GREEN, spaceBefore=11, spaceAfter=5)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11, leading=14, textColor=TEXT, spaceBefore=7, spaceAfter=3)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=8.7, leading=12.2, textColor=TEXT, spaceAfter=4)
    small = ParagraphStyle("Small", parent=body, fontSize=7.7, leading=10.5, textColor=MUTED)
    cell = ParagraphStyle("Cell", parent=body, fontSize=7.4, leading=9.6, textColor=TEXT)
    cell_small = ParagraphStyle("CellSmall", parent=cell, fontSize=7.0, leading=9.0, textColor=TEXT)

    story = []
    header = Table(
        [
            [p("RIGHT TO DREAM TALENT INTELLIGENCE", title)],
            [p("Core Calculations: Methodology, Meaning & Safeguards", subtitle)],
        ],
        colWidths=[180 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BG_DARK),
                ("BOX", (0, 0), (-1, -1), 1, BRAND_GREEN),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ]
        )
    )
    story.append(header)
    story.append(Spacer(1, 8))

    story.append(p("Purpose", h1))
    story.append(p("This document explains how the dashboard's core calculations are built and what they translate to in football intelligence terms. It is designed for leadership, recruitment, scouting, coaching, and analysis users who need to understand the meaning and limitations behind the metrics.", body))

    story.append(p("Golden Rules", h1))
    story.append(
        bullets(
            [
                "<b>Missing is not zero.</b> Blank values are preserved as unknown unless zero genuinely means zero.",
                "<b>Correlation is not causation.</b> A strong region, club, or pathway does not automatically prove that source caused the outcome.",
                "<b>Small samples require caution.</b> The dashboard labels evidence strength before recommending action.",
                "<b>Player development requires care.</b> The dashboard uses ratings, IDP, and squad progression; it does not claim full match-performance measurement.",
            ],
            body,
        )
    )

    story.append(p("Core Standardisation", h1))
    rows = [
        [p("Calculation", cell), p("How It Is Built", cell), p("What It Translates To", cell), p("Caution", cell)],
        [p("Player Name Normalisation", cell), p("Lowercase, trim spaces, remove accents, punctuation, apostrophes, hyphen differences, and duplicated spaces.", cell_small), p("Allows the system to compare names across Player Master, Heatmap, and Squad Movement data.", cell_small), p("It improves matching, but does not prove two similar names are the same person.", cell_small)],
        [p("Region Standardisation", cell), p("Known variants are corrected, for example Northen Region -> Northern Region and Greater Accra -> Greater Accra Region.", cell_small), p("Prevents the same region appearing as multiple categories.", cell_small), p("New spelling variants should be added when discovered.", cell_small)],
        [p("Squad Standardisation", cell), p("Known typos are corrected, for example 1-Tean -> 1-Team.", cell_small), p("Keeps filters and squad counts consistent.", cell_small), p("This is a controlled correction, not a broad fuzzy replacement.", cell_small)],
        [p("Player ID", cell), p("Each Player Master row receives a stable ID such as RTD-0001.", cell_small), p("The dashboard does not use raw names as the final relational key.", cell_small), p("Future versions should persist IDs across refreshed exports.", cell_small)],
    ]
    story.append(methodology_table(rows, [36 * mm, 55 * mm, 51 * mm, 38 * mm]))

    story.append(p("Rating & Status Calculations", h1))
    rows = [
        [p("Calculation", cell), p("Formula / Logic", cell), p("Meaning", cell), p("Important Limitation", cell)],
        [p("Football Rating Score", cell), p("A+ = 5, A = 4, B = 3, C = 2, C- = 1.", cell_small), p("Converts rating labels into a numeric scale for comparison and charts.", cell_small), p("It depends on the consistency of the original rating process.", cell_small)],
        [p("Academic Rating Score", cell), p("Uses the same A+ to C- mapping where academic ratings exist.", cell_small), p("Allows academic and football indicators to sit in the same analytical model.", cell_small), p("Sparse ratings reduce confidence in comparisons.", cell_small)],
        [p("Development Status", cell), p("Green/Ahead or A/A+ -> High Performing. As Expected or B -> On Track. Orange/Behind or C/C- -> Watch. Red -> At Risk. Otherwise Insufficient Data.", cell_small), p("Creates a simple development-support category for review workflows.", cell_small), p("Insufficient data is not treated as negative performance.", cell_small)],
        [p("Players Requiring Attention", cell), p("Count of players classified as Watch or At Risk.", cell_small), p("Shows the number of players who may merit development review.", cell_small), p("This is a prompt for professional review, not an automated judgement.", cell_small)],
    ]
    story.append(methodology_table(rows, [36 * mm, 62 * mm, 47 * mm, 35 * mm]))

    story.append(PageBreak())
    story.append(p("Squad Movement & Development", h1))
    rows = [
        [p("Calculation", cell), p("Formula / Logic", cell), p("Meaning", cell), p("Important Limitation", cell)],
        [p("Squad Level", cell), p("Foundation=1, Junior=2, Development=3, Transition=4, Advanced=5, IA=6, First Team=7. RTD Pro, External Pros, and US Students are outcome states at level 8.", cell_small), p("Creates a developmental hierarchy for progression analysis.", cell_small), p("Girls Squad is not forced into the male hierarchy and needs pathway-specific interpretation.", cell_small)],
        [p("Previous / Next Squad", cell), p("For each matched player, observations are sorted by date, then previous and next squad are calculated.", cell_small), p("Reconstructs movement through the academy over time.", cell_small), p("Depends on the quality and completeness of observation dates.", cell_small)],
        [p("Squad Level Change", cell), p("Current squad level minus previous squad level.", cell_small), p("Positive means upward movement, negative means regression, zero means no level change.", cell_small), p("Not every valid pathway is strictly linear.", cell_small)],
        [p("Movement Type", cell), p("First observation, Promotion, Regression, No Change, Professional Transition, or Education Transition.", cell_small), p("Makes the Sankey and monthly movement views interpretable.", cell_small), p("A movement event is an observed record change, not necessarily the exact decision date.", cell_small)],
        [p("Months In Previous Squad", cell), p("Days between current and previous observation divided by 30.44.", cell_small), p("Approximates how long a player spent in the previous squad before the next observation.", cell_small), p("Observation cadence affects precision.", cell_small)],
        [p("Development Velocity", cell), p("Highest squad level divided by years observed. Years observed is latest observation minus first observation, with a 0.1 year minimum to avoid division by zero.", cell_small), p("Directional indicator of how quickly a player has moved through the observed squad hierarchy.", cell_small), p("Not a full performance metric. It should be read with observation count and age context.", cell_small)],
    ]
    story.append(methodology_table(rows, [35 * mm, 66 * mm, 45 * mm, 34 * mm]))

    story.append(p("Recruitment & Source Effectiveness", h1))
    rows = [
        [p("Calculation", cell), p("How It Is Built", cell), p("What It Translates To", cell), p("Caution", cell)],
        [p("Players Recruited", cell), p("Count of players grouped by source type: region, hometown, entry club, or nationality.", cell_small), p("Shows recruitment volume by source.", cell_small), p("Volume alone does not prove source quality.", cell_small)],
        [p("Advanced+ %", cell), p("Share of players from the source whose highest squad level is 5 or above.", cell_small), p("Shows how often a source has produced players reaching Advanced Squad or higher.", cell_small), p("Small samples can make percentages unstable.", cell_small)],
        [p("IA+ %", cell), p("Share of players from the source whose highest squad level is 6 or above.", cell_small), p("Shows deeper progression toward IA and beyond.", cell_small), p("Requires reliable squad movement matching.", cell_small)],
        [p("Professional Outcome %", cell), p("Share of players categorised as Professional Football or External Professional.", cell_small), p("Indicates known professional pathway outcomes.", cell_small), p("Known outcomes may be incomplete.", cell_small)],
        [p("Education Outcome %", cell), p("Share of players categorised as US Education.", cell_small), p("Indicates education pathway outcomes.", cell_small), p("Education pathway labels depend on source data quality.", cell_small)],
        [p("Average Known Market Value", cell), p("Average market value among records where market value exists.", cell_small), p("Directional commercial signal for known valued players.", cell_small), p("Coverage is low, so this is not total academy valuation.", cell_small)],
    ]
    story.append(methodology_table(rows, [35 * mm, 58 * mm, 51 * mm, 36 * mm]))

    story.append(PageBreak())
    story.append(p("Recruitment Success Index", h1))
    story.append(p("The Recruitment Success Index, or RSI, is a directional source/player outcome indicator. It must not be called a talent score and must not be treated as objective truth.", body))
    rows = [
        [p("Component", cell), p("Weight", cell), p("How It Is Calculated", cell), p("Interpretation", cell)],
        [p("Squad Progression", cell), p("30%", cell), p("Highest squad level / 8 x 30.", cell_small), p("Rewards players who have reached higher levels or outcome states.", cell_small)],
        [p("Football Rating", cell), p("25%", cell), p("Football rating score / 5 x 25.", cell_small), p("Adds current football assessment where available.", cell_small)],
        [p("Development Velocity", cell), p("20%", cell), p("Development velocity capped at 8, then / 8 x 20.", cell_small), p("Rewards faster observed progression while limiting extreme values.", cell_small)],
        [p("Market Value Percentile", cell), p("10%", cell), p("Market value percentile x 10, missing values receive no market-value contribution.", cell_small), p("Adds a directional external/commercial signal where known.", cell_small)],
        [p("Pathway Outcome", cell), p("15%", cell), p("Adds 15 points if pathway outcome is Professional Football, External Professional, or First Team.", cell_small), p("Recognises high-value pathway destinations.", cell_small)],
    ]
    story.append(methodology_table(rows, [39 * mm, 20 * mm, 66 * mm, 55 * mm]))

    story.append(p("Evidence Strength", h1))
    rows = [
        [p("Classification", cell), p("Rule", cell), p("What It Means", cell)],
        [p("INSUFFICIENT", cell), p("Sample size below 3.", cell_small), p("Do not recommend action from this alone.", cell_small)],
        [p("WEAK", cell), p("Sample size below 8 or completeness below 45%.", cell_small), p("Directional signal only.", cell_small)],
        [p("MODERATE", cell), p("Sample size below 15 or completeness below 70%.", cell_small), p("Useful for investigation, still requires context.", cell_small)],
        [p("STRONG", cell), p("Sample size 15+ and completeness 70%+.", cell_small), p("More reliable for decision-support, still not causal proof.", cell_small)],
    ]
    story.append(methodology_table(rows, [42 * mm, 64 * mm, 74 * mm]))

    story.append(p("Geographic Concentration & Diversity", h1))
    rows = [
        [p("Calculation", cell), p("Formula", cell), p("Translation", cell), p("Caution", cell)],
        [p("Recruitment Share", cell), p("Players in region / total players.", cell_small), p("Shows how much of the academy population comes from each region.", cell_small), p("Share is affected by current recruitment strategy and data completeness.", cell_small)],
        [p("Concentration HHI", cell), p("Sum of squared regional shares.", cell_small), p("Higher value means recruitment is more concentrated in fewer regions.", cell_small), p("It does not prove other regions lack talent.", cell_small)],
        [p("Geographic Diversity Index", cell), p("(1 - concentration HHI) x 100.", cell_small), p("Higher value means recruitment is more geographically diversified.", cell_small), p("Diversity is a footprint measure, not a performance outcome.", cell_small)],
    ]
    story.append(methodology_table(rows, [38 * mm, 43 * mm, 58 * mm, 41 * mm]))

    story.append(p("Dashboard KPI Translations", h1))
    story.append(
        bullets(
            [
                "<b>Total Players:</b> count of player master records in the current filter context.",
                "<b>Active Players:</b> players with no exit date.",
                "<b>Female %:</b> female players divided by total players in the current filter context.",
                "<b>International Players:</b> players whose nationality is not Ghana.",
                "<b>Known Market Value:</b> sum of market value where available; missing values are not zero.",
                "<b>Valuation Coverage:</b> percentage of players with a market value present.",
                "<b>Regions Represented:</b> distinct player-origin regions in the filtered data.",
            ],
            body,
        )
    )

    story.append(p("How To Read Recommendations", h1))
    story.append(p("Recommendation cards are decision-support prompts. They should be read as: what the data shows, why it may matter, what could be investigated next, and how confident the evidence is. They do not replace scout, coach, or leadership judgement.", body))

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT_PATH)
