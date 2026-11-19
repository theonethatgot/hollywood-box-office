"""Fast, incremental Wikidata ingestion (v2) into the persistent store.

    python datapipe/fetch_wikidata.py --from-year 1975 --to-year 1984
    python datapipe/fetch_wikidata.py --from-year 1985 --to-year 1989 --statement-order

Design (see docs/INGESTION.md for measurements)
- Bulk SPARQL with VALUES lists does almost all the work: ~300 films' full facts
  or ~1,000 people per request, typically under a second each.
- Adaptive pacing: a minimum interval between queries that doubles on HTTP 429
  (honouring Retry-After) and relaxes on success. Timeouts split the chunk.
- Optional statement order for cast lists (approximate billing) via
  Special:EntityData with a small worker pool. Skip it if you build the local
  IMDb billing file instead (datapipe/imdb_billing.py).
- Everything lands in data/raw/wikidata/store.sqlite. Every stage skips ids it
  has already covered, so new ranges and reruns only fetch what is missing.
"""
from __future__ import annotations

import argparse
import json
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from store import Store, import_legacy  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "wikidata"
UA = "hsim-datapipe/0.2 (research prototype)"
SPARQL = "https://query.wikidata.org/sparql"
ENTITY = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"


def q(uri: str) -> str:
    return uri.rsplit("/", 1)[1]


class QueryTooHeavy(Exception):
    pass


# ------------------------------------------------------------------ client ---
class Client:
    """HTTP client with per-host adaptive pacing, Retry-After, and statistics."""

    def __init__(self, min_interval: float = 0.5, max_interval: float = 60.0, host_min: dict | None = None):
        self.min_interval, self.max_interval = min_interval, max_interval
        self.host_min = host_min or {}          # per-host minimum interval overrides
        self.interval: dict = {}
        self.next_ok: dict = {}
        self.lock = threading.Lock()
        self.stats: dict = {}

    def stat(self, stage, key, n=1.0):
        with self.lock:
            st = self.stats.setdefault(stage, {"requests": 0, "ok": 0, "http_429": 0, "http_5xx": 0, "timeouts": 0,
                                                "retries": 0, "split_chunks": 0, "seconds_waiting": 0.0,
                                                "seconds_in_requests": 0.0, "items": 0})
            st[key] += n

    def _pace(self, host, stage):
        with self.lock:
            now = time.time()
            start = max(now, self.next_ok.get(host, 0.0))
            self.next_ok[host] = start + self.interval.get(host, self.host_min.get(host, self.min_interval))
        if start > now:
            self.stat(stage, "seconds_waiting", start - now)
            time.sleep(start - now)

    def _adjust(self, host, ok: bool, retry_after: float | None = None):
        with self.lock:
            floor = self.host_min.get(host, self.min_interval)
            cur = self.interval.get(host, floor)
            if ok:
                self.interval[host] = max(floor, cur * 0.9)
            else:
                self.interval[host] = min(self.max_interval, max(cur * 2, retry_after or 0.0))
                self.next_ok[host] = time.time() + max(self.interval[host], retry_after or 0.0)

    def request(self, url: str, stage: str, data: bytes | None = None, tries: int = 8, timeout: float = 90):
        host = urllib.parse.urlparse(url).netloc
        for i in range(tries):
            self._pace(host, stage)
            self.stat(stage, "requests")
            if i:
                self.stat(stage, "retries")
            t0 = time.time()
            try:
                headers = {"User-Agent": UA, "Accept": "application/sparql-results+json, application/json"}
                if data:
                    headers["Content-Type"] = "application/x-www-form-urlencoded"
                req = urllib.request.Request(url, data=data, headers=headers)
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    body = json.loads(r.read().decode())
                self.stat(stage, "ok")
                self.stat(stage, "seconds_in_requests", time.time() - t0)
                self._adjust(host, True)
                return body
            except urllib.error.HTTPError as e:
                self.stat(stage, "seconds_in_requests", time.time() - t0)
                ra = float(e.headers.get("retry-after") or 0) or None
                if e.code == 429:
                    self.stat(stage, "http_429")
                    self._adjust(host, False, ra)
                elif e.code >= 500:
                    self.stat(stage, "http_5xx")
                    if data is not None and e.code in (500, 502, 504):
                        raise QueryTooHeavy(e.code) from e        # caller splits the chunk
                    self._adjust(host, False, ra)
                else:
                    raise
            except TimeoutError as e:
                self.stat(stage, "seconds_in_requests", time.time() - t0)
                self.stat(stage, "timeouts")
                if data is not None:
                    raise QueryTooHeavy("timeout") from e
                self._adjust(host, False)
            except (urllib.error.URLError, json.JSONDecodeError, ConnectionError):
                self.stat(stage, "seconds_in_requests", time.time() - t0)
                self.stat(stage, "timeouts")
                self._adjust(host, False)
        raise RuntimeError(f"giving up after {tries} tries: {url[:120]}")


