# HIT140 Task 1 — Player-level interceptions

Do defenders have a higher mean number of interceptions per 90 minutes than midfielders in the 2026 FIFA World Cup?

Task 1 was initially squad-level. The group later agreed to redesign Task 1 at player level to diversify observational units and demonstrate Week 3 sampling. Tasks 2–4 remain team-level and use all 48 teams. This redesign changes only Task 1.

Task 1 uses the saved FBref webpage data/raw/fbref_player_miscellaneous_2026.html and programmatic HTML extraction of the Player Miscellaneous Stats 2026 World Cup table (id stats_misc). It does not use FIFA HTML extraction. The visible table is preferred; commented HTML is searched only if the visible table is absent, avoiding double counting. Repeated headers are excluded. Player, Pos, Squad, 90s and Int are selected by data-stat attributes; the Squad link text excludes decorative country codes. Blank values are not filled with zeros. No acquisition date is asserted.

Eligibility requires Pos exactly DF or exactly MF, 90s > 0, and nonmissing Int, followed by a minimum of 1.0 90s (approximately 90 minutes using the rounded source field). Mixed positions (including DF,MF and FW,MF), GK and FW are excluded. The final eligible population contains 253 DF and 254 MF (507 players); the full population is saved to data/processed/task1_player_population.csv.

Within each eligible position group, pandas DataFrame.sample(n=30, replace=False, random_state=140) selects a simple random sample without replacement. The source HTML row order is preserved before sampling; the seed is reset to 140 for each group. random_state=140 makes selection reproducible for the same input order and software. The combined sample has 60 players and is saved to data/processed/task1_player_sample.csv. This is SRS within each position, not an unrestricted SRS of all 507 players. Only the random sample is analyzed.

## Run

Required packages: beautifulsoup4, pandas, numpy, scipy and matplotlib.

From HIT140_Task1_Gaurav:

```bash
python src/extract_player_data.py
python src/validate_data.py
python src/prepare_data.py
python src/analyze.py
python -m py_compile src/*.py
```

The pipeline saves extracted, population and sampled CSVs plus validation, sampling and analysis JSON records in data/processed. Analysis regenerates docs/analysis_summary.md and figures/task1_interceptions_per90_boxplot.png and figures/task1_interceptions_per90_histogram.png.

See [analysis summary](docs/analysis_summary.md) for results, [analysis plan](docs/analysis_plan.md) for State → Plan → Solve → Conclude, [journal](docs/project_journal.md), [sources](docs/data_sources.md), and [decisions](docs/decision_log.md). Legacy squad CSV files are retained only as historical artifacts and are not read by the current scripts.

Players within the same team may share team/tactical context, so perfect independence is a limitation. Sampling fractions are 30/253 and 30/254 (about 12%); the required course SE omits a finite-population correction. Random sampling does not remove team dependence. The t procedure is approximate, especially with skewness or outliers. Rounded 90s affect calculated rates. Inference concerns the eligible players represented by the saved table, not excluded positions or all football players. Position-associated differences do not establish causation.
