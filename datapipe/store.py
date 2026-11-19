"""Persistent local store for raw Wikidata records (gitignored: data/raw/).

Every fetched entity and every bulk-query result is kept, so later runs (new
year ranges, new start-year snapshots) only fetch what is missing.

Tables
  entity(qid, kind, json, source, fetched_at)   film entities (statement order kept)
  rows(name, key, qid, json)                     bulk SPARQL rows, keyed per subject id
  seen(name, qid, fetched_at)                    which ids a bulk stage has already covered
  film_year(qid, year)                           film lists per release year
"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data" / "raw" / "wikidata" / "store.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS entity (qid TEXT PRIMARY KEY, kind TEXT, json TEXT, source TEXT, fetched_at REAL);
CREATE TABLE IF NOT EXISTS rows (name TEXT, key TEXT, qid TEXT, json TEXT, PRIMARY KEY (name, key));
CREATE INDEX IF NOT EXISTS rows_by_qid ON rows (name, qid);
CREATE TABLE IF NOT EXISTS seen (name TEXT, qid TEXT, fetched_at REAL, PRIMARY KEY (name, qid));
CREATE TABLE IF NOT EXISTS film_year (qid TEXT PRIMARY KEY, year INTEGER);
CREATE TABLE IF NOT EXISTS years_done (year INTEGER PRIMARY KEY);
"""


class Store:
    def __init__(self, path: Path = DEFAULT):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.executescript(SCHEMA)

    # ---- entities ----
    def has_entity(self, qid: str) -> bool:
        return self.db.execute("SELECT 1 FROM entity WHERE qid=?", (qid,)).fetchone() is not None

    def put_entity(self, qid: str, kind: str, data: dict, source: str) -> None:
        self.db.execute("INSERT OR REPLACE INTO entity VALUES (?,?,?,?,?)",
                        (qid, kind, json.dumps(data), source, time.time()))

    def entities(self, kind: str):
        for qid, js, src in self.db.execute("SELECT qid, json, source FROM entity WHERE kind=? ORDER BY qid", (kind,)):
            yield qid, json.loads(js), src

    def entity_source(self, qid: str) -> str | None:
        r = self.db.execute("SELECT source FROM entity WHERE qid=?", (qid,)).fetchone()
        return r[0] if r else None

    # ---- bulk rows ----
    def put_rows(self, name: str, subject_var: str, rows: list) -> None:
        self.db.executemany("INSERT OR IGNORE INTO rows VALUES (?,?,?,?)",
                            [(name, json.dumps(r, sort_keys=True), r.get(subject_var, "").rsplit("/", 1)[-1],
                              json.dumps(r)) for r in rows])

    def rows(self, name: str) -> list:
        return [json.loads(js) for (js,) in self.db.execute("SELECT json FROM rows WHERE name=? ORDER BY key", (name,))]

    def mark_seen(self, name: str, qids) -> None:
        now = time.time()
        self.db.executemany("INSERT OR IGNORE INTO seen VALUES (?,?,?)", [(name, q, now) for q in qids])

    def unseen(self, name: str, qids) -> list:
        have = {q for (q,) in self.db.execute("SELECT qid FROM seen WHERE name=?", (name,))}
        return [q for q in qids if q not in have]

    # ---- film lists ----
    def put_films(self, year_of: dict, years) -> None:
        self.db.executemany("INSERT OR REPLACE INTO film_year VALUES (?,?)", list(year_of.items()))
        self.db.executemany("INSERT OR IGNORE INTO years_done VALUES (?)", [(y,) for y in years])

    def years_done(self) -> set:
        return {y for (y,) in self.db.execute("SELECT year FROM years_done")}

    def films(self, y0: int, y1: int) -> dict:
        return dict(self.db.execute("SELECT qid, year FROM film_year WHERE year BETWEEN ? AND ?", (y0, y1)))

    def commit(self):
        self.db.commit()


def import_legacy(store: Store, raw: Path) -> dict:
    """Bring the v1 file cache (data/raw/wikidata/*.json, films/*.json) into the store (once)."""
    n = {"entities": 0, "rows": 0}
    if store.db.execute("SELECT 1 FROM seen WHERE name='_legacy_import'").fetchone():
        return n
    films_dir = raw / "films"
    if films_dir.exists():
        for f in sorted(films_dir.glob("*.json")):
            if store.has_entity(f.stem):
                continue
            ent = json.loads(f.read_text())
            src = "sparql-bulk" if str(ent.get("cast_order", "")).startswith("unordered") else "entitydata"
            store.put_entity(f.stem, "film", ent, src)
            n["entities"] += 1
    subject = {"people": "p", "spouses": "p", "honours": "p", "labels": "x", "filmitems": "f", "filmmeta": "f",
               "filmdates": "f", "imdbids": "x", "exclude": "f"}
    for f in sorted(raw.glob("q_*.json")):
        prefix = f.stem[2:].split("_")[0]           # q_<prefix>_<years or hash>.json
        rows = json.loads(f.read_text())
        if prefix == "films":
            y0, y1 = (int(x) for x in f.stem.split("_")[-2:])
            store.put_films({r["f"].rsplit("/", 1)[1]: int(r["y"]) for r in rows}, range(y0, y1 + 1))
        elif prefix in subject:
            store.put_rows(prefix, subject[prefix], rows)
            n["rows"] += len(rows)
    for f in sorted(raw.glob("seen_*.json")):
        store.mark_seen(f.stem[5:], json.loads(f.read_text()))
    store.mark_seen("_legacy_import", ["done"])
    store.commit()
    return n
