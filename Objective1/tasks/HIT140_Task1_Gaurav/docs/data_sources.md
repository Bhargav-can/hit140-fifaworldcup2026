# Task 1 data sources

Task 1 was initially squad-level. The group later agreed to redesign Task 1 at player level to diversify observational units and demonstrate Week 3 sampling. Tasks 2–4 remain team-level and use all 48 teams. This redesign changes only Task 1.

Task 1 uses the saved FBref webpage data/raw/fbref_player_miscellaneous_2026.html and programmatic HTML extraction of the Player Miscellaneous Stats 2026 World Cup table (id stats_misc). It does not use FIFA HTML extraction. The visible table is preferred; commented HTML is searched only if the visible table is absent, avoiding double counting. Repeated headers are excluded. Player, Pos, Squad, 90s and Int are selected by data-stat attributes; the Squad link text excludes decorative country codes. Blank values are not filled with zeros. No acquisition date is asserted.

The saved page's canonical link is https://fbref.com/en/comps/1/misc/World-Cup-Stats. This is provenance embedded in the file, not a newly fetched source or a dated snapshot URL. The table caption identifies 2026 World Cup. No live web retrieval is needed.

Fields: Player is the player name; Pos is the source position label; Squad is the team; 90s is playing time in 90-minute units; Int is total interceptions. InterceptionsPer90 is derived from Int / 90s, not a separate scraped statistic.

The extracted CSV preserves all 1,039 player rows. task1_validation.json records missingness, duplicates, position counts and ranges; task1_sampling.json records exposure distributions, thresholds and group sizes. No missing data are imputed. Numeric parsing errors, invalid counts, duplicate identities or missing identity fields stop the pipeline.

Eligibility requires Pos exactly DF or exactly MF, 90s > 0, and nonmissing Int, followed by a minimum of 1.0 90s (approximately 90 minutes using the rounded source field). Mixed positions (including DF,MF and FW,MF), GK and FW are excluded. The final eligible population contains 253 DF and 254 MF (507 players); the full population is saved to data/processed/task1_player_population.csv.

Legacy squad defensive-action and FIFA progression CSVs, and task1_defensive_progression.csv, belong to the superseded squad-level design and are not current analysis inputs.
