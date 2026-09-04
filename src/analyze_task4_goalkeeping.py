"""Describe goalkeeper save percentages by progression status for Task 4."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "task4_goalkeeping_progression.csv"
)
FIGURES_DIR = PROJECT_ROOT / "figures"
BOXPLOT_PATH = FIGURES_DIR / "task4_save_percentage_boxplot.png"
HISTOGRAM_PATH = FIGURES_DIR / "task4_save_percentage_histogram.png"

REQUIRED_COLUMNS = ["Squad", "Save%", "ProgressionStatus"]
PROGRESSED = "Progressed"
ELIMINATED = "Group-stage eliminated"


def calculate_statistics(save_percentages):
    """Return the requested descriptive statistics for one group."""
    q1 = save_percentages.quantile(0.25)
    q3 = save_percentages.quantile(0.75)

    return {
        "count": save_percentages.count(),
        "mean": save_percentages.mean(),
        "median": save_percentages.median(),
        "standard deviation": save_percentages.std(),
        "minimum": save_percentages.min(),
        "maximum": save_percentages.max(),
        "Q1": q1,
        "Q3": q3,
        "IQR": q3 - q1,
    }


def print_outliers(dataframe, status):
    """Print 1.5 x IQR fences and possible outliers for one group."""
    group = dataframe[dataframe["ProgressionStatus"].eq(status)]
    q1 = group["Save%"].quantile(0.25)
    q3 = group["Save%"].quantile(0.75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    outliers = group[
        group["Save%"].lt(lower_fence) | group["Save%"].gt(upper_fence)
    ][["Squad", "Save%"]]

    print(f"\n{status}:")
    print(f"Lower fence: {lower_fence:.2f}")
    print(f"Upper fence: {upper_fence:.2f}")
    print("Squads outside the fences:")
    if outliers.empty:
        print("None")
    else:
        print(outliers.to_string(index=False))


def create_figures(progressed_save_percentages, eliminated_save_percentages):
    """Create and save the boxplot and histogram."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.boxplot(
        [progressed_save_percentages, eliminated_save_percentages],
        tick_labels=[PROGRESSED, ELIMINATED],
    )
    plt.title("Goalkeeper Save Percentage by Progression Status")
    plt.xlabel("Progression status")
    plt.ylabel("Save percentage (%)")
    plt.tight_layout()
    plt.savefig(BOXPLOT_PATH, dpi=300)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(
        progressed_save_percentages,
        bins=8,
        alpha=0.65,
        label=PROGRESSED,
        edgecolor="black",
    )
    plt.hist(
        eliminated_save_percentages,
        bins=8,
        alpha=0.65,
        label=ELIMINATED,
        edgecolor="black",
    )
    plt.title("Distribution of Goalkeeper Save Percentage")
    plt.xlabel("Save percentage (%)")
    plt.ylabel("Number of teams")
    plt.legend()
    plt.tight_layout()
    plt.savefig(HISTOGRAM_PATH, dpi=300)
    plt.close()


def main():
    """Validate the data, calculate statistics, and create figures."""
    goalkeeping = pd.read_csv(DATA_PATH)

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in goalkeeping.columns
    ]
    if missing_columns:
        print(f"ERROR: Required columns were not found: {missing_columns}")
        print(f"Available columns: {goalkeeping.columns.tolist()}")
        return 1

    progressed_count = goalkeeping["ProgressionStatus"].eq(PROGRESSED).sum()
    eliminated_count = goalkeeping["ProgressionStatus"].eq(ELIMINATED).sum()
    missing_save_percentage_count = goalkeeping["Save%"].isna().sum()
    missing_status_count = goalkeeping["ProgressionStatus"].isna().sum()

    validation_checks = {
        "Total rows == 48": len(goalkeeping) == 48,
        "Progressed rows == 32": progressed_count == 32,
        "Group-stage eliminated rows == 16": eliminated_count == 16,
        "Missing Save% == 0": missing_save_percentage_count == 0,
        "Missing ProgressionStatus == 0": missing_status_count == 0,
    }

    print("Validation checks:")
    for check, result in validation_checks.items():
        print(f"{check}: {result}")

    if not all(validation_checks.values()):
        print("\nERROR: Validation failed. Analysis was not completed.")
        return 1

    progressed_save_percentages = goalkeeping.loc[
        goalkeeping["ProgressionStatus"].eq(PROGRESSED), "Save%"
    ]
    eliminated_save_percentages = goalkeeping.loc[
        goalkeeping["ProgressionStatus"].eq(ELIMINATED), "Save%"
    ]

    statistics_table = pd.DataFrame(
        {
            PROGRESSED: calculate_statistics(progressed_save_percentages),
            ELIMINATED: calculate_statistics(eliminated_save_percentages),
        }
    ).T

    print("\nDescriptive statistics:")
    print(statistics_table.to_string(float_format=lambda value: f"{value:.2f}"))

    mean_difference = (
        progressed_save_percentages.mean()
        - eliminated_save_percentages.mean()
    )
    print("\nObserved difference in group means")
    print("(Progressed mean - Group-stage eliminated mean):")
    print(f"{mean_difference:.2f} percentage points")

    print("\nPotential outliers using the 1.5 x IQR rule:")
    print_outliers(goalkeeping, PROGRESSED)
    print_outliers(goalkeeping, ELIMINATED)

    create_figures(progressed_save_percentages, eliminated_save_percentages)

    print("\nFigure files created:")
    print(BOXPLOT_PATH)
    print(HISTOGRAM_PATH)

    return 0


if __name__ == "__main__":
    sys.exit(main())
