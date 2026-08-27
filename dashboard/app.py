from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE_PATH = ROOT / "warehouse" / "bi_system.sqlite"
MARTS_DIR = ROOT / "data" / "marts"
LOGO_PATH = ROOT / "assets" / "right_to_dream_logo.png"

BRAND = {
    "bg": "#050706",
    "surface": "#0b1512",
    "surface_2": "#10231d",
    "primary": "#10a068",
    "primary_dark": "#0b6f49",
    "accent": "#f8f8f8",
    "green": "#5fe38b",
    "amber": "#ffbf47",
    "red": "#ff6b6b",
    "text": "#f8f8f8",
    "muted": "#aab8b1",
    "border": "rgba(255,255,255,.08)",
}

SQUAD_COLORS = {
    "Foundation Squad": "#6da9ff",
    "Junior Squad": "#58c7f3",
    "Development Squad": "#30d5c8",
    "Transition Squad": "#5fe38b",
    "Advanced Squad": "#d7ff3f",
    "IA Squad": "#ffdf5d",
    "First Team": "#ff9f43",
    "RTD Pro": "#ff6b6b",
    "External Pros": "#d96cff",
    "US Students": "#b0b8c1",
    "Girls Squad": "#ff7ac8",
}

PAGE_INTROS = {
    "Command Centre": ("How healthy is the Right to Dream talent system today?", "DATA -> INSIGHT -> DIAGNOSIS -> RECOMMENDATION -> ACTION"),
    "Recruitment Landscape": ("Where are we finding talent?", "Geographic recruitment footprint, concentration, and coverage."),
    "Recruitment Opportunities": ("Where should we investigate next?", "A decision-support view, not proof of hidden talent."),
    "Source Effectiveness": ("Who produces our strongest outcomes?", "Compare regions, towns, entry clubs, and nationalities."),
    "Player Development": ("Who is developing?", "Uses ratings, IDP, and squad progression. It is not match-event performance."),
    "Squad Movement": ("How does talent move through Right to Dream?", "Longitudinal movement, transitions, and pathway friction."),
    "Player 360": ("Individual player profile.", "Player journey, origin, peer context, and suggested next review."),
    "Pathways": ("Where does Right to Dream take players?", "Current known pathway and outcome categories."),
    "Women's Intelligence": ("Women's talent intelligence.", "RTD female recruitment and Black Queens reference landscape are kept separate."),
    "Recruitment Advisor": ("What should Right to Dream consider doing next?", "Evidence-based recommendations with confidence labels."),
    "Data Quality": ("How much should we trust the analysis?", "Limitations, completeness, matching, and review queues."),
}

