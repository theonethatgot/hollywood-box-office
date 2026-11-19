"""OPTIONAL local enrichment: billing order from IMDb's non-commercial datasets.

    python datapipe/imdb_billing.py --stage all

IMDb's datasets are licensed for personal, non-commercial use and may not be
republished. This script therefore writes ONLY to gitignored locations:
  data/raw/imdb/            the downloaded dataset
  data/local/imdb_billing.json   {film QID: [cast QIDs in IMDb billing order]}
The committed pack keeps Wikidata statement order; hsim/world/historical.py
applies the local billing file when it exists.

The Wikidata ↔ IMDb id mapping (property P345) is itself CC0 Wikidata data.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_wikidata import UA, Client, Ingest, q  # noqa: E402
from store import Store  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
IMDB_RAW = ROOT / "data" / "raw" / "imdb"
LOCAL = ROOT / "data" / "local"
PRINCIPALS = "https://datasets.imdbws.com/title.principals.tsv.gz"

def stage_ids(y0: int, y1: int):
    """Wikidata -> IMDb id mapping (CC0) for the range's films and their cast."""
    store = Store()
    ing = Ingest(store, Client())
    films = sorted(ing.film_list(y0, y1))
    people, _ = ing.people_of(films)
    ing.bulk("imdbids", films + people)


def stage_download():
    IMDB_RAW.mkdir(parents=True, exist_ok=True)
    out = IMDB_RAW / "title.principals.tsv.gz"
    if out.exists():
        print("principals already downloaded")
        return
    req = urllib.request.Request(PRINCIPALS, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=600) as r, open(out.with_suffix(".part"), "wb") as fh:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            fh.write(b)
    out.with_suffix(".part").rename(out)
    print(f"downloaded {out.stat().st_size / 1e6:.0f} MB")


def stage_build():
    to_q = {r["imdb"]: q(r["x"]) for r in Store().rows("imdbids")}
    film_t = {t: qq for t, qq in to_q.items() if t.startswith("tt")}
    order = {}
    t0 = time.time()
    with gzip.open(IMDB_RAW / "title.principals.tsv.gz", "rt", encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            t, ordering, n, cat = line.split("\t", 4)[:4]
            if t in film_t and cat in ("actor", "actress", "self"):
                order.setdefault(film_t[t], []).append((int(ordering), n))
    billing = {}
    for fq, rows in order.items():
        qs = [to_q[n] for _, n in sorted(rows) if n in to_q]
        if qs:
            billing[fq] = qs
    LOCAL.mkdir(parents=True, exist_ok=True)
    (LOCAL / "imdb_billing.json").write_text(json.dumps(billing))
    print(f"billing order for {len(billing)} films in {time.time() - t0:.0f}s -> data/local/imdb_billing.json "
          f"(local only, never commit)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["ids", "download", "build", "all"], default="all")
    ap.add_argument("--from-year", type=int, default=1975)
    ap.add_argument("--to-year", type=int, default=1989)
    a = ap.parse_args()
    if a.stage in ("ids", "all"):
        stage_ids(a.from_year, a.to_year)
    if a.stage in ("download", "all"):
        stage_download()
    if a.stage in ("build", "all"):
        stage_build()


if __name__ == "__main__":
    main()
