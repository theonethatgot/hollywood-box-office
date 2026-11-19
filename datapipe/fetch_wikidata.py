"""Fetch US films and their people from Wikidata (CC0) into a local raw cache.

    python datapipe/fetch_wikidata.py --from-year 1975 --to-year 1984

Designed to be polite under strict rate limits:
  1. One SPARQL query lists film items (instance of film, country of origin USA).
  2. People facts, spouses, honours and labels come from a handful of bulk SPARQL
     queries (the query service may allow ~1 request per minute).
  3. Film entities come from Special:EntityData one by one (~1.5/s), because the
     statement order of cast members approximates billing order.
Raw JSON goes to data/raw/wikidata/ (gitignored); datapipe/build_pack.py turns
it into the committable data pack. Every step resumes from its cache.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "wikidata"
UA = "hsim-datapipe/0.1 (research prototype)"
SPARQL = "https://query.wikidata.org/sparql"
ENTITY = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"


def _request(url: str, data: bytes | None = None, tries: int = 8) -> dict:
    for i in range(tries):
        try:
            headers = {"User-Agent": UA, "Accept": "application/sparql-results+json, application/json"}
            if data:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            wait = int(e.headers.get("retry-after") or 0) + 5 if e.code == 429 else 2 ** i * 2
            if e.code == 429 and "query.wikidata" in url:
                wait = max(wait, 65)
            print(f"  HTTP {e.code}; retry {i+1}/{tries} in {wait}s", flush=True)
            time.sleep(wait)
        except Exception as e:   # noqa: BLE001
            print(f"  error {e}; retry {i+1}/{tries}", flush=True)
            time.sleep(2 ** i * 2)
    raise RuntimeError(f"failed: {url[:160]}")


def sparql(query: str, cache: Path) -> list:
    if cache.exists():
        return json.loads(cache.read_text())
    data = _request(SPARQL, data=urllib.parse.urlencode({"query": query, "format": "json"}).encode())
    rows = [{k: v["value"] for k, v in b.items()} for b in data["results"]["bindings"]]
    cache.write_text(json.dumps(rows))
    print(f"  {cache.name}: {len(rows)} rows", flush=True)
    time.sleep(61)       # respect ~1 query/minute
    return rows


def q(uri: str) -> str:
    return uri.rsplit("/", 1)[1]


FILMS = """SELECT ?f (MIN(YEAR(?d)) AS ?y) WHERE {{
  ?f wdt:P31 wd:Q11424; wdt:P495 wd:Q30; wdt:P577 ?d.
  FILTER(YEAR(?d) >= {y0} && YEAR(?d) <= {y1}) }} GROUP BY ?f"""

PEOPLE = """SELECT ?p ?label ?gender ?birth ?death ?manner ?sl ?desc WHERE {{
  VALUES ?p {{ {values} }}
  ?p wdt:P569 ?birth.
  OPTIONAL {{ ?p wdt:P21 ?gender }} OPTIONAL {{ ?p wdt:P570 ?death }} OPTIONAL {{ ?p wdt:P1196 ?manner }}
  OPTIONAL {{ ?p wikibase:sitelinks ?sl }}
  OPTIONAL {{ ?p rdfs:label ?label FILTER(LANG(?label) = "en") }}
  OPTIONAL {{ ?p schema:description ?desc FILTER(LANG(?desc) = "en") }}
}}"""

SPOUSES = """SELECT ?p ?sp ?start ?end WHERE {{
  VALUES ?p {{ {values} }}
  ?p p:P26 ?st. ?st ps:P26 ?sp.
  OPTIONAL {{ ?st pq:P580 ?start }} OPTIONAL {{ ?st pq:P582 ?end }}
}}"""

HONOURS = """SELECT ?p ?kind ?award ?awardLabel ?date ?work WHERE {{
  VALUES ?p {{ {values} }}
  VALUES (?prop ?ps ?kind) {{ (p:P1411 ps:P1411 "nominated") (p:P166 ps:P166 "won") }}
  ?p ?prop ?st. ?st ?ps ?award.
  ?award rdfs:label ?awardLabel FILTER(LANG(?awardLabel) = "en")
  FILTER(CONTAINS(?awardLabel, "Academy Award") || CONTAINS(?awardLabel, "Golden Globe") ||
         CONTAINS(?awardLabel, "BAFTA") || CONTAINS(?awardLabel, "Emmy") || CONTAINS(?awardLabel, "Tony Award"))
  OPTIONAL {{ ?st pq:P585 ?date }} OPTIONAL {{ ?st pq:P1686 ?work }}
}}"""

EXCLUDE = """SELECT DISTINCT ?f WHERE {{
  ?f wdt:P31 wd:Q11424; wdt:P495 wd:Q30; wdt:P577 ?d.
  FILTER(YEAR(?d) >= {y0} && YEAR(?d) <= {y1})
  {{ ?f wdt:P31 ?c. VALUES ?c {{ wd:Q24862 wd:Q506240 wd:Q93204 wd:Q21191270 wd:Q1261214 }} }}
  UNION {{ ?f wdt:P2047 ?dur. FILTER(?dur < 60) }}
}}"""

LABELS = """SELECT ?x ?label WHERE {{
  VALUES ?x {{ {values} }}
  ?x rdfs:label ?label FILTER(LANG(?label) = "en")
}}"""


FILM_ITEMS = """SELECT ?f ?prop ?v WHERE {{
  VALUES ?f {{ {values} }}
  VALUES ?prop {{ wdt:P136 wdt:P750 wdt:P272 wdt:P155 wdt:P179 wdt:P57 wdt:P161 }}
  ?f ?prop ?v. FILTER(ISIRI(?v))
}}"""

FILM_META = """SELECT ?f ?label ?desc ?sl (MIN(?d) AS ?date) (MAX(?cost) AS ?costUsd) (MAX(?bo) AS ?boUsd) WHERE {{
  VALUES ?f {{ {values} }}
  ?f wdt:P577 ?d.
  OPTIONAL {{ ?f rdfs:label ?label FILTER(LANG(?label) = "en") }}
  OPTIONAL {{ ?f schema:description ?desc FILTER(LANG(?desc) = "en") }}
  OPTIONAL {{ ?f wikibase:sitelinks ?sl }}
  OPTIONAL {{ ?f p:P2130/psv:P2130 [ wikibase:quantityAmount ?cost; wikibase:quantityUnit wd:Q4917 ] }}
  OPTIONAL {{ ?f p:P2142/psv:P2142 [ wikibase:quantityAmount ?bo; wikibase:quantityUnit wd:Q4917 ] }}
}} GROUP BY ?f ?label ?desc ?sl"""


FILM_DATES = """SELECT ?f ?t ?prec WHERE {{
  VALUES ?f {{ {values} }}
  ?f p:P577/psv:P577 [ wikibase:timeValue ?t; wikibase:timePrecision ?prec ].
}}"""


def bulk_films(missing: list, out: Path) -> None:
    """Facts for films not fetched as entities, via bulk SPARQL. Cast order is lost
    (marked 'unordered'); build_pack.py applies a hindsight-free ordering."""
    chunked(FILM_ITEMS, missing, "filmitems", 350)
    chunked(FILM_META, missing, "filmmeta", 350)
    chunked(FILM_DATES, missing, "filmdates", 700)
    props = {"http://www.wikidata.org/prop/direct/" + k: k for k in ("P136", "P750", "P272", "P155", "P179", "P57", "P161")}
    items, meta = {}, {}
    for path in RAW.glob("q_filmitems_*.json"):
        for r in json.loads(path.read_text()):
            items.setdefault(q(r["f"]), {}).setdefault(props[r["prop"]], []).append(q(r["v"]))
    for path in RAW.glob("q_filmmeta_*.json"):
        for r in json.loads(path.read_text()):
            meta[q(r["f"])] = r
    for f in missing:
        if (out / f"{f}.json").exists() or f not in meta:
            continue
        m = meta[f]
        claims = {k: [{"mainsnak": {"datavalue": {"value": {"id": v}}}} for v in sorted(set(vs))]
                  for k, vs in items.get(f, {}).items()}
        claims["P577"] = [{"mainsnak": {"datavalue": {"value": {"time": "+" + m["date"][:10] + "T00:00:00Z", "precision": 11}}}}]
        for key, prop in (("costUsd", "P2130"), ("boUsd", "P2142")):
            if m.get(key):
                claims[prop] = [{"mainsnak": {"datavalue": {"value": {"amount": m[key], "unit": "http://www.wikidata.org/entity/Q4917"}}}}]
        slim = {"id": f, "labels": {"en": {"value": m.get("label", "")}}, "descriptions": {"en": {"value": m.get("desc", "")}},
                "sitelinks": {f"s{i}": 1 for i in range(int(float(m.get("sl", 0))))}, "claims": claims,
                "cast_order": "unordered"}
        (out / f"{f}.json").write_text(json.dumps(slim))


def chunked(template: str, ids: list, name: str, size: int) -> None:
    """Query ids in chunks; remembers which ids were already queried so reruns
    (or a parallel early pass) only fetch what is missing."""
    import hashlib
    seen_path = RAW / f"seen_{name}.json"
    seen = set(json.loads(seen_path.read_text())) if seen_path.exists() else set()
    todo = [i for i in ids if i not in seen]
    print(f"{name}: {len(todo)} of {len(ids)} ids to query", flush=True)
    for k in range(0, len(todo), size):
        chunk = todo[k:k + size]
        vals = " ".join(f"wd:{i}" for i in chunk)
        tag = hashlib.sha1(vals.encode()).hexdigest()[:10]
        sparql(template.format(values=vals), RAW / f"q_{name}_{tag}.json")
        seen.update(chunk)
        seen_path.write_text(json.dumps(sorted(seen)))


def claim_ids(ent: dict, prop: str) -> list:
    out = []
    for c in ent.get("claims", {}).get(prop, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(v, dict) and "id" in v:
            out.append(v["id"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-year", type=int, default=1975)
    ap.add_argument("--to-year", type=int, default=1984)
    ap.add_argument("--focus-year", type=int, default=1980, help="fetch films nearest this start year first")
    ap.add_argument("--entities-only", action="store_true")
    ap.add_argument("--bulk-films", action="store_true", help="fetch remaining films via bulk SPARQL (cast order lost)")
    ap.add_argument("--dates-only", action="store_true", help="fetch all dated P577 values for bulk-fetched films")
    ap.add_argument("--people-now", action="store_true", help="skip entity fetching; look up people of films already fetched")
    a = ap.parse_args()
    y0, y1 = a.from_year, a.to_year
    RAW.mkdir(parents=True, exist_ok=True)

    rows = sparql(FILMS.format(y0=y0, y1=y1), RAW / f"q_films_{y0}_{y1}.json")
    year_of = {q(r["f"]): int(r["y"]) for r in rows}
    # shorts, TV films, documentaries, TV specials and anything under 60 minutes are not theatrical features
    excluded = {q(r["f"]) for r in sparql(EXCLUDE.format(y0=y0, y1=y1), RAW / f"q_exclude_{y0}_{y1}.json")}
    year_of = {f: y for f, y in year_of.items() if f not in excluded}
    focus = a.focus_year or (y0 + y1) // 2
    # fetch the years nearest the focus start year first, so a usable pack exists early
    films = sorted(year_of, key=lambda f: (abs(year_of[f] - focus + 0.5), f))
    print(f"films: {len(films)}", flush=True)
    out = RAW / "films"
    out.mkdir(exist_ok=True)
    todo = [] if a.people_now else [f for f in films if not (out / f"{f}.json").exists()]
    if a.bulk_films:
        bulk_films(todo, out)
        todo = []
    if a.dates_only:
        unordered = [p.stem for p in out.glob("*.json") if '"cast_order": "unordered"' in p.read_text()]
        chunked(FILM_DATES, sorted(unordered), "filmdates", 700)
        return
    print(f"film entities: {len(todo)} to fetch", flush=True)
    keep = ("P577", "P136", "P161", "P57", "P750", "P272", "P2130", "P2142", "P155", "P179")
    for i, f in enumerate(todo):
        data = _request(ENTITY.format(f))
        ents = data.get("entities", {})
        ent = ents.get(f) or next(iter(ents.values()), None)
        if ent:
            slim = {"id": f, "labels": {"en": ent.get("labels", {}).get("en", {})},
                    "descriptions": {"en": ent.get("descriptions", {}).get("en", {})},
                    "sitelinks": {k: 1 for k in ent.get("sitelinks", {})},
                    "claims": {p: ent["claims"][p] for p in keep if p in ent.get("claims", {})}}
            (out / f"{f}.json").write_text(json.dumps(slim))
        if i % 200 == 0:
            print(f"  film entities {i}/{len(todo)}", flush=True)
        time.sleep(0.5)
    if a.entities_only:
        return
    people, refs = set(), set()
    for f in films:
        path = out / f"{f}.json"
        if not path.exists():
            continue
        ent = json.loads(path.read_text())
        cast = claim_ids(ent, "P161")
        people.update(cast[:40] if ent.get("cast_order") == "unordered" else cast[:12])
        people.update(claim_ids(ent, "P57")[:3])
        for prop in ("P136", "P750", "P272", "P179"):
            refs.update(claim_ids(ent, prop))
    people = sorted(people)
    print(f"people: {len(people)}; labels: {len(refs)}", flush=True)
    chunked(SPOUSES, people, "spouses", 2000)
    for path in RAW.glob("q_spouses_*.json"):          # name spouses who are outside the film set
        refs.update(q(r["sp"]) for r in json.loads(path.read_text()))
    chunked(LABELS, sorted(refs), "labels", 1500)
    chunked(PEOPLE, people, "people", 1200)
    chunked(HONOURS, people, "honours", 1200)
    print("done", flush=True)


if __name__ == "__main__":
    main()
