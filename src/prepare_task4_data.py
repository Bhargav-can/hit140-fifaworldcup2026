"""Prepare and validate the Task 4 goalkeeping progression dataset."""

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GOALKEEPING_PATH = (
    PROJECT_ROOT / "data" / "raw" / "fbref_squad_goalkeeping_2026_raw.csv"
)
PROGRESSION_PATH = (
    PROJECT_ROOT / "data" / "raw" / "fifa_round_of_32_teams_2026.csv"
)
OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "task4_goalkeeping_progression.csv"
)
ANALYSIS_COLUMNS = ["Squad", "MP", "Min", "SoTA", "Saves", "Save%"]


def flatten_columns(dataframe):
    """Replace the two-row FBref header with clear, unique column names."""
    flat_columns = []

    for group, column in dataframe.columns:
        group = str(group).strip()
        column = str(column).strip()

        if group == "Penalty Kicks" and column == "Save%":
            flat_columns.append("Penalty Save%")
        elif column.startswith("Unnamed"):
            flat_columns.append(group)
        else:
            flat_columns.append(column)

    dataframe.columns = flat_columns
    return dataframe


def print_team_list(teams):
    """Print one team per line."""
    for team in teams:
        print(team)


def main():
    """Merge the two sources, validate the classification, and save the result."""
    raw_goalkeeping = pd.read_csv(GOALKEEPING_PATH, header=[0, 1])
    goalkeeping = flatten_columns(raw_goalkeeping.copy())

    missing_columns = [
        column for column in ANALYSIS_COLUMNS if column not in goalkeeping.columns
    ]
    if missing_columns:
        print(f"ERROR: Required FBref columns were not found: {missing_columns}")
        print(f"Available columns: {goalkeeping.columns.tolist()}")
        return 1

    goalkeeping = goalkeeping[ANALYSIS_COLUMNS].copy()
    goalkeeping["Squad"] = (
        goalkeeping["Squad"]
        .astype("string")
        .str.replace(r"^[a-z]{2,3}\s+", "", regex=True)
    )
    goalkeeping["Squad"] = goalkeeping["Squad"].replace(
        {"Bosnia–Herz": "Bosnia and Herzegovina"}
    )

    for column in ANALYSIS_COLUMNS[1:]:
        goalkeeping[column] = pd.to_numeric(goalkeeping[column], errors="coerce")

    progression = pd.read_csv(PROGRESSION_PATH)
    expected_progression_columns = ["Squad", "ProgressedBeyondGroup"]
    if progression.columns.tolist() != expected_progression_columns:
        print(
            "ERROR: FIFA progression file must contain exactly these columns: "
            f"{expected_progression_columns}"
        )
        return 1

    progressed_teams = progression.loc[
        progression["ProgressedBeyondGroup"].eq(True), "Squad"
    ].astype("string")

    print("Total rows:")
    print(len(goalkeeping))

    print("\nUnique squads:")
    print(goalkeeping["Squad"].nunique())

    print("\nDuplicate squads:")
    print(goalkeeping.duplicated(subset="Squad").sum())

    unmatched_teams = sorted(
        set(progressed_teams) - set(goalkeeping["Squad"].dropna())
    )
    print("\nUnmatched FIFA progressed-team name count:")
    print(len(unmatched_teams))

    print("\nUnmatched FIFA progressed-team names:")
    if unmatched_teams:
        print_team_list(unmatched_teams)
        print("\nERROR: Progression-team names must match cleaned FBref Squad names.")
        return 1
    print("None")

    goalkeeping["ProgressionStatus"] = goalkeeping["Squad"].apply(
        lambda squad: (
            "Progressed" if squad in set(progressed_teams) else "Group-stage eliminated"
        )
    )

    progressed = goalkeeping[
        goalkeeping["ProgressionStatus"].eq("Progressed")
    ]
    eliminated = goalkeeping[
        goalkeeping["ProgressionStatus"].eq("Group-stage eliminated")
    ]

    progressed_count = len(progressed)
    eliminated_count = len(eliminated)
    missing_status_count = goalkeeping["ProgressionStatus"].isna().sum()

    print("\nProgressed count:")
    print(progressed_count)

    print("\nGroup-stage-eliminated count:")
    print(eliminated_count)

    print("\nMissing ProgressionStatus count:")
    print(missing_status_count)

    print("\nProgressed teams:")
    print_team_list(progressed["Squad"].tolist())

    print("\nGroup-stage-eliminated teams:")
    print_team_list(eliminated["Squad"].tolist())

    total_teams_valid = len(goalkeeping) == 48
    progressed_teams_valid = progressed_count == 32
    eliminated_teams_valid = eliminated_count == 16

    print("\nValidation checks:")
    print(f"Total teams == 48: {total_teams_valid}")
    print(f"Progressed teams == 32: {progressed_teams_valid}")
    print(f"Group-stage-eliminated teams == 16: {eliminated_teams_valid}")

    validation_succeeded = all(
        [
            total_teams_valid,
            progressed_teams_valid,
            eliminated_teams_valid,
            goalkeeping["Squad"].is_unique,
            missing_status_count == 0,
        ]
    )
    if not validation_succeeded:
        print("\nERROR: Validation failed. The processed dataset was not saved.")
        return 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    goalkeeping.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved validated dataset to: {OUTPUT_PATH}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
