from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
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
OUTPUT_PATH = OUTPUT_DIR / "navant_rtd_tech_stack_recommendation.pdf"
LOGO_PATH = ROOT / "assets" / "navant_group_logo.png"

BLACK = colors.HexColor("#101010")
GREEN = colors.HexColor("#10a068")
GREY = colors.HexColor("#f4f5f4")
LIGHT_GREEN = colors.HexColor("#e8f7f0")
TEXT = colors.HexColor("#1d2522")
MUTED = colors.HexColor("#5d6a64")


def para(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=8) for item in items],
        bulletType="bullet",
        leftIndent=15,
        spaceAfter=5,
    )


def table(rows, widths, header=True):
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLACK if header else GREY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white if header else TEXT),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), GREY),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d3d8d5")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def build_pdf():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=13 * mm,
        bottomMargin=13 * mm,
        title="RTD Talent Intelligence Tech Stack Recommendation",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title", parent=styles["Title"], fontSize=21, leading=25, alignment=TA_CENTER, textColor=BLACK)
    notice = ParagraphStyle("Notice", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=14, alignment=TA_CENTER, textColor=colors.white)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=MUTED)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=14, leading=18, textColor=BLACK, spaceBefore=11, spaceAfter=5)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11, leading=14, textColor=GREEN, spaceBefore=8, spaceAfter=4)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=8.7, leading=12.2, textColor=TEXT, spaceAfter=4)
    small = ParagraphStyle("Small", parent=body, fontSize=7.5, leading=10, textColor=MUTED)
    cell = ParagraphStyle("Cell", parent=body, fontSize=7.2, leading=9.4, textColor=TEXT)
    cell_small = ParagraphStyle("CellSmall", parent=cell, fontSize=6.8, leading=8.8, textColor=TEXT)

    story = []
    story.append(
        Table(
            [[para("<b>Internal use only - not to be distributed</b>", notice)]],
            colWidths=[180 * mm],
            style=[
                ("BACKGROUND", (0, 0), (-1, -1), BLACK),
                ("BOX", (0, 0), (-1, -1), 1, BLACK),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ],
        )
    )
    story.append(Spacer(1, 8))
    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=70 * mm, height=47 * mm)
        logo.hAlign = "CENTER"
        story.append(logo)
    story.append(para("Right to Dream Talent Intelligence", title))
    story.append(para("Production Tech Stack Recommendation for Contract Delivery", subtitle))
    story.append(Spacer(1, 8))

    story.append(para("Executive Recommendation", h1))
    story.append(
        para(
            "The current MVP proves the concept, but the production solution should move beyond a local Streamlit and SQLite setup. A winning contract should be delivered as a governed cloud data platform with automated integrations, trusted analytical models, secure access, and dashboards tailored to executives, coaches, analysts, recruitment teams, and scouts.",
            body,
        )
    )
    story.append(
        para(
            "<b>Recommended production route:</b> Airbyte Cloud or Fivetran -> BigQuery -> dbt -> Power BI, with a custom React/Next.js and FastAPI application added later for premium Player 360 and scouting workflows.",
            body,
        )
    )

    story.append(para("Recommended Stack", h1))
    rows = [
        [para("Layer", cell), para("Recommended Tool", cell), para("Purpose", cell), para("Alternatives", cell)],
        [para("Ingestion", cell), para("Airbyte Cloud or Fivetran", cell), para("Connect scouting systems, player management systems, databases, APIs, files, and SaaS tools.", cell_small), para("Custom Python connectors, Stitch, Meltano.", cell_small)],
        [para("Warehouse", cell), para("BigQuery or Snowflake", cell), para("Central, secure, scalable analytics database.", cell_small), para("MotherDuck, Postgres, Microsoft Fabric.", cell_small)],
        [para("Transformation", cell), para("dbt", cell), para("Version-controlled models, tests, lineage, and repeatable business definitions.", cell_small), para("SQLMesh, Dataform, stored procedures.", cell_small)],
        [para("Dashboards", cell), para("Power BI or Tableau", cell), para("Governed executive and operational dashboards.", cell_small), para("Metabase, Superset, custom React dashboards.", cell_small)],
        [para("Custom Product Layer", cell), para("React/Next.js + FastAPI", cell), para("Player 360, scouting workflows, notes, action queues, and decision-support features.", cell_small), para("Retool, Streamlit, Dash.", cell_small)],
        [para("Orchestration", cell), para("Dagster, Prefect, Airflow, or dbt Cloud jobs", cell), para("Scheduled pipelines, retries, monitoring, and alerts.", cell_small), para("Cloud scheduler, cron, managed vendor jobs.", cell_small)],
        [para("Identity & Security", cell), para("Microsoft Entra ID or Google Workspace SSO", cell), para("Role-based access for executives, coaches, scouts, and analysts.", cell_small), para("Auth0, Okta, Clerk.", cell_small)],
    ]
    story.append(table(rows, [28 * mm, 42 * mm, 68 * mm, 42 * mm]))

    story.append(para("Option 1 - Lean, Cost-Effective Stack", h1))
    story.append(para("Best when the client wants a professional system quickly, with sensible cost control and a clear path to scale.", body))
    rows = [
        [para("Layer", cell), para("Tool", cell), para("Indicative Pricing", cell)],
        [para("Ingestion", cell), para("Airbyte Cloud", cell), para("Starts at about $10/month, then usage-based. API sources from about $15 per million rows; file/database sources around $10 per GB synced.", cell_small)],
        [para("Warehouse", cell), para("BigQuery", cell), para("First 1 TiB of queries/month free, then about $6.25 per TiB processed. Storage varies by region and usage.", cell_small)],
        [para("Transformation", cell), para("dbt Core", cell), para("Open-source/free, but requires engineering setup and ownership.", cell_small)],
        [para("BI", cell), para("Power BI Pro", cell), para("$14/user/month, paid yearly. 20 users = about $280/month.", cell_small)],
        [para("Jobs/Hosting", cell), para("Cloud Run / scheduler", cell), para("Usually low at small scale; budget $20-$200/month initially.", cell_small)],
    ]
    story.append(table(rows, [32 * mm, 43 * mm, 105 * mm]))
    story.append(para("<b>Estimated total:</b> roughly $300-$800/month before implementation, support, and any custom integration work.", body))
    story.append(bullets(["Pros: cost-effective, fast to launch, strong executive dashboard route, good Microsoft/Google compatibility.", "Cons: dbt Core needs technical ownership, Airbyte connectors may need monitoring, Power BI may need design effort to avoid a generic BI feel."], body))

    story.append(PageBreak())
    story.append(para("Option 2 - Enterprise Reliability Stack", h1))
    story.append(para("Best when Right to Dream prioritises reliability, governance, procurement confidence, and long-term global scaling.", body))
    rows = [
        [para("Layer", cell), para("Tool", cell), para("Indicative Pricing", cell)],
        [para("Ingestion", cell), para("Fivetran", cell), para("Free Plan up to 500,000 monthly active rows. Paid plans are usage-based by monthly active rows; annual contracts may apply.", cell_small)],
        [para("Warehouse", cell), para("Snowflake", cell), para("Consumption-based by cloud, edition, region, storage, and compute credits. Requires cost monitoring.", cell_small)],
        [para("Transformation", cell), para("dbt Cloud", cell), para("Developer tier available for individuals; team/enterprise pricing depends on users and features.", cell_small)],
        [para("BI", cell), para("Tableau or Power BI", cell), para("Tableau Standard: Viewer $15, Explorer $42, Creator $75 per user/month billed annually. Power BI Pro: $14/user/month.", cell_small)],
        [para("Orchestration", cell), para("dbt Cloud / Dagster", cell), para("Pricing depends on deployment and team requirements.", cell_small)],
    ]
    story.append(table(rows, [32 * mm, 43 * mm, 105 * mm]))
    story.append(para("<b>Estimated total:</b> roughly $1,000-$5,000/month before implementation and support, depending on users, refresh frequency, and connected systems.", body))
    story.append(bullets(["Pros: high reliability, mature governance, recognised enterprise data stack, strong for multiple academies/countries.", "Cons: higher cost, Snowflake requires cost discipline, Fivetran can become expensive as data changes increase, Tableau can be costly for creator/explorer users."], body))

    story.append(para("Option 3 - Bespoke Football Intelligence Product", h1))
    story.append(para("Best when the client wants a true internal football intelligence platform, not just dashboards.", body))
    rows = [
        [para("Layer", cell), para("Tool", cell), para("Indicative Pricing", cell)],
        [para("Ingestion", cell), para("Airbyte/Fivetran/custom API connectors", cell), para("Usage-based or custom engineering cost, depending on source systems.", cell_small)],
        [para("Warehouse", cell), para("BigQuery, Snowflake, or MotherDuck", cell), para("MotherDuck Business is $250/org/month + usage; storage about $0.04/GB/month; compute from about $0.60/hour Pulse or $2.40/hour Standard in US region.", cell_small)],
        [para("Backend", cell), para("Python FastAPI", cell), para("Open-source; hosting and engineering apply.", cell_small)],
        [para("Frontend", cell), para("React / Next.js", cell), para("Open-source; hosting and engineering apply.", cell_small)],
        [para("Hosting/Auth", cell), para("Vercel/Azure/AWS/GCP + SSO", cell), para("Early hosting often $20-$500+/month; identity cost depends on provider and user count.", cell_small)],
    ]
    story.append(table(rows, [32 * mm, 50 * mm, 98 * mm]))
    story.append(para("<b>Estimated platform total:</b> roughly $300-$2,000/month, but implementation cost is materially higher because this is software product development, not only dashboard delivery.", body))
    story.append(bullets(["Pros: best user experience, true Player 360, scouting notes, action tracking, role-specific workflows, strong differentiation.", "Cons: more engineering, longer delivery timeline, more QA/security responsibility, requires product ownership."], body))

    story.append(para("Tool Alternatives: Pros & Cons", h1))
    rows = [
        [para("Category", cell), para("Tool", cell), para("Pros", cell), para("Cons", cell)],
        [para("BI", cell), para("Power BI", cell), para("Cost-effective, familiar to executives, strong Microsoft security and sharing.", cell_small), para("Can feel generic unless carefully designed.", cell_small)],
        [para("BI", cell), para("Tableau", cell), para("Strong visual analytics and exploratory analysis.", cell_small), para("Higher cost for authors and power users.", cell_small)],
        [para("BI", cell), para("Metabase", cell), para("Simple, fast, cheaper internal analytics.", cell_small), para("Less premium for a bespoke football intelligence product.", cell_small)],
        [para("Warehouse", cell), para("BigQuery", cell), para("Serverless, scalable, low admin.", cell_small), para("Query costs need monitoring.", cell_small)],
        [para("Warehouse", cell), para("Snowflake", cell), para("Excellent enterprise warehouse and governance.", cell_small), para("Requires credit/cost management.", cell_small)],
        [para("Warehouse", cell), para("MotherDuck", cell), para("Elegant path from lightweight analytics to cloud DuckDB-style workflows.", cell_small), para("Newer ecosystem than BigQuery/Snowflake.", cell_small)],
        [para("Ingestion", cell), para("Airbyte", cell), para("Flexible, cost-effective, open-source roots.", cell_small), para("Some connectors need more maintenance.", cell_small)],
        [para("Ingestion", cell), para("Fivetran", cell), para("Very reliable managed connectors.", cell_small), para("Can become expensive with high monthly active rows.", cell_small)],
    ]
    story.append(table(rows, [24 * mm, 34 * mm, 61 * mm, 61 * mm]))

    story.append(PageBreak())
    story.append(para("Suggested Contract Delivery Roadmap", h1))
    story.append(para("<b>Phase 1 - Production BI Foundation:</b> implement Airbyte or Fivetran, BigQuery, dbt, and Power BI. Focus on clean integrations, core data model, executive dashboards, coach dashboards, recruitment dashboards, and data quality monitoring.", body))
    story.append(para("<b>Phase 2 - Bespoke Product Layer:</b> add a custom Next.js/FastAPI platform for Player 360, scouting review queues, notes, action tracking, and role-specific decision support.", body))
    story.append(para("<b>Phase 3 - Advanced Intelligence:</b> add scenario analysis, recruitment coverage modelling, player observation workflows, external scouting evidence, and performance data integrations.", body))

    story.append(para("What To Avoid", h1))
    story.append(
        bullets(
            [
                "Do not keep SQLite/Streamlit as the long-term production system.",
                "Do not connect dashboards directly to messy source systems.",
                "Do not let each department define metrics separately.",
                "Do not call the Recruitment Success Index a talent score.",
                "Do not treat missing values as zero.",
                "Do not infer causality from correlation.",
            ],
            body,
        )
    )

    story.append(para("Final Cost Summary", h1))
    rows = [
        [para("Option", cell), para("Best Fit", cell), para("Indicative Monthly Platform Cost", cell), para("Indicative Annual Platform Cost", cell), para("Implementation Notes", cell)],
        [para("1. Lean Production BI", cell), para("Fast, cost-conscious production foundation.", cell_small), para("$300-$800/month", cell_small), para("$3,600-$9,600/year", cell_small), para("Lowest platform cost; needs technical setup and dashboard design discipline.", cell_small)],
        [para("2. Enterprise Reliability", cell), para("Governance, reliability, procurement confidence, scale.", cell_small), para("$1,000-$5,000/month", cell_small), para("$12,000-$60,000/year", cell_small), para("Strongest enterprise path; higher vendor cost and more cost governance required.", cell_small)],
        [para("3. Bespoke Product", cell), para("Premium internal football intelligence platform.", cell_small), para("$300-$2,000/month platform cost", cell_small), para("$3,600-$24,000/year platform cost", cell_small), para("Platform cost can be moderate, but build cost is much higher due to custom software engineering.", cell_small)],
    ]
    story.append(table(rows, [30 * mm, 45 * mm, 38 * mm, 36 * mm, 31 * mm]))
    story.append(para("Costs are indicative as of August 2026 and exclude implementation labour, support retainer, custom connector development, data migration, procurement taxes, currency conversion, and vendor discounts. Vendor pricing should be revalidated during procurement.", small))

    story.append(para("Pricing Sources To Revalidate", h1))
    story.append(
        bullets(
            [
                "Airbyte: https://airbyte.com/pricing and https://airbyte.com/product/airbyte-cloud",
                "Fivetran: https://www.fivetran.com/pricing",
                "BigQuery: https://cloud.google.com/bigquery/pricing",
                "Power BI: https://www.microsoft.com/en-us/power-platform/products/power-bi/pricing",
                "Tableau: https://www.tableau.com/pricing",
                "Metabase: https://www.metabase.com/upgrade/",
                "MotherDuck: https://motherduck.com/product/pricing/",
                "Snowflake: https://www.snowflake.com/en/pricing-options/",
            ],
            small,
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT_PATH)
