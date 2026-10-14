"""Cross-check linreg_2_1.csv against linreg_2_2.csv and the saved sources."""
import importlib.util
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("b", ROOT / "scripts" / "build_datasets.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

m1 = pd.read_csv(ROOT / "data" / "linreg_2_1.csv")
m2 = pd.read_csv(ROOT / "data" / "linreg_2_2.csv")
teams = pd.read_csv(ROOT / "data" / "team_features.csv")
matches = b.parse_matches(b.PAGE["fixtures"])

problems = []

def check(name, ok, detail=""):
    problems.append((name, bool(ok), detail))

check("2.1 has 104 rows and 10 columns", m1.shape == (104, 10), str(m1.shape))
check("2.2 has 208 rows and 10 columns", m2.shape == (208, 10), str(m2.shape))
check("no empty cells in 2.1", int(m1.isna().sum().sum()) == 0)
check("no empty cells in 2.2", int(m2.isna().sum().sum()) == 0)
check("104 unique matches", m1.match_id.nunique() == 104)
check("208 unique team-matches", m2.team_match_id.nunique() == 208)
check("parsed fixtures also 104", len(matches) == 104)
check("48 teams", teams.team.nunique() == 48)

# Each match has two team rows, and those goals reproduce goal difference.
m2 = m2.copy()
m2["match_id"] = m2.team_match_id.str.extract(r"^(M\d+_[^_]+_[^_]+)_")
# team names can contain no underscore after our replace, but multi-word names had spaces removed.
# Safer: match_id is the prefix used when the row was built as f"{match_id}_{team}"
# Rebuild from known match ids.
ids = sorted(m1.match_id, key=len, reverse=True)

def split_id(row_id):
    for mid in ids:
        if row_id.startswith(mid + "_"):
            return mid, row_id[len(mid) + 1 :]
    return None, None

m2[["match_id", "team_key"]] = m2.team_match_id.apply(lambda s: pd.Series(split_id(s)))
check("every 2.2 row maps to a 2.1 match", m2.match_id.notna().all())
counts = m2.groupby("match_id").size()
check("every match has exactly two team rows", (counts == 2).all(), str(counts.value_counts().to_dict()))

# Goals in the two rows must add in the fixture order.
merged = matches.merge(m1, on="match_id")
goals = {}
for row in m2.itertuples(index=False):
    goals.setdefault(row.match_id, {})[row.team_key] = row.goals

bad_scores = []
for row in merged.itertuples(index=False):
    g = goals[row.match_id]
    a_key = row.team_a.replace(" ", "")
    b_key = row.team_b.replace(" ", "")
    if g.get(a_key) != row.goals_a or g.get(b_key) != row.goals_b:
        bad_scores.append((row.match_id, row.team_a, row.goals_a, g.get(a_key), row.team_b, row.goals_b, g.get(b_key)))
    if (row.goals_a - row.goals_b) != row.goal_diff:
        bad_scores.append(("diff", row.match_id, row.goal_diff, row.goals_a, row.goals_b))
check("2.2 goals match fixture scores and 2.1 goal difference", len(bad_scores) == 0, str(bad_scores[:8]))
check("total goals are 308", int(m2.goals.sum()) == 308, str(m2.goals.sum()))

# Known results
known = {
    "M001_Mexico_SouthAfrica": (2, 0),
    "M104_Spain_Argentina": (1, 0),
    "M103_France_England": (4, 6),
}
for mid, (ga, gb) in known.items():
    row = matches.set_index("match_id").loc[mid]
    check(mid, (row.goals_a, row.goals_b) == (ga, gb), f"{row.team_a} {row.goals_a}-{row.goals_b} {row.team_b}")

# FIFA points for the top of the 11 June ranking
rank = b.parse_ranking().set_index("team")
expected_points = {
    "Argentina": 1877.27,
    "Spain": 1874.71,
    "France": 1870.70,
    "England": 1828.02,
}
for team, pts in expected_points.items():
    got = float(teams.set_index("team").loc[team, "fifa_points"])
    check(f"FIFA points {team}", abs(got - pts) < 0.02, f"{got} vs {pts}")

# 2.1 gaps equal team-feature differences
base = teams.set_index("team")
gap_bad = []
for row in merged.itertuples(index=False):
    a, bteam = base.loc[row.team_a], base.loc[row.team_b]
    pairs = {
        "fifa_points_diff": a.fifa_points - bteam.fifa_points,
        "qual_gd_per_game_diff": a.qual_gd_per_game - bteam.qual_gd_per_game,
        "market_value_avg_diff": a.market_value_avg_m - bteam.market_value_avg_m,
        "age_avg_diff": a.avg_age - bteam.avg_age,
        "wc_experience_diff": a.wc_participations - bteam.wc_participations,
    }
    for col, val in pairs.items():
        if abs(getattr(row, col) - val) > 1e-6:
            gap_bad.append((row.match_id, col, getattr(row, col), val))
check("2.1 gaps match team_features", len(gap_bad) == 0, str(gap_bad[:6]))

# 2.2 levels match team_features, and qual GD identity holds
level_bad = []
for row in m2.itertuples(index=False):
    mid, key = split_id(row.team_match_id)
    match = matches.set_index("match_id").loc[mid]
    team = match.team_a if match.team_a.replace(" ", "") == key else match.team_b
    opp = match.team_b if team == match.team_a else match.team_a
    t, o = base.loc[team], base.loc[opp]
    if abs(row.qual_gf_per_game - t.qual_gf_per_game) > 1e-6:
        level_bad.append((row.team_match_id, "gf"))
    if abs(row.opp_qual_ga_per_game - o.qual_ga_per_game) > 1e-6:
        level_bad.append((row.team_match_id, "opp ga"))
    if abs(row.foreigners_pct - t.foreigners_pct) > 1e-6:
        level_bad.append((row.team_match_id, "foreigners"))
    if abs(row.opp_foreigners_pct - o.foreigners_pct) > 1e-6:
        level_bad.append((row.team_match_id, "opp foreigners"))
    if row.squad_size != t.squad_size or row.opp_squad_size != o.squad_size:
        level_bad.append((row.team_match_id, "squad"))
check("2.2 levels match team_features", len(level_bad) == 0, str(level_bad[:6]))

x1 = set(m1.columns) - {"match_id", "goal_diff"}
x2 = set(m2.columns) - {"team_match_id", "goals", "match_id", "team_key"}
check("each model has 8 explanatory variables", len(x1) == 8 and len(x2) == 8, f"{len(x1)} and {len(x2)}")
check("no explanatory variable name is shared", x1.isdisjoint(x2), str(sorted(x1 & x2)))

ident_bad = []
for row in merged.itertuples(index=False):
    a, bteam = base.loc[row.team_a], base.loc[row.team_b]
    built = (a.qual_gf_per_game - a.qual_ga_per_game) - (bteam.qual_gf_per_game - bteam.qual_ga_per_game)
    if abs(built - row.qual_gd_per_game_diff) > 1e-6:
        ident_bad.append(row.match_id)
check("qual GD gap equals GF gap minus GA gap", len(ident_bad) == 0, str(ident_bad[:6]))

# First match for every team: rest 14 and tournament form 0
first = []
seen = set()
for row in matches.sort_values(["date", "match_n"]).itertuples(index=False):
    for team, side_goals in ((row.team_a, "a"), (row.team_b, "b")):
        if team in seen:
            continue
        seen.add(team)
        key = team.replace(" ", "")
        r2 = m2[(m2.match_id == row.match_id) & (m2.team_key == key)].iloc[0]
        if r2.wc_goals_so_far != 0 or r2.opp_wc_ga_so_far != 0:
            first.append((team, r2.wc_goals_so_far, r2.opp_wc_ga_so_far))
check("all 48 teams start with no earlier World Cup goals", len(first) == 0 and len(seen) == 48, str(first[:6]))

# Host flag only for the three hosts, and it agrees across tables
host_bad = []
for row in merged.itertuples(index=False):
    country = b.venue_country(row.venue)
    expected = 1 if row.team_a == country else (-1 if row.team_b == country else 0)
    if row.host != expected:
        host_bad.append((row.match_id, row.host, expected, row.venue))
check("host flags agree with the venue", len(host_bad) == 0, str(host_bad[:6]))

# No team plays twice on the same day
day_pairs = []
for row in matches.itertuples(index=False):
    day_pairs.append((row.date, row.team_a))
    day_pairs.append((row.date, row.team_b))
dup_days = pd.Series(day_pairs).duplicated().sum()
check("no team plays twice on the same date", dup_days == 0, str(dup_days))

# Qualifying sample size
odd = teams[(teams.played < 3) | (teams.played > 20) | (teams.qual_gf_per_game > 6)]
check(
    "qualifying or Gold Cup sample is between 3 and 20 games",
    odd.empty,
    odd[["team", "played", "qual_gf_per_game", "qual_ga_per_game"]].to_string(index=False) if len(odd) else "",
)

print(f"CHECKS {sum(ok for _, ok, _ in problems)}/{len(problems)} passed")
for name, ok, detail in problems:
    mark = "OK" if ok else "FAIL"
    extra = f" | {detail}" if detail and not ok else ""
    print(f"{mark}: {name}{extra}")
