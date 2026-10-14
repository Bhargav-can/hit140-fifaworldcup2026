# Decision log — Task 2

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

## D04 — Use yellow cards per match

- Scope: Task-specific.
- Rationale: Raw totals depend on how many matches teams play.
- Consequence: Calculate `CrdY / MP` for exposure comparability; contextual differences remain.

## D05 — Use a two-sided alternative

- Scope: Task-specific.
- Rationale: The question asks whether the means differ, without specifying higher or lower.
- Consequence: Use `H1: mu_progressed != mu_eliminated`.

## D06 — Retain IQR-flagged observations

- Scope: Task-specific.
- Rationale: Egypt, Czechia, Tunisia, and Türkiye have valid observed values; an IQR flag alone is not evidence of a data error.
- Consequence: Retain all 48 teams and disclose the flags when assessing the t procedure.

## D07 — Use the Week 4 t procedure

- Scope: Shared course method.
- Rationale: The course uses State → Plan → Solve → Conclude.
- Consequence: Use `sqrt(s1^2/n1 + s2^2/n2)`, conservative `min(n1 - 1, n2 - 1)` degrees of freedom, `alpha = 0.05`, and `scipy.stats.t` critical values/p-values.

## D08 — Restrict inference and avoid causal claims

- Scope: Shared interpretation.
- Rationale: All tournament teams are included, without simple random sampling or an experimental design.
- Consequence: Interpret association primarily within the 2026 FIFA World Cup; acknowledge contextual confounding.

