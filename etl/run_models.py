import re
import sqlite3
import unicodedata
from datetime import datetime

import pandas as pd

from etl.config import WAREHOUSE_PATH


RATING_SCORE = {
    "A+": 5,
    "A": 4,
    "B": 3,
    "C": 2,
    "C-": 1,
}

SQUAD_LEVEL = {
    "Foundation Squad": 1,
    "Junior Squad": 2,
    "Development Squad": 3,
    "Transition Squad": 4,
    "Advanced Squad": 5,
    "IA Squad": 6,
    "First Team": 7,
    "RTD Pro": 8,
    "External Pros": 8,
    "US Students": 8,
    "Girls Squad": None,
}

OUTCOME_MAP = {
    "RTD Pro": "Professional Football",
    "External Pros": "External Professional",
    "US Students": "US Education",
    "First Team": "First Team",
}

REGION_FIXES = {
    "northen region": "Northern Region",
    "northern": "Northern Region",
    "greater accra": "Greater Accra Region",
    "brong ahafo": "Brong Ahafo Region",
    "brong-ahafo region": "Brong Ahafo Region",
}

SQUAD_FIXES = {
    "1-Tean": "1-Team",
}


def normalise_name(value: object) -> str:
    if pd.isna(value):
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.lower().replace("'", "").replace("-", " ")
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def standardise_region(value: object) -> object:
    if pd.isna(value):
        return pd.NA
    text = re.sub(r"\s+", " ", str(value)).strip()
    key = text.lower()
    return REGION_FIXES.get(key, text)


def standardise_squad(value: object) -> object:
    if pd.isna(value):
        return pd.NA
    text = re.sub(r"\s+", " ", str(value)).strip()
    return SQUAD_FIXES.get(text, text)


def evidence_strength(sample_size: int, completeness: float = 1.0) -> str:
    if sample_size < 3:
        return "INSUFFICIENT"
    if sample_size < 8 or completeness < 0.45:
        return "WEAK"
    if sample_size < 15 or completeness < 0.70:
        return "MODERATE"
    return "STRONG"


def development_status(row: pd.Series) -> str:
    idp = str(row.get("idp_progress", "")).strip().lower()
    rating = str(row.get("football_rating", "")).strip().upper()
    if idp in {"green", "ahead"} or rating in {"A+", "A"}:
        return "HIGH PERFORMING"
    if idp in {"as expected"} or rating == "B":
        return "ON TRACK"
    if idp in {"orange", "behind"} or rating in {"C", "C-"}:
        return "WATCH"
    if idp == "red":
        return "AT RISK"
    return "INSUFFICIENT DATA"


def pathway_outcome(pathway: object, exit_date: object) -> str:
    if pd.isna(pathway) or str(pathway).strip() == "":
        return "Exited" if pd.notna(exit_date) else "Unknown"
    text = str(pathway).strip()
    lower = text.lower()
    if "student" in lower or "ucla" in lower or "education" in lower:
        return "US Education"
    if "pro" in lower:
        return "Professional Football"
    if "first" in lower:
        return "First Team"
    if "fcn" in lower or "academy" in lower:
        return "Academy Development"
    if pd.notna(exit_date):
        return "Exited"
    return text


def quality_score(row: pd.Series, has_movement: bool) -> tuple[int, str]:
    fields = [
        "dob",
        "entry_date",
        "age_at_entry",
        "entry_club",
        "hometown",
        "region",
        "latitude",
        "longitude",
        "football_rating",
        "academic_rating",
        "idp_progress",
        "pathway",
        "football_squad",
        "basic_market_value",
    ]
    present = sum(pd.notna(row.get(field)) and str(row.get(field)).strip() != "" for field in fields)
    score = round((present + int(has_movement)) / (len(fields) + 1) * 100)
    entry_age = row.get("age_at_entry")
    invalid_age = pd.notna(entry_age) and (float(entry_age) <= 0 or float(entry_age) > 30)
    position_looks_like_date = bool(re.match(r"\d{4}-\d{2}-\d{2}", str(row.get("position", ""))))
    if invalid_age or position_looks_like_date:
        return score, "REVIEW REQUIRED"
    if score >= 70:
        return score, "GOOD"
    if score >= 45:
        return score, "PARTIAL"
    return score, "POOR"


