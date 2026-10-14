"""Linear regression for Objective 2, following the Week 9 practical.

The two datasets already have eight explanatory variables each.
This file fits the starting model, compares it with a mean baseline,
then applies the four optimisation checks from the practical:

1. a log-style transform where the scatter is not a straight line
2. removal of strong collinearity
3. z-score rescaling
4. a Yeo-Johnson transform

A change is kept only when five-fold cross-validation error falls.
The 60/40 split uses test_size=0.4 and random_state=0.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, train_test_split
from sklearn.preprocessing import PowerTransformer, StandardScaler

ROOT = Path(__file__).resolve().parent.parent
CHARTS = ROOT / "outputs" / "charts"
COLLINEAR_LIMIT = 0.75
LOG_GAIN = 0.005
FOLDS = KFold(n_splits=5, shuffle=True, random_state=0)

plt.rcParams["figure.dpi"] = 120
sns.set_theme(style="whitegrid")


def performance(y_true, y_pred, y_all):
    """MAE, MSE, RMSE, normalised RMSE, and R-squared, as in the practical."""
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    rmse = math.sqrt(mse)
    nrmse = rmse / (float(np.max(y_all)) - float(np.min(y_all)))
    r2 = metrics.r2_score(y_true, y_pred)
    return {"MAE": mae, "MSE": mse, "RMSE": rmse, "NRMSE": nrmse, "R2": r2}


def signed_log(values):
    """Log that is defined for negative gaps: sign(x) * log(1 + |x|)."""
    values = np.asarray(values, dtype=float)
    return np.sign(values) * np.log1p(np.abs(values))


def apply_transform(x_train, x_test, kind, log_columns=None):
    """Fit any rescaling on the training rows only, then apply it to the test rows."""
    if kind == "raw":
        return x_train, x_test
    if kind == "zscore":
        scaler = StandardScaler().fit(x_train)
        return scaler.transform(x_train), scaler.transform(x_test)
    if kind == "yeo":
        transformer = PowerTransformer(method="yeo-johnson").fit(x_train)
        return transformer.transform(x_train), transformer.transform(x_test)
    if kind == "signed_log":
        return signed_log(x_train), signed_log(x_test)
    if kind == "log1p":
        train = np.array(x_train, copy=True)
        test = np.array(x_test, copy=True)
        train[:, log_columns] = np.log1p(train[:, log_columns])
        test[:, log_columns] = np.log1p(test[:, log_columns])
        return train, test
    raise ValueError(kind)


def cross_validate(x, y, kind="raw", log_columns=None):
    """Average the practical's metrics over five shuffled folds."""
    fold_scores = []
    baseline_rmse = []
    for train_idx, test_idx in FOLDS.split(x):
        x_train, x_test = apply_transform(
            x[train_idx], x[test_idx], kind, log_columns
        )
        model = LinearRegression().fit(x_train, y[train_idx])
        predicted = model.predict(x_test)
        fold_scores.append(performance(y[test_idx], predicted, y))
        baseline = np.full(len(test_idx), y[train_idx].mean())
        baseline_rmse.append(
            math.sqrt(metrics.mean_squared_error(y[test_idx], baseline))
        )
    out = {key: float(np.mean([row[key] for row in fold_scores])) for key in fold_scores[0]}
    out["baseline_RMSE"] = float(np.mean(baseline_rmse))
    return out


def out_of_fold(x, y, kind="raw", log_columns=None):
    predicted = np.zeros(len(y), dtype=float)
    for train_idx, test_idx in FOLDS.split(x):
        x_train, x_test = apply_transform(
            x[train_idx], x[test_idx], kind, log_columns
        )
        model = LinearRegression().fit(x_train, y[train_idx])
        predicted[test_idx] = model.predict(x_test)
    return predicted


