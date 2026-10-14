"""Competing models and robustness checks for Objective 2.

Builds on analyse_linreg.py. Adds:
1. Repeated cross-validation (5 folds x 20 repeats) so every RMSE has a spread.
2. Grouped folds for 2.2, so both rows of a match always sit in the same fold.
3. Nested selection of the log columns, so the kept model is not scored on the
   same folds that chose it.
4. Competing algorithms: OLS variants, Ridge, Lasso, Huber, Poisson (2.2),
   and a random forest as a non-linear check.
5. Football-facing checks: how often the predicted winner is right, and whether
   predicted goal counts match the observed spread of scores.

Run: python scripts/compare_models.py
Writes outputs/charts/hd_*.png and outputs/hd_results.json.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import (
    HuberRegressor,
    LassoCV,
    LinearRegression,
    PoissonRegressor,
    RidgeCV,
)
from sklearn.model_selection import GroupKFold, KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PowerTransformer, StandardScaler

import analyse_linreg as base

ROOT = Path(__file__).resolve().parent.parent
CHARTS = ROOT / "outputs" / "charts"
REPEATS = 20
LOG_GAIN = base.LOG_GAIN

INK = "#1f2933"
MUTED = "#8a94a0"
BLUE = "#1f4e79"
GREEN = "#2e7d32"
RED = "#c62828"
AMBER = "#e08e0b"

plt.style.use("default")
plt.rcParams.update(
    {
        "axes.titlesize": 8.5,
        "axes.labelsize": 7.5,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "axes.grid": True,
        "grid.color": "#e5e8ec",
        "grid.linewidth": 0.6,
        "axes.axisbelow": True,
        "figure.dpi": 150,
        "font.size": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
    }
)


# --------------------------------------------------------------------------
# Folds
# --------------------------------------------------------------------------
def fold_sets(n, groups=None):
    """Yield (repeat, train_idx, test_idx). Grouped when groups is given."""
    for r in range(REPEATS):
        if groups is None:
            splitter = KFold(n_splits=5, shuffle=True, random_state=r)
            splits = splitter.split(np.zeros(n))
        else:
            splitter = GroupKFold(n_splits=5, shuffle=True, random_state=r)
            splits = splitter.split(np.zeros(n), groups=groups)
        for train_idx, test_idx in splits:
            yield r, train_idx, test_idx


# --------------------------------------------------------------------------
# Feature recipes (all fitted on training rows only)
# --------------------------------------------------------------------------
def log_columns(x, idx):
    return base.transform_columns(x, idx) if idx else x


def choose_logs(x, y, groups=None):
    """Inner-loop version of the practical's log rule: keep a log only when
    5-fold CV RMSE on the training rows falls by more than LOG_GAIN."""
    if groups is None:
        inner = list(KFold(5, shuffle=True, random_state=0).split(x))
    else:
        inner = list(GroupKFold(5, shuffle=True, random_state=0).split(x, groups=groups))

    def rmse(mat):
        errs = []
        for tr, te in inner:
            m = LinearRegression().fit(mat[tr], y[tr])
            errs.append(math.sqrt(np.mean((y[te] - m.predict(mat[te])) ** 2)))
        return float(np.mean(errs))

    start = rmse(x)
    keep = []
    for j in range(x.shape[1]):
        if np.unique(x[:, j]).size < 4:
            continue
        if start - rmse(log_columns(x, [j])) > LOG_GAIN:
            keep.append(j)
    return keep


class Recipe:
    """A model plus how its inputs are prepared. fit/predict on raw matrices."""

    def __init__(self, name, estimator, columns=None, logs=None, nested_logs=False,
                 family="Linear (OLS)"):
        self.name = name
        self.estimator = estimator
        self.columns = columns
        self.logs = logs or []
        self.nested_logs = nested_logs
        self.family = family

    def _prep(self, x):
        x = log_columns(x, self._logs)
        return x[:, self.columns] if self.columns is not None else x

    def fit(self, x, y, groups=None):
        self._logs = choose_logs(x, y, groups) if self.nested_logs else self.logs
        self.model_ = clone(self.estimator).fit(self._prep(x), y)
        return self

    def predict(self, x):
        return self.model_.predict(self._prep(x))


def evaluate(recipes, x, y, groups=None):
    """Repeated CV. Returns per-recipe RMSE/MAE arrays (one value per repeat)
    and the out-of-fold predictions from repeat 0."""
    out = {}
    for rec in recipes:
        rmse = np.zeros(REPEATS)
        mae = np.zeros(REPEATS)
        r2 = np.zeros(REPEATS)
        sq = {r: [] for r in range(REPEATS)}
        ab = {r: [] for r in range(REPEATS)}
        r2s = {r: [] for r in range(REPEATS)}
        oof = np.zeros(len(y))
        for r, tr, te in fold_sets(len(y), groups):
            g_tr = None if groups is None else groups[tr]
            fitted = Recipe(rec.name, rec.estimator, rec.columns, rec.logs,
                            rec.nested_logs).fit(x[tr], y[tr], g_tr)
            p = fitted.predict(x[te])
            sq[r].append(math.sqrt(np.mean((y[te] - p) ** 2)))
            ab[r].append(np.mean(np.abs(y[te] - p)))
            ss = np.sum((y[te] - y[te].mean()) ** 2)
            r2s[r].append(1 - np.sum((y[te] - p) ** 2) / ss)
            if r == 0:
                oof[te] = p
        for r in range(REPEATS):
            rmse[r] = np.mean(sq[r])
            mae[r] = np.mean(ab[r])
            r2[r] = np.mean(r2s[r])
        out[rec.name] = {"rmse": rmse, "mae": mae, "r2": r2, "oof": oof,
                         "family": rec.family}
    return out


def summarise(scores, baseline_name="Mean baseline"):
    base_rmse = scores[baseline_name]["rmse"]
    rows = []
    for name, s in scores.items():
        rows.append(
            {
                "model": name,
                "family": s["family"],
                "RMSE": float(s["rmse"].mean()),
                "RMSE_sd": float(s["rmse"].std(ddof=1)),
                "MAE": float(s["mae"].mean()),
                "R2": float(s["r2"].mean()),
                "beats_baseline_pct": float((s["rmse"] < base_rmse).mean() * 100),
                "gain_vs_baseline_pct": float((1 - s["rmse"].mean() / base_rmse.mean()) * 100),
            }
        )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def fig_signal(match, x1, team, x2, path):
    """How strongly each input tracks the response, both tasks side by side."""
    pretty = {
        "fifa_points_diff": "FIFA points gap",
        "qual_gd_per_game_diff": "Qualifying GD gap",
        "market_value_avg_diff": "Market value gap",
        "age_avg_diff": "Average age gap",
        "host": "Host flag",
        "rest_days_diff": "Rest days gap",
        "wc_gd_so_far": "WC form gap (GD so far)",
        "wc_experience_diff": "WC experience gap",
        "qual_gf_per_game": "Qualifying goals for",
        "opp_qual_ga_per_game": "Opp. qualifying goals against",
        "wc_goals_so_far": "WC goals so far",
        "opp_wc_ga_so_far": "Opp. WC goals against so far",
        "foreigners_pct": "% squad abroad",
        "opp_foreigners_pct": "Opp. % squad abroad",
        "squad_size": "Squad size",
        "opp_squad_size": "Opp. squad size",
    }
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.5))
    for ax, frame, cols, ycol, title in (
        (axes[0], match, x1, "goal_diff", "2.1  Goal difference (104 matches)"),
        (axes[1], team, x2, "goals", "2.2  Goals scored (208 team-matches)"),
    ):
        r = frame[cols].corrwith(frame[ycol]).sort_values()
        n = len(frame)
        crit = stats.t.ppf(0.975, n - 2)
        r_crit = crit / math.sqrt(n - 2 + crit ** 2)
        colors = [BLUE if abs(v) >= r_crit else MUTED for v in r]
        ax.barh([pretty[c] for c in r.index], r.values, color=colors, height=0.65)
        ax.axvline(0, color=INK, lw=0.8)
        for s in (-r_crit, r_crit):
            ax.axvline(s, color=RED, lw=0.8, ls="--")
        ax.set_xlim(-0.35, 0.65)
        ax.set_title(title, fontsize=8.5, loc="left", color=INK)
        ax.set_xlabel("Pearson r with the response")
        for i, v in enumerate(r.values):
            ax.text(v + (0.015 if v >= 0 else -0.015), i, f"{v:.2f}",
                    va="center", ha="left" if v >= 0 else "right", fontsize=6.5, color=INK)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def fig_competition(t1, t2, path, highlight1, highlight2):
    """Dot-and-whisker: mean repeated-CV RMSE with its spread, against the baseline."""
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    for ax, table, title, hl in (
        (axes[0], t1, "2.1  Goal difference", highlight1),
        (axes[1], t2, "2.2  Goals scored (grouped folds)", highlight2),
    ):
        table = table.sort_values("RMSE", ascending=False).reset_index(drop=True)
        b = table.loc[table.model == "Mean baseline", "RMSE"].iloc[0]
        for i, row in table.iterrows():
            if row.model == "Mean baseline":
                c = MUTED
            elif row.model == hl:
                c = GREEN
            elif row.family.startswith("Non-linear"):
                c = AMBER
            else:
                c = BLUE
            ax.errorbar(row.RMSE, i, xerr=row.RMSE_sd, fmt="o", color=c, ms=4.5,
                        capsize=2, lw=1)
            ax.text(row.RMSE + row.RMSE_sd + 0.006, i, f"{row.RMSE:.3f}",
                    va="center", fontsize=6.5, color=INK)
        ax.axvline(b, color=MUTED, ls=":", lw=1)
        ax.set_yticks(range(len(table)))
        ax.set_yticklabels(table.model, fontsize=7)
        ax.set_title(title, fontsize=8.5, loc="left", color=INK)
        ax.set_xlabel("RMSE over 20 repeats of 5-fold CV (mean ± 1 SD)")
        lo = table.RMSE.min() - 0.06
        hi = table.RMSE.max() + 0.07
        ax.set_xlim(lo, hi)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def fig_coefficients(match, cols1, team, cols2, path):
    """Standardised OLS coefficients with 95% intervals: which inputs matter."""
    pretty = {
        "fifa_points_diff": "FIFA points gap",
        "qual_gd_per_game_diff": "Qualifying GD gap",
        "age_avg_diff": "Average age gap",
        "host": "Host flag",
        "rest_days_diff": "Rest days gap",
        "wc_gd_so_far": "WC form gap",
        "slog_market_value": "Market value gap (signed log)",
        "slog_wc_experience": "WC experience gap (signed log)",
        "log_qual_gf": "Qualifying goals for (log 1+x)",
        "opp_qual_ga_per_game": "Opp. qualifying goals against",
        "wc_goals_so_far": "WC goals so far",
        "opp_wc_ga_so_far": "Opp. WC goals against so far",
        "foreigners_pct": "% squad abroad",
        "opp_foreigners_pct": "Opp. % squad abroad",
        "squad_size": "Squad size",
        "opp_squad_size": "Opp. squad size",
    }
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.6))
    out = {}
    for ax, frame, ycol, title, tag in (
        (axes[0], cols1, match["goal_diff"], "2.1  Kept model (goals of margin per SD)", "2.1"),
        (axes[1], cols2, team["goals"], "2.2  Kept model (goals per SD)", "2.2"),
    ):
        z = (frame - frame.mean()) / frame.std(ddof=0)
        fit = sm.OLS(ycol.to_numpy(float), sm.add_constant(z)).fit()
        ci = fit.conf_int().drop("const")
        coef = fit.params.drop("const")
        order = coef.sort_values().index
        for i, name in enumerate(order):
            sig = fit.pvalues[name] < 0.05
            c = BLUE if sig else MUTED
            ax.plot([ci.loc[name, 0], ci.loc[name, 1]], [i, i], color=c, lw=1.6)
            ax.plot(coef[name], i, "o", color=c, ms=4.5)
        ax.axvline(0, color=INK, lw=0.8)
        ax.set_yticks(range(len(order)))
        ax.set_yticklabels([pretty[n] for n in order], fontsize=7)
        ax.set_title(title, fontsize=8.5, loc="left", color=INK)
        ax.set_xlabel("Change per 1 SD of input, 95% CI")
        out[tag] = {
            "r2": float(fit.rsquared),
            "adj_r2": float(fit.rsquared_adj),
            "coef": {n: float(coef[n]) for n in coef.index},
            "p": {n: float(fit.pvalues[n]) for n in coef.index},
        }
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_story(match, y1, oof1, team, y2, pois_mu, path):
    """Left: where the goal-difference model is wrong (named upsets/blowouts).
    Right: does a Poisson model reproduce the observed spread of scorelines?"""
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1.35, 1]})
    ax = axes[0]
    resid = y1 - oof1
    ax.axhspan(-0.5, 0.5, color="#eef2f6", zorder=0)
    ax.scatter(oof1, y1, s=14, color=BLUE, alpha=0.65, zorder=2)
    lim = [-5, 7]
    ax.plot(lim, lim, color=INK, lw=0.8)
    ax.axhline(0, color=MUTED, lw=0.6)
    ax.axvline(0, color=MUTED, lw=0.6)
    worst = np.argsort(-np.abs(resid))[:6]
    label_y = 7.0
    for i in sorted(worst, key=lambda k: (-y1[k], oof1[k])):
        parts = match.match_id.iloc[i].split("_")
        a = "Bosnia" if parts[1] == "BosniaandHerzegovina" else parts[1]
        label = f"{a} {int(y1[i]):+d} v {parts[2]}"
        ax.scatter(oof1[i], y1[i], s=26, color=RED, zorder=3)
        if y1[i] > 0 and oof1[i] > 0:
            # stacked column in the empty top-left, with a leader line
            label_y = min(label_y, y1[i]) if label_y == 7.0 else min(label_y - 0.85, y1[i])
            ax.annotate(label, (oof1[i], y1[i]), xytext=(-3.0, label_y), textcoords="data",
                        fontsize=6.5, color=RED, va="center", ha="left",
                        arrowprops=dict(arrowstyle="-", color=RED, lw=0.5, alpha=0.6))
        else:
            above = y1[i] > 0
            ax.annotate(label, (oof1[i], y1[i]), xytext=(5, 9 if above else 0),
                        textcoords="offset points", fontsize=6.5, color=RED, va="center",
                        ha="left")
    ax.set_xlim(-3.2, 4.6)
    ax.set_ylim(-4.8, 7.4)
    ax.set_xlabel("Predicted goal difference (out-of-fold)")
    ax.set_ylabel("Actual goal difference")
    ax.set_title("2.1  The line reads the favourite; blowouts are the misses",
                 fontsize=8.5, loc="left", color=INK)

    ax = axes[1]
    ks = np.arange(0, 8)
    observed = np.array([(y2 == k).sum() for k in ks])
    expected = np.array([stats.poisson.pmf(k, pois_mu).sum() for k in ks])
    expected[-1] += stats.poisson.sf(ks[-1], pois_mu).sum()
    ax.bar(ks - 0.2, observed, width=0.4, color=BLUE, label="Observed")
    ax.bar(ks + 0.2, expected, width=0.4, color=AMBER, label="Poisson model, expected")
    ax.set_xticks(ks)
    ax.set_xlabel("Goals scored by a team in a match")
    ax.set_ylabel("Team-matches")
    ax.legend(frameon=False, fontsize=7)
    ax.set_title("2.2  Scorelines follow a count distribution", fontsize=8.5,
                 loc="left", color=INK)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return {"observed": observed.tolist(), "expected": [float(v) for v in expected]}


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    CHARTS.mkdir(parents=True, exist_ok=True)
    match = pd.read_csv(ROOT / "data" / "linreg_2_1.csv")
    team = pd.read_csv(ROOT / "data" / "linreg_2_2.csv")
    x1 = [c for c in match.columns if c not in ("match_id", "goal_diff")]
    x2 = [c for c in team.columns if c not in ("team_match_id", "goals")]
    X1 = match[x1].to_numpy(float)
    y1 = match.goal_diff.to_numpy(float)
    X2 = team[x2].to_numpy(float)
    y2 = team.goals.to_numpy(float)
    groups = team.team_match_id.str.extract(r"^(M\d+)")[0].to_numpy()

    i_mv, i_exp = x1.index("market_value_avg_diff"), x1.index("wc_experience_diff")
    reduced = [i for i, c in enumerate(x1) if c not in ("market_value_avg_diff", "wc_experience_diff")]
    i_qgf = x2.index("qual_gf_per_game")
    lin = LinearRegression()
    alphas = np.logspace(-3, 3, 40)
    ridge = make_pipeline(StandardScaler(), RidgeCV(alphas=alphas))
    lasso = make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=0, max_iter=20000))
    huber = make_pipeline(StandardScaler(), HuberRegressor(max_iter=2000))
    forest = RandomForestRegressor(n_estimators=300, min_samples_leaf=5, random_state=0, n_jobs=-1)
    yeo = make_pipeline(PowerTransformer(method="yeo-johnson"), LinearRegression())

    recipes1 = [
        Recipe("Mean baseline", DummyRegressor(), family="Baseline"),
        Recipe("OLS, all 8", lin),
        Recipe("OLS, collinear pair removed", lin, columns=reduced),
        Recipe("OLS, Yeo-Johnson", yeo),
        Recipe("OLS, log MV + exp. (kept)", lin, logs=[i_mv, i_exp]),
        Recipe("OLS, logs chosen in inner CV", lin, nested_logs=True),
        Recipe("OLS, FIFA points only", lin, columns=[0]),
        Recipe("Ridge (alpha by CV)", ridge, logs=[i_mv, i_exp], family="Regularised linear"),
        Recipe("Lasso (alpha by CV)", lasso, logs=[i_mv, i_exp], family="Regularised linear"),
        Recipe("Huber (robust)", huber, logs=[i_mv, i_exp], family="Robust linear"),
        Recipe("Random forest", forest, family="Non-linear check"),
    ]
    poisson = make_pipeline(StandardScaler(), PoissonRegressor(alpha=1e-4, max_iter=2000))
    recipes2 = [
        Recipe("Mean baseline", DummyRegressor(), family="Baseline"),
        Recipe("OLS, all 8", lin),
        Recipe("OLS, Yeo-Johnson", yeo),
        Recipe("OLS, log qual. GF (kept)", lin, logs=[i_qgf]),
        Recipe("OLS, logs chosen in inner CV", lin, nested_logs=True),
        Recipe("OLS, 2 qualifying rates", lin, columns=[0, 1]),
        Recipe("Ridge (alpha by CV)", ridge, logs=[i_qgf], family="Regularised linear"),
        Recipe("Lasso (alpha by CV)", lasso, logs=[i_qgf], family="Regularised linear"),
        Recipe("Huber (robust)", huber, logs=[i_qgf], family="Robust linear"),
        Recipe("Poisson GLM", poisson, logs=[i_qgf], family="Count model"),
        Recipe("Random forest", forest, family="Non-linear check"),
    ]

    s1 = evaluate(recipes1, X1, y1)
    s2 = evaluate(recipes2, X2, y2, groups)
    s2_ungrouped = evaluate([recipes2[0], recipes2[3]], X2, y2)
    t1 = summarise(s1)
    t2 = summarise(s2)

    # Paired comparisons on the same 20 repeats
    def paired(scores, a, b):
        d = scores[a]["rmse"] - scores[b]["rmse"]
        return {"mean_diff": float(d.mean()), "a_better_pct": float((d < 0).mean() * 100)}

    # Football view of 2.1: does the sign of the prediction pick the winner?
    oof1 = s1["OLS, log MV + exp. (kept)"]["oof"]
    decided = y1 != 0
    winner_model = float((np.sign(oof1[decided]) == np.sign(y1[decided])).mean() * 100)
    fifa = match.fifa_points_diff.to_numpy()
    winner_fifa = float((np.sign(fifa[decided]) == np.sign(y1[decided])).mean() * 100)
    within1 = float((np.abs(y1 - oof1) <= 1).mean() * 100)

    # Coefficients of the kept models
    k1 = match[[c for c in x1 if c not in ("market_value_avg_diff", "wc_experience_diff")]].copy()
    k1["slog_market_value"] = base.signed_log(match.market_value_avg_diff)
    k1["slog_wc_experience"] = base.signed_log(match.wc_experience_diff)
    k2 = team[[c for c in x2 if c != "qual_gf_per_game"]].copy()
    k2.insert(0, "log_qual_gf", np.log1p(team.qual_gf_per_game))
    coefs = fig_coefficients(match, k1, team, k2, CHARTS / "hd_coefficients.png")

    # Poisson fitted means (out-of-fold) for the scoreline figure
    pois_mu = np.clip(s2["Poisson GLM"]["oof"], 1e-6, None)

    fig_signal(match, x1, team, x2, CHARTS / "hd_signal.png")
    fig_competition(t1, t2, CHARTS / "hd_competition.png",
                    "OLS, log MV + exp. (kept)", "OLS, log qual. GF (kept)")
    dist = fig_story(match, y1, oof1, team, y2, pois_mu, CHARTS / "hd_story.png")

    # Residual diagnostics on the kept in-sample fits
    f1 = sm.OLS(y1, sm.add_constant(k1)).fit()
    f2 = sm.OLS(y2, sm.add_constant(k2)).fit()
    from statsmodels.stats.diagnostic import het_breuschpagan
    from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
    Z = sm.add_constant(match[x1]).to_numpy(float)
    diag = {
        "bp_p_21": float(het_breuschpagan(f1.resid, f1.model.exog)[1]),
        "bp_p_22": float(het_breuschpagan(f2.resid, f2.model.exog)[1]),
        "shapiro_p_21": float(stats.shapiro(f1.resid).pvalue),
        "shapiro_p_22": float(stats.shapiro(f2.resid).pvalue),
        "max_vif_21": float(max(vif(Z, i) for i in range(1, Z.shape[1]))),
        "goals_mean": float(y2.mean()),
        "goals_var": float(y2.var(ddof=1)),
        "draws": int((y1 == 0).sum()),
    }

    results = {
        "table_21": t1.round(4).to_dict(orient="records"),
        "table_22": t2.round(4).to_dict(orient="records"),
        "ungrouped_22": {k: float(v["rmse"].mean()) for k, v in s2_ungrouped.items()},
        "paired": {
            "21_kept_vs_all8": paired(s1, "OLS, log MV + exp. (kept)", "OLS, all 8"),
            "21_fifa_vs_kept": paired(s1, "OLS, FIFA points only", "OLS, log MV + exp. (kept)"),
            "21_ridge_vs_kept": paired(s1, "Ridge (alpha by CV)", "OLS, log MV + exp. (kept)"),
            "21_nested_vs_kept": paired(s1, "OLS, logs chosen in inner CV", "OLS, log MV + exp. (kept)"),
            "22_kept_vs_all8": paired(s2, "OLS, log qual. GF (kept)", "OLS, all 8"),
            "22_two_vs_kept": paired(s2, "OLS, 2 qualifying rates", "OLS, log qual. GF (kept)"),
            "22_pois_vs_kept": paired(s2, "Poisson GLM", "OLS, log qual. GF (kept)"),
            "22_kept_vs_base": paired(s2, "OLS, log qual. GF (kept)", "Mean baseline"),
        },
        "winner": {"model_pct": winner_model, "fifa_pct": winner_fifa,
                   "decided": int(decided.sum()), "within1_pct": within1},
        "coefficients": coefs,
        "diagnostics": diag,
        "scorelines": dist,
    }
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "hd_results.json").write_text(json.dumps(results, indent=2))

    pd.set_option("display.width", 160)
    print("2.1 goal difference, 5-fold x 20 repeats")
    print(t1.round(3).to_string(index=False))
    print("\n2.2 goals scored, grouped 5-fold x 20 repeats")
    print(t2.round(3).to_string(index=False))
    print("\n2.2 ungrouped (the original fold design):", results["ungrouped_22"])
    print("\nPaired:", json.dumps(results["paired"], indent=1))
    print("Winner:", results["winner"])
    print("Diagnostics:", diag)
    print("Coefficients:", json.dumps(coefs, indent=1))


if __name__ == "__main__":
    main()
