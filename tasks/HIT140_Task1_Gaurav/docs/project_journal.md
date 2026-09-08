# Task 1 project journal

Task 1 was initially squad-level. The group later agreed to redesign Task 1 at player level to diversify observational units and demonstrate Week 3 sampling. Tasks 2–4 remain team-level and use all 48 teams. This redesign changes only Task 1.

The initial squad-level question compared progression groups. It is superseded by the player-level DF versus MF question; legacy squad CSVs are retained as historical inputs/outputs and are not read by the current pipeline.

Task 1 uses the saved FBref webpage data/raw/fbref_player_miscellaneous_2026.html and programmatic HTML extraction of the Player Miscellaneous Stats 2026 World Cup table (id stats_misc). It does not use FIFA HTML extraction. The visible table is preferred; commented HTML is searched only if the visible table is absent, avoiding double counting. Repeated headers are excluded. Player, Pos, Squad, 90s and Int are selected by data-stat attributes; the Squad link text excludes decorative country codes. Blank values are not filled with zeros. No acquisition date is asserted.

Validation found 1,039 raw player rows and 1,039 unique player/squad pairs, with no missing required fields or duplicates. Raw 90s ranges from 0 to 9; Int ranges from 0 to 15.

Before the playing-time threshold, there are 299 DF and 337 MF with positive 90s and nonmissing Int. Their 90s distributions are: DF min 0.1, Q1 1.15, median 2.7, Q3 3.95, max 8.3; MF min 0.1, Q1 1.0, median 2.1, Q3 3.0, max 8.3. At thresholds 0.1, 0.5 and 1.0, DF/MF counts are 299/337, 275/306 and 253/254. The preferred 1.0 threshold retains at least 30 per group and reduces unstable rates from very short exposure; it was selected using playing time and counts, before sample outcome analysis. If 1.0 failed, the script would try the lowest simple threshold 0.1, then 0.5; if neither supports 30 in both groups it stops.

Eligibility requires Pos exactly DF or exactly MF, 90s > 0, and nonmissing Int, followed by a minimum of 1.0 90s (approximately 90 minutes using the rounded source field). Mixed positions (including DF,MF and FW,MF), GK and FW are excluded. The final eligible population contains 253 DF and 254 MF (507 players); the full population is saved to data/processed/task1_player_population.csv.

Within each eligible position group, pandas DataFrame.sample(n=30, replace=False, random_state=140) selects a simple random sample without replacement. The source HTML row order is preserved before sampling; the seed is reset to 140 for each group. random_state=140 makes selection reproducible for the same input order and software. The combined sample has 60 players and is saved to data/processed/task1_player_sample.csv. This is SRS within each position, not an unrestricted SRS of all 507 players. Only the random sample is analyzed.

The Week 4 analysis calculates sample summaries, outliers, confidence intervals and a one-sided t test, and generates both figures. Results are in analysis_summary.md. No dates or activities by individual group members are inferred or assigned.
