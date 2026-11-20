"""LOCAL-ONLY: index IMDb's non-commercial bulk datasets for a year range.

    python datapipe/imdb_index.py --from-year 1985 --to-year 1992

IMDb's datasets are for personal, non-commercial use and may not be republished.
Everything this script reads lives in data/raw/imdb/ and everything it writes goes
to data/local/ (both gitignored). Never commit its output.

One streaming pass per file, filtered as it goes, with timings per stage:
  title.basics   -> titles of type movie / tvMovie / video in the range
  title.ratings  -> vote counts (a notability signal)
  title.crew     -> directors and writers
  title.principals -> cast and crew with billing order, category and character
  name.basics    -> people in those titles: name, birth/death year, professions
  title.akas     -> per-title regions (US presence) and US titles
Output: data/local/imdb_<y0>_<y1>.json and timings in data/raw/imdb/index_stats.json.
"""
from __future__ import annotations

import argparse
import gzip
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "imdb"
LOCAL = ROOT / "data" / "local"
TYPES = {"movie", "tvMovie", "video"}


def rows(name: str):
    with gzip.open(RAW / f"{name}.tsv.gz", "rt", encoding="utf-8") as fh:
        header = next(fh).rstrip("\n").split("\t")
        for line in fh:
            yield header, line.rstrip("\n").split("\t")


def nul(x):
    return None if x == "\\N" else x


def build(y0: int, y1: int) -> dict:
    stats, t_all = {}, time.time()

    t = time.time()
    titles = {}
    for _, r in rows("title.basics"):
        tconst, ttype, primary, original, adult, start, end, runtime, genres = r
        if ttype not in TYPES or start == "\\N" or not (y0 <= int(start) <= y1):
            continue
        titles[tconst] = {"type": ttype, "title": primary, "original": original, "adult": adult == "1",
                          "year": int(start), "runtime": int(runtime) if runtime.isdigit() else None,
                          "genres": [] if genres == "\\N" else genres.split(",")}
    stats["title.basics"] = round(time.time() - t, 1)

    t = time.time()
    for _, (tconst, rating, votes) in rows("title.ratings"):
        if tconst in titles:
            titles[tconst]["rating"], titles[tconst]["votes"] = float(rating), int(votes)
    stats["title.ratings"] = round(time.time() - t, 1)

    t = time.time()
    for _, (tconst, directors, writers) in rows("title.crew"):
        if tconst in titles:
            titles[tconst]["directors"] = [] if directors == "\\N" else directors.split(",")
            titles[tconst]["writers"] = [] if writers == "\\N" else writers.split(",")
    stats["title.crew"] = round(time.time() - t, 1)

    t = time.time()
    people = set()
    for _, r in rows("title.principals"):
        tconst = r[0]
        if tconst not in titles:
            continue
        _, ordering, nconst, category, job, characters = r
        chars = json.loads(characters) if characters != "\\N" else []
        titles[tconst].setdefault("principals", []).append([int(ordering), nconst, category, chars])
        people.add(nconst)
    for x in titles.values():
        people.update(x.get("directors", []))
    stats["title.principals"] = round(time.time() - t, 1)

    t = time.time()
    names = {}
    for _, r in rows("name.basics"):
        if r[0] in people:
            nconst, name, birth, death, prof, known = r
            names[nconst] = {"name": name, "birth": nul(birth), "death": nul(death),
                             "professions": [] if prof == "\\N" else prof.split(",")}
    stats["name.basics"] = round(time.time() - t, 1)

    t = time.time()
    for _, r in rows("title.akas"):
        tid = r[0]
        if tid not in titles:
            continue
        region = r[3]
        x = titles[tid]
        if region != "\\N":
            x.setdefault("regions", [])
            if region not in x["regions"]:
                x["regions"].append(region)
        if region == "US" and "us_title" not in x:
            x["us_title"] = r[2]
    stats["title.akas"] = round(time.time() - t, 1)

    stats["total"] = round(time.time() - t_all, 1)
    stats["titles"], stats["people"] = len(titles), len(names)
    return {"range": [y0, y1], "titles": titles, "people": names, "stats": stats}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-year", type=int, default=1985)
    ap.add_argument("--to-year", type=int, default=1992)
    a = ap.parse_args()
    out = build(a.from_year, a.to_year)
    LOCAL.mkdir(parents=True, exist_ok=True)
    path = LOCAL / f"imdb_{a.from_year}_{a.to_year}.json"
    path.write_text(json.dumps(out))
    (RAW / "index_stats.json").write_text(json.dumps(out["stats"], indent=1))
    print(json.dumps(out["stats"], indent=1))
    print(f"-> {path} (local only, never commit)")


if __name__ == "__main__":
    main()
