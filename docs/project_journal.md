# Project Journal

## Purpose

This journal records the group's real analytical process, including data-source investigation, question formulation and refinement, methodological decisions, progress, reviews, and lessons learned.

## 1. Initial Project Setup

- A shared GitHub repository was established for the HIT140 FIFA World Cup 2026 project, with `main` used as the stable shared branch.
- Individual working branches were created for Bhargav, Gaurav, Kushal, and Sharif.
- The initial project architecture included `docs/`, `notebooks/`, `src/`, `environment.yaml`, and `.gitignore`.
- Objective 1 / Assessment 2 was scoped to the Weeks 1–5 statistical workflow.
- Four distinct analytic tasks were required. Each task must include data preparation and wrangling, descriptive statistics, a confidence interval, and a one- or two-sample t-test.
- Python was selected as the analysis workflow.

## 2. Data Source Investigation

| Stage | Source | Data Level | Variables Observed | Potential Use | Issues / Limitations | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Task 4 source comparison | FIFA | Team | Goalkeeper statistics and Round of 32 progression information | Official tournament source checked for Task 4 goalkeeper statistics and progression classification | The variables needed to calculate goalkeeper save percentage directly, especially shots on target against, were not confirmed for this task | Not selected as the goalkeeper-performance source; selected to identify the 32 teams that progressed beyond the group stage |
| Task 4 source comparison | Stats Don't Lie | Not verified | Goalkeeper performance variables considered | Considered as a possible World Cup goalkeeper statistics source | Save percentage or the full inputs needed to calculate it could not be verified for Task 4 | Not selected for Task 4 acquisition |
| Task 4 source comparison and validation | FBref | Squad | Squad, MP, Min, shots on target against, saves, and Save% | Exact squad-level variable match for Task 4 | The raw CSV had a two-level header and two Save% fields, so the overall Performance Save% was explicitly selected rather than Penalty Kicks Save% | Browser-provided CSV export successfully loaded and validated in Python: 48 × 21 raw shape, 48 × 7 selected shape, 48 unique squads, 0 duplicates, no missing selected values, no zero or missing SoTA observations, and Save% from 33.3 to 90.9 with all values between 0 and 100; squad names were cleaned by removing FBref's leading lowercase country code |
| Task 4 acquisition method | FBref | Squad | Squad goalkeeping table | Acquire the selected Task 4 source while preserving a raw copy | `pandas.read_html()` returned HTTP 403 Forbidden; a second controlled request using `requests` with a browser-style User-Agent also returned HTTP 403 | Aggressive bypassing and scraping workarounds were rejected; FBref's browser-provided CSV text export was used instead |

## 3. Analytic Question Development

| Stage | Initial Idea | Data / Method Consideration | Outcome | Reason |
| --- | --- | --- | --- | --- |
| Initial consideration | Compare defensive performance between defenders and midfielders. | Playing time needs to be considered when comparing players. | Refined to compare mean defensive actions (tackles + interceptions) per 90 minutes. | Normalising for playing time makes the comparison more meaningful. |
| Initial consideration | Compare the proportion of defenders and midfielders receiving at least one yellow card. | A comparison of proportions does not naturally match the required one-sample/two-sample t-test workflow. | Not retained in this form. | The proposed outcome and required statistical workflow were not well aligned. |
| Reformulation | Retain the discipline theme. | A match-level numerical outcome can support a comparison of means. | Reformulated as a comparison of group-stage and knockout-stage yellow cards per match. | This formulation better aligns the theme with the course workflow. |
| Further investigation | Examine attacking performance. | Relevant data must be validated before the question is confirmed. | Identified as a theme for investigation. | Data availability and suitability remain to be checked. |
| Further investigation | Examine goalkeeping performance. | The FBref squad goalkeeper CSV was loaded and validated in Python. | Confirmed as Task 4. | The validated data contain the required goalkeeping variables for all 48 participating squads. |

Questions 1–3 remain subject to data validation. Task 4 is confirmed following dataset validation.

## 4. Current Candidate Questions

1. Defenders vs midfielders: mean defensive actions per 90. **Candidate — pending data validation.**
2. Group stage vs knockout stage: mean yellow cards per match. **Candidate — pending data validation.**
3. Progressed vs group-stage-eliminated teams: mean attempts on target per match. **Candidate — pending data validation.**
4. Progressed vs group-stage-eliminated teams: mean goalkeeper save percentage. **Confirmed — dataset validated.**

## 5. Task Allocation