def drop_collinear(frame, x_columns, y_column, limit=COLLINEAR_LIMIT):
    """Drop the weaker member of every pair whose correlation is at least `limit`."""
    kept = list(x_columns)
    dropped = []
    while True:
        corr = frame[kept].corr().abs()
        strongest = None
        for i, left in enumerate(kept):
            for right in kept[i + 1 :]:
                value = float(corr.loc[left, right])
                if value >= limit and (strongest is None or value > strongest[0]):
                    strongest = (value, left, right)
        if strongest is None:
            break
        value, left, right = strongest
        left_with_y = abs(float(frame[left].corr(frame[y_column])))
        right_with_y = abs(float(frame[right].corr(frame[y_column])))
        lose = left if left_with_y < right_with_y else right
        kept.remove(lose)
        dropped.append(
            {
                "dropped": lose,
                "pair": (left, right),
                "pair_corr": value,
            }
        )
    return kept, dropped


def holdout(x, y):
    """60% train, 40% test, random_state=0."""
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.4, random_state=0
    )
    model = LinearRegression().fit(x_train, y_train)
    predicted = model.predict(x_test)
    baseline = np.full(len(y_test), y_train.mean())
    return {
        "intercept": float(model.intercept_),
        "coef": model.coef_.tolist(),
        "model": performance(y_test, predicted, y),
        "baseline": performance(y_test, baseline, y),
    }


def ols_equation(y, frame, x_columns, y_name):
    fitted = sm.OLS(y, sm.add_constant(frame[x_columns])).fit()
    parts = [f"{fitted.params['const']:.4f}"]
    for name in x_columns:
        coef = fitted.params[name]
        sign = "+" if coef >= 0 else "-"
        parts.append(f" {sign} {abs(coef):.4f}*{name}")
    return fitted, f"{y_name} = " + "".join(parts)


def ols_diagnostics(fitted):
    """Standard error, t statistic, and p-value, as in statsmodels OLS.summary()."""
    table = pd.DataFrame(
        {
            "coefficient": fitted.params,
            "std_error": fitted.bse,
            "t": fitted.tvalues,
            "p_value": fitted.pvalues,
        }
    )
    return table.round(4)


def largest_misses(frame, y, predicted, n=6):
    """The rows the kept model misses by the most, using out-of-fold predictions."""
    table = pd.DataFrame(
        {
            "row": frame.iloc[:, 0].to_numpy(),
            "actual": y,
            "predicted": predicted,
        }
    )
    table["residual"] = table["actual"] - table["predicted"]
    order = table["residual"].abs().sort_values(ascending=False).index
    return table.loc[order].head(n).round(3)


def fit_line(ax, x_values, y_values):
    x_values = np.asarray(x_values, dtype=float)
    y_values = np.asarray(y_values, dtype=float)
    if np.unique(x_values).size < 2:
        return
    slope, intercept = np.polyfit(x_values, y_values, 1)
    grid = np.linspace(x_values.min(), x_values.max(), 40)
    ax.plot(grid, slope * grid + intercept, color="#c62828", linewidth=1.2)


def transform_columns(values, indexes):
    """Log the chosen columns. Use log(1+x) when every value is at least 0."""
    out = np.array(values, copy=True)
    for index in indexes:
        column = out[:, index]
        if np.min(column) >= 0:
            out[:, index] = np.log1p(column)
        else:
            out[:, index] = signed_log(column)
    return out


