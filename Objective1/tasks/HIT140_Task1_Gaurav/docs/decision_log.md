# Task 1 decision log

Task 1 was initially squad-level. The group later agreed to redesign Task 1 at player level to diversify observational units and demonstrate Week 3 sampling. Tasks 2–4 remain team-level and use all 48 teams. This redesign changes only Task 1.

Use the provided local FBref player table, without network scraping or FIFA HTML extraction. Preserve source order, omit repeated headers, and avoid extracting the commented duplicate table.

Before the playing-time threshold, there are 299 DF and 337 MF with positive 90s and nonmissing Int. Their 90s distributions are: DF min 0.1, Q1 1.15, median 2.7, Q3 3.95, max 8.3; MF min 0.1, Q1 1.0, median 2.1, Q3 3.0, max 8.3. At thresholds 0.1, 0.5 and 1.0, DF/MF counts are 299/337, 275/306 and 253/254. The preferred 1.0 threshold retains at least 30 per group and reduces unstable rates from very short exposure; it was selected using playing time and counts, before sample outcome analysis. If 1.0 failed, the script would try the lowest simple threshold 0.1, then 0.5; if neither supports 30 in both groups it stops.

Eligibility requires Pos exactly DF or exactly MF, 90s > 0, and nonmissing Int, followed by a minimum of 1.0 90s (approximately 90 minutes using the rounded source field). Mixed positions (including DF,MF and FW,MF), GK and FW are excluded. The final eligible population contains 253 DF and 254 MF (507 players); the full population is saved to data/processed/task1_player_population.csv.

Within each eligible position group, pandas DataFrame.sample(n=30, replace=False, random_state=140) selects a simple random sample without replacement. The source HTML row order is preserved before sampling; the seed is reset to 140 for each group. random_state=140 makes selection reproducible for the same input order and software. The combined sample has 60 players and is saved to data/processed/task1_player_sample.csv. This is SRS within each position, not an unrestricted SRS of all 507 players. Only the random sample is analyzed.

Normalize interceptions by each player's exposure rather than compare unequal-exposure totals. Use the stipulated conservative two-sample t method at alpha 0.05, not a pooled-variance test. Keep legitimate IQR outliers and report them. Use common histogram bins for fair visual comparison.

Players within the same team may share team/tactical context, so perfect independence is a limitation. Sampling fractions are 30/253 and 30/254 (about 12%); the required course SE omits a finite-population correction. Random sampling does not remove team dependence. The t procedure is approximate, especially with skewness or outliers. Rounded 90s affect calculated rates. Inference concerns the eligible players represented by the saved table, not excluded positions or all football players. Position-associated differences do not establish causation.

No dates or other members' activities are invented. Historical squad files remain marked as superseded; Tasks 2–4 and the protected repository are outside this redesign.
