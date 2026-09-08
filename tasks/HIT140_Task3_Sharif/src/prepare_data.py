"""Prepare the Task 3 attacking-performance analysis data."""

from pathlib import Path

import numpy as np
import pandas as pd

from validate_data import load_selected_data


BASE_DIR = Path(__file__).resolve().parents[1]
FIFA_PATH = BASE_DIR / "data" / "raw" / "fifa_round_of_32_teams_2026.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "task3_attacking_progression.csv"
ALIASES = {"Bosnia–Herz": "Bosnia and Herzegovina"}


def load_progressed_squads(fbref_squads):
    fifa = pd.read_csv(FIFA_PATH)
    required = {"Squad", "ProgressedBeyondGroup"}
    if not required.issubset(fifa.columns):
        raise ValueError(f"FIFA file must contain {sorted(required)}")
    if fifa["Squad"].isna().any() or fifa["Squad"].duplicated().any():
        raise ValueError("FIFA progression squad names must be complete and unique")
    progressed_flag = fifa["ProgressedBeyondGroup"].astype(str).str.strip().str.lower()
    if not set(progressed_flag.unique()).issubset({"true", "false"}):
        raise ValueError("ProgressedBeyondGroup must contain only True or False")
    progressed = set(fifa.loc[progressed_flag == "true", "Squad"].str.strip())
    unmatched = sorted(progressed - set(fbref_squads))
    print(f"Unmatched FIFA progression names: {unmatched}")
    if unmatched:
        raise ValueError(f"Unmatched FIFA progression names: {unmatched}")
    if len(progressed) != 32:
        raise ValueError(f"Expected 32 progressed squads; found {len(progressed)}")
    return progressed


def main():
    _, selected, _, _ = load_selected_data()
    prepared = selected.copy()
    prepared["Squad"] = prepared["Squad"].replace(ALIASES)
    progressed = load_progressed_squads(prepared["Squad"])
    prepared["Progression"] = np.where(
        prepared["Squad"].isin(progressed), "Progressed", "Group-stage eliminated"
    )
    counts = prepared["Progression"].value_counts()
    if len(prepared) != 48 or prepared["Squad"].nunique() != 48:
        raise ValueError("Prepared data must contain 48 unique squads")
    if counts.get("Progressed", 0) != 32 or counts.get("Group-stage eliminated", 0) != 16:
        raise ValueError(f"Expected progression counts 32/16; found {counts.to_dict()}")
    if prepared.isna().any().any():
        raise ValueError("Prepared data contains missing values")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prepared.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved processed data: {OUTPUT_PATH.relative_to(BASE_DIR)}")
    print(f"Progressed count: {counts['Progressed']}")
    print(f"Group-stage eliminated count: {counts['Group-stage eliminated']}")


if __name__ == "__main__":
    main()
