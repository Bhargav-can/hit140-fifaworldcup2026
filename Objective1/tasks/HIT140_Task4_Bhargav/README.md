# HIT140 Task 4 — Bhargav

## Research question

Do teams that progressed beyond the group stage have a higher mean goalkeeper save percentage than teams eliminated in the group stage?

## Data sources

- FBref squad goalkeeping CSV export: `data/raw/fbref_squad_goalkeeping_2026_raw.csv`, from https://fbref.com/en/comps/1/2026/keepers/2026-World-Cup-Stats. The analysis uses overall Performance Save%, not Penalty Kicks Save%.
- FIFA Round of 32 membership: `data/raw/fifa_round_of_32_teams_2026.csv`. The original source log does not record a specific FIFA URL or access date.

Raw source values are preserved. Preparation removes country-code prefixes and applies the existing explicit `Bosnia–Herz` to `Bosnia and Herzegovina` name mapping.

## Folder structure

```text
HIT140_Task4_Bhargav/
├── data/
│   ├── raw/           # Two original source CSV files
│   └── processed/     # task4_goalkeeping_progression.csv
├── figures/           # Task 4 histogram and boxplot PNG files
├── src/               # validate_data.py, prepare_data.py, analyze.py
├── docs/              # Analysis plan, data sources, Task 4 journal
└── README.md
```

## Run order

Requires Python with pandas, NumPy, SciPy, and Matplotlib installed. From this task folder:

```bash
python src/validate_data.py
python src/prepare_data.py
python src/analyze.py
python -m py_compile src/*.py
```

All input and output paths resolve relative to this task folder through `Path(__file__)`; no external task folders are needed.

## Variables and method

- Response: overall goalkeeper `Save%`, measured as a percentage at squad level.
- Grouping: `ProgressionStatus`, either `Progressed` or `Group-stage eliminated`.
- H0: mu_progressed = mu_eliminated.
- H1: mu_progressed > mu_eliminated; alpha = 0.05.
- Independent two-sample t-test with the existing Week 4 standard error and conservative `df = min(n1 - 1, n2 - 1)`. The difference confidence interval is two-sided at 95%.

## Final results

| Quantity | Result |
| --- | ---: |
| Total teams | 48 |
| Progressed / group-stage eliminated | 32 / 16 |
| Progressed mean Save% | 67.99% |
| Eliminated mean Save% | 58.53% |
| Difference (Progressed − Eliminated) | 9.46 percentage points |
| 95% CI for difference | [0.67, 18.26] percentage points |
| t | 2.2934 |
| df | 15 |
| One-sided p | 0.0183 |

Reject H0. Among the 2026 FIFA World Cup teams, progressed teams had a higher mean goalkeeper Save% than teams eliminated in the group stage. Association only, not causation.

## Figures

- [Histogram](figures/task4_save_percentage_histogram.png): both groups retain common histogram bin edges.
- [Boxplot](figures/task4_save_percentage_boxplot.png).

## Limitations

All 48 tournament teams were included; this is not a simple random sample. Inference should be interpreted cautiously within this tournament and not broadly generalized. Opposition quality and shots faced may influence Save%; progression is observational and does not establish causation. No 1.5 × IQR outliers were detected, and both groups had mild skewness.

## Documentation

- [Analysis plan, confidence intervals, test and interpretation](docs/analysis_plan.md)
- [Data sources and validation notes](docs/data_sources.md)
- [Task 4 source investigation and project journal](docs/project_journal.md)

This folder contains copies of the original Task 4 files and Task 4 documentation excerpts. Original repository files and shared group documents remain in place; future shared documentation belongs in `docs/group/` at repository level.
