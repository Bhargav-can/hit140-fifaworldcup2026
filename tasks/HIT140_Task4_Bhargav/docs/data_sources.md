# Data Sources

Add each proposed or confirmed data source to the table. Record validation notes after checking its relevance, reliability, completeness, and limitations.

| Source | URL | Data Description | Variables of Interest | Access Date | Validation Notes |
|---|---|---|---|---|---|
| FIFA |  | Official 2026 World Cup knockout-stage information | Round of 32 membership and progression beyond the group stage |  | Authoritative tournament source used to identify the 32 teams that progressed beyond the group stage. The FIFA classification was harmonised with FBref at squad level and validated before analysis. |
| Stats Don't Lie |  | World Cup statistics source considered for Task 4 | Goalkeeper performance variables |  | Required Save% or equivalent inputs could not be verified for Task 4 |
| FBref | https://fbref.com/en/comps/1/2026/keepers/2026-World-Cup-Stats | 2026 World Cup squad goalkeeping statistics | Squad, MP, Min, SoTA, Saves, Save% |  | Goalkeeper-performance source for Task 4. The browser-exported raw dataset was successfully validated in Python and contains 48 unique squad observations with the required variables and no missing selected values. The two-row header was parsed, the overall Performance Save% was selected rather than Penalty Kicks Save%, and FBref's two- or three-letter leading lowercase country codes were removed from squad names. Squad names were harmonised with the FIFA progression source and validated before analysis. |
