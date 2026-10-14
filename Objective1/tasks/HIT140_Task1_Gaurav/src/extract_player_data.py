"""Extract the saved FBref player table once, preserving its row order."""
from pathlib import Path
from bs4 import BeautifulSoup, Comment
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / 'data/raw/fbref_player_miscellaneous_2026.html'
EXTRACTED = BASE / 'data/processed/task1_player_extracted.csv'
FIELDS = {'Player': 'player', 'Pos': 'position', 'Squad': 'team',
          '90s': 'minutes_90s', 'Int': 'interceptions'}


def extract():
    soup = BeautifulSoup(RAW.read_text(encoding='utf-8'), 'html.parser')
    tables = soup.find_all('table', id='stats_misc')
    if not tables:
        for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
            if 'stats_misc' in comment:
                tables.extend(BeautifulSoup(str(comment), 'html.parser').find_all('table', id='stats_misc'))
    if len(tables) != 1:
        raise ValueError(f'Expected one player table; found {len(tables)}')
    table = tables[0]
    if '2026 World Cup' not in table.caption.get_text(' ', strip=True):
        raise ValueError('Unexpected table caption')
    rows = []
    for row in table.select('tbody tr'):
        if 'thead' in row.get('class', []):
            continue  # Repeated column headings are not players.
        result = {}
        for name, stat in FIELDS.items():
            cell = row.find(attrs={'data-stat': stat})
            if cell is None:
                raise ValueError(f'Missing field cell: {stat}')
            # The squad anchor excludes the decorative country-code flag.
            value = cell.find('a') if name == 'Squad' else cell
            result[name] = (value or cell).get_text(' ', strip=True)
        rows.append(result)
    if not rows:
        raise ValueError('No player rows extracted')
    return pd.DataFrame(rows, columns=FIELDS)


def main():
    data = extract()
    EXTRACTED.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(EXTRACTED, index=False)
    print(f'Extracted raw player count: {len(data)}')
    print(f'Saved: {EXTRACTED.relative_to(BASE)}')


if __name__ == '__main__':
    main()
