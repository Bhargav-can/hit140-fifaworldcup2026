"""Define the population and draw SRS without replacement within each position."""
import json
import pandas as pd
from extract_player_data import BASE
from validate_data import load_data, check_identity

GROUPS = ['DF', 'MF']


def main():
    data = load_data()
    check_identity(data)
    base = data.loc[data.Pos.isin(GROUPS) & data['90s'].gt(0) & data.Int.notna()].copy()
    distribution = base.groupby('Pos')['90s'].describe()
    print('90s distribution before minimum-playing-time rule:\n', distribution.to_string())
    counts = lambda threshold: {g: int(((base.Pos == g) & base['90s'].ge(threshold)).sum()) for g in GROUPS}
    candidates = {str(t): counts(t) for t in [0.1, 0.5, 1.0]}
    threshold = 1.0 if min(counts(1.0).values()) >= 30 else next(
        (t for t in [0.1, 0.5] if min(counts(t).values()) >= 30), None)
    if threshold is None:
        raise ValueError('BLOCKER: fewer than 30 players in either group at the lowest simple positive threshold (0.1 90s)')
    population = base.loc[base['90s'].ge(threshold)].copy()
    population['InterceptionsPer90'] = population.Int / population['90s']
    population.to_csv(BASE / 'data/processed/task1_player_population.csv', index=False)
    sample = pd.concat([population.loc[population.Pos == g].sample(n=30, replace=False, random_state=140) for g in GROUPS], ignore_index=True)
    sample.to_csv(BASE / 'data/processed/task1_player_sample.csv', index=False)
    metadata = {'threshold_90s': threshold, 'random_state': 140,
                'base_eligible_counts': base.Pos.value_counts().to_dict(),
                'playing_time_distribution_before_threshold': distribution.to_dict(orient='index'),
                'candidate_threshold_counts': candidates, 'population_counts': counts(threshold),
                'sample_counts': sample.Pos.value_counts().to_dict()}
    (BASE / 'data/processed/task1_sampling.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