# ----------------------------------------------------------------- queries ---
FILMS = """SELECT ?f (MIN(YEAR(?d)) AS ?y) WHERE {{
  ?f wdt:P31 wd:Q11424; wdt:P495 wd:Q30; wdt:P577 ?d.
  FILTER(YEAR(?d) >= {y0} && YEAR(?d) <= {y1}) }} GROUP BY ?f"""

EXCLUDE = """SELECT DISTINCT ?f WHERE {{
  ?f wdt:P31 wd:Q11424; wdt:P495 wd:Q30; wdt:P577 ?d.
  FILTER(YEAR(?d) >= {y0} && YEAR(?d) <= {y1})
  {{ ?f wdt:P31 ?c. VALUES ?c {{ wd:Q24862 wd:Q506240 wd:Q93204 wd:Q21191270 wd:Q1261214 }} }}
  UNION {{ ?f wdt:P2047 ?dur. FILTER(?dur < 60) }}
}}"""

BULK = {   # name: (subject variable, query template, chunk size)
    "filmitems": ("f", """SELECT ?f ?prop ?v WHERE {{ VALUES ?f {{ {values} }}
  VALUES ?prop {{ wdt:P136 wdt:P750 wdt:P272 wdt:P155 wdt:P179 wdt:P57 wdt:P161 }}
  ?f ?prop ?v. FILTER(ISIRI(?v)) }}""", 300),
    "filmmeta": ("f", """SELECT ?f ?label ?desc ?sl (MAX(?cost) AS ?costUsd) (MAX(?bo) AS ?boUsd) WHERE {{
  VALUES ?f {{ {values} }}
  OPTIONAL {{ ?f rdfs:label ?label FILTER(LANG(?label) = "en") }}
  OPTIONAL {{ ?f schema:description ?desc FILTER(LANG(?desc) = "en") }}
  OPTIONAL {{ ?f wikibase:sitelinks ?sl }}
  OPTIONAL {{ ?f p:P2130/psv:P2130 [ wikibase:quantityAmount ?cost; wikibase:quantityUnit wd:Q4917 ] }}
  OPTIONAL {{ ?f p:P2142/psv:P2142 [ wikibase:quantityAmount ?bo; wikibase:quantityUnit wd:Q4917 ] }}
}} GROUP BY ?f ?label ?desc ?sl""", 300),
    "filmdates": ("f", """SELECT ?f ?t ?prec WHERE {{ VALUES ?f {{ {values} }}
  ?f p:P577/psv:P577 [ wikibase:timeValue ?t; wikibase:timePrecision ?prec ]. }}""", 600),
    "people": ("p", """SELECT ?p ?label ?gender ?birth ?death ?manner ?sl ?desc WHERE {{
  VALUES ?p {{ {values} }}
  ?p wdt:P569 ?birth.
  OPTIONAL {{ ?p wdt:P21 ?gender }} OPTIONAL {{ ?p wdt:P570 ?death }} OPTIONAL {{ ?p wdt:P1196 ?manner }}
  OPTIONAL {{ ?p wikibase:sitelinks ?sl }}
  OPTIONAL {{ ?p rdfs:label ?label FILTER(LANG(?label) = "en") }}
  OPTIONAL {{ ?p schema:description ?desc FILTER(LANG(?desc) = "en") }} }}""", 1000),
    "spouses": ("p", """SELECT ?p ?sp ?start ?end WHERE {{ VALUES ?p {{ {values} }}
  ?p p:P26 ?st. ?st ps:P26 ?sp.
  OPTIONAL {{ ?st pq:P580 ?start }} OPTIONAL {{ ?st pq:P582 ?end }} }}""", 1500),
    "honours": ("p", """SELECT ?p ?kind ?award ?awardLabel ?date ?work WHERE {{
  VALUES ?p {{ {values} }}
  VALUES (?prop ?ps ?kind) {{ (p:P1411 ps:P1411 "nominated") (p:P166 ps:P166 "won") }}
  ?p ?prop ?st. ?st ?ps ?award.
  ?award rdfs:label ?awardLabel FILTER(LANG(?awardLabel) = "en")
  FILTER(CONTAINS(?awardLabel, "Academy Award") || CONTAINS(?awardLabel, "Golden Globe") ||
         CONTAINS(?awardLabel, "BAFTA") || CONTAINS(?awardLabel, "Emmy") || CONTAINS(?awardLabel, "Tony Award"))
  OPTIONAL {{ ?st pq:P585 ?date }} OPTIONAL {{ ?st pq:P1686 ?work }} }}""", 1000),
    "labels": ("x", """SELECT ?x ?label WHERE {{ VALUES ?x {{ {values} }}
  ?x rdfs:label ?label FILTER(LANG(?label) = "en") }}""", 1500),
    "imdbids": ("x", """SELECT ?x ?imdb WHERE {{ VALUES ?x {{ {values} }} ?x wdt:P345 ?imdb. }}""", 2000),
}


