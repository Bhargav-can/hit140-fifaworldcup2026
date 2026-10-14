# HIT140 Assessment 2 — Task 3: Attacking performance

## Research question

Do teams that progressed beyond the group stage have a higher mean number of shots on target per 90 minutes than teams eliminated in the group stage in the 2026 FIFA World Cup?

## Source files

- `data/raw/fbref_squad_shooting_2026_raw.csv`: FBref squad shooting export for the 48 teams.
- `data/raw/fifa_round_of_32_teams_2026.csv`: list of the 32 teams that progressed beyond the group stage.

No source URL is recorded in the supplied files, so none is asserted here.

## Engineered variable

`ShotsOnTargetPer90 = SoT / 90s`, where `SoT` is the FBref shots-on-target count and `90s` is playing time measured in 90-minute units. The calculated rate was compared with the supplied `SoT/90` field. The maximum absolute difference was 0.051628, and all values agreed within 0.06, a tolerance used for rounding in the displayed `90s` values.

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

The progressed teams had a mean of 4.296382 shots on target per 90, compared with 2.875000 for group-stage eliminated teams. The observed difference (Progressed minus Eliminated) was 1.421382, with a 95% confidence interval of (0.533412, 2.309352). The Week 4 one-sided test gave `t = 3.411831`, conservative `df = 15`, and `p = 0.001931`. At the 5% level, the analysis rejects the null hypothesis; these tournament data provide evidence that progressed teams had a higher mean shots-on-target rate.

## Limitations

The 48 teams are the tournament teams, not a simple random sample, so broad population generalisation is not supported. Opponents, schedules, match state, possession, team strength, and rounding in `90s` may affect the rate. Progression and attacking performance are associated measurements; this analysis does not show that progression caused the higher rate.

## Documentation

The four primary records document process, final methods, sources, and decisions.

- [docs/project_journal.md](docs/project_journal.md)
- [docs/analysis_plan.md](docs/analysis_plan.md)
- [docs/data_sources.md](docs/data_sources.md)
- [docs/decision_log.md](docs/decision_log.md)
- [docs/analysis_summary.md](docs/analysis_summary.md)
