# Shared Group Analysis Plan

## Stage — questions and designs
We use the following final four-task design. We compare defenders minus midfielders in Task 1 and progressed minus group-stage-eliminated teams in Tasks 2–4.

| Task / member | Level | Question | Response | Groups | Sampling approach | Test direction | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Task 1 — Gaurav | Player | Do defenders have a higher mean number of interceptions per 90 minutes than midfielders in the FIFA World Cup? | `InterceptionsPer90 = Int / 90s` | DF vs MF | From eligible DF = 253 and MF = 254, we randomly sample 30 each without replacement; `random_state = 140` | One-sided, DF > MF | p = 0.289485; we fail to reject H0 |
| Task 2 — Kushal | Team | Is the mean number of yellow cards per match different between progressed and group-stage-eliminated teams? | `YellowCardsPerMatch = CrdY / MP` | 32 progressed vs 16 eliminated | We retain all 48 teams | Two-sided | p = 0.340608; we fail to reject H0 |
| Task 3 — Sharif | Team | Do progressed teams have a higher mean number of shots on target per 90 minutes than eliminated teams? | `ShotsOnTargetPer90 = SoT / 90s` | 32 progressed vs 16 eliminated | We retain all 48 teams | One-sided, progressed > eliminated | p = 0.001931; we reject H0 |
| Task 4 — Bhargav | Team | Do progressed teams have a higher mean goalkeeper Save% than eliminated teams? | Goalkeeper Save% | 32 progressed vs 16 eliminated | We retain all 48 teams | One-sided, progressed > eliminated | p = 0.0183; we reject H0 |

## Stage — final statistical evidence
We use alpha = 0.05, the course two-group standard error, and `df = min(n1 - 1, n2 - 1)`. We report two-sided 95% confidence intervals.

| Task | First-group mean | Second-group mean | Mean difference | 95% CI for difference | t | df |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1.103230 | 0.994448 | 0.108782 | (-0.287660, 0.505224) | 0.561203 | 29 |
| 2 | 1.267969 | 1.437500 | -0.169531 | (-0.536665, 0.197602) | -0.984240 | 15 |
| 3 | 4.296382 | 2.875000 | 1.421382 | (0.533412, 2.309352) | 3.411831 | 15 |
| 4 | 67.99 | 58.53 | 9.46 percentage points | (0.67, 18.26) percentage points | 2.2934 | 15 |

## Stage — interpretation
We find insufficient evidence for higher defender interceptions or a difference in yellow cards per match. We find evidence for higher mean shots on target per 90 and higher mean goalkeeper Save% among progressed teams under our course test assumptions. We report associations, not causal effects, and do not interpret non-rejection as proof of equality.