| Member | Candidate Task | Current Responsibility | Status |
| --- | --- | --- | --- |
| Gaurav | Task 1 | Defensive player performance | Pending dataset validation / work commencement |
| Kushal | Task 2 | Match discipline | Pending dataset validation / work commencement |
| Sharif | Task 3 | Attacking performance | Pending dataset validation / work commencement |
| Bhargav | Task 4 | Goalkeeping performance | Goalkeeper data and tournament progression classification integrated and validated; descriptive analysis pending |

## 6. Methodological Workflow

The planned course-aligned process is:

1. Data acquisition
2. Data validation
3. Question refinement
4. Population/sample definition
5. Data preparation and wrangling
6. Descriptive statistics
7. Confidence interval
8. State-Plan-Solve-Conclude hypothesis test
9. Assumption checking
10. Interpretation
11. Limitations
12. Peer review
13. Presentation integration

## 7. Progress Log

Earlier stages below were reconstructed from the existing repository history, working notes, validation outputs, and decisions already completed during the project. Stage labels are used instead of invented dates.

| Stage | Member(s) | Work Completed | Issue / Finding | Next Step |
| --- | --- | --- | --- | --- |
| Initial repository setup | Team | Created the shared GitHub repository for the HIT140 FIFA World Cup 2026 project; established `main` as the stable shared branch; created individual branches for Bhargav, Gaurav, Kushal, and Sharif; and set up `docs/`, `notebooks/`, `src/`, `environment.yaml`, and `.gitignore` | The project needed a shared structure that separated stable work, individual contributions, documentation, code, and notebooks | Scope Assessment 2 and agree on the analytical workflow |
| Assessment 2 planning | Team | Scoped Objective 1 to Weeks 1–5 and selected Python as the analysis workflow | Four distinct analytic tasks were required, each including data preparation and wrangling, descriptive statistics, a confidence interval, and a one- or two-sample t-test | Establish the planning documents and develop candidate questions |
| Planning and documentation setup | Team | Created `project_plan.md`, `decision_log.md`, `data_sources.md`, and `analysis_plan.md`; later added `project_journal.md` | The project required both a collaboration record and a reproducible technical record | Use Teams as the official collaboration trail and GitHub as the technical and version-control trail |
| Analytic-question development: defensive performance | Team | Refined the defensive-performance idea to compare defenders and midfielders using mean defensive actions (tackles plus interceptions) per 90 minutes | Raw defensive totals would not account for differences in playing time | Keep the question as a candidate pending dataset validation |
| Analytic-question development: discipline | Team | Rejected the original comparison of the proportions of defenders and midfielders receiving at least one yellow card, then reformulated the discipline theme as mean yellow cards per match for knockout-stage versus group-stage matches | A comparison of proportions did not naturally match the required one- or two-sample t-test workflow; a match-level numerical measure did | Keep the reformulated question as a candidate pending dataset validation |
| Analytic-question development: attacking and goalkeeping | Team | Developed the attacking question around mean attempts on target per match for progressed versus group-stage-eliminated teams and the goalkeeping question around mean goalkeeper Save% for the same progression groups | Both questions depended on locating and validating suitable data before confirmation | Investigate candidate sources; keep both questions provisional until validation |
| Task 4 source comparison and acquisition decision | Bhargav | Considered FIFA first because it is authoritative, then Stats Don't Lie, and finally FBref for goalkeeper variables | Complete Save% inputs were not confirmed from FIFA, and the required Save% or equivalent inputs could not be verified from Stats Don't Lie. FBref contained the required squad-level fields: Squad, MP, Min, SoTA, Saves, and Save% | Select FBref as the best-fit goalkeeper-performance source and attempt acquisition |
| FBref automated acquisition attempt 1 | Bhargav | Attempted to load the FBref table with `pandas.read_html()` | The local request returned HTTP 403 Forbidden | Try one controlled request with a browser-style User-Agent |
| FBref automated acquisition attempt 2 | Bhargav | Used `requests` with a browser-style User-Agent | The second request also returned HTTP 403 | Do not attempt aggressive bypassing or scraping workarounds; use FBref's browser-provided CSV text export |
| Raw goalkeeper data acquisition and inspection | Bhargav | Saved the browser-exported FBref squad goalkeeping table as a raw CSV and kept the raw source unchanged | Inspection revealed a two-row header, both Performance Save% and Penalty Kicks Save%, and leading lowercase country-code prefixes in Squad names | Explicitly select the overall Performance Save% and build a local validation script |
| Task 4 dataset validation | Bhargav | Created `src/validate_goalkeeping_data.py`, read the local FBref CSV with `header=[0, 1]`, and retained Squad, # Pl, MP, Min, SoTA, Saves, and Save% | Validation found a 48 × 21 raw shape, a 48 × 7 selected shape, 48 unique squads, 0 duplicates, no missing selected values, no zero or missing SoTA values, a Save% range of 33.3 to 90.9, and all Save% values between 0 and 100 | Confirm Task 4 and prepare the tournament progression classification |
| Progression-classification preparation | Bhargav | Used FIFA Round of 32 information to identify the 32 teams that progressed beyond the group stage; created the progression source file and `src/prepare_task4_data.py` | The intended complete classification was 32 Progressed and 16 Group-stage eliminated across all 48 squads | Integrate the FIFA classification with the FBref goalkeeper data and validate all names before saving |
| First cross-source integration failure | Bhargav | Ran the preparation script against 48 unique FBref squads with 0 duplicates | Name validation failed before processed data were saved. FBref's `eng England` value showed that the existing two-letter country-prefix cleaner was too narrow | Expand the country-prefix cleaner to accept two or three lowercase letters and rerun validation |
| Prefix-cleaning refinement | Bhargav | Changed the leading-country-code regex from `{2}` to `{2,3}` and reran validation | England then matched correctly; one genuine mismatch remained: FIFA used `Bosnia and Herzegovina`, while FBref used `Bosnia–Herz` | Decide on a transparent, verified cross-source harmonisation rule |
| Cross-source harmonisation decision | Bhargav | Left both raw source files unchanged, rejected fuzzy matching and automatic guessing, and added the single explicit verified alias `Bosnia–Herz` to `Bosnia and Herzegovina` in the integration script | The rule addressed the known source-specific label difference without obscuring or altering the raw evidence | Rerun the full integration validation and save output only if every check passes |
| Final Task 4 integration validation | Bhargav | Reran `src/prepare_task4_data.py` and created `data/processed/task4_goalkeeping_progression.csv` | Validation passed with 48 total teams, 48 unique squads, 0 duplicates, 0 unmatched FIFA progressed-team names, 0 missing `ProgressionStatus` values, 32 Progressed, and 16 Group-stage eliminated | Treat the Task 4 dataset as analysis-ready |
| Current Task 4 status | Bhargav | Completed and validated the Task 4 analysis-ready dataset | Descriptive statistics, confidence interval, t-test, assumptions, interpretation, and limitations have not yet been completed | Perform descriptive statistics and visual exploration for Task 4 |
| Task 4 descriptive analysis | Bhargav | Analysed the validated processed dataset by progression group; calculated descriptive statistics for Save%; and created a boxplot and histogram | Progressed teams had an observed mean Save% of 67.99%, compared with 58.53% for group-stage-eliminated teams, giving an observed difference of 9.46 percentage points. No potential outliers were identified in either group using the 1.5 × IQR rule. Statistical significance has not yet been assessed | Confidence interval and hypothesis-test planning |
| Task 4 confidence interval and assumption checking | Bhargav | Used the Week 4 course-aligned t-based confidence interval method. The individual group 95% CIs were [63.46, 72.52] for Progressed teams and [51.12, 65.94] for group-stage-eliminated teams. For the difference in means, the standard error was calculated as sqrt((s1^2 / n1) + (s2^2 / n2)), and the conservative smaller sample degrees of freedom was used: min(31, 15) = 15 | The 95% CI for the difference in means (Progressed minus Group-stage eliminated) was [0.67, 18.26] percentage points. No 1.5 × IQR outliers were detected, and skewness was mild in both groups (-0.22 and -0.12, respectively). The simple random sampling condition was not satisfied because the dataset included all 48 tournament teams rather than teams selected through simple random sampling. An inferential conclusion has not yet been made | State–Plan–Solve–Conclude two-sample t-test |
| Task 4 two-sample t-test | Bhargav | Used the State–Plan–Solve–Conclude workflow for a directional independent two-sample t-test with H0: mu_progressed = mu_eliminated, H1: mu_progressed > mu_eliminated, and alpha = 0.05. Applied the Week 4 conservative rule `df = min(31, 15) = 15` | The test gave `t = 2.2934` and a one-sided `p = 0.0183`. Because p < 0.05, H0 was rejected. There is evidence that, among the 2026 FIFA World Cup teams, progressed teams had a higher mean goalkeeper Save% than group-stage-eliminated teams; no causal claim was made. The simple-random-sampling limitation was retained, so the conclusion remains cautious and should not be broadly generalized beyond this tournament context | Integrate the course-aligned result into the final Task 4 report and presentation |

## 8. Review and Lessons Learned

**Review:** To be completed during the project.

**Lessons learned:** To be completed during the project.
