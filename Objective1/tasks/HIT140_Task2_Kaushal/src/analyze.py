"""Analyze yellow cards per match for Task 2."""

import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "hit140_matplotlib_cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "task2_discipline_progression.csv"
BOXPLOT_PATH = BASE_DIR / "figures" / "task2_yellow_cards_per_match_boxplot.png"
HISTOGRAM_PATH = BASE_DIR / "figures" / "task2_yellow_cards_per_match_histogram.png"
VALUE_COLUMN = "YellowCardsPerMatch"
GROUPS = ["Progressed", "Group-stage eliminated"]


def descriptive_statistics(values):
    q1, q3 = values.quantile(0.25), values.quantile(0.75)
    return {"count": int(values.count()), "mean": values.mean(), "median": values.median(),
            "std": values.std(ddof=1), "min": values.min(), "max": values.max(),
            "Q1": q1, "Q3": q3, "IQR": q3 - q1}


def mean_ci(values):
    critical = stats.t.ppf(0.975, df=len(values) - 1)
    margin = critical * values.std(ddof=1) / np.sqrt(len(values))
    return values.mean() - margin, values.mean() + margin


def outlier_details(group_data):
    q1, q3 = group_data[VALUE_COLUMN].quantile(0.25), group_data[VALUE_COLUMN].quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    rows = group_data.loc[(group_data[VALUE_COLUMN] < lower) | (group_data[VALUE_COLUMN] > upper),
                          ["Squad", VALUE_COLUMN]]
    details = [f"{row.Squad} ({getattr(row, VALUE_COLUMN):.4f})" for row in rows.itertuples()]
    return lower, upper, details


def create_figures(data):
    progressed = data.loc[data["Progression"] == GROUPS[0], VALUE_COLUMN]
    eliminated = data.loc[data["Progression"] == GROUPS[1], VALUE_COLUMN]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot([progressed, eliminated], tick_labels=GROUPS, patch_artist=True,
               boxprops={"facecolor": "#4C78A8", "alpha": 0.70}, medianprops={"color": "black"})
    ax.set_title("Yellow Cards per Match by Progression Status")
    ax.set_ylabel("Yellow cards per match")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(BOXPLOT_PATH, dpi=300)
    plt.close(fig)

    bin_edges = np.histogram_bin_edges(data[VALUE_COLUMN].to_numpy(), bins=8)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(progressed, bins=bin_edges, alpha=0.60, label=GROUPS[0], color="#4C78A8", edgecolor="white")
    ax.hist(eliminated, bins=bin_edges, alpha=0.60, label=GROUPS[1], color="#F58518", edgecolor="white")
    ax.set_title("Distribution of Yellow Cards per Match by Progression Status")
    ax.set_xlabel("Yellow cards per match")
    ax.set_ylabel("Number of teams")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(HISTOGRAM_PATH, dpi=300)
    plt.close(fig)
    return bin_edges


def main():
    data = pd.read_csv(DATA_PATH)
    required = {"Squad", "MP", "CrdY", VALUE_COLUMN, "Progression"}
    if not required.issubset(data.columns):
        raise ValueError(f"Processed data must contain {sorted(required)}")
    if data[list(required)].isna().any().any():
        raise ValueError("Processed analysis fields contain missing values")
    counts = data["Progression"].value_counts()
    if len(data) != 48 or counts.get(GROUPS[0], 0) != 32 or counts.get(GROUPS[1], 0) != 16:
        raise ValueError(f"Expected 48 teams split 32/16; found {counts.to_dict()}")

    samples = {group: data.loc[data["Progression"] == group, VALUE_COLUMN] for group in GROUPS}
    desc = {group: descriptive_statistics(values) for group, values in samples.items()}
    mean_cis = {group: mean_ci(values) for group, values in samples.items()}
    skewness = {group: values.skew() for group, values in samples.items()}
    outliers = {group: outlier_details(data[data["Progression"] == group]) for group in GROUPS}
    n1, n2 = len(samples[GROUPS[0]]), len(samples[GROUPS[1]])
    mean1, mean2 = desc[GROUPS[0]]["mean"], desc[GROUPS[1]]["mean"]
    sd1, sd2 = desc[GROUPS[0]]["std"], desc[GROUPS[1]]["std"]
    difference = mean1 - mean2
    standard_error = np.sqrt(sd1 ** 2 / n1 + sd2 ** 2 / n2)
    df = min(n1 - 1, n2 - 1)
    critical = stats.t.ppf(0.975, df=df)
    difference_ci = (difference - critical * standard_error, difference + critical * standard_error)
    t_statistic = difference / standard_error
    p_value = 2 * stats.t.sf(abs(t_statistic), df=df)
    bin_edges = create_figures(data)

    print("STATE")
    print("H0: mu_progressed = mu_eliminated")
    print("H1: mu_progressed != mu_eliminated")
    print("Response variable: yellow cards per match. Significance level: 0.05.")
    print("\nPLAN")
    print(f"Group sample sizes: Progressed n={n1}; Group-stage eliminated n={n2}")
    print(f"Missing analysis values: {int(data[list(required)].isna().sum().sum())}")
    for group in GROUPS:
        lower, upper, details = outliers[group]
        print(f"{group} skewness: {skewness[group]:.6f}")
        print(f"{group} 1.5 x IQR fences: [{lower:.6f}, {upper:.6f}]")
        print(f"{group} possible outliers: {details if details else 'None'}")
    print("Sampling condition: not satisfied as a simple random sample. The data contain all 48 tournament teams.")
    print("The t procedure is used for the course comparison, but inference is restricted primarily to this tournament.")

    print("\nSOLVE")
    result_table = pd.DataFrame(desc).T[["count", "mean", "median", "std", "min", "max", "Q1", "Q3", "IQR"]]
    print("Descriptive statistics:")
    print(result_table.to_string(float_format=lambda value: f"{value:.6f}"))
    for group in GROUPS:
        print(f"95% CI for {group} mean: ({mean_cis[group][0]:.6f}, {mean_cis[group][1]:.6f})")
    print(f"Observed difference in means (Progressed - Eliminated): {difference:.6f}")
    print(f"Standard error: {standard_error:.6f}")
    print(f"95% CI for difference in means: ({difference_ci[0]:.6f}, {difference_ci[1]:.6f})")
    print(f"t statistic: {t_statistic:.6f}")
    print(f"Conservative df: {df}")
    print(f"Two-sided p-value: {p_value:.6f}")
    print("Histogram common bin edges:", np.array2string(bin_edges, precision=6))

    print("\nCONCLUDE")
    if p_value < 0.05:
        print("Reject H0 at alpha = 0.05. The 2026 World Cup data provide evidence of a difference in mean yellow cards per match between the groups.")
    else:
        print("Fail to reject H0 at alpha = 0.05. The 2026 World Cup data do not provide sufficient evidence of a difference in mean yellow cards per match between the groups.")
    print("This is an association within the 2026 World Cup data and is not evidence that progression caused the difference.")
    print(f"Figures created: {BOXPLOT_PATH.relative_to(BASE_DIR)}, {HISTOGRAM_PATH.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
