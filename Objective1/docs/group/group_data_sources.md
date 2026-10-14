# Shared Group Data Sources

## Stage — source register
We register the sources and acquisition methods used in our final design. We omit URLs because no verified URLs have been supplied.

| Source | Task coverage | Acquisition / integration | Fields or role |
| --- | --- | --- | --- |
| FBref Player Miscellaneous Stats | Task 1 | We save the webpage locally as HTML and extract the table programmatically | Player position, `Int`, and `90s` support eligibility and `InterceptionsPer90` |
| FBref Squad Standard Stats | Task 2 | We use a structured FBref export | `CrdY` and `MP` support `YellowCardsPerMatch` |
| FBref Squad Shooting Stats | Task 3 | We use a structured FBref export | `SoT` and `90s` support `ShotsOnTargetPer90` |
| FBref Squad Goalkeeping Stats | Task 4 | We use FBref statistics and integrate FIFA progression data | Team identifiers and goalkeeper Save% support the goalkeeping comparison |
| FIFA progression classification | Tasks 2–4 where applicable | We use progression classification for team grouping; Task 4 explicitly integrates it with FBref statistics | We distinguish 32 progressed teams from 16 group-stage-eliminated teams |

## Stage — population and coverage
We begin Task 1 with 1039 raw players. After eligibility rules and a minimum of 1.0 90s, our eligible populations contain 253 defenders and 254 midfielders. We select 30 from each position group without replacement using `random_state = 140`.

We retain the complete 48-team tournament dataset in Tasks 2–4. We do not treat the 32 progressed and 16 eliminated teams as artificially drawn random samples.

## Stage — source integration and validation
We clean country-code prefixes and map `Bosnia–Herz` to `Bosnia and Herzegovina` in Task 4 to align team identifiers. Our validation criteria include unique observational units, numeric fields, positive denominators, expected group counts, and complete classification matching without duplicated teams. We do not invent unreported source fields, corrections, or file paths.

## Stage — access workflow and provenance limits
Our earlier Task 4 experience showed that direct automated FBref access could be blocked. We use browser-export and local-data workflows rather than aggressively bypassing restrictions. We do not state that Tasks 1–3 individually repeated the Task 4 access attempts.

We document the supplied source names and acquisition routes. We leave unspecified export details and unverified URLs unasserted, and rely on the existing local inputs and task workflows for further provenance.
