# Data source — Task 2

For the primary source register, see [data_sources.md](data_sources.md). This file retains the existing concise summary.

## FBref table used

The supplied file `fbref_squad_standard_2026_raw.csv` is an FBref squad standard-stats export. Its grouped two-row header was parsed by locating the row containing the exact labels `Squad`, `MP`, and `CrdY`.

## FIFA progression data

The supplied file `fifa_round_of_32_teams_2026.csv` identifies the 32 teams that progressed beyond the group stage. All other squads in the 48-team FBref data were classified as `Group-stage eliminated`.

## Fields and transformation

- `Squad`: team name; only an initial lowercase two- or three-letter code followed by whitespace was removed.
- `MP`: numeric matches played; required to be positive.
- `CrdY`: numeric yellow-card count.
- `YellowCardsPerMatch`: calculated as `CrdY / MP`.

## Naming harmonisation

The only cross-source alias applied was `Bosnia–Herz` to `Bosnia and Herzegovina`. No fuzzy matching was used. There were no unmatched FIFA progression names.

No exact source URL is present in the supplied files or project context.
