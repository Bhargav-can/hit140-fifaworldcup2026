"""Describe goalkeeper save percentages by progression status for Task 4."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t


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


def calculate_mean_confidence_interval(save_percentages, confidence_level=0.95):
    """Calculate a t confidence interval for one population mean."""
    sample_size = save_percentages.count()
    sample_mean = save_percentages.mean()
    sample_standard_deviation = save_percentages.std()
    standard_error = sample_standard_deviation / sample_size**0.5
    degrees_of_freedom = sample_size - 1
    alpha = 1 - confidence_level
    t_critical = t.ppf(1 - alpha / 2, degrees_of_freedom)
    margin_of_error = t_critical * standard_error

    return {
        "n": sample_size,
        "mean": sample_mean,
        "standard error": standard_error,
        "degrees of freedom": degrees_of_freedom,
        "t critical value": t_critical,
        "lower bound": sample_mean - margin_of_error,
        "upper bound": sample_mean + margin_of_error,
    }


def calculate_difference_confidence_interval(
    progressed_save_percentages,
    eliminated_save_percentages,
    confidence_level=0.95,
):
    """Calculate the course-aligned t interval for a difference in means."""
    progressed_n = progressed_save_percentages.count()
    eliminated_n = eliminated_save_percentages.count()
    progressed_variance = progressed_save_percentages.var()
    eliminated_variance = eliminated_save_percentages.var()

    progressed_variance_component = progressed_variance / progressed_n
    eliminated_variance_component = eliminated_variance / eliminated_n
    standard_error = (
        progressed_variance_component + eliminated_variance_component
    ) ** 0.5

    # Week 4 uses the smaller group's degrees of freedom as a conservative value.
    degrees_of_freedom = min(progressed_n - 1, eliminated_n - 1)

    mean_difference = (
        progressed_save_percentages.mean()
        - eliminated_save_percentages.mean()
    )
    alpha = 1 - confidence_level
    t_critical = t.ppf(1 - alpha / 2, degrees_of_freedom)
    margin_of_error = t_critical * standard_error

    return {
        "mean difference": mean_difference,
        "standard error": standard_error,
        "degrees of freedom": degrees_of_freedom,
        "lower bound": mean_difference - margin_of_error,
        "upper bound": mean_difference + margin_of_error,
    }


def print_mean_confidence_interval(status, confidence_interval):
    """Print the components of a confidence interval for one group mean."""
    print(f"\n{status}:")
    print(f"n: {confidence_interval['n']}")
    print(f"Mean: {confidence_interval['mean']:.2f}")
    print(f"Standard error: {confidence_interval['standard error']:.2f}")
    print(f"Degrees of freedom: {confidence_interval['degrees of freedom']}")
    print(f"t critical value: {confidence_interval['t critical value']:.4f}")
    print(f"Lower 95% CI: {confidence_interval['lower bound']:.2f}")
    print(f"Upper 95% CI: {confidence_interval['upper bound']:.2f}")


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

    print("\nAssumption checks:")
    print("Shape diagnostics:")
    print(f"{PROGRESSED} n: {progressed_save_percentages.count()}")
    print(f"{PROGRESSED} skewness: {progressed_save_percentages.skew():.2f}")
    print(f"{ELIMINATED} n: {eliminated_save_percentages.count()}")
    print(f"{ELIMINATED} skewness: {eliminated_save_percentages.skew():.2f}")
    print("\nSampling-condition diagnostic:")
    print("Simple random sampling condition: not satisfied / not applicable.")
    print(
        "The dataset contains the 48 participating teams in the 2026 FIFA "
        "World Cup rather than teams selected through a simple random sampling "
        "procedure."
    )

    print("\nPotential outliers using the 1.5 x IQR rule:")
    print_outliers(goalkeeping, PROGRESSED)
    print_outliers(goalkeeping, ELIMINATED)

    progressed_variance = progressed_save_percentages.var()
    eliminated_variance = eliminated_save_percentages.var()
    print("\nSample variance check:")
    print(f"{PROGRESSED} sample variance: {progressed_variance:.2f}")
    print(f"{ELIMINATED} sample variance: {eliminated_variance:.2f}")
    print(
        "The difference-in-means 95% CI uses the conservative Week 4 course "
        "approach with the smaller sample degrees of freedom."
    )

    progressed_confidence_interval = calculate_mean_confidence_interval(
        progressed_save_percentages
    )
    eliminated_confidence_interval = calculate_mean_confidence_interval(
        eliminated_save_percentages
    )

    print("\n95% confidence intervals for group mean Save%:")
    print_mean_confidence_interval(PROGRESSED, progressed_confidence_interval)
    print_mean_confidence_interval(ELIMINATED, eliminated_confidence_interval)

    difference_confidence_interval = calculate_difference_confidence_interval(
        progressed_save_percentages, eliminated_save_percentages
    )
    print("\n95% confidence interval for the difference in mean Save%")
    print("(Progressed mean - Group-stage eliminated mean):")
    print(
        "Observed mean difference: "
        f"{difference_confidence_interval['mean difference']:.2f} percentage points"
    )
    print(
        "Standard error of the difference: "
        f"{difference_confidence_interval['standard error']:.2f}"
    )
    print(
        "Degrees of freedom used: "
        f"{difference_confidence_interval['degrees of freedom']}"
    )
    print(
        "95% CI lower bound: "
        f"{difference_confidence_interval['lower bound']:.2f} percentage points"
    )
    print(
        "95% CI upper bound: "
        f"{difference_confidence_interval['upper bound']:.2f} percentage points"
    )

    create_figures(progressed_save_percentages, eliminated_save_percentages)

    print("\nFigure files created:")
    print(BOXPLOT_PATH)
    print(HISTOGRAM_PATH)

    return 0


if __name__ == "__main__":
    sys.exit(main())