pio.templates["rtd_powerbi"] = go.layout.Template(
    layout={
        "paper_bgcolor": BRAND["surface"],
        "plot_bgcolor": BRAND["surface"],
        "font": {"family": "Avenir Next, Helvetica Neue, Arial, sans-serif", "color": BRAND["text"], "size": 12},
        "colorway": [
            BRAND["primary"],
            "#111111",
            "#4d7ea8",
            "#d99000",
            "#6e5aa8",
            "#2da86b",
            "#c94444",
            "#7f8a85",
        ],
        "margin": {"l": 36, "r": 18, "t": 58, "b": 36},
        "xaxis": {"gridcolor": "rgba(255,255,255,.08)", "zerolinecolor": "rgba(255,255,255,.12)", "linecolor": "rgba(255,255,255,.12)"},
        "yaxis": {"gridcolor": "rgba(255,255,255,.08)", "zerolinecolor": "rgba(255,255,255,.12)", "linecolor": "rgba(255,255,255,.12)"},
        "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    }
)
pio.templates.default = "rtd_powerbi"


@st.cache_data
def read_table(table_name: str, warehouse_mtime: float) -> pd.DataFrame:
    if WAREHOUSE_PATH.exists():
        with sqlite3.connect(WAREHOUSE_PATH) as con:
            return pd.read_sql_query(f"select * from {table_name}", con)

    csv_path = MARTS_DIR / f"{table_name}.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)

    return pd.DataFrame()


def add_theme() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        :root {{
            --rtd-green: {BRAND["primary"]};
            --rtd-green-dark: {BRAND["primary_dark"]};
            --rtd-black: {BRAND["accent"]};
            --rtd-bg: {BRAND["bg"]};
            --rtd-surface: {BRAND["surface"]};
            --rtd-border: {BRAND["border"]};
            --rtd-muted: {BRAND["muted"]};
        }}
        .stApp {{
            background: {BRAND["bg"]};
            color: {BRAND["text"]};
            font-family: "Inter", "Avenir Next", "Helvetica Neue", Arial, sans-serif;
        }}
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #050706 0%, #0b1512 100%);
            border-right: 1px solid rgba(16,160,104,.28);
        }}
        h1, h2, h3, h4, h5, h6, p, label, span, div {{
            letter-spacing: 0 !important;
            font-family: "Inter", "Avenir Next", "Helvetica Neue", Arial, sans-serif;
        }}
        h1, h2, h3 {{
            color: var(--rtd-black);
            font-weight: 800;
        }}
        [data-testid="stSidebar"] img {{
            display: block;
            margin: 8px auto 18px auto;
        }}
        [data-testid="stSidebar"] h3 {{
            color: var(--rtd-black);
            font-size: 13px;
            text-transform: uppercase;
            border-top: 4px solid var(--rtd-green);
            padding-top: 12px;
        }}
        [data-testid="stSidebar"] [role="radiogroup"] label {{
            border-radius: 4px;
            padding: 5px 8px;
        }}
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
            background: rgba(16,160,104,.16);
        }}
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stCaption {{
            color: var(--rtd-muted);
        }}
        .hero {{
            padding: 18px 22px;
            background: linear-gradient(135deg, rgba(16,160,104,.18), rgba(248,248,248,.04));
            border-top: 5px solid var(--rtd-green);
            border-left: 1px solid rgba(16,160,104,.32);
            border-right: 1px solid rgba(16,160,104,.32);
            border-bottom: 1px solid rgba(16,160,104,.32);
            border-radius: 2px;
            margin-bottom: 14px;
            box-shadow: 0 1px 2px rgba(17, 17, 17, .05);
        }}
        .hero .brand {{
            color: var(--rtd-green-dark);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
        }}
        .hero .title {{
            color: {BRAND["text"]};
            font-size: 26px;
            font-weight: 850;
            margin-top: 4px;
        }}
        .hero .question {{
            color: {BRAND["muted"]};
            font-size: 13px;
            margin-top: 8px;
        }}
        .kpi {{
            background: {BRAND["surface"]};
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 2px;
            padding: 14px 15px;
            min-height: 102px;
            box-shadow: 0 1px 2px rgba(17, 17, 17, .05);
        }}
        .kpi .label {{
            color: {BRAND["muted"]};
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
        }}
        .kpi .value {{
            color: {BRAND["text"]};
            font-size: 27px;
            font-weight: 850;
            margin-top: 6px;
        }}
        .kpi .context {{
            color: {BRAND["muted"]};
            font-size: 11px;
            margin-top: 8px;
        }}
        .insight {{
            background: {BRAND["surface_2"]};
            border: 1px solid rgba(255,255,255,.08);
            border-left: 5px solid var(--rtd-green);
            border-radius: 2px;
            padding: 14px 16px;
            margin: 10px 0;
            box-shadow: 0 1px 2px rgba(17, 17, 17, .05);
        }}
        .tag {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 2px;
            background: rgba(16,160,104,.20);
            color: var(--rtd-green);
            font-size: 10px;
            font-weight: 800;
            margin-right: 6px;
        }}
        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }}
        [data-testid="stMetric"], [data-testid="stDataFrame"], .stPlotlyChart {{
            background: {BRAND["surface"]};
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 2px;
            padding: 8px;
            box-shadow: 0 1px 2px rgba(17, 17, 17, .05);
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            border-bottom: 1px solid rgba(255,255,255,.08);
        }}
        .stTabs [data-baseweb="tab"] {{
            background: {BRAND["surface"]};
            border: 1px solid rgba(255,255,255,.08);
            border-bottom: none;
            border-radius: 2px 2px 0 0;
            padding: 8px 12px;
            color: var(--rtd-muted);
        }}
        button[kind="primary"], .stButton > button {{
            background: var(--rtd-green);
            color: #ffffff;
            border-radius: 2px;
            border: 1px solid var(--rtd-green-dark);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(page: str) -> None:
    question, context = PAGE_INTROS[page]
    st.markdown(
        f"""
        <div class="hero">
            <div class="brand">RIGHT TO DREAM TALENT INTELLIGENCE</div>
            <div class="title">{page}</div>
            <div class="question"><b>{question}</b><br>{context}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi(label: str, value: str, context: str = "") -> None:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="context">{context}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(title: str, fact: str, interpretation: str, recommendation: str) -> None:
    st.markdown(
        f"""
        <div class="insight">
            <span class="tag">FACT</span><b>{title}</b><br>{fact}<br><br>
            <span class="tag">INTERPRETATION</span>{interpretation}<br><br>
            <span class="tag">RECOMMENDATION</span>{recommendation}
        </div>
        """,
        unsafe_allow_html=True,
    )


def fmt_number(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:,.0f}"


def fmt_pct(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"{value * 100:.0f}%"


def apply_filters(players: pd.DataFrame) -> pd.DataFrame:
    filtered = players.copy()
    if selected_genders:
        filtered = filtered[filtered["gender"].isin(selected_genders)]
    if selected_regions:
        filtered = filtered[filtered["region"].isin(selected_regions)]
    if selected_squads:
        filtered = filtered[filtered["current_squad"].isin(selected_squads)]
    if selected_pathways:
        filtered = filtered[filtered["current_pathway"].isin(selected_pathways)]
    if selected_ratings:
        filtered = filtered[filtered["football_rating"].isin(selected_ratings)]
    return filtered


st.set_page_config(page_title="Right to Dream Talent Intelligence", layout="wide")
add_theme()

warehouse_mtime = WAREHOUSE_PATH.stat().st_mtime if WAREHOUSE_PATH.exists() else 0

players = read_table("dim_player", warehouse_mtime)
movement = read_table("fact_squad_movement", warehouse_mtime)
source_effectiveness = read_table("mart_source_effectiveness", warehouse_mtime)
summary = read_table("mart_dashboard_summary", warehouse_mtime)
black_queens = read_table("mart_black_queens", warehouse_mtime)
region_concentration = read_table("mart_region_concentration", warehouse_mtime)
dim_squad = read_table("dim_squad", warehouse_mtime)

if players.empty:
    st.warning("No warehouse data found. Run `python -m etl.load_raw` and `python -m etl.run_models` first.")
    st.stop()

metric = dict(zip(summary["metric"], summary["value"]))

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=132)
    st.markdown("### TALENT INTELLIGENCE")
    page = st.radio(
        "Navigation",
        list(PAGE_INTROS.keys()),
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("#### Global Filters")
    selected_genders = st.multiselect("Gender", sorted(players["gender"].dropna().unique()), default=sorted(players["gender"].dropna().unique()))
    selected_regions = st.multiselect("Region", sorted(players["region"].dropna().unique()), default=sorted(players["region"].dropna().unique()))
    selected_squads = st.multiselect("Squad", sorted(players["current_squad"].dropna().unique()))
    selected_pathways = st.multiselect("Pathway", sorted(players["current_pathway"].dropna().unique()))
    selected_ratings = st.multiselect("Football Rating", sorted(players["football_rating"].dropna().unique()))
    st.caption("Reset filters by clearing selections or using the page refresh.")

filtered = apply_filters(players)
movement_filtered = movement[movement["player_id"].isin(filtered["player_id"])]

hero(page)

if page == "Command Centre":
    cols = st.columns(4)
    with cols[0]:
        kpi("Total Players", fmt_number(len(filtered)), "Filtered academy population")
    with cols[1]:
        kpi("Active Players", fmt_number(filtered["is_active"].sum()), "Players without exit date")
    with cols[2]:
        kpi("Average Entry Age", f"{filtered['entry_age'].dropna().mean():.1f}", "Valid records only")
    with cols[3]:
        female_pct = filtered["gender"].str.lower().eq("female").mean() if len(filtered) else 0
        kpi("Female %", f"{female_pct * 100:.0f}%", "Filtered player population")

    cols = st.columns(4)
    with cols[0]:
        kpi("Regions Represented", fmt_number(filtered["region"].nunique()), "Recruitment footprint")
    with cols[1]:
        kpi("Known Market Value", f"${filtered['market_value'].sum(skipna=True):,.0f}", "Only records with valuation")
    with cols[2]:
        coverage = filtered["market_value"].notna().mean() if len(filtered) else 0
        kpi("Valuation Coverage", f"{coverage * 100:.0f}%", "Missing values are not zero")
    with cols[3]:
        attention = filtered["development_status"].isin(["WATCH", "AT RISK"]).sum()
        kpi("Review Attention", fmt_number(attention), "Watch or at-risk indicators")

    left, right = st.columns([1.2, 1])
    pipeline = filtered.groupby("current_squad", as_index=False).size().rename(columns={"size": "players"})
    pipeline = pipeline.merge(dim_squad, left_on="current_squad", right_on="squad", how="left").sort_values("squad_level")
    left.plotly_chart(
        px.bar(
            pipeline,
            x="current_squad",
            y="players",
            color="current_squad",
            color_discrete_map=SQUAD_COLORS,
            title="Talent Pipeline",
        ),
        use_container_width=True,
    )
    region_top = filtered.groupby("region", as_index=False).size().rename(columns={"size": "players"}).sort_values("players", ascending=False)
    right.plotly_chart(px.bar(region_top.head(8), x="players", y="region", orientation="h", title="Top Recruitment Regions"), use_container_width=True)

    top3_share = region_top.head(3)["players"].sum() / len(filtered) if len(filtered) else 0
    insight(
        "Executive Insight",
        f"The top three regions represent {top3_share * 100:.0f}% of the currently filtered player population.",
        "A high share can indicate a productive recruitment footprint, but also potential concentration risk.",
        "Review whether underrepresented regions have enough scouting evidence before treating them as opportunities.",
    )

elif page == "Recruitment Landscape":
    map_data = filtered.dropna(subset=["latitude", "longitude"])
    st.plotly_chart(
        px.scatter_mapbox(
            map_data,
            lat="latitude",
            lon="longitude",
            color="region",
            size="recruitment_success_index",
            hover_name="player_name",
            hover_data=["hometown", "entry_club", "entry_age", "football_rating", "development_velocity"],
            zoom=5,
            height=640,
            title="Recruitment Geography: Player Locations",
        ).update_layout(mapbox_style="carto-darkmatter"),
        use_container_width=True,
    )
    st.dataframe(region_concentration.sort_values("players", ascending=False), use_container_width=True, hide_index=True)
    hhi = (region_concentration["share"] ** 2).sum()
    insight(
        "Geographic Concentration",
        f"Recruitment concentration index is {hhi:.3f}; lower values indicate broader geographic spread.",
        "This is a concentration signal, not proof that unrecruited regions contain missed elite talent.",
        "Pair this with external scouting data such as youth participation, clubs, and scout visits before reallocating resources.",
    )

elif page == "Recruitment Opportunities":
    region_sources = source_effectiveness[source_effectiveness["source_type"].eq("region")].copy()
    benchmark = region_sources["recruitment_success_index"].median()
    region_sources["opportunity_zone"] = "Limited Evidence"
    region_sources.loc[(region_sources["players_recruited"] >= 8) & (region_sources["recruitment_success_index"] >= benchmark), "opportunity_zone"] = "Protect & Invest"
    region_sources.loc[(region_sources["players_recruited"] < 8) & (region_sources["recruitment_success_index"] >= benchmark), "opportunity_zone"] = "Expansion Opportunity"
    region_sources.loc[(region_sources["players_recruited"] >= 8) & (region_sources["recruitment_success_index"] < benchmark), "opportunity_zone"] = "Review Strategy"
    st.plotly_chart(
        px.scatter(
            region_sources,
            x="players_recruited",
            y="recruitment_success_index",
            size="advanced_plus_pct",
            color="opportunity_zone",
            hover_name="source_name",
            hover_data=["average_entry_age", "professional_outcome_pct", "evidence_strength"],
            title="Recruitment Opportunity Matrix",
        ),
        use_container_width=True,
    )
    st.dataframe(region_sources.sort_values("recruitment_success_index", ascending=False), use_container_width=True, hide_index=True)

elif page == "Source Effectiveness":
    source_type = st.segmented_control("Source Type", ["region", "hometown", "entry_club", "nationality"], default="region")
    table = source_effectiveness[source_effectiveness["source_type"].eq(source_type)].sort_values("recruitment_success_index", ascending=False)
    st.plotly_chart(
        px.bar(table.head(15), x="recruitment_success_index", y="source_name", orientation="h", color="evidence_strength", title="Recruitment Success Index by Source"),
        use_container_width=True,
    )
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.caption("Initial RSI weights: 30% squad progression, 25% football rating, 20% development velocity, 15% pathway outcome, 10% market value percentile. These are configurable assumptions, not objective truth.")

elif page == "Player Development":
    dev = filtered.copy()
    dev["known_market_value"] = dev["market_value"]
    dev["bubble_size"] = dev["market_value"].fillna(0)
    if dev["bubble_size"].max() <= 0:
        dev["bubble_size"] = 1
    else:
        baseline = max(dev["bubble_size"].max() * 0.03, 1)
        dev["bubble_size"] = dev["bubble_size"].replace(0, baseline)
    st.plotly_chart(
        px.scatter(
            dev,
            x="development_velocity",
            y="football_rating_score",
            size="bubble_size",
            color="development_status",
            hover_name="player_name",
            hover_data={
                "current_squad": True,
                "entry_age": True,
                "academic_rating": True,
                "promotions": True,
                "data_quality_class": True,
                "known_market_value": ":,.0f",
                "bubble_size": False,
            },
            title="Development Matrix",
        ),
        use_container_width=True,
    )
    st.dataframe(
        dev[["player_name", "current_age", "current_squad", "football_rating", "academic_rating", "idp_progress", "promotions", "development_velocity", "current_pathway", "current_flag"]].sort_values("development_velocity", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

elif page == "Squad Movement":
    transitions = movement_filtered.dropna(subset=["previous_squad"])
    transitions = transitions.copy()
    transitions["movement_month"] = pd.to_datetime(transitions["observation_date"], errors="coerce").dt.to_period("M").astype(str)
    month_counts = transitions.groupby("movement_month", as_index=False).size().rename(columns={"size": "movement_events"})
    selected_month = st.select_slider(
        "Movement Month",
        options=month_counts["movement_month"].tolist(),
        value=month_counts["movement_month"].max(),
    )
    view_mode = st.segmented_control("Sankey View", ["Selected Month", "All Time"], default="Selected Month")
    sankey_source = transitions if view_mode == "All Time" else transitions[transitions["movement_month"].eq(selected_month)]
    st.plotly_chart(
        px.bar(
            month_counts,
            x="movement_month",
            y="movement_events",
            title="Squad Movement Events by Month",
        ),
        use_container_width=True,
    )
    matrix = sankey_source.groupby(["previous_squad", "squad"], as_index=False).size().rename(columns={"size": "movements"})
    if matrix.empty:
        st.info("No squad transitions found for the selected month and filters.")
        st.stop()
    labels = sorted(set(matrix["previous_squad"]).union(matrix["squad"]))
    index = {label: i for i, label in enumerate(labels)}
    sankey = go.Figure(
        data=[
            go.Sankey(
                node={"label": labels, "color": [SQUAD_COLORS.get(label, BRAND["muted"]) for label in labels]},
                link={
                    "source": matrix["previous_squad"].map(index),
                    "target": matrix["squad"].map(index),
                    "value": matrix["movements"],
                },
            )
        ]
    )
    title_suffix = "All Time" if view_mode == "All Time" else selected_month
    sankey.update_layout(
        title_text=f"Squad Transition Flow: {title_suffix}",
        paper_bgcolor=BRAND["surface"],
        plot_bgcolor=BRAND["surface"],
        font_color=BRAND["text"],
        margin={"l": 18, "r": 18, "t": 58, "b": 18},
    )
    st.plotly_chart(sankey, use_container_width=True)
    st.dataframe(matrix.sort_values("movements", ascending=False), use_container_width=True, hide_index=True)

elif page == "Player 360":
    query = st.text_input("Search Player", "")
    options = filtered["player_name"].sort_values().tolist()
    if query:
        options = [name for name in options if query.lower() in name.lower()]
    selected_player = st.selectbox("Select Player", options)
    player = filtered[filtered["player_name"].eq(selected_player)].iloc[0]
    cols = st.columns(4)
    with cols[0]:
        kpi("Current Squad", str(player["current_squad"]), "Latest master record")
    with cols[1]:
        kpi("Age", f"{player['current_age']:.1f}", str(player["nationality"]))
    with cols[2]:
        kpi("Football Rating", str(player["football_rating"]), "Mapped score shown in data")
    with cols[3]:
        kpi("Development Velocity", f"{player['development_velocity']:.2f}", "Levels per observed year")
    journey = movement[movement["player_id"].eq(player["player_id"])].sort_values("observation_date")
    st.plotly_chart(px.line(journey, x="observation_date", y="squad_level", color="squad", markers=True, hover_data=["squad"], title="Player Journey"), use_container_width=True)
    insight(
        "Recommended Action",
        f"{player['player_name']} has development status: {player['development_status']} and data quality: {player['data_quality_class']}.",
        "Recommendations should account for observation history, age, squad context, and missing data.",
        "Use this profile as a review prompt for coaches/scouts, not as an automated judgement.",
    )

elif page == "Pathways":
    pathway = filtered.groupby("pathway_outcome", as_index=False).size().rename(columns={"size": "players"}).sort_values("players", ascending=False)
    st.plotly_chart(px.bar(pathway, x="pathway_outcome", y="players", title="Known Pathway Outcomes"), use_container_width=True)
    st.dataframe(filtered[["player_name", "current_pathway", "pathway_outcome", "region", "entry_club", "highest_squad_level"]], use_container_width=True, hide_index=True)

elif page == "Women's Intelligence":
    female = filtered[filtered["gender"].str.lower().eq("female")]
    cols = st.columns(3)
    with cols[0]:
        kpi("Female Players", fmt_number(len(female)), "RTD player master")
    with cols[1]:
        kpi("Girls Squad", fmt_number(female["current_squad"].eq("Girls Squad").sum()), "Current squad label")
    with cols[2]:
        kpi("Black Queens Reference", fmt_number(len(black_queens)), "Not assumed RTD outcomes")
    left, right = st.columns(2)
    left.plotly_chart(px.bar(female.groupby("region", as_index=False).size(), x="region", y="size", title="RTD Female Recruitment Geography"), use_container_width=True)
    right.plotly_chart(px.bar(black_queens.groupby("region", as_index=False).size(), x="region", y="size", title="Black Queens Reference Landscape"), use_container_width=True)
    st.dataframe(black_queens, use_container_width=True, hide_index=True)

elif page == "Recruitment Advisor":
    candidates = source_effectiveness[
        (source_effectiveness["source_type"].eq("region"))
        & (source_effectiveness["evidence_strength"].isin(["MODERATE", "STRONG"]))
    ].sort_values("recruitment_success_index", ascending=False)
    for _, row in candidates.head(5).iterrows():
        insight(
            f"SCOUT MORE / PROTECT: {row['source_name']}",
            f"{int(row['players_recruited'])} players; RSI {row['recruitment_success_index']:.1f}; Advanced+ {row['advanced_plus_pct'] * 100:.0f}%.",
            f"Evidence strength is {row['evidence_strength']}. This suggests a source worth structured review, not a causal claim.",
            "Review scouting coverage, player histories, and external market evidence before changing recruitment allocation.",
        )
    st.caption("Automated advice is decision support. It does not replace scout, coach, or leadership judgement.")

elif page == "Data Quality":
    quality = filtered.groupby("data_quality_class", as_index=False).size().rename(columns={"size": "players"})
    st.plotly_chart(px.bar(quality, x="data_quality_class", y="players", color="data_quality_class", title="Player Data Quality Classification"), use_container_width=True)
    cols = st.columns(4)
    with cols[0]:
        kpi("Market Coverage", f"{filtered['market_value'].notna().mean() * 100:.0f}%", "Directional only")
    with cols[1]:
        kpi("Coordinates Coverage", f"{filtered[['latitude', 'longitude']].notna().all(axis=1).mean() * 100:.0f}%", "Map reliability")
    with cols[2]:
        kpi("Squad History Coverage", f"{filtered['observation_count'].notna().mean() * 100:.0f}%", "Movement matching")
    with cols[3]:
        kpi("Review Required", fmt_number(filtered["data_quality_class"].eq("REVIEW REQUIRED").sum()), "Potentially invalid fields")
    st.dataframe(
        filtered[["player_id", "player_name", "data_quality_score", "data_quality_class", "entry_age", "position", "region", "football_rating", "academic_rating", "idp_progress"]].sort_values("data_quality_score"),
        use_container_width=True,
        hide_index=True,
    )
