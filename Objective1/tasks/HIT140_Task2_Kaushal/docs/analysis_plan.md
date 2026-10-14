# Analysis plan — Task 2: Discipline

This is the current, completed method and verified result record. Process history is in [project_journal.md](project_journal.md), source provenance in [data_sources.md](data_sources.md), and rationale in [decision_log.md](decision_log.md).

## Research question

Is the mean number of yellow cards per match different between teams that progressed beyond the group stage and teams eliminated in the group stage in the 2026 FIFA World Cup?

## Variables

- Explanatory variable: progression status (`Progressed` or `Group-stage eliminated`).
- Response variable: `YellowCardsPerMatch = CrdY / MP`.

## Source and data preparation

The analysis uses the supplied FBref squad standard-stats CSV and FIFA progression CSV. The FBref two-row header was detected, the initial lowercase country-code prefix was removed from squad names, and the explicit Bosnia alias was applied. The final data contain 48 unique teams: 32 progressed and 16 eliminated. The selected analysis fields have no missing values or duplicate squads, and there were no unmatched progression names.

## Validation status and response construction

Raw shape: `(48, 21)`. Selected shape before progression classification: `(48, 4)`. The selected table contains `Squad`, `MP`, `CrdY`, and the engineered `YellowCardsPerMatch` response.

Validation confirmed 48 unique squads, 0 missing selected analysis values, and 0 duplicate squads. All FIFA progression names matched after explicit harmonisation. The final groups contain 32 Progressed and 16 Group-stage eliminated teams.

Dividing yellow cards by matches played makes exposure more comparable than raw totals. It does not adjust for referee, opponent or match context, or equalise the precision of rates based on different match counts. Each squad contributes one response value; group means give each team equal weight. Progression is the categorical grouping variable and the calculated rate is the quantitative response.

## Assumption checks

Progressed skewness was 0.597588 and eliminated skewness was -0.456322. The 1.5 x IQR rule flagged Egypt = 2.4000 in the progressed group and Czechia = 0.3333, Tunisia = 0.3333, and Türkiye = 0.6667 in the eliminated group. These observations were retained because they are valid tournament observations and there is no evidence of data error; an outlier flag alone does not establish invalidity.

All tournament teams are included, so sampling is not simple random sampling. The groups contain distinct teams, but shared matches and opponents can create dependence; the course t procedure does not establish independence or a random-sampling design. Skewness and IQR checks describe distributional shape, not proof of normality.

## Descriptive results

| Group | Count | Mean | Median | SD | Min | Max | Q1 | Q3 | IQR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Progressed | 32 | 1.267969 | 1.250000 | 0.465822 | 0.500000 | 2.400000 | 0.950000 | 1.525000 | 0.575000 |
| Group-stage eliminated | 16 | 1.437500 | 1.333333 | 0.605148 | 0.333333 | 2.333333 | 1.333333 | 1.750000 | 0.416667 |

The observed difference in means (Progressed minus Eliminated) was -0.169531. Skewness was 0.597588 for progressed teams and -0.456322 for eliminated teams. The 1.5 x IQR rule flagged Egypt in the progressed group and Czechia, Tunisia, and Türkiye in the eliminated group as possible outliers. They were retained because they are valid observed team values.

## Confidence intervals

Each group mean interval uses `mean ± scipy.stats.t.ppf(0.975, n - 1) * s / sqrt(n)`, with sample SD (`ddof=1`). The difference is always Progressed minus Eliminated. Its two-sided 95% interval uses `difference ± scipy.stats.t.ppf(0.975, df) * SE`, where `SE = sqrt(s1^2/n1 + s2^2/n2)` and conservative `df = min(n1 - 1, n2 - 1) = 15`. Calculations use unrounded values; reported results are rounded to six decimal places.


- Progressed mean: 95% CI (1.100022, 1.435915).
- Group-stage eliminated mean: 95% CI (1.115040, 1.759960).
- Difference in means: 95% CI (-0.536665, 0.197602), using the Week 4 conservative `df = 15` method.

## Hypothesis test — State → Plan → Solve → Conclude

**STATE:** `H0: mu_progressed = mu_eliminated`; `H1: mu_progressed != mu_eliminated`.

**PLAN:** Use the independent two-sample t procedure with `SE = sqrt(s1^2/n1 + s2^2/n2)` and `df = min(n1 - 1, n2 - 1)`. This is a two-sided test at `alpha = 0.05`.

The test statistic is `t = (mean_progressed - mean_eliminated) / SE`, under a null difference of zero. `scipy.stats.t` supplies critical values and p-values; the p-value is calculated as `2 * scipy.stats.t.sf(abs(t), df)`.

**SOLVE:** `SE = 0.172246`, `t = -0.984240`, `df = 15`, and two-sided `p = 0.340608`.

**CONCLUDE:** Fail to reject the null hypothesis. The 2026 World Cup data do not provide sufficient evidence that the two groups differed in mean yellow cards per match.

## Limitations

The teams form the tournament field rather than a simple random sample, so the sampling condition for broad population inference is not met. Interpretation is restricted primarily to these 48 teams in this tournament. The possible outliers and differences in referees, opponents, schedules, match states, and matches played may affect the comparison. The result describes association and does not establish that progression caused a difference in yellow cards.

## Current completion status

Complete: acquisition, validation, cleaning/harmonisation, feature engineering, descriptive statistics, assumption checks, confidence intervals, Week 4 testing, interpretation, figures, and documentation.

- [Comparison boxplot](../figures/task2_yellow_cards_per_match_boxplot.png)
- [Comparison histogram](../figures/task2_yellow_cards_per_match_histogram.png)

The processed analysis table is `data/processed/task2_discipline_progression.csv`. Run instructions remain in the [README](../README.md).
