# Analysis summary — Task 3

For the final method and detailed result record, see [analysis_plan.md](analysis_plan.md). This file retains the existing concise summary.

## Research question

Do teams that progressed beyond the group stage have a higher mean number of shots on target per 90 minutes than teams eliminated in the group stage in the 2026 FIFA World Cup?

## Variables

- Explanatory variable: progression status (`Progressed` or `Group-stage eliminated`).
- Response variable: `ShotsOnTargetPer90 = SoT / 90s`.

## Source and data preparation

The analysis uses the supplied FBref squad shooting CSV and FIFA progression CSV. The FBref two-row header was detected, the initial lowercase country-code prefix was removed from squad names, and the explicit Bosnia alias was applied. The final data contain 48 unique teams: 32 progressed and 16 eliminated. The selected analysis fields have no missing values or duplicate squads, and there were no unmatched progression names. The calculated rate agreed with the supplied `SoT/90` field within 0.06 for all teams; the maximum absolute difference was 0.051628.

## Descriptive results

| Group | Count | Mean | Median | SD | Min | Max | Q1 | Q3 | IQR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Progressed | 32 | 4.296382 | 4.225000 | 1.582951 | 1.000000 | 7.375000 | 3.359670 | 5.462713 | 2.103044 |
| Group-stage eliminated | 16 | 2.875000 | 2.333333 | 1.234534 | 0.666667 | 5.333333 | 2.333333 | 3.666667 | 1.333333 |

The observed difference in means (Progressed minus Eliminated) was 1.421382. Skewness was -0.099909 for progressed teams and 0.582384 for eliminated teams. The 1.5 x IQR check found no possible outliers in either group.

## Confidence intervals

- Progressed mean: 95% CI (3.725667, 4.867097).
- Group-stage eliminated mean: 95% CI (2.217163, 3.532837).
- Difference in means: 95% CI (0.533412, 2.309352), using the Week 4 conservative `df = 15` method.

## Hypothesis test

**STATE:** `H0: mu_progressed = mu_eliminated`; `H1: mu_progressed > mu_eliminated`.

**PLAN:** Use the independent two-sample t procedure with `SE = sqrt(s1^2/n1 + s2^2/n2)` and `df = min(n1 - 1, n2 - 1)`. This is a one-sided test at `alpha = 0.05`.

**SOLVE:** `SE = 0.416604`, `t = 3.411831`, `df = 15`, and one-sided `p = 0.001931`.

**CONCLUDE:** Reject the null hypothesis. The 2026 World Cup data provide evidence that progressed teams had a higher mean number of shots on target per 90 minutes.

## Limitations

The teams form the tournament field rather than a simple random sample, so the sampling condition for broad population inference is not met. Interpretation is restricted primarily to these 48 teams in this tournament. Opponents, schedules, match state, possession, team strength, and rounding in playing time may affect the comparison. The result describes association and does not establish that progression caused a higher shots-on-target rate.
