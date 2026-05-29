import re
from itertools import combinations

import matplotlib.pyplot as plt
import pandas as pd


def compute_league_winners(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Pos"] == 1].reset_index(drop=True)


def compute_top4_counts(
    df: pd.DataFrame,
    city_col: str = "City",
    team_col: str = "Team",
    pos_col: str = "Pos",
    pts_col: str = "Pts",
) -> tuple[pd.DataFrame, pd.DataFrame]:

    def parse_val(val):
        if pd.isna(val):
            return pd.NA
        return int(re.sub(r"\[.*?\]", "", str(val)).strip())

    df = df.copy()
    df["_pos"] = df[pos_col].apply(parse_val)
    df["_pts"] = df[pts_col].apply(parse_val)

    team_records = []

    for season, group in df.groupby("season"):
        top4_pos = set(group[group["_pos"] <= 4][team_col])
        fourth_pts = group["_pts"].nlargest(4).min()
        top4_pts = set(group[group["_pts"] >= fourth_pts][team_col])

        for _, row in group.iterrows():
            team = row[team_col]
            city = row.get(city_col, None)
            team_records.append({
                "team": team,
                "city": city,
                "season": season,
                "in_top4_by_pos": team in top4_pos,
                "in_top4_by_pts": team in top4_pts,
            })

    season_df = pd.DataFrame(team_records)

    # --- Team aggregation ---
    team_agg = (
        season_df.groupby("team")
        .agg(
            top4_by_pos=("in_top4_by_pos", "sum"),
            top4_by_pts=("in_top4_by_pts", "sum"),
            seasons_in_league=("season", "count"),
        )
        .astype({"top4_by_pos": int, "top4_by_pts": int})
        .sort_index()
    )
    team_agg["top4_by_pos_pct"] = (team_agg["top4_by_pos"] / team_agg["seasons_in_league"]).round(3)
    team_agg["top4_by_pts_pct"] = (team_agg["top4_by_pts"] / team_agg["seasons_in_league"]).round(3)

    # --- City aggregation ---
    city_agg = (
        season_df.groupby("city")
        .agg(
            top4_by_pos=("in_top4_by_pos", "sum"),
            top4_by_pts=("in_top4_by_pts", "sum"),
            seasons_in_league=("season", "count"),
        )
        .astype({"top4_by_pos": int, "top4_by_pts": int})
        .sort_index()
    )
    city_agg["top4_by_pos_pct"] = (city_agg["top4_by_pos"] / city_agg["seasons_in_league"]).round(3)
    city_agg["top4_by_pts_pct"] = (city_agg["top4_by_pts"] / city_agg["seasons_in_league"]).round(3)

    return team_agg, city_agg


def compute_dominant_teams(
    df: pd.DataFrame,
    teams: list[str],
    label: str = "dominant",
    top_n: int = 4,
    definition: str = "pos",
    pos_col: str = "Pos",
    pts_col: str = "Pts",
) -> pd.DataFrame:

    def parse_val(val):
        if pd.isna(val):
            return pd.NA
        return int(re.sub(r"\[.*?\]", "", str(val)).strip())

    df = df.copy()
    df["_pos"] = df[pos_col].apply(parse_val)
    df["_pts"] = df[pts_col].apply(parse_val)

    records = []
    for season, group in df.groupby("season"):
        if definition == "pos":
            top_n_teams = set(group[group["_pos"] <= top_n]["Team"])
        else:
            nth_pts = group["_pts"].nlargest(top_n).min()
            top_n_teams = set(group[group["_pts"] >= nth_pts]["Team"])

        teams_in_top = [t for t in teams if t in top_n_teams]

        row_data = {
            "season": season,
            f"number_of_{label}": len(teams_in_top),
            label: teams_in_top,
        }

        for team in teams:
            team_row = group[group["Team"] == team]
            if team_row.empty:
                row_data[f"pos_{team}"] = -1
                row_data[f"pts_{team}"] = -1
            else:
                row_data[f"pos_{team}"] = int(team_row["_pos"].values[0])
                row_data[f"pts_{team}"] = int(team_row["_pts"].values[0])

        records.append(row_data)

    result = pd.DataFrame(records)
    result["positions"] = result[[f"pos_{t}" for t in teams]].values.tolist()
    result["points"] = result[[f"pts_{t}" for t in teams]].values.tolist()

    return result[["season", f"number_of_{label}", label, "positions", "points"]]


def compute_dominant_combinations(
    df: pd.DataFrame,
    teams: list[str],
    combo_size: int = 3,
    top_n: int = 4,
    definition: str = "pos",
    pos_col: str = "Pos",
    pts_col: str = "Pts",
) -> pd.DataFrame:

    def parse_val(val):
        if pd.isna(val):
            return pd.NA
        return int(re.sub(r"\[.*?\]", "", str(val)).strip())

    df = df.copy()
    df["_pos"] = df[pos_col].apply(parse_val)
    df["_pts"] = df[pts_col].apply(parse_val)

    season_top = {}
    for season, group in df.groupby("season"):
        if definition == "pos":
            season_top[season] = set(group[group["_pos"] <= top_n]["Team"])
        else:
            nth_pts = group["_pts"].nlargest(top_n).min()
            season_top[season] = set(group[group["_pts"] >= nth_pts]["Team"])

    total_seasons = len(season_top)
    records = []

    for combo in combinations(teams, combo_size):
        counts = {i: 0 for i in range(combo_size + 1)}

        for season, top_set in season_top.items():
            n_in_top = sum(t in top_set for t in combo)
            counts[n_in_top] += 1

        row = {"combination": combo}
        for i in range(combo_size + 1):
            row[f"{i}_of_{combo_size}"] = counts[i]
            row[f"{i}_of_{combo_size}_pct"] = round(counts[i] / total_seasons, 3)

        threshold = combo_size - 1
        row[f"at_least_{threshold}_of_{combo_size}"] = sum(
            counts[i] for i in range(threshold, combo_size + 1)
        )
        row[f"at_least_{threshold}_of_{combo_size}_pct"] = round(
            row[f"at_least_{threshold}_of_{combo_size}"] / total_seasons, 3
        )

        records.append(row)

    return (
        pd.DataFrame(records)
        .sort_values(f"{combo_size}_of_{combo_size}_pct", ascending=False)
        .reset_index(drop=True)
    )


def plot_dominant_teams(
    df: pd.DataFrame,
    label: str = "dominant",
    title: str = None,
    figsize: tuple = (16, 4),
) -> None:
    count_col = f"number_of_{label}"
    colors = df[count_col].apply(lambda x: "green" if x > 1 else "red")

    fig, ax = plt.subplots(figsize=figsize)

    ax.scatter(
        x=df["season"],
        y=df[count_col],
        c=colors,
        s=60,
        zorder=3,
    )

    ax.set_xticks(df["season"])
    ax.set_xticklabels(df["season"], rotation=90, fontsize=8)
    ax.set_yticks(range(0, df[count_col].max() + 2))
    ax.set_ylabel(f"Number of {label} in Top 4")
    ax.set_xlabel("Season")
    ax.set_title(title or f"{label.capitalize()} teams in Top 4 by season")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Decade vertical lines
    seasons = df["season"].tolist()
    decades = {s for s in seasons if int(s[:4]) % 10 == 0}
    for s in decades:
        ax.axvline(x=s, color="grey", linestyle="--", linewidth=0.8, alpha=0.6, zorder=1)

    plt.tight_layout()
    plt.show()
