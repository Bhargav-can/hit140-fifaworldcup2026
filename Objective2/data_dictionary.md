# Data dictionary — Objective 2

Two linear regression tables. Each has ten columns: one key, eight explanatory variables, and one response. The key is not an explanatory variable. The two tables do not share an explanatory variable.

| Table | File | Rows | Response |
| --- | --- | --- | --- |
| 2.1 Goal difference | `data/linreg_2_1.csv` | 104 matches | `goal_diff` |
| 2.2 Goals scored | `data/linreg_2_2.csv` | 208 team-matches | `goals` |

`data/team_features.csv` is the 48-team lookup used only to check these tables. The models do not read it. `scripts/build_datasets.py` rebuilds both tables from the pages in `data/raw`.

## Rules

- Every explanatory variable is known before kickoff. Shots, shots on target, and xG from the match being predicted are not used.
- A number is included only when it could be collected for all 48 teams.
- Club goals per 90, shots on target per 90, shot-creating actions, box touches, and keeper save rate are not in these tables. Those FBref player pages could not be downloaded for every squad. Squad market value is the complete pre-match measure of the selected players.
- Model 2.1 uses the gap between the two teams. Model 2.2 uses one team’s scoring record and the opponent’s squad. Market value, age, rest, and home advantage are only in 2.1.
- Team A is the team named first on the fixtures page. Every 2.1 gap is team A minus team B.
- Extra-time goals are included. Penalty-shootout kicks are not. A 0–0 match decided on penalties has a goal difference of 0.
- The 208 team-rows sum to 308 goals, the tournament total.

## Sources

| Source | What was taken |
| --- | --- |
| WorldCupStats fixtures page | Date, teams, full-time score, and venue, for all 104 matches |
| FIFA ranking published 11 June 2026 | Ranking points. The next official update was 20 July 2026, after the final, so this ranking is valid before every match |
| Wikipedia qualification standings | Goals for, goals against, and games played. New Zealand’s semi-final (7–0 Fiji) and final (3–0 against New Caledonia) are added, because the group table stops before those two games |
| 2025 CONCACAF Gold Cup | The same rates for Mexico, Canada, and the United States, because those three did not play qualification |
| Transfermarkt squad list (page saved on [date, before 11 June 2026]) | Average age, average market value in millions of euros, World Cup appearances of the squad, the percentage of players based at foreign clubs, and squad size |

For a team’s first World Cup match, rest is set to 14 days. Every team gets the same starting value, so the rest gap in 2.1 is 0 when both teams are playing their first match. Later matches use the real number of days since that team’s previous World Cup game.

`wc_gd_so_far`, `wc_goals_so_far`, and `opp_wc_ga_so_far` use only matches already played. They are 0 before a team’s first match.

## Linear regression 2.1 — goal difference

| Column | Role | Definition |
| --- | --- | --- |
| `match_id` | Key | Identifies the match. Not an explanatory variable. |
| `fifa_points_diff` | Explanatory | Team A ranking points minus team B ranking points. The single clearest measure of which side is stronger. |
| `qual_gd_per_game_diff` | Explanatory | Gap in goal difference per qualifying game. Hosts use the 2025 Gold Cup instead of qualification. |
| `market_value_avg_diff` | Explanatory | Gap in average club market value, in millions of euros, of the players who were selected. |
| `age_avg_diff` | Explanatory | Gap in average squad age. |
| `host` | Explanatory | +1 if team A is the United States, Mexico, or Canada playing at home, −1 if team B is, otherwise 0. |
| `rest_days_diff` | Explanatory | Gap in days since each team’s previous World Cup match. First match is set to 14 days, so the opening gap is 0. |
| `wc_gd_so_far` | Explanatory | Gap in goal difference per game from earlier 2026 World Cup matches only. 0 before a team’s first match. |
| `wc_experience_diff` | Explanatory | Gap in how many World Cups the selected players have already appeared in. |
| `goal_diff` | Response | Team A goals minus team B goals. |

## Linear regression 2.2 — goals scored by one team

| Column | Role | Definition |
| --- | --- | --- |
| `team_match_id` | Key | Identifies one team in one match. Not an explanatory variable. |
| `qual_gf_per_game` | Explanatory | Goals this team scores per qualifying game. Hosts use the 2025 Gold Cup. |
| `opp_qual_ga_per_game` | Explanatory | Goals the opponent concedes per qualifying game. |
| `wc_goals_so_far` | Explanatory | This team’s goals per game in earlier 2026 World Cup matches. 0 before their first match. |
| `opp_wc_ga_so_far` | Explanatory | Goals the opponent has conceded per earlier 2026 World Cup match. 0 before their first match. |
| `foreigners_pct` | Explanatory | Share of this squad that plays club football abroad. |
| `opp_foreigners_pct` | Explanatory | The same share for the opponent. |
| `squad_size` | Explanatory | Number of players in this squad. |
| `opp_squad_size` | Explanatory | Number of players in the opponent’s squad. |
| `goals` | Response | Goals this team scored in the match, including extra time and excluding penalty-shootout kicks. |
