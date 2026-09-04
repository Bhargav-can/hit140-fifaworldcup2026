# Analysis Plan

## Analytic Task 1

### Analytic Question

[To be defined.]

### Population

[To be defined.]

### Sample

[To be defined.]

### Variables

[To be defined.]

### Data Wrangling

[To be defined.]

### Descriptive Statistics

[To be defined.]

### Confidence Interval

[To be defined.]

### Hypothesis Test

[To be defined.]

### Assumptions

[To be defined.]

### Interpretation

[To be completed after analysis.]

### Limitations

[To be identified.]

## Analytic Task 2

### Analytic Question

[To be defined.]

### Population

[To be defined.]

### Sample

[To be defined.]

### Variables

[To be defined.]

### Data Wrangling

[To be defined.]

### Descriptive Statistics

[To be defined.]

### Confidence Interval

[To be defined.]

### Hypothesis Test

[To be defined.]

### Assumptions

[To be defined.]

### Interpretation

[To be completed after analysis.]

### Limitations

[To be identified.]

## Analytic Task 3

### Analytic Question

[To be defined.]

### Population

[To be defined.]

### Sample

[To be defined.]

### Variables

[To be defined.]

### Data Wrangling

[To be defined.]

### Descriptive Statistics

[To be defined.]

### Confidence Interval

[To be defined.]

### Hypothesis Test

[To be defined.]

### Assumptions

[To be defined.]

### Interpretation

[To be completed after analysis.]

### Limitations

[To be identified.]

## Analytic Task 4

### Analytic Question

Do teams that progressed beyond the group stage have a higher mean goalkeeper save percentage than teams eliminated in the group stage?

### Population

Teams participating in the 2026 FIFA World Cup.

### Sample

All 48 participating squads represented by the FBref squad goalkeeping dataset.

### Variables

- Grouping variable: `ProgressionStatus` (Progressed vs Group-stage eliminated), based on FIFA Round of 32 membership.
- Numerical variable: goalkeeper save percentage (overall Performance Save%).

### Data Wrangling

- Parse the two-row FBref CSV header.
- Select the overall Performance Save% rather than Penalty Kicks Save%.
- Remove the two- or three-letter leading lowercase FBref country prefix from each squad name.
- Explicitly harmonise `Bosnia–Herz` to `Bosnia and Herzegovina` for cross-source matching; do not use fuzzy matching or automatic guessing.
- Classify teams using FIFA Round of 32 membership and create `ProgressionStatus`.
- Retain Squad, MP, Min, SoTA, Saves, Save%, and ProgressionStatus.
- Validate 32 progressed teams, 16 group-stage-eliminated teams, and 48 teams in total before analysis.

### Descriptive Statistics

| Progression group | n | Mean Save% | Median | Standard deviation | Minimum | Maximum | Q1 | Q3 | IQR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Progressed | 32 | 67.99 | 69.80 | 12.57 | 42.90 | 90.90 | 58.67 | 77.12 | 18.45 |
| Group-stage eliminated | 16 | 58.53 | 58.95 | 13.91 | 33.30 | 83.30 | 50.00 | 67.28 | 17.28 |

The observed difference in group means (Progressed mean minus Group-stage eliminated mean) was 9.46 percentage points. A boxplot and histogram were created for visual exploration of Save% by progression group.

### Confidence Interval

The 95% t confidence intervals for the group mean Save% values were:

| Progression group | Mean Save% | Standard error | Degrees of freedom | 95% confidence interval |
| --- | ---: | ---: | ---: | ---: |
| Progressed | 67.99 | 2.22 | 31 | [63.46, 72.52] |
| Group-stage eliminated | 58.53 | 3.48 | 15 | [51.12, 65.94] |

For the difference in means (Progressed minus Group-stage eliminated), the standard error was calculated using `sqrt((s1^2 / n1) + (s2^2 / n2))`. The observed difference was 9.46 percentage points, the standard error was 4.13, and the 95% confidence interval was [0.67, 18.26] percentage points. The degrees of freedom were `min(n1 - 1, n2 - 1) = min(31, 15) = 15`, following the Week 4 conservative smaller-sample-degrees-of-freedom approach.

### Hypothesis Test

Not yet completed.

### Assumptions

- No 1.5 × IQR outliers were detected in either group.
- Skewness was mild in both groups: -0.22 for Progressed teams and -0.12 for group-stage-eliminated teams.
- The simple random sampling condition was not satisfied / not applicable because the dataset contains all 48 participating 2026 FIFA World Cup teams rather than teams selected through a simple random sampling procedure.
- Inference should therefore be interpreted cautiously and in the context of the 2026 FIFA World Cup teams.

### Interpretation

[To be completed after analysis.]

### Limitations

[To be identified.]
