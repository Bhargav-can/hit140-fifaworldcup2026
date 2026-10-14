# HIT140 Assessment 3 — Objective 2: Predicting FIFA World Cup 2026 scores

Two linear regression tasks built only from information available before kickoff.

| Task | Dataset | Rows | Response | Explanatory variables |
| --- | --- | --- | --- | --- |
| 2.1 Goal difference | `data/linreg_2_1.csv` | 104 matches | `goal_diff` (team A − team B) | 8 |
| 2.2 Goals scored | `data/linreg_2_2.csv` | 208 team-matches | `goals` | 8 |

The two tasks share no explanatory variable (the brief allows up to four). Every column, its source and the reason it was chosen are in [`data_dictionary.md`](data_dictionary.md).

**Team:** Bharghav · Sharif · Gaurav · Kaushal — see [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md).

## Repository layout

```text
data/
  linreg_2_1.csv              104 matches, 8 explanatory variables, goal difference
  linreg_2_2.csv              208 team-matches, 8 explanatory variables, goals scored
  team_features.csv           48-team lookup, used only by the verification script
  raw/                        saved source pages the tables were built from
scripts/
  build_datasets.py           rebuilds the two tables from data/raw
  verify_datasets.py          28 data checks (row counts, 308 goals, gaps, host flags)
  analyse_linreg.py           Week 9 practical pipeline: baseline, 60/40 split, 5-fold CV,
                              collinearity, z-score, log, Yeo-Johnson (report Table 1)
  compare_models.py           repeated, grouped and nested CV; Ridge, Lasso, Huber,
                              Poisson GLM, random forest (report Table 2, Figures 1-4)
notebooks/
  objective2_analysis.ipynb   every step with its output, statsmodels summaries,
                              largest residuals and the model comparison
outputs/
  charts/                     all figures
  hd_results.json             numbers behind Table 2 and Figures 1-4
report/
  Objective2_Group_Report.docx
```

## How to run

Python 3.10 or later.

```bash
pip install -r requirements.txt

python scripts/verify_datasets.py     # expect: CHECKS 28/28 passed
python scripts/analyse_linreg.py      # practical pipeline, Table 1, charts linreg_2_*.png
python scripts/compare_models.py      # competing models, Table 2, charts hd_*.png (about 2 minutes)
jupyter notebook notebooks/objective2_analysis.ipynb
```

`build_datasets.py` only needs to be run to rebuild the CSV files from the saved pages in `data/raw`. Every random step uses a fixed seed, so the numbers in the report reproduce exactly.

## Main results

| | 2.1 Goal difference | 2.2 Goals scored |
| --- | --- | --- |
| Mean baseline RMSE | 2.015 | 1.386 |
| Best model | Ridge, signed logs of market value and World Cup experience | Two qualifying rates (OLS) / log of qualifying goals for |
| Best RMSE (20 × 5-fold CV) | 1.526 (24% below baseline) | 1.347–1.359 (2–3% below baseline) |
| In football terms | Picks the winner in 70 of 80 decided matches | Poisson GLM reproduces the observed spread of scores |
