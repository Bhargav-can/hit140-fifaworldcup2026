"""Validate the local FBref squad goalkeeping data for the 2026 World Cup."""

import sys
from pathlib import Path

import pandas as pd


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "fbref_squad_goalkeeping_2026_raw.csv"
)
SELECTED_COLUMNS = ["Squad", "# Pl", "MP", "Min", "SoTA", "Saves", "Save%"]


def flatten_columns(dataframe):
    """Replace the two-row header with clear, unique column names."""
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


def print_rows_or_none(dataframe):
    """Print selected rows clearly, including when no rows match."""
    if dataframe.empty:
        print("None")
    else:
        print(dataframe.to_string(index=False))


def main():
    """Read, clean, and validate the local goalkeeping CSV."""
    raw_goalkeeping = pd.read_csv(DATA_PATH, header=[0, 1])

    print("Raw dataframe shape:")
    print(raw_goalkeeping.shape)

    goalkeeping = flatten_columns(raw_goalkeeping.copy())

    missing_columns = [
        column for column in SELECTED_COLUMNS if column not in goalkeeping.columns
    ]
    if missing_columns:
        print(f"ERROR: Required columns were not found: {missing_columns}")
        print(f"Available columns: {goalkeeping.columns.tolist()}")
        return 1

    goalkeeping = goalkeeping[SELECTED_COLUMNS].copy()

    goalkeeping["Squad"] = (
        goalkeeping["Squad"]
        .astype("string")
        .str.replace(r"^[a-z]{2,3}\s+", "", regex=True)
    )

    for column in SELECTED_COLUMNS[1:]:
        goalkeeping[column] = pd.to_numeric(goalkeeping[column], errors="coerce")

    print("\nSelected dataframe shape:")
    print(goalkeeping.shape)

    print("\nSelected column names:")
    print(goalkeeping.columns.tolist())

    print("\nFirst 10 cleaned rows:")
    print(goalkeeping.head(10).to_string(index=False))

    print("\nData types:")
    print(goalkeeping.dtypes.to_string())

    print("\nMissing-value counts:")
    print(goalkeeping.isna().sum().to_string())

    print("\nDuplicate Squad count:")
    print(goalkeeping.duplicated(subset="Squad").sum())

    unique_squad_count = goalkeeping["Squad"].nunique()
    print("\nNumber of unique squads:")
    print(unique_squad_count)

    print("\nMinimum and maximum Save%:")
    print((goalkeeping["Save%"].min(), goalkeeping["Save%"].max()))

    print("\nRows where Save% is missing:")
    print_rows_or_none(goalkeeping[goalkeeping["Save%"].isna()])

    print("\nRows where SoTA is zero or missing:")
    zero_or_missing_sota = goalkeeping[
        goalkeeping["SoTA"].eq(0) | goalkeeping["SoTA"].isna()
    ]
    print_rows_or_none(zero_or_missing_sota)

    print("\nValidation checks:")
    print(f"Unique Squad count equals 48: {unique_squad_count == 48}")
    valid_save_percentages = goalkeeping["Save%"].dropna().between(0, 100).all()
    print(
        "All non-missing Save% values are between 0 and 100: "
        f"{valid_save_percentages}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
