# Contributions and decision log

Each member edits their own row in their own commit. Link the GitHub Issues and pull requests for the work.

## Who did what

| Member | Student ID | Main responsibility | Files | Issues / PRs |
| --- | --- | --- | --- | --- |
| Kaushal | [Student ID] | Data collection, repository setup | `data/`, `scripts/build_datasets.py`, `scripts/verify_datasets.py`, `data_dictionary.md` | [#] |
| Bharghav | [Student ID] | Linear regression 2.1 | `scripts/analyse_linreg.py` (2.1), `outputs/charts/linreg_2_1_*` | [#] |
| Sharif | [Student ID] | Linear regression 2.2, notebook | `notebooks/objective2_analysis.ipynb`, `outputs/charts/linreg_2_2_*` | [#] |
| Gaurav | [Student ID] | Model comparison, report | `scripts/compare_models.py`, `outputs/charts/hd_*`, `report/` | [#] |

Edit the table so it describes what each person actually did.

## Decisions

| Date | Decision | Reason | Agreed by |
| --- | --- | --- | --- |
| [date] | Use only variables available for all 48 teams | Club per-90 statistics (FBref) could not be downloaded for every squad, so they were dropped rather than estimated | [names] |
| [date] | Use the FIFA ranking of 11 June 2026 | Last ranking before the tournament; the next update came after the final | [names] |
| [date] | Hosts use 2025 Gold Cup rates | Mexico, Canada and the United States did not play qualification | [names] |
| [date] | Tournament form uses earlier matches only, 0 before a team's first match | Keeps every variable known before kickoff | [names] |
| [date] | Keep a transform only if five-fold CV RMSE falls | Rule from the Week 9 practical | [names] |
| [date] | Add repeated, grouped and nested CV and competing algorithms | Single-split differences of 0.01–0.06 goals were within noise | [names] |
| [date] | Recommend Ridge for 2.1 | Lowest RMSE (1.526) and beats OLS in 18 of 20 repeats | [names] |

## Progress checks

| Date | Status | Next steps |
| --- | --- | --- |
| [date] | | |
