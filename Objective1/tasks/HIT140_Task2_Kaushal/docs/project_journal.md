# Project journal — Task 2: Discipline

This process record uses stages rather than inferred dates. It follows the four-member group's Task 4 workflow described in the shared project context; it does not assign undocumented individual activity.

## Stage 1 — Source evaluation and shared acquisition lesson

In the earlier Task 4 workflow completed by Bhargav, direct automated access to FBref had been blocked. This prior team experience informed the shared decision to use FBref table CSV exports for Tasks 1–3 rather than repeat aggressive automated scraping. It is a shared project lesson, not a record of task-specific failed scraping attempts.

FBref supplied the task-specific squad statistics. The already validated FIFA Round-of-32 classification supplied the common progression grouping, maintaining consistency across the project.

## Stage 2 — Task scope and source acquisition

The task focuses on discipline at squad level. FBref Standard Stats provided the usable `Squad`, `MP`, and `CrdY` fields needed to compare yellow-card rates across progression groups.

The local acquisition records are `data/raw/fbref_squad_standard_2026_raw.csv` and `data/raw/fifa_round_of_32_teams_2026.csv`. Exact source URLs and acquisition dates are not recorded in the supplied documentation.

## Stage 3 — Validation and cleaning

The actual FBref field-label row was located beneath the grouped header, and numeric analysis fields were parsed. Raw shape was `(48, 21)`; selected shape after response construction and before grouping was `(48, 4)`. The selected table contains `Squad`, `MP`, `CrdY`, and the engineered `YellowCardsPerMatch` response.

Squad names were trimmed and only an initial lowercase two- or three-letter country-code prefix followed by whitespace was removed. The explicit known alias `{"Bosnia–Herz": "Bosnia and Herzegovina"}` harmonised FBref with FIFA. No fuzzy matching was used.

Validation confirmed 48 unique squads, 0 missing selected analysis values, and 0 duplicate squads. All FIFA progression names matched after explicit harmonisation. The final groups contain 32 Progressed and 16 Group-stage eliminated teams. Denominators were positive and source counts non-negative. No missing analysis values required imputation.

## Stage 4 — Feature engineering and integration

The engineered response is `YellowCardsPerMatch = CrdY / MP`. Dividing yellow cards by matches played makes exposure more comparable than raw totals. It does not adjust for referee, opponent or match context, or equalise the precision of rates based on different match counts.

Membership in the validated FIFA progression list identifies Progressed teams; the other teams in the complete FBref tournament field are Group-stage eliminated. The processed output is `data/processed/task2_discipline_progression.csv`.

## Stage 5 — Descriptive statistics and assumption checks

Group counts, means, medians, sample SDs, ranges, quartiles, and IQRs were calculated. Progressed skewness was 0.597588 and eliminated skewness was -0.456322. The 1.5 x IQR rule flagged Egypt = 2.4000 in the progressed group and Czechia = 0.3333, Tunisia = 0.3333, and Türkiye = 0.6667 in the eliminated group. These observations were retained because they are valid tournament observations and there is no evidence of data error; an outlier flag alone does not establish invalidity.

Including all 48 tournament teams does not provide simple random sampling. These checks support a cautious course comparison, with interpretation primarily restricted to the 2026 FIFA World Cup.

## Stage 6 — Confidence intervals and Week 4 hypothesis test

The completed analysis used State → Plan → Solve → Conclude, 95% t confidence intervals, `SE = sqrt(s1^2/n1 + s2^2/n2)`, conservative `df = min(n1 - 1, n2 - 1) = 15`, and `alpha = 0.05`. Critical values and p-values used `scipy.stats.t`.

The two-sided p = 0.340608. **Fail to reject H0.** There is insufficient evidence of a difference in mean yellow cards per match between progressed and eliminated teams. Full descriptive and inferential results are retained in [analysis_plan.md](analysis_plan.md).

## Stage 7 — Interpretation, figures, and documentation

Interpretation is tournament-specific and concerns association only, not causation. Task-specific context and remaining methodological limitations are recorded in the analysis plan.

Completed figure outputs are [the boxplot](../figures/task2_yellow_cards_per_match_boxplot.png) and [the histogram](../figures/task2_yellow_cards_per_match_histogram.png). The four primary documentation files record process, final method, sources, and decisions. The analysis is complete; this documentation update does not rerun or alter the analysis outputs.
