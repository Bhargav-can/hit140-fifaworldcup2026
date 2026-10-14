# Shared Group Methodology

## Stage — observational units and study design
We use players as the observational units in Task 1 and teams as the observational units in Tasks 2–4. We deliberately match the statistical design to the observational unit rather than forcing identical sampling methods across questions.

For Task 1, we distinguish the 1039 raw player records from the eligible populations: 253 defenders and 254 midfielders after eligibility rules and a minimum of 1.0 90s. We draw a simple random sample without replacement within each position group: 30 defenders and 30 midfielders, using `random_state = 140`. This demonstrates the Week 3 concepts of population, sample, and simple random sampling. Our inference targets the eligible position populations, not every raw player record. The supplied design does not specify the full position-eligibility rules, so we do not invent how mixed-position records were handled.

For Tasks 2–4, we retain the complete tournament dataset of 48 teams: 32 progressed and 16 group-stage-eliminated teams. We do not impose artificial random sampling on these complete team groups. Our descriptive differences describe the included tournament teams; the t-based inference is a course-method, model-based comparison rather than uncertainty from a random sample of these 48 teams.

## Stage — acquisition and wrangling
We acquire Task 1 through a locally saved FBref Player Miscellaneous Stats HTML webpage and programmatic extraction. We use structured FBref exports for Tasks 2 and 3. We integrate FBref goalkeeper statistics and FIFA progression data for Task 4, using FIFA progression classification for the team comparisons where applicable.

Our earlier Task 4 experience showed that direct automated FBref access could be blocked. We therefore use browser-export and local-data workflows rather than aggressively bypassing restrictions. We do not claim that Tasks 1–3 individually repeated those access attempts.

We clean country-code prefixes and map `Bosnia–Herz` to `Bosnia and Herzegovina` for the Task 4 integration. We treat team-name harmonisation as a matching step, not a change to performance values.

## Stage — validation and feature engineering
We define validation checks around numeric parsing, missing values, duplicate observational units, positive denominators, eligible position membership, group counts, and successful team classification joins. We check that joins do not duplicate teams or silently remove records. These are our validation criteria; we do not invent a separate audit history or undocumented corrections.

We calculate the response variables as follows:

| Task | Response | Definition |
| --- | --- | --- |
| 1 | InterceptionsPer90 | `Int / 90s` |
| 2 | YellowCardsPerMatch | `CrdY / MP` |
| 3 | ShotsOnTargetPer90 | `SoT / 90s` |
| 4 | Goalkeeper Save% | FBref goalkeeper save percentage |

We use per-match or per-90 responses where specified to account for differing exposure. We express Task 4 mean differences in percentage points. We retain valid outliers rather than removing observations solely because they are extreme; we distinguish unusual valid values from parsing or data-quality errors.

## Stage — statistical procedure
We follow the Week 4 State → Plan → Solve → Conclude framework:

- **State:** We identify the response, groups, population of interest, and hypotheses.
- **Plan:** We specify the sampling or complete-team design, test direction, assumptions, and alpha = 0.05.
- **Solve:** We calculate group means, their difference, the standard error, a t statistic, a p-value, and a 95% confidence interval.
- **Conclude:** We state the evidence in context without treating non-rejection as proof of equality or claiming causation.

We define the mean difference as defenders minus midfielders in Task 1 and progressed minus eliminated teams in Tasks 2–4. We use the course two-group standard error and conservative degrees of freedom:

`SE = sqrt(s1^2/n1 + s2^2/n2)`

`df = min(n1 - 1, n2 - 1)`

`t = (mean1 - mean2) / SE`

`95% CI = (mean1 - mean2) ± t_(0.975, df) × SE`

We use df = 29 for Task 1 and df = 15 for Tasks 2–4. We test a zero mean difference as the null boundary. Tasks 1, 3, and 4 use an upper-tail alternative that the first group mean is higher; Task 2 uses a two-sided alternative that the means differ. We report two-sided 95% confidence intervals for all tasks, including those with one-sided tests.

## Stage — assumptions and limitations
We treat observations as independent for the course calculations, while recognising that players within teams and teams facing one another may be dependent. We assess the relevance of skew and extreme values to a t-based comparison; the smaller eliminated group contains only 16 teams. We do not assert that normality or independence has been formally established.

Our player results depend on the eligible population, participation threshold, position rules, and selected samples. Our complete-team results describe this tournament and do not automatically generalise to other competitions. Different opponents, match exposure, team strategy, and progression-related selection can affect the comparisons even after normalisation. We interpret the reported confidence intervals within the model assumptions, especially because Tasks 2–4 are not random samples of tournament teams.

We make no causal claims: progression status and performance statistics are observed together. Rejecting a null hypothesis does not establish that the response caused progression, and failing to reject does not establish equal means. We apply alpha = 0.05 separately to the four questions; no multiple-testing adjustment is specified in our design.

## Stage — reproducibility and reporting
We document source types, extraction routes, response formulas, group sizes, sample sizes, random seed, test directions, degrees of freedom, and final results across these shared files. We rely on the existing local inputs and task workflows for exact reproduction. We do not invent source URLs, filenames, full eligibility rules, or processing details that have not been supplied. We preserve the supplied numerical precision and separate documented results from validation criteria.
