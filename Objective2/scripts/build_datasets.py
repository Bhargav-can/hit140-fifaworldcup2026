"""Build the two World Cup 2026 linear-regression tables from scraped pages.

Sources already downloaded beside this project, or fetched here:
- Match scores, dates, venues: worldcupstats.app fixtures page
- FIFA ranking points on 11 June 2026: published ranking table
- Qualifying goals for and against: Wikipedia qualification standings
- Squad age, market value, World Cup experience, share of foreign-based players:
  Transfermarkt participating-teams page
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Pages saved during collection. The script can re-download them.
PAGE = {
    "fixtures": RAW / "fixtures.txt",
    "squads": RAW / "transfermarkt_squads.html",
    "uefa": RAW / "qual_uefa.html",
    "afc": RAW / "qual_afc.html",
    "caf": RAW / "qual_caf.html",
    "concacaf": RAW / "qual_concacaf.html",
    "conmebol": RAW / "qual_conmebol.html",
    "ofc": RAW / "qual_ofc.html",
    "gold_cup": RAW / "gold_cup_2025.html",
}


def canon(name: str) -> str:
    name = re.sub(r"\[.*?\]", "", str(name))
    name = re.sub(r"\s*\([^)]*\)", "", name)
    name = name.replace("\xa0", " ").strip()
    name = re.sub(r"\s+", " ", name)
    aliases = {
        "USA": "United States",
        "US": "United States",
        "United States of America": "United States",
        "Korea Republic": "South Korea",
        "South Korea": "South Korea",
        "IR Iran": "Iran",
        "Iran": "Iran",
        "Türkiye": "Turkey",
        "Turkiye": "Turkey",
        "Turkey": "Turkey",
        "Czech Republic": "Czechia",
        "Czechia": "Czechia",
        "Côte d'Ivoire": "Ivory Coast",
        "Cote d'Ivoire": "Ivory Coast",
        "Ivory Coast": "Ivory Coast",
        "Congo DR": "DR Congo",
        "DR Congo": "DR Congo",
        "Democratic Republic of the Congo": "DR Congo",
        "Cabo Verde": "Cape Verde",
        "Cape Verde": "Cape Verde",
        "Bosnia and Herzegovina": "Bosnia and Herzegovina",
        "Bosnia & Herzegovina": "Bosnia and Herzegovina",
        "Bosnia-Herzegovina": "Bosnia and Herzegovina",
        "Curaçao": "Curacao",
        "Curacao": "Curacao",
        "China PR": "China",
    }
    return aliases.get(name, name)


def money_to_m(text: str) -> float:
    text = text.replace("€", "").replace(",", "").strip().lower()
    if text.endswith("bn"):
        return float(text[:-2]) * 1000
    if text.endswith("m"):
        return float(text[:-1])
    if text.endswith("k"):
        return float(text[:-1]) / 1000
    return float(text)


def parse_matches(path: Path) -> pd.DataFrame:
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
    rows = []
    for i, line in enumerate(lines):
        if line != "–":
            continue
        team_a = lines[i - 2]
        score_a = lines[i - 1]
        score_b = lines[i + 1]
        team_b = lines[i + 2]
        if not (score_a.isdigit() and score_b.isdigit()):
            continue
        venue = None
        date_text = None
        group_or_match = None
        for j in range(i - 3, max(-1, i - 12), -1):
            if lines[j] == "·" and venue is None:
                venue = lines[j + 1]
            if re.fullmatch(r"\d{1,2} (Jun|Jul)", lines[j]) and date_text is None:
                date_text = lines[j]
            if group_or_match is None and (
                lines[j].startswith("Match ") or lines[j].startswith("Group ")
            ):
                group_or_match = lines[j]
        if date_text is None or venue is None:
            continue
        day, mon = date_text.split()
        month = 6 if mon == "Jun" else 7
        rows.append(
            {
                "date": pd.Timestamp(year=2026, month=month, day=int(day)),
                "label": group_or_match or "",
                "venue": venue,
                "team_a": canon(team_a),
                "team_b": canon(team_b),
                "goals_a": int(score_a),
                "goals_b": int(score_b),
            }
        )
    df = pd.DataFrame(rows).drop_duplicates(
        subset=["date", "team_a", "team_b", "goals_a", "goals_b"]
    )
    df = df.sort_values(["date", "label", "team_a"]).reset_index(drop=True)
    df["match_n"] = df.index + 1
    df["match_id"] = df.apply(
        lambda r: f"M{r.match_n:03d}_{r.team_a}_{r.team_b}".replace(" ", ""),
        axis=1,
    )
    return df


def venue_country(venue: str) -> str:
    mexico = ("Ciudad de México", "Guadalajara", "Monterrey", "Akron", "Azteca", "BBVA")
    canada = ("Toronto", "BC Place", "Vancouver", "BMO")
    if any(k in venue for k in mexico):
        return "Mexico"
    if any(k in venue for k in canada):
        return "Canada"
    return "United States"


def host_flag(team_a: str, team_b: str, venue: str) -> int:
    country = venue_country(venue)
    if team_a == country:
        return 1
    if team_b == country:
        return -1
    return 0


def is_host_team(team: str, venue: str) -> int:
    return int(team == venue_country(venue) and team in {"Mexico", "Canada", "United States"})


def parse_ranking() -> pd.DataFrame:
    # The June 11, 2026 table is the last ranking before the tournament.
    # FIFA's next update was 20 July 2026, the day after the final.
    html_path = RAW / "fifa_ranking_2026_06_11.html"
    if not html_path.exists():
        url = "http://hiyun0727.blogspot.com/2026/06/fifa-mens-world-ranking-20260611.html"
        r = requests.get(url, headers=HEADERS, timeout=60)
        r.raise_for_status()
        html_path.write_text(r.text, encoding="utf-8")
    tables = pd.read_html(html_path)
    table = max(tables, key=len)
    table = table.iloc[:, :3].copy()
    table.columns = ["rank", "team", "fifa_points"]
    table["team"] = table["team"].map(canon)
    table["fifa_points"] = pd.to_numeric(table["fifa_points"], errors="coerce")
    table = table.dropna(subset=["fifa_points"])
    return table[["team", "fifa_points"]].drop_duplicates("team")


def standings_from_html(path: Path) -> pd.DataFrame:
    tables = pd.read_html(path)
    kept = []
    for table in tables:
        flat = pd.DataFrame(table)
        flat.columns = [
            " ".join(str(c) for c in col).strip() if isinstance(col, tuple) else str(col)
            for col in flat.columns
        ]
        cols = {c.lower(): c for c in flat.columns}
        gf = next((cols[k] for k in cols if k == "gf" or k.endswith(" gf")), None)
        ga = next((cols[k] for k in cols if k == "ga" or k.endswith(" ga")), None)
        pld = next((cols[k] for k in cols if k in {"pld", "mp", "played"} or k.endswith(" pld")), None)
        team_col = next((c for c in flat.columns if "team" in c.lower()), None)
        if not (gf and ga and pld and team_col):
            continue
        part = flat[[team_col, pld, gf, ga]].copy()
        part.columns = ["team", "played", "gf", "ga"]
        part["team"] = part["team"].astype(str).map(canon)
        for col in ["played", "gf", "ga"]:
            part[col] = pd.to_numeric(part[col], errors="coerce")
        part = part.dropna(subset=["played", "gf", "ga"])
        part = part[part["played"] > 0]
        kept.append(part)
    if not kept:
        return pd.DataFrame(columns=["team", "played", "gf", "ga"])
    all_rows = pd.concat(kept, ignore_index=True)
    # If a team is in a group table and a later summary, keep the longer record.
    all_rows = all_rows.sort_values("played").drop_duplicates("team", keep="last")
    return all_rows


def parse_squads(path: Path) -> pd.DataFrame:
    text = path.read_text(encoding="utf-8") if path.suffix == ".txt" else None
    if text is None:
        from bs4 import BeautifulSoup

        text = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml").get_text("\n", strip=True)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    start = next(i for i, ln in enumerate(lines) if ln == "France")
    # Each block: name, squad, age, world cups, foreigners %, total value, average value
    rows = []
    i = start
    while i + 6 < len(lines):
        name = lines[i]
        if name.startswith("©") or name.startswith("Transfermarkt"):
            break
        block = lines[i + 1 : i + 7]
        if not re.fullmatch(r"\d+", block[0]):
            i += 1
            continue
        if "€" not in block[4] or "€" not in block[5]:
            i += 1
            continue
        rows.append(
            {
                "team": canon(name),
                "squad_size": int(block[0]),
                "avg_age": float(block[1]),
                "wc_participations": int(block[2]),
                "foreigners_pct": float(block[3].replace("%", "")),
                "market_value_total_m": money_to_m(block[4]),
                "market_value_avg_m": money_to_m(block[5]),
            }
        )
        i += 7
    return pd.DataFrame(rows).drop_duplicates("team")


def add_running_form(matches: pd.DataFrame) -> pd.DataFrame:
    history = {team: [] for team in set(matches["team_a"]).union(matches["team_b"])}
    last_date = {}
    records = []
    for row in matches.itertuples(index=False):
        for side, team, opp in (
            ("a", row.team_a, row.team_b),
            ("b", row.team_b, row.team_a),
        ):
            past = history[team]
            if past:
                rest = (row.date - last_date[team]).days
                gd_so_far = sum(item["gd"] for item in past) / len(past)
                gf_so_far = sum(item["gf"] for item in past) / len(past)
                ga_so_far = sum(item["ga"] for item in past) / len(past)
            else:
                rest = 14  # same baseline for every team's first match
                gd_so_far = 0.0
                gf_so_far = 0.0
                ga_so_far = 0.0
            records.append(
                {
                    "match_id": row.match_id,
                    "side": side,
                    "rest_days": rest,
                    "wc_gd_so_far": gd_so_far,
                    "wc_gf_so_far": gf_so_far,
                    "wc_ga_so_far": ga_so_far,
                }
            )
        history[row.team_a].append({"gd": row.goals_a - row.goals_b, "gf": row.goals_a, "ga": row.goals_b})
        history[row.team_b].append({"gd": row.goals_b - row.goals_a, "gf": row.goals_b, "ga": row.goals_a})
        last_date[row.team_a] = row.date
        last_date[row.team_b] = row.date
    return pd.DataFrame(records)


def host_gold_cup(path: Path) -> pd.DataFrame:
    """2025 Gold Cup is the last full tournament the three hosts played before 2026."""
    from bs4 import BeautifulSoup

    lines = [
        ln.strip()
        for ln in BeautifulSoup(path.read_text(encoding="utf-8"), "lxml").get_text("\n").splitlines()
        if ln.strip()
    ]
    hosts = {"Mexico", "Canada", "United States"}
    totals = {team: {"played": 0, "gf": 0, "ga": 0} for team in hosts}
    seen = set()
    for i, line in enumerate(lines[1:-1], start=1):
        match = re.fullmatch(r"(\d+)–(\d+)", line)
        if not match:
            continue
        team_a = canon(lines[i - 1])
        team_b = canon(lines[i + 1])
        if team_a not in hosts and team_b not in hosts:
            continue
        if not re.fullmatch(r"[A-Za-z .'-]+", team_a) or not re.fullmatch(r"[A-Za-z .'-]+", team_b):
            continue
        key = tuple(sorted((team_a, team_b)) + [match.group(1), match.group(2)])
        if key in seen:
            continue
        seen.add(key)
        gf, ga = int(match.group(1)), int(match.group(2))
        if team_a in hosts:
            totals[team_a]["played"] += 1
            totals[team_a]["gf"] += gf
            totals[team_a]["ga"] += ga
        if team_b in hosts:
            totals[team_b]["played"] += 1
            totals[team_b]["gf"] += ga
            totals[team_b]["ga"] += gf
    rows = []
    for team, rec in totals.items():
        rows.append(
            {
                "team": team,
                "played": rec["played"],
                "qual_gf_per_game": rec["gf"] / rec["played"],
                "qual_ga_per_game": rec["ga"] / rec["played"],
                "qual_gd_per_game": (rec["gf"] - rec["ga"]) / rec["played"],
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    matches = parse_matches(PAGE["fixtures"])
    ranking = parse_ranking()
    squads = parse_squads(PAGE["squads"])
    qual = pd.concat(
        [standings_from_html(PAGE[k]) for k in ("uefa", "afc", "caf", "concacaf", "conmebol", "ofc")],
        ignore_index=True,
    )
    qual = qual.sort_values("played").drop_duplicates("team", keep="last")
    qual["qual_gf_per_game"] = qual["gf"] / qual["played"]
    qual["qual_ga_per_game"] = qual["ga"] / qual["played"]
    qual["qual_gd_per_game"] = (qual["gf"] - qual["ga"]) / qual["played"]
    hosts = host_gold_cup(PAGE["gold_cup"])
    qual = pd.concat([qual, hosts], ignore_index=True)
    qual = qual.drop_duplicates("team", keep="last")
    # The OFC group table stops at 3 matches (19 goals, 1 conceded). The same
    # page records the semi-final, New Zealand 7-0 Fiji, and the final,
    # New Caledonia 0-3 New Zealand. Those two games belong in the record.
    nz = qual["team"] == "New Zealand"
    qual.loc[nz, ["played", "gf", "ga"]] = [5, 29, 1]
    qual.loc[nz, "qual_gf_per_game"] = 29 / 5
    qual.loc[nz, "qual_ga_per_game"] = 1 / 5
    qual.loc[nz, "qual_gd_per_game"] = 28 / 5

    teams = sorted(set(matches["team_a"]).union(matches["team_b"]))
    base = pd.DataFrame({"team": teams})
    base = base.merge(ranking, on="team", how="left")
    base = base.merge(squads, on="team", how="left")
    base = base.merge(
        qual[["team", "played", "qual_gf_per_game", "qual_ga_per_game", "qual_gd_per_game"]],
        on="team",
        how="left",
    )
    missing = base[base.isna().any(axis=1)]
    missing_path = OUT / "unmatched_teams.csv"
    missing.to_csv(missing_path, index=False)

    form = add_running_form(matches)
    form_a = form[form["side"] == "a"].drop(columns="side")
    form_b = form[form["side"] == "b"].drop(columns="side")
    form_a = form_a.add_suffix("_a").rename(columns={"match_id_a": "match_id"})
    form_b = form_b.add_suffix("_b").rename(columns={"match_id_b": "match_id"})
    m = matches.merge(form_a, on="match_id").merge(form_b, on="match_id")

    def take(frame, team_col, cols):
        out = frame[[team_col]].merge(base, left_on=team_col, right_on="team", how="left")
        return out[cols]

    a_cols = ["fifa_points", "qual_gf_per_game", "qual_ga_per_game", "qual_gd_per_game",
              "market_value_avg_m", "avg_age", "wc_participations", "foreigners_pct"]
    left = take(m, "team_a", a_cols).add_suffix("_a")
    right = take(m, "team_b", a_cols).add_suffix("_b")
    m = pd.concat([m.reset_index(drop=True), left, right], axis=1)
    m["host"] = [host_flag(a, b, v) for a, b, v in zip(m.team_a, m.team_b, m.venue)]

    model_1 = pd.DataFrame(
        {
            "match_id": m["match_id"],
            "fifa_points_diff": m["fifa_points_a"] - m["fifa_points_b"],
            "qual_gd_per_game_diff": m["qual_gd_per_game_a"] - m["qual_gd_per_game_b"],
            "market_value_avg_diff": m["market_value_avg_m_a"] - m["market_value_avg_m_b"],
            "age_avg_diff": m["avg_age_a"] - m["avg_age_b"],
            "host": m["host"],
            "rest_days_diff": m["rest_days_a"] - m["rest_days_b"],
            "wc_gd_so_far": m["wc_gd_so_far_a"] - m["wc_gd_so_far_b"],
            "wc_experience_diff": m["wc_participations_a"] - m["wc_participations_b"],
            "goal_diff": m["goals_a"] - m["goals_b"],
        }
    )

    rows = []
    for row in m.itertuples(index=False):
        for team, opp, goals, gf_so_far, opp_ga_so_far in (
            (row.team_a, row.team_b, row.goals_a, row.wc_gf_so_far_a, row.wc_ga_so_far_b),
            (row.team_b, row.team_a, row.goals_b, row.wc_gf_so_far_b, row.wc_ga_so_far_a),
        ):
            t = base.set_index("team").loc[team]
            o = base.set_index("team").loc[opp]
            rows.append(
                {
                    "team_match_id": f"{row.match_id}_{team.replace(' ', '')}",
                    "qual_gf_per_game": t.qual_gf_per_game,
                    "opp_qual_ga_per_game": o.qual_ga_per_game,
                    "wc_goals_so_far": gf_so_far,
                    "opp_wc_ga_so_far": opp_ga_so_far,
                    "foreigners_pct": t.foreigners_pct,
                    "opp_foreigners_pct": o.foreigners_pct,
                    "squad_size": t.squad_size,
                    "opp_squad_size": o.squad_size,
                    "goals": goals,
                }
            )
    model_2 = pd.DataFrame(rows)

    model_1_path = OUT / "linreg_2_1.csv"
    model_2_path = OUT / "linreg_2_2.csv"
    base_path = OUT / "team_features.csv"
    model_1.to_csv(model_1_path, index=False)
    model_2.to_csv(model_2_path, index=False)
    base.to_csv(base_path, index=False)
    print("matches", len(matches), "model1", model_1.shape, "model2", model_2.shape)
    print("missing teams", missing["team"].tolist())
    print("model1 nulls", int(model_1.isna().sum().sum()), "model2 nulls", int(model_2.isna().sum().sum()))


if __name__ == "__main__":
    main()
