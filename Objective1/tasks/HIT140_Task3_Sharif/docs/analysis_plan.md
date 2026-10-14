# Analysis plan — Task 3: Attacking performance

This is the current, completed method and verified result record. Process history is in [project_journal.md](project_journal.md), source provenance in [data_sources.md](data_sources.md), and rationale in [decision_log.md](decision_log.md).

## Research question

Do teams that progressed beyond the group stage have a higher mean number of shots on target per 90 minutes than teams eliminated in the group stage in the 2026 FIFA World Cup?

## Variables

- Explanatory variable: progression status (`Progressed` or `Group-stage eliminated`).
- Response variable: `ShotsOnTargetPer90 = SoT / 90s`.

## Source and data preparation

The analysis uses the supplied FBref squad shooting CSV and FIFA progression CSV. The FBref two-row header was detected, the initial lowercase country-code prefix was removed from squad names, and the explicit Bosnia alias was applied. The final data contain 48 unique teams: 32 progressed and 16 eliminated. The selected analysis fields have no missing values or duplicate squads, and there were no unmatched progression names. The calculated rate agreed with the supplied `SoT/90` field within 0.06 for all teams; the maximum absolute difference was 0.051628.

## Validation status and response construction

Raw shape: `(48, 13)`. Selected shape before progression classification: `(48, 6)`. The selected table contains `Squad`, `90s`, `SoT`, `FBrefSoTPer90`, `ShotsOnTargetPer90`, and `SoTPer90AbsoluteDifference`. The maximum absolute difference between calculated and supplied rates was 0.051628. All comparisons were within the existing 0.06 tolerance. This was treated as consistent with displayed/rounded `90s` values, not as a data mismatch.

Validation confirmed 48 unique squads, 0 missing selected analysis values, and 0 duplicate squads. All FIFA progression names matched after explicit harmonisation. The final groups contain 32 Progressed and 16 Group-stage eliminated teams.

Calculate the response from `SoT / 90s` rather than relying only on a precomputed rate. The supplied rate is used only for validation. Per-90 normalisation accounts for different playing-time exposure. Each squad contributes one response value; group means give each team equal weight. Progression is the categorical grouping variable and the calculated rate is the quantitative response.

## Assumption checks

Progressed skewness was -0.099909 and eliminated skewness was 0.582384. Neither group had observations outside the 1.5 x IQR fences; all valid teams were retained.

All tournament teams are included, so sampling is not simple random sampling. The groups contain distinct teams, but shared matches and opponents can create dependence; the course t procedure does not establish independence or a random-sampling design. Skewness and IQR checks describe distributional shape, not proof of normality.

## Descriptive results

| Group | Count | Mean | Median | SD | Min | Max | Q1 | Q3 | IQR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Progressed | 32 | 4.296382 | 4.225000 | 1.582951 | 1.000000 | 7.375000 | 3.359670 | 5.462713 | 2.103044 |
| Group-stage eliminated | 16 | 2.875000 | 2.333333 | 1.234534 | 0.666667 | 5.333333 | 2.333333 | 3.666667 | 1.333333 |

The observed difference in means (Progressed minus Eliminated) was 1.421382. Skewness was -0.099909 for progressed teams and 0.582384 for eliminated teams. The 1.5 x IQR check found no possible outliers in either group.

## Confidence intervals

Each group mean interval uses `mean ± scipy.stats.t.ppf(0.975, n - 1) * s / sqrt(n)`, with sample SD (`ddof=1`). The difference is always Progressed minus Eliminated. Its two-sided 95% interval uses `difference ± scipy.stats.t.ppf(0.975, df) * SE`, where `SE = sqrt(s1^2/n1 + s2^2/n2)` and conservative `df = min(n1 - 1, n2 - 1) = 15`. Calculations use unrounded values; reported results are rounded to six decimal places.


- Progressed mean: 95% CI (3.725667, 4.867097).
- Group-stage eliminated mean: 95% CI (2.217163, 3.532837).
- Difference in means: 95% CI (0.533412, 2.309352), using the Week 4 conservative `df = 15` method.

## Hypothesis test — State → Plan → Solve → Conclude

**STATE:** `H0: mu_progressed = mu_eliminated`; `H1: mu_progressed > mu_eliminated`.

**PLAN:** Use the independent two-sample t procedure with `SE = sqrt(s1^2/n1 + s2^2/n2)` and `df = min(n1 - 1, n2 - 1)`. This is a one-sided test at `alpha = 0.05`.

The test statistic is `t = (mean_progressed - mean_eliminated) / SE`, under a null difference of zero. `scipy.stats.t` supplies critical values and p-values; the p-value is calculated as `scipy.stats.t.sf(t, df)`.

**SOLVE:** `SE = 0.416604`, `t = 3.411831`, `df = 15`, and one-sided `p = 0.001931`.

**CONCLUDE:** Reject the null hypothesis. The 2026 World Cup data provide evidence that progressed teams had a higher mean number of shots on target per 90 minutes.

## Limitations

The teams form the tournament field rather than a simple random sample, so the sampling condition for broad population inference is not met. Interpretation is restricted primarily to these 48 teams in this tournament. Opponents, schedules, match state, possession, team strength, and rounding in playing time may affect the comparison. The result describes association and does not establish that progression caused a higher shots-on-target rate.

## Current completion status

Complete: acquisition, validation, cleaning/harmonisation, feature engineering, descriptive statistics, assumption checks, confidence intervals, Week 4 testing, interpretation, figures, and documentation.

- [Comparison boxplot](../figures/task3_shots_on_target_per90_boxplot.png)
- [Comparison histogram](../figures/task3_shots_on_target_per90_histogram.png)

The processed analysis table is `data/processed/task3_attacking_progression.csv`. Run instructions remain in the [README](../README.md).
