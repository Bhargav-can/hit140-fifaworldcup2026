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

[To be defined.]

### Confidence Interval

[To be defined.]

### Hypothesis Test

[To be defined.]

### Assumptions

[To be checked before inferential analysis.]

### Interpretation

[To be completed after analysis.]

### Limitations

[To be identified.]
