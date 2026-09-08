"""Validate the raw FBref shooting data for Task 3."""

from pathlib import Path
import re

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_DIR / "data" / "raw" / "fbref_squad_shooting_2026_raw.csv"
CODE_PREFIX = re.compile(r"^[a-z]{2,3}\s+")


def find_header_row(path, required_labels):
    """Find the FBref header row, allowing for an optional grouped header."""
    preview = pd.read_csv(path, header=None, dtype=str, keep_default_na=False)
    for row_number in range(min(5, len(preview))):
        labels = {str(value).strip() for value in preview.iloc[row_number]}
        if set(required_labels).issubset(labels):
            return row_number
    raise ValueError(f"Could not find a header row containing {sorted(required_labels)}")


def find_exact_column(data, label, required=True):
    matches = [column for column in data.columns if str(column).strip() == label]
    if not matches and not required:
        return None
    if len(matches) != 1:
        raise ValueError(f"Expected one exact '{label}' column; found {matches}")
    return matches[0]


def clean_squad_name(value):
    """Remove only an initial lowercase two- or three-letter country code."""
    return CODE_PREFIX.sub("", str(value).strip())


def load_selected_data():
    """Load, parse, select, clean, and validate the fields used in Task 3."""
    header_row = find_header_row(RAW_PATH, {"Squad", "90s", "SoT"})
    raw = pd.read_csv(RAW_PATH, header=header_row)
    data = raw.dropna(how="all").copy()
    squad_column = find_exact_column(data, "Squad")
    nineties_column = find_exact_column(data, "90s")
    sot_column = find_exact_column(data, "SoT")
    provided_column = find_exact_column(data, "SoT/90", required=False)
    source_columns = [squad_column, nineties_column, sot_column]
    if provided_column is not None:
        source_columns.append(provided_column)
    selected = data[source_columns].copy()
    selected.columns = ["Squad", "90s", "SoT"] + (["FBrefSoTPer90"] if provided_column else [])
    selected = selected[selected["Squad"].notna()].copy()
    selected["Squad"] = selected["Squad"].map(clean_squad_name)
    numeric_columns = ["90s", "SoT"] + (["FBrefSoTPer90"] if provided_column else [])
    for column in numeric_columns:
        selected[column] = pd.to_numeric(selected[column], errors="coerce")
    selected["ShotsOnTargetPer90"] = selected["SoT"] / selected["90s"]

    missing = selected.isna().sum()
    duplicate_count = int(selected["Squad"].duplicated().sum())
    if len(selected) != 48 or selected["Squad"].nunique() != 48:
        raise ValueError("Expected exactly 48 rows and 48 unique squads")
    if duplicate_count:
        raise ValueError(f"Found {duplicate_count} duplicate squad rows")
    if missing.any():
        raise ValueError(f"Missing or non-numeric required values:\n{missing}")
    if (selected["90s"] <= 0).any():
        raise ValueError("All 90s values must be positive")
    if (selected["SoT"] < 0).any():
        raise ValueError("Shots-on-target counts cannot be negative")
    if provided_column is not None:
        selected["SoTPer90AbsoluteDifference"] = (
            selected["ShotsOnTargetPer90"] - selected["FBrefSoTPer90"]
        ).abs()
    return raw, selected, header_row, provided_column


def main():
    raw, selected, header_row, provided_column = load_selected_data()
    print("TASK 3 DATA VALIDATION")
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
    for column in ["90s", "SoT", "ShotsOnTargetPer90"]:
        print(f"{column} min/max: {selected[column].min():.6f} / {selected[column].max():.6f}")
    if provided_column is not None:
        max_difference = selected["SoTPer90AbsoluteDifference"].max()
        agreement = np.allclose(selected["ShotsOnTargetPer90"], selected["FBrefSoTPer90"], atol=0.06, rtol=0)
        print(f"Provided SoT/90 column: '{provided_column}'")
        print(f"Maximum absolute calculated-versus-provided difference: {max_difference:.6f}")
        print(f"Agreement within 0.06 (reasonable rounding for displayed 90s): {agreement}")
        if not agreement:
            raise ValueError("Calculated SoT/90 does not agree with the supplied field within rounding tolerance")
    else:
        print("No provided SoT/90 column was present; the response was calculated from SoT / 90s.")
    print("Validation passed.")


if __name__ == "__main__":
    main()
