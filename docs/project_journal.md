# Project Journal

## Purpose

This journal records the group's real analytical process, including data-source investigation, question formulation and refinement, methodological decisions, progress, reviews, and lessons learned.

## 1. Initial Project Setup

- A shared GitHub repository was established.
- Individual working branches exist for Bhargav, Gaurav, Kushal, and Sharif.
- The current assessment scope is Objective 1 / Assessment 2.
- The team is using the Weeks 1–5 statistical workflow required by the assessment.

## 2. Data Source Investigation

| Stage | Source | Data Level | Variables Observed | Potential Use | Issues / Limitations | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Task 4 source comparison | FIFA | Team | Goalkeeper saves, goals conceded, and other team goalkeeping metrics | Official tournament source checked first for Task 4 goalkeeper statistics | The variables needed to calculate goalkeeper save percentage directly, especially shots on target against, were not confirmed for this task | Not selected for Task 4 acquisition |
| Task 4 source comparison | Stats Don't Lie | Not verified | Goalkeeper performance variables considered | Considered as a possible World Cup goalkeeper statistics source | Save percentage or the full inputs needed to calculate it could not be verified for Task 4 | Not selected for Task 4 acquisition |
| Task 4 source comparison and validation | FBref | Squad | Squad, MP, Min, shots on target against, saves, and Save% | Exact squad-level variable match for Task 4 | The raw CSV had a two-level header and two Save% fields, so the overall Performance Save% was explicitly selected rather than Penalty Kicks Save% | Browser-provided CSV export successfully loaded and validated in Python: 48 × 21 raw shape, 48 × 7 selected shape, 48 unique squads, 0 duplicates, no missing selected values, no zero or missing SoTA observations, and Save% from 33.3 to 90.9 with all values between 0 and 100; squad names were cleaned by removing FBref's leading lowercase country code |

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
| Bhargav | Task 4 | Goalkeeping performance | Dataset validated; tournament progression classification pending |

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

| Stage | Member(s) | Work Completed | Issue / Finding | Next Step |
| --- | --- | --- | --- | --- |
| Task 4 source comparison and acquisition decision | Bhargav | Compared FIFA, Stats Don't Lie, and FBref for goalkeeper variables and tested automated FBref retrieval | FIFA did not provide all confirmed variables required for Save%; Stats Don't Lie fields were not verified; FBref had the required variables but blocked automated requests | Save the FBref source-provided CSV export as the raw dataset and validate it in Python |
| Task 4 dataset validation | Bhargav | Loaded and validated the FBref squad goalkeeper CSV in Python | Dataset contained 48 unique squads, no duplicates, no missing selected values, no zero/missing SoTA observations, and valid Save% values from 33.3 to 90.9 | Classify squads by tournament progression and begin descriptive analysis |

## 8. Review and Lessons Learned

**Review:** To be completed during the project.

**Lessons learned:** To be completed during the project.
