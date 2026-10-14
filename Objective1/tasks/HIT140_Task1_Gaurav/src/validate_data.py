"""Validate all extracted player rows before eligibility filtering."""
import json
import numpy as np
import pandas as pd
from extract_player_data import BASE, EXTRACTED, FIELDS


def load_data():
    data = pd.read_csv(EXTRACTED, dtype=str)
    if list(data.columns) != list(FIELDS):
        raise ValueError('Unexpected extracted columns')
    for col in ['90s', 'Int']:
        data[col] = pd.to_numeric(data[col], errors='raise')
        if not np.isfinite(data[col].dropna()).all() or (data[col].dropna() < 0).any():
            raise ValueError(f'Invalid numeric values in {col}')
    if (data['Int'].dropna() % 1 != 0).any():
        raise ValueError('Interceptions must be whole counts')
    return data


def validate(data):
    report = {
        'raw_player_count': len(data),
        'unique_player_squad_rows': len(data.drop_duplicates(['Player', 'Squad'])),
        'missing': {k: int(v) for k, v in data.isna().sum().items()},
        'duplicate_player_squad_rows': int(data.duplicated(['Player', 'Squad']).sum()),
        'rows_in_duplicate_sets': int(data.duplicated(['Player', 'Squad'], keep=False).sum()),
        'counts_by_position': {k: int(v) for k, v in data.Pos.value_counts(dropna=False).items()},
        'ranges': {c: {'min': float(data[c].min()), 'max': float(data[c].max())} for c in ['90s', 'Int']},
    }
    return report


def check_identity(data):
    if data[['Player', 'Pos', 'Squad']].isna().any().any():
        raise ValueError('Missing player identity/position; resolve before sampling')
    if data.duplicated(['Player', 'Squad']).any():
        raise ValueError('Duplicate player/squad rows; resolve before sampling')


def main():
    data = load_data()
    report = validate(data)
    (BASE / 'data/processed/task1_validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    check_identity(data)
    print('Validation passed; missing numeric fields are excluded by eligibility.')


if __name__ == '__main__':
    main()
