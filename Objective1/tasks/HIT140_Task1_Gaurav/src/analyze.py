"""Week 4 State → Plan → Solve → Conclude, using only the random sample."""
import json
import os
from pathlib import Path
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'hit140_matplotlib_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from extract_player_data import BASE


def main():
    data = pd.read_csv(BASE / 'data/processed/task1_player_sample.csv')
    if data.isna().any().any() or data.duplicated(['Player', 'Squad']).any():
        raise ValueError('Missing or duplicate sample rows')
    if data.Pos.value_counts().to_dict() != {'DF': 30, 'MF': 30}:
        raise ValueError('Expected exactly 30 DF and 30 MF')
    if not np.allclose(data.InterceptionsPer90, data.Int / data['90s']):
        raise ValueError('Incorrect rates')
    summaries, values = {}, {}
    for group in ['DF', 'MF']:
        rows = data.loc[data.Pos == group]
        x = rows.InterceptionsPer90
        values[group] = x
        q1, q3 = x.quantile([.25, .75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        margin = stats.t.ppf(.975, len(x)-1) * x.std(ddof=1) / np.sqrt(len(x))
        summaries[group] = dict(n=len(x), mean=x.mean(), median=x.median(), sd=x.std(ddof=1),
                                min=x.min(), max=x.max(), Q1=q1, Q3=q3, IQR=iqr,
                                skewness=x.skew(), mean_ci95=[x.mean()-margin, x.mean()+margin],
                                outlier_fences=[low, high],
                                outliers=rows.loc[(x < low) | (x > high), ['Player', 'Squad', 'InterceptionsPer90']].to_dict('records'))
    difference = summaries['DF']['mean'] - summaries['MF']['mean']
    se = np.sqrt(sum(s['sd']**2 / s['n'] for s in summaries.values()))
    df = min(s['n']-1 for s in summaries.values())
    if not np.isfinite(se) or se <= 0:
        raise ValueError('Cannot perform t inference with zero or invalid SE')
    t = difference / se
    p = stats.t.sf(t, df)
    ci = [difference-stats.t.ppf(.975, df)*se, difference+stats.t.ppf(.975, df)*se]
    conclusion = ('Reject H0. The sample provides evidence' if p < .05 else 'Fail to reject H0. The sample does not provide sufficient evidence') + ' that eligible defenders have a higher mean interceptions-per-90 rate than eligible midfielders at alpha = 0.05.'
    warnings = ['Players within the same team may share team/tactical context, so perfect independence is a limitation.',
                'Inference is restricted to eligible players in the saved table; position is observational and does not establish causation.',
                'Rounded 90s affect rates. The specified course SE does not apply a finite-population correction.',
                'Skewness and outliers can affect t inference; flagged observations are retained, not removed.']
    edges = np.histogram_bin_edges(data.InterceptionsPer90, bins=8)
    figures = BASE / 'figures'
    figures.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot([values[g] for g in ['DF', 'MF']], tick_labels=['Defenders (n=30)', 'Midfielders (n=30)'])
    ax.set(title='Interceptions per 90 Minutes: Defenders vs Midfielders', ylabel='Interceptions per 90 minutes')
    ax.grid(axis='y', alpha=.25)
    fig.tight_layout()
    fig.savefig(figures / 'task1_interceptions_per90_boxplot.png', dpi=200)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharex=True, sharey=True)
    for ax, g, color in zip(axes, ['DF', 'MF'], ['#4C78A8', '#F58518']):
        ax.hist(values[g], bins=edges, color=color, edgecolor='white')
        ax.set(title=f'{"Defenders" if g == "DF" else "Midfielders"} (n=30)', xlabel='Interceptions per 90 minutes', ylabel='Number of players')
    fig.suptitle('Distribution of Interceptions per 90 Minutes by Position')
    fig.tight_layout()
    fig.savefig(figures / 'task1_interceptions_per90_histogram.png', dpi=200)
    plt.close(fig)
    result = dict(groups=summaries, difference=difference, SE=se, df=df, ci95_difference=ci,
                  t=t, p_one_sided=p, alpha=.05, conclusion=conclusion, warnings=warnings,
                  histogram_bin_edges=edges.tolist())
    (BASE / 'data/processed/task1_analysis_results.json').write_text(json.dumps(result, indent=2) + '\n')
    lines = ['# Task 1 player-level analysis summary', '', '## State', '',
             'Do defenders have a higher mean number of interceptions per 90 minutes than midfielders in the 2026 FIFA World Cup?', '',
             '`H0: mu_DF = mu_MF`; `H1: mu_DF > mu_MF`. Alpha = 0.05; one-sided test.', '',
             '## Plan', '', 'Analyze only the reproducible random sample: 30 DF and 30 MF, sampled without replacement separately using random_state=140. See analysis_plan.md for population eligibility and sampling details.', '',
             '## Solve', '', '| Group | n | Mean | Median | SD | Min | Max | Q1 | Q3 | IQR | Skewness |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for g, s in summaries.items():
        lines.append('| ' + g + ' | ' + ' | '.join(str(s[k]) if k == 'n' else f'{s[k]:.6f}' for k in ['n','mean','median','sd','min','max','Q1','Q3','IQR','skewness']) + ' |')
    for g, s in summaries.items():
        lines += ['', f"{g} mean 95% CI: ({s['mean_ci95'][0]:.6f}, {s['mean_ci95'][1]:.6f}).",
                  f"{g} 1.5 × IQR fences: {s['outlier_fences']}. Outliers (retained): {s['outliers'] or 'None'}."]
    lines += ['', f'DF − MF = {difference:.6f}; SE = {se:.6f}; conservative df = {df}.',
              f'Two-sided 95% CI for difference: ({ci[0]:.6f}, {ci[1]:.6f}).',
              f't = {t:.6f}; one-sided p = {p:.8f}.', '', '## Conclude', '', conclusion, '', *warnings,
              '', 'This compares position-associated rates, not a causal effect of position.']
    (BASE / 'docs/analysis_summary.md').write_text('\n'.join(lines) + '\n')
    print('STATE → PLAN → SOLVE → CONCLUDE')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