# ------------------------------------------------------------------ stages ---
class Ingest:
    def __init__(self, store: Store, client: Client):
        self.store, self.client = store, client

    def sparql(self, query: str, stage: str) -> list:
        body = urllib.parse.urlencode({"query": query, "format": "json"}).encode()
        data = self.client.request(SPARQL, stage, data=body)
        return [{k: v["value"] for k, v in b.items()} for b in data["results"]["bindings"]]

    def bulk(self, name: str, ids) -> None:
        var, template, size = BULK[name]
        ids = sorted(set(ids))
        todo = self.store.unseen(name, ids)
        print(f"  {name}: {len(todo)} of {len(ids)} ids missing", flush=True)
        stack = [todo[k:k + size] for k in range(0, len(todo), size)][::-1]
        while stack:
            chunk = stack.pop()
            try:
                rows = self.sparql(template.format(values=" ".join(f"wd:{i}" for i in chunk)), name)
            except QueryTooHeavy:
                if len(chunk) <= 25:
                    raise
                self.client.stat(name, "split_chunks")
                half = len(chunk) // 2
                stack += [chunk[half:], chunk[:half]]
                continue
            self.store.put_rows(name, var, rows)
            self.store.mark_seen(name, chunk)
            self.store.commit()
            self.client.stat(name, "items", len(chunk))

    def film_list(self, y0: int, y1: int) -> dict:
        done = self.store.years_done()
        missing = [y for y in range(y0, y1 + 1) if y not in done]
        for k in range(0, len(missing), 5):
            a, b = missing[k], missing[min(k + 4, len(missing) - 1)]
            rows = self.sparql(FILMS.format(y0=a, y1=b), "film_list")
            excluded = self.sparql(EXCLUDE.format(y0=a, y1=b), "film_list")
            self.store.put_rows("exclude", "f", excluded)
            self.store.put_films({q(r["f"]): int(r["y"]) for r in rows}, range(a, b + 1))
            self.store.commit()
        films = self.store.films(y0, y1)
        excl = {q(r["f"]) for r in self.store.rows("exclude")}
        return {f: y for f, y in films.items() if f not in excl}

    def statement_order(self, films: list, workers: int) -> None:
        todo = [f for f in films if self.store.entity_source(f) != "entitydata"]
        print(f"  statement order: {len(todo)} films need entity data ({workers} workers)", flush=True)
        keep = ("P577", "P136", "P161", "P57", "P750", "P272", "P2130", "P2142", "P155", "P179")
        lock = threading.Lock()

        def one(f):
            data = self.client.request(ENTITY.format(f), "statement_order")
            ents = data.get("entities", {})
            ent = ents.get(f) or next(iter(ents.values()), None)
            if ent:
                slim = {"id": f, "labels": {"en": ent.get("labels", {}).get("en", {})},
                        "descriptions": {"en": ent.get("descriptions", {}).get("en", {})},
                        "sitelinks": {k: 1 for k in ent.get("sitelinks", {})},
                        "claims": {p: ent["claims"][p] for p in keep if p in ent.get("claims", {})}}
                with lock:
                    self.store.put_entity(f, "film", slim, "entitydata")
            self.client.stat("statement_order", "items")

        t0 = time.time()
        with ThreadPoolExecutor(workers) as ex:
            for i, _ in enumerate(ex.map(one, todo), 1):
                if i % 250 == 0:
                    with lock:
                        self.store.commit()
                    print(f"    {i}/{len(todo)} ({i / (time.time() - t0) * 60:.0f}/min)", flush=True)
        self.store.commit()

    def people_of(self, films) -> tuple:
        fs, cast, refs = set(films), set(), set()
        for r in self.store.rows("filmitems"):
            if q(r["f"]) not in fs:
                continue
            prop, v = r["prop"].rsplit("/", 1)[1], q(r["v"])
            (cast if prop in ("P161", "P57") else refs).add(v)
        return sorted(cast), sorted(refs)


