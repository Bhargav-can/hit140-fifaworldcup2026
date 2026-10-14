# Task 1 analysis plan

Task 1 was initially squad-level. The group later agreed to redesign Task 1 at player level to diversify observational units and demonstrate Week 3 sampling. Tasks 2–4 remain team-level and use all 48 teams. This redesign changes only Task 1.

## State

Do defenders have a higher mean number of interceptions per 90 minutes than midfielders in the 2026 FIFA World Cup?

H0: mu_DF = mu_MF. H1: mu_DF > mu_MF. Alpha = 0.05; one-sided test. The means refer to the eligible player populations.

## Plan — Week 3 population and sampling

Task 1 uses the saved FBref webpage data/raw/fbref_player_miscellaneous_2026.html and programmatic HTML extraction of the Player Miscellaneous Stats 2026 World Cup table (id stats_misc). It does not use FIFA HTML extraction. The visible table is preferred; commented HTML is searched only if the visible table is absent, avoiding double counting. Repeated headers are excluded. Player, Pos, Squad, 90s and Int are selected by data-stat attributes; the Squad link text excludes decorative country codes. Blank values are not filled with zeros. No acquisition date is asserted.

Eligibility requires Pos exactly DF or exactly MF, 90s > 0, and nonmissing Int, followed by a minimum of 1.0 90s (approximately 90 minutes using the rounded source field). Mixed positions (including DF,MF and FW,MF), GK and FW are excluded. The final eligible population contains 253 DF and 254 MF (507 players); the full population is saved to data/processed/task1_player_population.csv.

Before the playing-time threshold, there are 299 DF and 337 MF with positive 90s and nonmissing Int. Their 90s distributions are: DF min 0.1, Q1 1.15, median 2.7, Q3 3.95, max 8.3; MF min 0.1, Q1 1.0, median 2.1, Q3 3.0, max 8.3. At thresholds 0.1, 0.5 and 1.0, DF/MF counts are 299/337, 275/306 and 253/254. The preferred 1.0 threshold retains at least 30 per group and reduces unstable rates from very short exposure; it was selected using playing time and counts, before sample outcome analysis. If 1.0 failed, the script would try the lowest simple threshold 0.1, then 0.5; if neither supports 30 in both groups it stops.

Within each eligible position group, pandas DataFrame.sample(n=30, replace=False, random_state=140) selects a simple random sample without replacement. The source HTML row order is preserved before sampling; the seed is reset to 140 for each group. random_state=140 makes selection reproducible for the same input order and software. The combined sample has 60 players and is saved to data/processed/task1_player_sample.csv. This is SRS within each position, not an unrestricted SRS of all 507 players. Only the random sample is analyzed.

## Solve — Week 4

InterceptionsPer90 = Int / 90s. Give each sampled player equal weight. Calculate n, mean, median, sample standard deviation (ddof=1), min, max, Q1, Q3, IQR and pandas unbiased sample skewness separately for DF and MF. Quartiles use pandas linear interpolation. Flag observations strictly outside Q1 − 1.5 × IQR and Q3 + 1.5 × IQR; retain valid outliers.

Each group mean has a two-sided 95% t interval: mean ± scipy.stats.t.ppf(0.975, n−1) × s/sqrt(n).

Difference = mean_DF − mean_MF. SE = sqrt(s_DF²/n_DF + s_MF²/n_MF). Conservative df = min(n_DF−1, n_MF−1) = 29. Difference 95% CI = difference ± scipy.stats.t.ppf(0.975, df) × SE. t = difference/SE; one-sided p = scipy.stats.t.sf(t, df). No pooled variance or Welch–Satterthwaite df is substituted. Calculate with unrounded values. The requested two-sided 95% CI is reported alongside the one-sided test; they have different rejection boundaries.

The boxplot and histogram use only sampled observations. Both histogram panels use the same eight-bin edges calculated from the combined sample and shared axis scales.

## Conclude

Reject H0 only if p < 0.05; otherwise fail to reject it. See analysis_summary.md for computed results.

Players within the same team may share team/tactical context, so perfect independence is a limitation. Sampling fractions are 30/253 and 30/254 (about 12%); the required course SE omits a finite-population correction. Random sampling does not remove team dependence. The t procedure is approximate, especially with skewness or outliers. Rounded 90s affect calculated rates. Inference concerns the eligible players represented by the saved table, not excluded positions or all football players. Position-associated differences do not establish causation.
