# Decision log — Task 3

Decision IDs organise the completed rationale without implying dates or undocumented individual actions. Source facts and validation are recorded in [data_sources.md](data_sources.md); results and limitations are in [analysis_plan.md](analysis_plan.md).

## D01 — Use FBref table CSV exports

- Scope: Shared project.
- Rationale: Earlier Task 4 automated FBref access was blocked.
- Consequence: Apply the prior team lesson without attributing those failed attempts to this task.

## D02 — Reuse FIFA progression classification

- Scope: Shared project.
- Rationale: The Round-of-32 classification was already validated for the project.
- Consequence: Use consistent groups: 32 progressed and 16 eliminated from 48 teams.

## D03 — Use explicit naming harmonisation

- Scope: Shared project.
- Rationale: FBref uses Bosnia–Herz while FIFA uses Bosnia and Herzegovina.
- Consequence: Apply `{"Bosnia–Herz": "Bosnia and Herzegovina"}` after country-code-prefix removal; no fuzzy matching.

## D04 — Normalise shooting output per 90

- Scope: Task-specific.
- Rationale: Teams accumulated different playing-time exposure.
- Consequence: Use shots on target per 90 minutes rather than tournament totals.

## D05 — Calculate the response reproducibly

- Scope: Task-specific.
- Rationale: The source provides counts and playing-time units as well as a supplied rate.
- Consequence: Calculate `SoT / 90s`; use supplied `SoT/90` only as a validation comparison.

## D06 — Accept the validated rounding difference

- Scope: Task-specific.
- Rationale: Maximum absolute difference was 0.051628, within the existing 0.06 comparison tolerance.
- Consequence: Treat the difference as consistent with displayed/rounded `90s`; retain the calculated response and disclose rounding as a limitation.

## D07 — Use a one-sided alternative

- Scope: Task-specific.
- Rationale: The research question explicitly asks whether the progressed mean is higher.
- Consequence: Use `H1: mu_progressed > mu_eliminated`.

## D08 — Retain all valid teams

- Scope: Task-specific.
- Rationale: Selected values were complete and there were no IQR outliers.
- Consequence: Keep all 48 teams in the comparison.

## D09 — Use the Week 4 t procedure

- Scope: Shared course method.
- Rationale: The course uses State → Plan → Solve → Conclude.
- Consequence: Use `sqrt(s1^2/n1 + s2^2/n2)`, conservative `min(n1 - 1, n2 - 1)` degrees of freedom, `alpha = 0.05`, and `scipy.stats.t` critical values/p-values.

## D10 — Restrict inference and avoid causal claims

- Scope: Shared interpretation.
- Rationale: All tournament teams are included, without simple random sampling or an experimental design.
- Consequence: Interpret association primarily within the 2026 FIFA World Cup; acknowledge contextual confounding.

