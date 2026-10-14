# Analysis summary — Task 2

For the final method and detailed result record, see [analysis_plan.md](analysis_plan.md). This file retains the existing concise summary.

## Research question

Is the mean number of yellow cards per match different between teams that progressed beyond the group stage and teams eliminated in the group stage in the 2026 FIFA World Cup?

## Variables

- Explanatory variable: progression status (`Progressed` or `Group-stage eliminated`).
- Response variable: `YellowCardsPerMatch = CrdY / MP`.

## Source and data preparation

The analysis uses the supplied FBref squad standard-stats CSV and FIFA progression CSV. The FBref two-row header was detected, the initial lowercase country-code prefix was removed from squad names, and the explicit Bosnia alias was applied. The final data contain 48 unique teams: 32 progressed and 16 eliminated. The selected analysis fields have no missing values or duplicate squads, and there were no unmatched progression names.

## Descriptive results

| Group | Count | Mean | Median | SD | Min | Max | Q1 | Q3 | IQR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Progressed | 32 | 1.267969 | 1.250000 | 0.465822 | 0.500000 | 2.400000 | 0.950000 | 1.525000 | 0.575000 |
| Group-stage eliminated | 16 | 1.437500 | 1.333333 | 0.605148 | 0.333333 | 2.333333 | 1.333333 | 1.750000 | 0.416667 |

The observed difference in means (Progressed minus Eliminated) was -0.169531. Skewness was 0.597588 for progressed teams and -0.456322 for eliminated teams. The 1.5 x IQR rule flagged Egypt in the progressed group and Czechia, Tunisia, and Türkiye in the eliminated group as possible outliers. They were retained because they are valid observed team values.

## Confidence intervals

- Progressed mean: 95% CI (1.100022, 1.435915).
- Group-stage eliminated mean: 95% CI (1.115040, 1.759960).
- Difference in means: 95% CI (-0.536665, 0.197602), using the Week 4 conservative `df = 15` method.

## Hypothesis test

**STATE:** `H0: mu_progressed = mu_eliminated`; `H1: mu_progressed != mu_eliminated`.

**PLAN:** Use the independent two-sample t procedure with `SE = sqrt(s1^2/n1 + s2^2/n2)` and `df = min(n1 - 1, n2 - 1)`. This is a two-sided test at `alpha = 0.05`.

**SOLVE:** `SE = 0.172246`, `t = -0.984240`, `df = 15`, and two-sided `p = 0.340608`.

**CONCLUDE:** Fail to reject the null hypothesis. The 2026 World Cup data do not provide sufficient evidence that the two groups differed in mean yellow cards per match.

## Limitations

The teams form the tournament field rather than a simple random sample, so the sampling condition for broad population inference is not met. Interpretation is restricted primarily to these 48 teams in this tournament. The possible outliers and differences in referees, opponents, schedules, match states, and matches played may affect the comparison. The result describes association and does not establish that progression caused a difference in yellow cards.
