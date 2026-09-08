# HIT140 Assessment 2 — Task 2: Discipline

## Research question

Is the mean number of yellow cards per match different between teams that progressed beyond the group stage and teams eliminated in the group stage in the 2026 FIFA World Cup?

## Source files

- `data/raw/fbref_squad_standard_2026_raw.csv`: FBref squad standard-stats export for the 48 teams.
- `data/raw/fifa_round_of_32_teams_2026.csv`: list of the 32 teams that progressed beyond the group stage.

No source URL is recorded in the supplied files, so none is asserted here.

## Engineered variable

`YellowCardsPerMatch = CrdY / MP`, where `CrdY` is the FBref yellow-card count and `MP` is matches played. The scripts locate the actual FBref header before selecting these fields.

## Folder structure

```text
data/raw/          supplied FBref and FIFA CSV files
data/processed/    prepared 48-team analysis CSV
docs/              process, methods, sources, decisions, and summary
figures/           comparison boxplot and histogram
src/               validation, preparation, and analysis scripts
```

## Run instructions

From this task folder, run in this exact order:

```bash
python src/validate_data.py
python src/prepare_data.py
python src/analyze.py
```

Required Python packages are `pandas`, `numpy`, `scipy`, and `matplotlib`.

## Results

The progressed teams had a mean of 1.267969 yellow cards per match, compared with 1.437500 for group-stage eliminated teams. The observed difference (Progressed minus Eliminated) was -0.169531, with a 95% confidence interval of (-0.536665, 0.197602). The Week 4 two-sided test gave `t = -0.984240`, conservative `df = 15`, and `p = 0.340608`. At the 5% level, the analysis fails to reject the null hypothesis; the data do not provide sufficient evidence of a difference in group means.

## Limitations

The 48 teams are the tournament teams, not a simple random sample, so broad population generalisation is not supported. The per-match rate accounts for different match counts, but does not adjust for referee, opponent, match state, or playing style, or equalise the precision of rates based on different match counts. Several observations were flagged by the 1.5 x IQR rule. Progression and discipline are associated measurements; this analysis does not show that progression caused any difference.

## Documentation

The four primary records document process, final methods, sources, and decisions.

- [docs/project_journal.md](docs/project_journal.md)
- [docs/analysis_plan.md](docs/analysis_plan.md)
- [docs/data_sources.md](docs/data_sources.md)
- [docs/decision_log.md](docs/decision_log.md)
- [docs/analysis_summary.md](docs/analysis_summary.md)
