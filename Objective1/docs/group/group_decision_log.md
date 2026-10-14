# Shared Group Decision Log

## Stage — four distinct questions
We selected interceptions, discipline, attacking performance, and goalkeeping to give each task a distinct response and research question within our shared tournament project.

## Stage — course methods prioritised
We prioritised Week 3 population and sampling concepts and Week 4 State → Plan → Solve → Conclude. We use `SE = sqrt(s1^2/n1 + s2^2/n2)`, `df = min(n1 - 1, n2 - 1)`, alpha = 0.05, and 95% confidence intervals.

## Stage — Task 1 redesigned to player-level
We agreed to replace the earlier squad-level Task 1 design with a comparison of player interceptions per 90 for defenders and midfielders. We made this change to diversify observational units and demonstrate population definition and random sampling.

## Stage — methodological variety intentionally used
We match methods to the observational unit and question. We use player-level sampling in Task 1 and team-level comparisons in Tasks 2–4 rather than forcing identical designs.

## Stage — sampling and complete-team analysis
We sample 30 eligible defenders and 30 eligible midfielders without replacement using `random_state = 140`, from populations of 253 and 254 respectively after eligibility rules and a minimum of 1.0 90s. We retain all 48 teams in Tasks 2–4, with 32 progressed and 16 eliminated teams, and do not introduce artificial random sampling.

## Stage — varied acquisition methods
We use saved FBref HTML and programmatic extraction for Task 1, structured FBref exports for Tasks 2 and 3, and FBref statistics integrated with FIFA progression data for Task 4. Our Task 4 experience with potentially blocked direct automated access informed browser-export and local-data workflows; we do not claim that Tasks 1–3 repeated those attempts.

## Stage — per-match and per-90 normalisation
We use `Int / 90s`, `CrdY / MP`, and `SoT / 90s` for Tasks 1–3 to account for differing exposure. We use goalkeeper Save% for Task 4 and report its difference in percentage points.

## Stage — valid outliers retained
We retain valid extreme observations. We do not remove a value solely because it is unusual, while keeping data-quality validation distinct from outlier exclusion.

## Stage — no causal overclaiming
We describe differences and associations. We do not claim that progression causes performance differences or that a performance metric causes progression. We treat failure to reject H0 as insufficient evidence, not proof of equality.
