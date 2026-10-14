"""Validate the raw FBref standard-stats data for Task 2."""

from pathlib import Path
import re

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_DIR / "data" / "raw" / "fbref_squad_standard_2026_raw.csv"
CODE_PREFIX = re.compile(r"^[a-z]{2,3}\s+")


def find_header_row(path, required_labels):
    """Find the FBref header row, allowing for an optional grouped header."""
    preview = pd.read_csv(path, header=None, dtype=str, keep_default_na=False)
    for row_number in range(min(5, len(preview))):
        labels = {str(value).strip() for value in preview.iloc[row_number]}
        if set(required_labels).issubset(labels):
            return row_number
    raise ValueError(f"Could not find a header row containing {sorted(required_labels)}")


def find_exact_column(data, label):
    matches = [column for column in data.columns if str(column).strip() == label]
    if len(matches) != 1:
        raise ValueError(f"Expected one exact '{label}' column; found {matches}")
    return matches[0]


def clean_squad_name(value):
    """Remove only an initial lowercase two- or three-letter country code."""
    return CODE_PREFIX.sub("", str(value).strip())


def load_selected_data():
    """Load, parse, select, clean, and validate the fields used in Task 2."""
    header_row = find_header_row(RAW_PATH, {"Squad", "MP", "CrdY"})
    raw = pd.read_csv(RAW_PATH, header=header_row)
    data = raw.dropna(how="all").copy()
    columns = [find_exact_column(data, label) for label in ["Squad", "MP", "CrdY"]]
    selected = data[columns].copy()
    selected.columns = ["Squad", "MP", "CrdY"]
    selected = selected[selected["Squad"].notna()].copy()
    selected["Squad"] = selected["Squad"].map(clean_squad_name)
    selected["MP"] = pd.to_numeric(selected["MP"], errors="coerce")
    selected["CrdY"] = pd.to_numeric(selected["CrdY"], errors="coerce")
    selected["YellowCardsPerMatch"] = selected["CrdY"] / selected["MP"]

    missing = selected.isna().sum()
    duplicate_count = int(selected["Squad"].duplicated().sum())
    if len(selected) != 48 or selected["Squad"].nunique() != 48:
        raise ValueError("Expected exactly 48 rows and 48 unique squads")
    if duplicate_count:
        raise ValueError(f"Found {duplicate_count} duplicate squad rows")
    if missing.any():
        raise ValueError(f"Missing or non-numeric required values:\n{missing}")
    if (selected["MP"] <= 0).any():
        raise ValueError("All MP values must be positive")
    if (selected["CrdY"] < 0).any():
        raise ValueError("Yellow-card counts cannot be negative")
    return raw, selected, header_row


def main():
    raw, selected, header_row = load_selected_data()
    print("TASK 2 DATA VALIDATION")
    print(f"Detected header row (1-based): {header_row + 1}")
    print(f"Raw dataframe shape: {raw.shape}")
    print(f"Selected dataframe shape: {selected.shape}")
    print("Selected columns:", selected.columns.tolist())
    print("First rows:")
    print(selected.head().to_string(index=False))
    print("Data types:")
    print(selected.dtypes.to_string())
    print("Missing values:")
    print(selected.isna().sum().to_string())
    print(f"Duplicate squad count: {int(selected['Squad'].duplicated().sum())}")
    print(f"Unique squad count: {selected['Squad'].nunique()}")
    for column in ["MP", "CrdY", "YellowCardsPerMatch"]:
        print(f"{column} min/max: {selected[column].min():.6f} / {selected[column].max():.6f}")
    print("Validation passed.")


if __name__ == "__main__":
    main()
