# Shared Group Project Journal

## Stage — assignment planning
We structured our HIT140 Assessment 2 project around four complementary questions about FIFA World Cup performance. We prioritised the course methods and a shared approach to reporting evidence without causal claims.

## Stage — question development
We selected distinct questions covering interceptions, discipline, attacking performance, and goalkeeping. Our final task allocation is Task 1 — Gaurav, Task 2 — Kushal, Task 3 — Sharif, and Task 4 — Bhargav.

## Stage — initial source review
We identified FBref statistics as our performance sources and FIFA progression classification as the basis for distinguishing progressed teams from group-stage-eliminated teams where applicable. We used saved or structured local data as inputs to programmatic analysis.

## Stage — Task 4 workflow development
Our Task 4 experience showed that direct automated FBref access could be blocked. We adopted browser-export and local-data workflows rather than aggressively bypassing access restrictions. We integrated goalkeeper statistics with FIFA progression data, including country-code prefix cleaning and the name mapping `Bosnia–Herz` to `Bosnia and Herzegovina`. We do not attribute repeated access attempts to Tasks 1–3.

## Stage — Tasks 1–3 initial analyses
Our initial structure included a squad-level approach for Task 1, alongside team-level discipline and attacking questions. We record that initial structure without adding unsupported intermediate results or accounts of individual activity.

## Stage — methodology review
We deliberately matched our statistical design to each observational unit rather than forcing identical sampling methods. We aligned our work with Week 3 population and sampling concepts and the Week 4 State → Plan → Solve → Conclude framework.

## Stage — Task 1 redesign
We agreed to redesign Task 1 from squad-level to player-level analysis to diversify observational units and demonstrate Week 3 population and sampling concepts. Our revised question compares mean interceptions per 90 minutes for defenders and midfielders.

## Stage — player HTML extraction and sampling
We used a locally saved FBref Player Miscellaneous Stats HTML webpage and programmatic extraction. From 1039 raw players, the eligibility rules and minimum of 1.0 90s yielded 253 defenders and 254 midfielders. We sampled 30 players without replacement from each group using `random_state = 140`. We calculated `InterceptionsPer90 = Int / 90s`.

## Stage — final four-task structure
We retained player samples for Task 1 and all 48 teams for Tasks 2–4, with 32 progressed and 16 eliminated teams. At alpha = 0.05, we fail to reject the null hypotheses for interceptions and yellow cards, and reject the null hypotheses in favour of higher shots on target per 90 and higher goalkeeper Save% among progressed teams. We interpret these as comparisons and associations, not causal effects.

## Stage — presentation preparation
We organise our presentation around each question, observational unit, acquisition method, derived response, statistical evidence, and contextual conclusion. We use the final results in our analysis plan and explain why our player sampling and complete-team designs differ. This entry sets our presentation structure without claiming that a presentation has already been delivered.