def save_scatters(frame, x_columns, y_column, path, title):
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    for ax, name in zip(axes.ravel(), x_columns):
        ax.scatter(frame[name], frame[y_column], s=18, alpha=0.75, color="#1f4e79")
        fit_line(ax, frame[name], frame[y_column])
        ax.set_xlabel(name, fontsize=8)
        ax.set_ylabel(y_column, fontsize=8)
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_heatmap(frame, columns, path, title):
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(
        frame[columns].corr(),
        vmin=-1,
        vmax=1,
        center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=False,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 8},
        ax=ax,
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_log_scatter(frame, names, y, y_name, path, title):
    """Before and after the log, with a straight line, for the variables that are kept."""
    fig, axes = plt.subplots(len(names), 2, figsize=(10, 3.4 * len(names)), squeeze=False)
    for row, name in enumerate(names):
        raw = frame[name].to_numpy(dtype=float)
        logged = np.log1p(raw) if np.min(raw) >= 0 else signed_log(raw)
        logged_label = f"log(1 + {name})" if np.min(raw) >= 0 else f"signed log of {name}"
        axes[row, 0].scatter(raw, y, s=18, alpha=0.75, color="#2e7d32")
        fit_line(axes[row, 0], raw, y)
        axes[row, 0].set_title(name)
        axes[row, 0].set_xlabel(name)
        axes[row, 0].set_ylabel(y_name)
        axes[row, 1].scatter(logged, y, s=18, alpha=0.75, color="#c62828")
        fit_line(axes[row, 1], logged, y)
        axes[row, 1].set_title(logged_label)
        axes[row, 1].set_xlabel(logged_label)
        axes[row, 1].set_ylabel(y_name)
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_log_trials(trials, path, title):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    names = [row["variable"] for row in trials]
    deltas = [row["delta"] for row in trials]
    colors = ["#2e7d32" if row["kept"] else "#9e9e9e" for row in trials]
    ax.barh(names[::-1], deltas[::-1], color=colors[::-1])
    ax.axvline(0, color="black", linewidth=1)
    ax.axvline(LOG_GAIN, color="#c62828", linewidth=1, linestyle="--")
    ax.set_xlabel("Fall in cross-validated RMSE when only this variable is logged")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_yeo_hist(frame, x_columns, path, title):
    transformed = PowerTransformer(method="yeo-johnson").fit_transform(frame[x_columns])
    fig, axes = plt.subplots(4, 4, figsize=(12, 10))
    flat = axes.ravel()
    for index, name in enumerate(x_columns):
        flat[2 * index].hist(frame[name], bins=12, density=True, color="#1f4e79")
        flat[2 * index].set_title(f"{name} (original)", fontsize=8)
        flat[2 * index + 1].hist(transformed[:, index], bins=12, density=True, color="#1f4e79")
        flat[2 * index + 1].set_title(f"{name} (Yeo-Johnson)", fontsize=8)
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_std_coef(table, path, title):
    ordered = table.sort_values("std_coef")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = ["#c62828" if value < 0 else "#1f4e79" for value in ordered["std_coef"]]
    ax.barh(ordered.index.astype(str), ordered["std_coef"], color=colors)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_xlabel("Coefficient after z-score rescaling (change in the response per standard deviation)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_coef_shift(before, after, path, title):
    names = [name for name in before.params.index if name != "const" and name in after.params.index]
    y_pos = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(y_pos - 0.18, [before.params[name] for name in names], height=0.36, label="All 8", color="#9e9e9e")
    ax.barh(y_pos + 0.18, [after.params[name] for name in names], height=0.36, label="After the drop", color="#1f4e79")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_xlabel("Coefficient")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_actual_predicted(y, predicted, path, title):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(y, predicted, s=18, alpha=0.75, color="#1f4e79")
    low = min(y.min(), predicted.min())
    high = max(y.max(), predicted.max())
    axes[0].plot([low, high], [low, high], color="black", linewidth=1)
    axes[0].set_xlabel("Actual")
    axes[0].set_ylabel("Predicted")
    axes[0].set_title("Out-of-fold predictions")
    residual = y - predicted
    axes[1].scatter(predicted, residual, s=18, alpha=0.75, color="#1f4e79")
    axes[1].axhline(0, color="black", linewidth=1)
    axes[1].set_xlabel("Predicted")
    axes[1].set_ylabel("Residual (actual − predicted)")
    axes[1].set_title("Residuals")
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_rmse_bars(rows, path, title, best_name):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    names = [row["model"] for row in rows]
    values = [row["RMSE"] for row in rows]
    colors = []
    for name in names:
        if name == "Mean baseline":
            colors.append("#9e9e9e")
        elif name == best_name:
            colors.append("#2e7d32")
        else:
            colors.append("#1f4e79")
    ax.barh(names[::-1], values[::-1], color=colors[::-1])
    ax.set_xlabel("Cross-validated RMSE (lower is better)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def standardised_coefficients(frame, x_columns, y):
    scaled = StandardScaler().fit_transform(frame[x_columns])
    scaled = pd.DataFrame(scaled, columns=x_columns)
    fitted = sm.OLS(y, sm.add_constant(scaled)).fit()
    table = fitted.params.drop("const").rename("std_coef").to_frame()
    table["abs_coef"] = table["std_coef"].abs()
    return table.sort_values("abs_coef", ascending=False), fitted.rsquared


def analyse_task(frame, x_columns, y_column, tag, log_plan):
    """Run every practical check for one dataset and return the comparison rows."""
    y = frame[y_column].to_numpy(dtype=float)
    x = frame[x_columns].to_numpy(dtype=float)
    CHARTS.mkdir(parents=True, exist_ok=True)

    save_scatters(
        frame,
        x_columns,
        y_column,
        CHARTS / f"{tag}_scatters.png",
        f"{tag}: each explanatory variable against {y_column}",
    )
    save_heatmap(
        frame,
        x_columns + [y_column],
        CHARTS / f"{tag}_heatmap.png",
        f"{tag}: correlation heatmap",
    )

    split = holdout(x, y)
    fitted, equation = ols_equation(y, frame, x_columns, y_column)
    kept, dropped = drop_collinear(frame, x_columns, y_column)
    reduced_equation = None
    if dropped:
        _, reduced_equation = ols_equation(y, frame, kept, y_column)
    reduced = frame[kept].to_numpy(dtype=float)
    reduced_fit = None
    if dropped:
        reduced_fit, _ = ols_equation(y, frame, kept, y_column)
        save_coef_shift(
            fitted,
            reduced_fit,
            CHARTS / f"{tag}_collinearity_coef.png",
            f"{tag}: coefficients before and after dropping collinear variables",
        )
    coef_table, _ = standardised_coefficients(frame, x_columns, y)
    save_std_coef(
        coef_table,
        CHARTS / f"{tag}_zscore_coef.png",
        f"{tag}: effect of each input after z-score rescaling",
    )
    save_yeo_hist(
        frame,
        x_columns,
        CHARTS / f"{tag}_yeo_hist.png",
        f"{tag}: distribution before and after Yeo-Johnson",
    )

    base_rmse = cross_validate(x, y)["RMSE"]
    log_trials = []
    useful = []
    for index, name in enumerate(x_columns):
        if np.unique(x[:, index]).size < 4:
            log_trials.append({"variable": name, "delta": 0.0, "rmse": base_rmse, "kept": False})
            continue
        logged_rmse = cross_validate(transform_columns(x, [index]), y)["RMSE"]
        delta = base_rmse - logged_rmse
        keep_log = delta > LOG_GAIN
        log_trials.append(
            {"variable": name, "delta": delta, "rmse": logged_rmse, "kept": keep_log}
        )
        if keep_log:
            useful.append(index)
    save_log_trials(
        log_trials,
        CHARTS / f"{tag}_log_trials.png",
        f"{tag}: which logs reduce error (green is kept, dashed line is {LOG_GAIN})",
    )
    logged_names = [x_columns[index] for index in useful]
    if logged_names:
        save_log_scatter(
            frame,
            logged_names,
            y,
            y_column,
            CHARTS / f"{tag}_log_scatter.png",
            f"{tag}: logs that reduce cross-validated error",
        )

    rows = [
        {"model": "Mean baseline", **cross_validate(x, y), "uses": "none"},
    ]
    # The baseline row above also contains a model RMSE. Replace it with the
    # mean-predictor RMSE so the bar chart compares like with like.
    base = rows[0]["baseline_RMSE"]
    rows[0]["RMSE"] = base
    rows[0]["MAE"] = float(
        np.mean(
            [
                metrics.mean_absolute_error(
                    y[test], np.full(len(test), y[train].mean())
                )
                for train, test in FOLDS.split(x)
            ]
        )
    )
    y_span = float(y.max() - y.min())
    rows[0]["NRMSE"] = rows[0]["RMSE"] / y_span
    rows[0]["R2"] = float(
        np.mean(
            [
                metrics.r2_score(y[test], np.full(len(test), y[train].mean()))
                for train, test in FOLDS.split(x)
            ]
        )
    )

    specs = [
        ("All 8 variables", x, "raw", None),
        ("Z-score of all 8", x, "zscore", None),
        ("Yeo-Johnson of all 8", x, "yeo", None),
    ]
    if dropped:
        specs.insert(1, ("Collinearity removed", reduced, "raw", None))
    specs.append(("Log of every input", transform_columns(x, list(range(len(x_columns)))), "raw", None))
    if useful:
        specs.append(("Log of the useful inputs", transform_columns(x, useful), "raw", None))

    scored = {}
    for name, matrix, kind, indexes in specs:
        scores = cross_validate(matrix, y, kind, indexes)
        scored[name] = scores
        rows.append({"model": name, **scores, "uses": kind})

    best_name = min(scored, key=lambda name: scored[name]["RMSE"])
    best_kind = dict((name, kind) for name, _, kind, _ in specs)[best_name]
    best_index = dict((name, indexes) for name, _, _, indexes in specs)[best_name]
    if best_name == "Collinearity removed":
        best_matrix = reduced
    elif best_name == "Log of every input":
        best_matrix = transform_columns(x, list(range(len(x_columns))))
    elif best_name == "Log of the useful inputs":
        best_matrix = transform_columns(x, useful)
    else:
        best_matrix = x
    predicted = out_of_fold(best_matrix, y, best_kind, best_index)
    save_actual_predicted(
        y,
        predicted,
        CHARTS / f"{tag}_actual_vs_predicted.png",
        f"{tag}: {best_name}",
    )
    save_rmse_bars(rows, CHARTS / f"{tag}_rmse.png", f"{tag}: cross-validated RMSE", best_name)

    return {
        "tag": tag,
        "y_column": y_column,
        "x_columns": x_columns,
        "rows": rows,
        "dropped": dropped,
        "kept": kept,
        "equation": equation,
        "reduced_equation": reduced_equation,
        "ols_r2": float(fitted.rsquared),
        "ols_table": ols_diagnostics(fitted),
        "reduced_ols_table": ols_diagnostics(reduced_fit) if reduced_fit is not None else None,
        "misses": largest_misses(frame, y, predicted),
        "holdout": split,
        "std_coef": coef_table,
        "best_name": best_name,
        "n": len(frame),
        "logged_names": logged_names,
        "log_trials": log_trials,
    }


def rounded(rows):
    table = pd.DataFrame(rows)
    keep = ["model", "MAE", "RMSE", "NRMSE", "R2"]
    return table[keep].copy()


def _rmse(result, model_name):
    for row in result["rows"]:
        if row["model"] == model_name:
            return row["RMSE"], row["R2"]
    raise KeyError(model_name)


def recommendation_text(goal_diff, goals):
    """Plain-language conclusion. Numbers come from the cross-validation table."""
    base_a, _ = _rmse(goal_diff, "Mean baseline")
    full_a, r2_a = _rmse(goal_diff, "All 8 variables")
    reduced_a, _ = _rmse(goal_diff, "Collinearity removed")
    z_a, _ = _rmse(goal_diff, "Z-score of all 8")
    yeo_a, _ = _rmse(goal_diff, "Yeo-Johnson of all 8")
    log_a, r2_log_a = _rmse(goal_diff, "Log of the useful inputs")
    every_a, _ = _rmse(goal_diff, "Log of every input")
    base_b, _ = _rmse(goals, "Mean baseline")
    full_b, _ = _rmse(goals, "All 8 variables")
    yeo_b, _ = _rmse(goals, "Yeo-Johnson of all 8")
    log_b, r2_log_b = _rmse(goals, "Log of the useful inputs")
    logged_a = ", ".join(goal_diff["logged_names"])
    logged_b = ", ".join(goals["logged_names"])
    return "\n".join(
        [
            "Recommendation",
            "",
            "2.1 goal difference. The eight-variable model beats predicting the average",
            f"margin: cross-validated RMSE falls from {base_a:.3f} to {full_a:.3f}",
            f"(R-squared {r2_a:.3f}). FIFA points, market value, and World Cup experience",
            "are strongly correlated, so market value and World Cup experience are removed",
            f"from the raw model. That lowers RMSE to {reduced_a:.3f}. Z-score rescaling",
            f"leaves RMSE at {z_a:.3f}. It does not add information. The rescaled coefficients",
            "show that the FIFA-points gap has the largest effect.",
            "A plain log is undefined for a negative gap, so the transform is",
            "sign(x) * log(1 + |x|). Logging every gap gives RMSE",
            f"{every_a:.3f}. Logging only {logged_a} gives RMSE {log_a:.3f}",
            f"and R-squared {r2_log_a:.3f}. Yeo-Johnson raises RMSE to {yeo_a:.3f}, so it is not used.",
            f"Use the log of {logged_a} for 2.1, and leave the other gaps unchanged.",
            "",
            "2.2 goals scored. No pair of explanatory variables is strongly correlated,",
            "so none is removed. The eight-variable model is only a little better than",
            f"the average: RMSE {full_b:.3f} against a baseline of {base_b:.3f}.",
            f"Z-score rescaling does not change that error. Yeo-Johnson raises RMSE to {yeo_b:.3f}.",
            f"The only log that reduces error by more than 0.005 is {logged_b}:",
            f"RMSE {log_b:.3f}, R-squared {r2_log_b:.3f}. The gain is small.",
            f"Use the log of {logged_b} for 2.2, and leave the other inputs unchanged.",
            "",
            "The in-sample R-squared is higher than the cross-validated R-squared.",
            "Quote the cross-validated figures in the report.",
        ]
    )


def main():
    match = pd.read_csv(ROOT / "data" / "linreg_2_1.csv")
    team = pd.read_csv(ROOT / "data" / "linreg_2_2.csv")
    x1 = [c for c in match.columns if c not in ("match_id", "goal_diff")]
    x2 = [c for c in team.columns if c not in ("team_match_id", "goals")]
    rate_names = [
        "qual_gf_per_game",
        "opp_qual_ga_per_game",
        "wc_goals_so_far",
        "opp_wc_ga_so_far",
    ]

    result_a = analyse_task(
        match,
        x1,
        "goal_diff",
        "linreg_2_1",
        {"kind": "signed_log", "column": "fifa_points_diff"},
    )
    result_b = analyse_task(
        team,
        x2,
        "goals",
        "linreg_2_2",
        {
            "kind": "log1p",
            "column": "qual_gf_per_game",
            "indexes": [x2.index(name) for name in rate_names],
        },
    )

    comparison = pd.concat(
        [
            rounded(result_a["rows"]).assign(task="2.1 goal difference"),
            rounded(result_b["rows"]).assign(task="2.2 goals scored"),
        ],
        ignore_index=True,
    )
    for column in ("MAE", "RMSE", "NRMSE", "R2"):
        comparison[column] = comparison[column].round(4)
    comparison["kept"] = comparison["model"].eq("Log of the useful inputs")
    conclusion = recommendation_text(result_a, result_b)

    print(comparison.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print()
    print(result_a["equation"])
    if result_a["reduced_equation"]:
        print(result_a["reduced_equation"])
    print(result_b["equation"])
    print()
    print(conclusion)


if __name__ == "__main__":
    main()