def main() -> None:
    if not WAREHOUSE_PATH.exists():
        raise FileNotFoundError("Warehouse not found. Run `python -m etl.load_raw` first.")

    with sqlite3.connect(WAREHOUSE_PATH) as con:
        players = pd.read_sql_query("select * from raw_ghana_rtd_players", con)
        heatmap = pd.read_sql_query("select * from raw_ghana_heatmap", con)
        movement = pd.read_sql_query("select * from raw_squad_movement", con)
        black_queens = pd.read_sql_query("select * from raw_black_queens", con)

        for df, name_col in [(players, "full_name"), (heatmap, "full_name"), (movement, "name")]:
            df["player_name_normalised"] = df[name_col].map(normalise_name)

        players["region"] = players["region"].map(standardise_region)
        heatmap["region"] = heatmap["region"].map(standardise_region)
        black_queens["region"] = black_queens["region"].map(standardise_region)
        players["football_squad"] = players["football_squad"].map(standardise_squad)
        movement["squad"] = movement["squad"].map(standardise_squad)

        players["player_id"] = ["RTD-" + str(index + 1).zfill(4) for index in range(len(players))]
        players["football_rating_score"] = players["football_rating"].map(
            lambda value: RATING_SCORE.get(str(value).strip().upper()) if pd.notna(value) else pd.NA
        )
        players["academic_rating_score"] = players["academic_rating"].map(
            lambda value: RATING_SCORE.get(str(value).strip().upper()) if pd.notna(value) else pd.NA
        )

        movement_match = movement.merge(
            players[["player_id", "player_name_normalised", "dob"]],
            left_on=["player_name_normalised", "dob"],
            right_on=["player_name_normalised", "dob"],
            how="left",
        )
        missing = movement_match["player_id"].isna()
        if missing.any():
            fallback = movement_match.loc[missing].drop(columns=["player_id"]).merge(
                players[["player_id", "player_name_normalised"]],
                on="player_name_normalised",
                how="left",
            )
            movement_match.loc[missing, "player_id"] = fallback["player_id"].values

        movement_match["match_method"] = movement_match["player_id"].map(
            lambda value: "Exact normalised name + DOB/name" if pd.notna(value) else "Unmatched"
        )
        movement_match["match_score"] = movement_match["player_id"].map(lambda value: 95 if pd.notna(value) else 0)
        movement_match["match_confidence"] = movement_match["player_id"].map(
            lambda value: "Near Certain" if pd.notna(value) else "Manual Review"
        )
        movement_match["manual_review_required"] = movement_match["player_id"].isna()

        matched_names = set(movement_match.dropna(subset=["player_id"])["player_id"])
        quality = players.apply(lambda row: quality_score(row, row["player_id"] in matched_names), axis=1)
        players["data_quality_score"] = [item[0] for item in quality]
        players["data_quality_class"] = [item[1] for item in quality]
        players["development_status"] = players.apply(development_status, axis=1)
        players["pathway_outcome"] = players.apply(lambda row: pathway_outcome(row["pathway"], row["exit_date"]), axis=1)
        players["is_active"] = players["exit_date"].isna()

        dim_player = players.rename(
            columns={
                "full_name": "player_name",
                "age_today": "current_age",
                "age_at_entry": "entry_age",
                "foot": "preferred_foot",
                "football_squad": "current_squad",
                "pathway": "current_pathway",
                "flag": "current_flag",
                "basic_market_value": "market_value",
            }
        )

        movement_match["observation_date"] = pd.to_datetime(movement_match["date"], errors="coerce")
        movement_match = movement_match.sort_values(["player_id", "observation_date", "squad"])
        movement_match["previous_squad"] = movement_match.groupby("player_id")["squad"].shift(1)
        movement_match["next_squad"] = movement_match.groupby("player_id")["squad"].shift(-1)
        movement_match["squad_level"] = movement_match["squad"].map(SQUAD_LEVEL)
        movement_match["previous_squad_level"] = movement_match["previous_squad"].map(SQUAD_LEVEL)
        movement_match["squad_level_change"] = movement_match["squad_level"] - movement_match["previous_squad_level"]
        movement_match["previous_observation_date"] = movement_match.groupby("player_id")["observation_date"].shift(1)
        movement_match["days_in_previous_squad"] = (
            movement_match["observation_date"] - movement_match["previous_observation_date"]
        ).dt.days
        movement_match["months_in_previous_squad"] = movement_match["days_in_previous_squad"] / 30.44
        movement_match["movement_type"] = "No Change"
        movement_match.loc[movement_match["squad_level_change"] > 0, "movement_type"] = "Promotion"
        movement_match.loc[movement_match["squad_level_change"] < 0, "movement_type"] = "Regression"
        movement_match.loc[movement_match["previous_squad"].isna(), "movement_type"] = "First Observation"
        movement_match.loc[movement_match["squad"].isin(["RTD Pro", "External Pros"]), "movement_type"] = "Professional Transition"
        movement_match.loc[movement_match["squad"].eq("US Students"), "movement_type"] = "Education Transition"

        movement_summary = (
            movement_match.dropna(subset=["player_id"])
            .groupby("player_id")
            .agg(
                first_observation=("observation_date", "min"),
                latest_observation=("observation_date", "max"),
                highest_squad_level=("squad_level", "max"),
                current_observed_squad=("squad", "last"),
                promotions=("movement_type", lambda values: (values == "Promotion").sum()),
                regressions=("movement_type", lambda values: (values == "Regression").sum()),
                squad_changes=("squad", lambda values: values.ne(values.shift()).sum() - 1),
                observation_count=("squad", "size"),
            )
            .reset_index()
        )
        movement_summary["years_observed"] = (
            (movement_summary["latest_observation"] - movement_summary["first_observation"]).dt.days / 365.25
        ).clip(lower=0.1)
        movement_summary["development_velocity"] = (
            movement_summary["highest_squad_level"].fillna(0) / movement_summary["years_observed"]
        )

        dim_player = dim_player.merge(movement_summary, on="player_id", how="left")
        dim_player["development_velocity"] = dim_player["development_velocity"].fillna(0)
        dim_player["highest_squad_level"] = dim_player["highest_squad_level"].fillna(0)
        dim_player["recruitment_success_index"] = (
            dim_player["highest_squad_level"].fillna(0) / 8 * 30
            + dim_player["football_rating_score"].fillna(0) / 5 * 25
            + dim_player["development_velocity"].clip(upper=8) / 8 * 20
            + dim_player["market_value"].rank(pct=True).fillna(0) * 10
            + dim_player["pathway_outcome"].isin(["Professional Football", "External Professional", "First Team"]).astype(int) * 15
        ).round(1)

        dim_player_columns = [
            "player_id",
            "player_name",
            "player_name_normalised",
            "gender",
            "nationality",
            "dob",
            "current_age",
            "entry_age",
            "entry_date",
            "entry_club",
            "entry_rating",
            "preferred_foot",
            "position",
            "current_squad",
            "current_pathway",
            "hometown",
            "region",
            "latitude",
            "longitude",
            "football_rating",
            "football_rating_score",
            "academic_rating",
            "academic_rating_score",
            "idp_progress",
            "development_status",
            "current_flag",
            "market_value",
            "contract_end",
            "exit_date",
            "is_active",
            "pathway_outcome",
            "highest_squad_level",
            "promotions",
            "squad_changes",
            "observation_count",
            "development_velocity",
            "recruitment_success_index",
            "data_quality_score",
            "data_quality_class",
        ]

        source_effectiveness = []
        for dimension in ["region", "hometown", "entry_club", "nationality"]:
            grouped = dim_player.groupby(dimension, dropna=True)
            table = grouped.agg(
                players_recruited=("player_id", "count"),
                average_entry_age=("entry_age", "mean"),
                average_football_rating=("football_rating_score", "mean"),
                average_development_velocity=("development_velocity", "mean"),
                advanced_plus_pct=("highest_squad_level", lambda values: (values >= 5).mean()),
                ia_plus_pct=("highest_squad_level", lambda values: (values >= 6).mean()),
                professional_outcome_pct=("pathway_outcome", lambda values: values.isin(["Professional Football", "External Professional"]).mean()),
                education_outcome_pct=("pathway_outcome", lambda values: values.eq("US Education").mean()),
                average_known_market_value=("market_value", "mean"),
                recruitment_success_index=("recruitment_success_index", "mean"),
                data_completeness=("data_quality_score", "mean"),
            ).reset_index()
            table["source_type"] = dimension
            table = table.rename(columns={dimension: "source_name"})
            table["evidence_strength"] = table.apply(
                lambda row: evidence_strength(int(row["players_recruited"]), float(row["data_completeness"]) / 100),
                axis=1,
            )
            source_effectiveness.append(table)

        mart_source_effectiveness = pd.concat(source_effectiveness, ignore_index=True)
        total_players = len(dim_player)
        region_counts = dim_player.groupby("region", dropna=True).size().reset_index(name="players")
        region_counts["share"] = region_counts["players"] / total_players
        concentration = float((region_counts["share"] ** 2).sum()) if total_players else 0
        diversity = round((1 - concentration) * 100, 1)

        mart_dashboard_summary = pd.DataFrame(
            [
                ("total_players", total_players),
                ("active_players", int(dim_player["is_active"].sum())),
                ("female_players", int(dim_player["gender"].str.lower().eq("female").sum())),
                ("international_players", int((~dim_player["nationality"].str.lower().eq("ghana")).sum())),
                ("regions_represented", int(dim_player["region"].nunique())),
                ("known_market_value", float(dim_player["market_value"].sum(skipna=True))),
                ("market_value_coverage_pct", round(dim_player["market_value"].notna().mean() * 100, 1)),
                ("players_requiring_attention", int(dim_player["development_status"].isin(["WATCH", "AT RISK"]).sum())),
                ("geographic_diversity_index", diversity),
                ("recruitment_concentration_hhi", round(concentration, 3)),
            ],
            columns=["metric", "value"],
        )

        dim_squad = pd.DataFrame(
            [{"squad": squad, "squad_level": level, "outcome_type": OUTCOME_MAP.get(squad, "Academy Development")} for squad, level in SQUAD_LEVEL.items()]
        )

        dates = pd.date_range(
            movement_match["observation_date"].min(),
            movement_match["observation_date"].max(),
            freq="D",
        )
        dim_date = pd.DataFrame({"date": dates})
        dim_date["week"] = dim_date["date"].dt.isocalendar().week.astype(int)
        dim_date["month"] = dim_date["date"].dt.to_period("M").astype(str)
        dim_date["quarter"] = dim_date["date"].dt.to_period("Q").astype(str)
        dim_date["year"] = dim_date["date"].dt.year
        dim_date["season"] = dim_date["year"].astype(str)
        dim_date["academic_year"] = dim_date["date"].map(
            lambda d: f"{d.year}-{str(d.year + 1)[-2:]}" if d.month >= 8 else f"{d.year - 1}-{str(d.year)[-2:]}"
        )

        dim_geography = heatmap[["region", "hometown", "latitude", "longitude", "nationality"]].drop_duplicates()
        dim_geography = dim_geography.rename(columns={"nationality": "country"})
        dim_geography["standardised_region"] = dim_geography["region"]
        dim_geography["geography_type"] = "Player Origin"

        outputs = {
            "dim_player": dim_player[dim_player_columns],
            "fact_squad_movement": movement_match,
            "dim_squad": dim_squad,
            "dim_date": dim_date,
            "dim_geography": dim_geography,
            "mart_source_effectiveness": mart_source_effectiveness,
            "mart_dashboard_summary": mart_dashboard_summary,
            "mart_black_queens": black_queens.rename(columns={"full_names": "full_name"}),
            "mart_region_concentration": region_counts,
        }

        for name, df in outputs.items():
            df.to_sql(name, con, if_exists="replace", index=False)
            print(f"Built model: {name} ({len(df)} rows)")


if __name__ == "__main__":
    main()