def run(y0: int, y1: int, statement_order: bool, workers: int, min_interval: float,
        entity_interval: float = 0.1) -> dict:
    store = Store()
    imported = import_legacy(store, RAW)
    if imported["entities"] or imported["rows"]:
        print(f"imported legacy cache: {imported}", flush=True)
    client = Client(min_interval=min_interval, host_min={"www.wikidata.org": entity_interval})
    ing = Ingest(store, client)
    t0 = time.time()
    films = ing.film_list(y0, y1)
    ids = sorted(films)
    print(f"films {y0}-{y1}: {len(ids)}", flush=True)
    for name in ("filmitems", "filmmeta", "filmdates"):
        ing.bulk(name, ids)
    people, refs = ing.people_of(ids)
    print(f"people: {len(people)}; referenced items: {len(refs)}", flush=True)
    for name in ("people", "spouses", "honours"):
        ing.bulk(name, people)
    spouses = {q(r["sp"]) for r in store.rows("spouses")}
    ing.bulk("labels", set(refs) | spouses)
    if statement_order:
        ing.statement_order(ids, workers)
    summary = {"years": [y0, y1], "films": len(ids), "people": len(people), "seconds": round(time.time() - t0, 1),
               "stages": {k: {kk: round(vv, 2) for kk, vv in v.items()} for k, v in client.stats.items()}}
    (RAW / "last_run_stats.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2), flush=True)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-year", type=int, default=1975)
    ap.add_argument("--to-year", type=int, default=1984)
    ap.add_argument("--statement-order", action="store_true",
                    help="also fetch per-film entities for cast statement order (IMDb billing is the faster alternative)")
    ap.add_argument("--workers", type=int, default=4, help="concurrent EntityData requests (keep small)")
    ap.add_argument("--min-interval", type=float, default=0.5, help="minimum seconds between SPARQL requests")
    ap.add_argument("--entity-interval", type=float, default=0.1,
                    help="minimum seconds between Special:EntityData requests across all workers (0.1 = max 600/min)")
    a = ap.parse_args()
    run(a.from_year, a.to_year, a.statement_order, a.workers, a.min_interval, a.entity_interval)


if __name__ == "__main__":
    main()
