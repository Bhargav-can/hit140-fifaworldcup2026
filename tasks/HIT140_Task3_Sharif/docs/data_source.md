# Data source — Task 3

For the primary source register, see [data_sources.md](data_sources.md). This file retains the existing concise summary.

## FBref table used

The supplied file `fbref_squad_shooting_2026_raw.csv` is an FBref squad shooting export. Its grouped two-row header was parsed by locating the row containing the exact labels `Squad`, `90s`, and `SoT`. The supplied `SoT/90` field was also read for a validation comparison.

## FIFA progression data

The supplied file `fifa_round_of_32_teams_2026.csv` identifies the 32 teams that progressed beyond the group stage. All other squads in the 48-team FBref data were classified as `Group-stage eliminated`.

## Fields and transformation

- `Squad`: team name; only an initial lowercase two- or three-letter code followed by whitespace was removed.
- `90s`: numeric playing time in 90-minute units; required to be positive.
- `SoT`: numeric shots-on-target count.
- `ShotsOnTargetPer90`: calculated reproducibly as `SoT / 90s`.
- `FBrefSoTPer90`: the supplied rate, retained only for comparison.

The maximum absolute difference between the calculated and supplied rates was 0.051628. Every comparison was within 0.06, which is consistent with calculation from the displayed, rounded `90s` field.

## Naming harmonisation

The only cross-source alias applied was `Bosnia–Herz` to `Bosnia and Herzegovina`. No fuzzy matching was used. There were no unmatched FIFA progression names.

No exact source URL is present in the supplied files or project context.
