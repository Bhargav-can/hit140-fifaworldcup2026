# Data sources — Task 2

## Source register

| Source and local file | Role and fields | Reason selected |
|---|---|---|
| FBref table CSV export: `data/raw/fbref_squad_standard_2026_raw.csv` | Squad statistics: `Squad`, `MP`, `CrdY` | Provides the task-specific counts and exposure needed to construct the response for the 48-team tournament field. |
| FIFA classification: `data/raw/fifa_round_of_32_teams_2026.csv` | `Squad`, `ProgressedBeyondGroup` | Reuses the already validated Round-of-32 progression classification across tasks. |

## Acquisition provenance

In the earlier Task 4 workflow completed by Bhargav, direct automated access to FBref had been blocked. This prior team experience informed the shared decision to use FBref table CSV exports for Tasks 1–3 rather than repeat aggressive automated scraping. It is a shared project lesson, not a record of task-specific failed scraping attempts.

No exact source URL or acquisition date is recorded in the supplied documentation. Reproduction here starts from the retained local CSV exports; source access history beyond the shared lesson is not asserted.

## Source-derived fields and transformations

- `Squad`: team name; only an initial lowercase two- or three-letter code followed by whitespace was removed.
- `MP`: numeric matches played; required to be positive.
- `CrdY`: numeric yellow-card count.
- `YellowCardsPerMatch`: calculated as `CrdY / MP`.

The selected table contains `Squad`, `MP`, `CrdY`, and the engineered `YellowCardsPerMatch` response.

The response `YellowCardsPerMatch = CrdY / MP` is an analysis-derived variable, not a FIFA field. Progression is derived from the FIFA classification. The source selection and response choices are analytical decisions recorded in [decision_log.md](decision_log.md).

## Validation and cross-source integration

The grouped FBref header was parsed by locating the required exact field labels. Raw shape: `(48, 21)`; selected shape before progression classification: `(48, 4)`. Numeric denominators were required to be positive and event counts non-negative.

Squad names were trimmed and only an initial lowercase two- or three-letter country-code prefix followed by whitespace was removed. The explicit known alias `{"Bosnia–Herz": "Bosnia and Herzegovina"}` harmonised FBref with FIFA. No fuzzy matching was used.

Validation confirmed 48 unique squads, 0 missing selected analysis values, and 0 duplicate squads. All FIFA progression names matched after explicit harmonisation. The final groups contain 32 Progressed and 16 Group-stage eliminated teams. Teams in the FIFA progression list are labelled Progressed; the remaining teams in the complete FBref field are labelled Group-stage eliminated. This classification relies on the validated list being complete.

## Reproducibility and limits

The existing `src/validate_data.py`, `src/prepare_data.py`, and `src/analyze.py` implement validation, construction/integration, and analysis respectively. The [README](../README.md) retains their run order. The processed table is `data/processed/task2_discipline_progression.csv`. Running preparation or analysis regenerates outputs; this documentation update leaves those outputs unchanged.

Source validation establishes usable fields and consistent integration; it does not supply a random sample or remove contextual confounding. See [analysis_plan.md](analysis_plan.md) for statistical assumptions, tournament-specific limitations, and results.
