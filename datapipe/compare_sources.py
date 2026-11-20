"""Coverage and completeness of Wikidata vs IMDb (bulk) for a release-year range.

    python datapipe/compare_sources.py --from-year 1989 --to-year 1991

Reads the Wikidata store (data/raw/wikidata/store.sqlite) and the local IMDb index
(data/local/imdb_<y0>_<y1>.json from datapipe/imdb_index.py). Prints aggregate counts
only; no IMDb records are written anywhere.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from store import Store  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# Reference: the 25 highest-grossing US releases of 1990 (title as on IMDb / Wikidata)
TOP_1990 = ["Home Alone", "Ghost", "Dances with Wolves", "Pretty Woman", "Teenage Mutant Ninja Turtles",
            "The Hunt for Red October", "Total Recall", "Die Hard 2", "Dick Tracy", "Kindergarten Cop",
            "Back to the Future Part III", "Presumed Innocent", "Days of Thunder", "Another 48 Hrs.",
            "Bird on a Wire", "Flatliners", "Look Who's Talking Too", "Misery", "Edward Scissorhands",
            "Goodfellas", "The Godfather Part III", "Awakenings", "Arachnophobia", "Problem Child", "Gremlins 2: The New Batch"]


def q(uri):
    return uri.rsplit("/", 1)[1]


def pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "n/a"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-year", type=int, default=1989)
    ap.add_argument("--to-year", type=int, default=1991)
    ap.add_argument("--index", default=str(ROOT / "data" / "local" / "imdb_1985_1992.json"))
    a = ap.parse_args()
    years = range(a.from_year, a.to_year + 1)
    imdb = json.loads(Path(a.index).read_text())
    T, N = imdb["titles"], imdb["people"]

    st = Store()
    films = st.films(a.from_year, a.to_year)
    excl = {q(r["f"]) for r in st.rows("exclude")}
    W = {f for f in films if f not in excl}
    to_t = {q(r["x"]): r["imdb"] for r in st.rows("imdbids")}
    W_t = {to_t[f]: f for f in W if f in to_t}

    def us_feature(t, x):
        return (x["type"] == "movie" and x["year"] in years and not x["adult"] and "US" in x.get("regions", [])
                and (x["runtime"] is None or x["runtime"] >= 60))
    A = {t for t, x in T.items() if us_feature(t, x)}
    tiers = {"all US-released features": A}
    for v in (1000, 5000, 25000):
        tiers[f"... with >= {v:,} IMDb votes"] = {t for t in A if T[t].get("votes", 0) >= v}

    print(f"Release years {a.from_year}-{a.to_year}")
    print(f"Wikidata US-origin feature films: {len(W)} ({pct(len(W_t), len(W))} have an IMDb id)")
    print("IMDb tiers and how many of them the Wikidata pack covers:")
    for name, s in tiers.items():
        hit = sum(1 for t in s if t in W_t)
        print(f"  {name:32s} {len(s):6d}   in Wikidata pack: {hit:5d} ({pct(hit, len(s))})")
    notable = tiers["... with >= 5,000 IMDb votes"]
    missing = [t for t in notable if t not in W_t]
    # why are they missing: not US origin (Wikidata P495) vs absent
    print(f"  notable films missing from the pack: {len(missing)} (mostly non-US productions released in the US; "
          f"the pack filters on country of origin = US)")

    # ---- field completeness, Wikidata
    meta = {q(r["f"]): r for r in st.rows("filmmeta")}
    dates = {}
    for r in st.rows("filmdates"):
        dates.setdefault(q(r["f"]), []).append(int(r["prec"]))
    items = {}
    for r in st.rows("filmitems"):
        f = q(r["f"])
        if f in W:
            items.setdefault(f, {}).setdefault(r["prop"].rsplit("/", 1)[1], set()).add(q(r["v"]))
    n = len(W)
    def wc(fn):
        return pct(sum(1 for f in W if fn(f)), n)
    print("\nWikidata field completeness (pack films):")
    print(f"  day-precision release date {wc(lambda f: max(dates.get(f, [0])) >= 11)}; director {wc(lambda f: 'P57' in items.get(f, {}))}; "
          f">=5 cast {wc(lambda f: len(items.get(f, {}).get('P161', ())) >= 5)}; distributor {wc(lambda f: 'P750' in items.get(f, {}))}; "
          f"budget {wc(lambda f: meta.get(f, {}).get('costUsd'))}; box office {wc(lambda f: meta.get(f, {}).get('boUsd'))}")
    ppl = {q(r["p"]): r for r in st.rows("people")}
    cast = {p for f in W for p in items.get(f, {}).get("P161", ())}
    known = [p for p in cast if p in ppl]
    print(f"  cast members: {len(cast)}; gender {pct(sum(1 for p in known if ppl[p].get('gender')), len(cast))}; "
          f"full birth date {pct(sum(1 for p in known if ppl[p].get('birth')), len(cast))}")
    spouses = {q(r["p"]) for r in st.rows("spouses")}
    print(f"  cast with a documented spouse: {pct(sum(1 for p in cast if p in spouses), len(cast))}")

    # ---- field completeness, IMDb (same notable set)
    s = notable
    def ic(fn):
        return pct(sum(1 for t in s if fn(T[t])), len(s))
    acts = lambda x: [p for p in x.get("principals", []) if p[2] in ("actor", "actress")]
    print(f"\nIMDb field completeness (>= 5,000 votes, {len(s)} films):")
    print(f"  director {ic(lambda x: x.get('directors'))}; >=5 billed cast {ic(lambda x: len(acts(x)) >= 5)}; "
          f"character names {ic(lambda x: any(p[3] for p in acts(x)))}; release date: year only; "
          f"distributor / budget / box office: none")
    cast_i = {p[1] for t in s for p in acts(T[t])}
    print(f"  cast members: {len(cast_i)}; gender (from actor/actress) 100%; birth year "
          f"{pct(sum(1 for p in cast_i if N.get(p, {}).get('birth')), len(cast_i))}; spouses: none")

    # ---- anchors
    by_title = {}
    for t, x in T.items():
        if x["type"] == "movie" and x["year"] == 1990:
            by_title.setdefault(x["title"].lower(), []).append(t)
    print("\nTop 25 of 1990 (anchors):")
    rows = []
    for title in TOP_1990:
        ts = sorted(by_title.get(title.lower(), []), key=lambda t: -T[t].get("votes", 0))
        t = ts[0] if ts else None
        f = W_t.get(t)
        rows.append((title, bool(t), bool(f), bool(f and meta.get(f, {}).get("boUsd")),
                     bool(f and max(dates.get(f, [0])) >= 11), bool(f and 'P750' in items.get(f, {}))))
    for r in rows:
        print(f"  {r[0][:32]:32s} imdb={'Y' if r[1] else '-'} wikidata={'Y' if r[2] else '-'} "
              f"wd_box_office={'Y' if r[3] else '-'} wd_day_date={'Y' if r[4] else '-'} wd_distributor={'Y' if r[5] else '-'}")
    print(f"  IMDb {sum(r[1] for r in rows)}/25; Wikidata {sum(r[2] for r in rows)}/25; "
          f"box office {sum(r[3] for r in rows)}/25; day date {sum(r[4] for r in rows)}/25; distributor {sum(r[5] for r in rows)}/25")


if __name__ == "__main__":
    main()
