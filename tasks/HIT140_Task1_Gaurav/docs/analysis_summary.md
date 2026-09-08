# Task 1 player-level analysis summary

## State

Do defenders have a higher mean number of interceptions per 90 minutes than midfielders in the 2026 FIFA World Cup?

`H0: mu_DF = mu_MF`; `H1: mu_DF > mu_MF`. Alpha = 0.05; one-sided test.

## Plan

Analyze only the reproducible random sample: 30 DF and 30 MF, sampled without replacement separately using random_state=140. See analysis_plan.md for population eligibility and sampling details.

## Solve

| Group | n | Mean | Median | SD | Min | Max | Q1 | Q3 | IQR | Skewness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DF | 30 | 1.103230 | 1.121593 | 0.661466 | 0.000000 | 2.750000 | 0.591085 | 1.350282 | 0.759197 | 0.539660 |
| MF | 30 | 0.994448 | 0.909091 | 0.830452 | 0.000000 | 3.636364 | 0.421908 | 1.465909 | 1.044001 | 1.274066 |

DF mean 95% CI: (0.856234, 1.350225).
DF 1.5 × IQR fences: [-0.5477105505189853, 2.489078307712521]. Outliers (retained): [{'Player': 'Khuliso Mudau', 'Squad': 'South Africa', 'InterceptionsPer90': 2.75}].

MF mean 95% CI: (0.684352, 1.304544).
MF 1.5 × IQR fences: [-1.144094244330093, 3.031911092052601]. Outliers (retained): [{'Player': 'Salih Özcan', 'Squad': 'Türkiye', 'InterceptionsPer90': 3.636363636363636}].

DF − MF = 0.108782; SE = 0.193837; conservative df = 29.
Two-sided 95% CI for difference: (-0.287660, 0.505224).
t = 0.561203; one-sided p = 0.28948518.

## Conclude

Fail to reject H0. The sample does not provide sufficient evidence that eligible defenders have a higher mean interceptions-per-90 rate than eligible midfielders at alpha = 0.05.

Players within the same team may share team/tactical context, so perfect independence is a limitation.
Inference is restricted to eligible players in the saved table; position is observational and does not establish causation.
Rounded 90s affect rates. The specified course SE does not apply a finite-population correction.
Skewness and outliers can affect t inference; flagged observations are retained, not removed.

This compares position-associated rates, not a causal effect of position.
