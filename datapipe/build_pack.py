"""Build a compact historical data pack from the raw Wikidata cache.

    python datapipe/build_pack.py --from-year 1975 --to-year 1984

The pack holds documented facts only (CC0 Wikidata): films (date, genres, cast in
statement order, directors, distributors/companies, cost, box office, series) and
people (gender, birth/death, manner of death, spouses with dates, major awards
and nominations with dates, sitelink count as a notability signal).
No attribute estimates are stored: those are computed for the chosen start date
at load time (hsim/world/historical.py), so one pack serves every start date it covers.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "wikidata"
MALE, FEMALE = "Q6581097", "Q6581072"
USD = "http://www.wikidata.org/entity/Q4917"


def qid(uri: str) -> str:
    return uri.rsplit("/", 1)[1]


def _val(c):
    return c.get("mainsnak", {}).get("datavalue", {}).get("value")


def _ids(ent, prop):
    return [v["id"] for v in (_val(c) for c in ent.get("claims", {}).get(prop, [])) if isinstance(v, dict) and "id" in v]


def _wb_time(v) -> str | None:
    if not isinstance(v, dict) or "time" not in v:
        return None
    return _iso(v["time"], v.get("precision", 11))


def _iso(t: str, prec: int = 11) -> str | None:
    """Wikidata/SPARQL timestamps → ISO date (year precision → mid-year)."""
    t = t.lstrip("+")
    try:
        y, m, d = int(t[0:4]), int(t[5:7]) or 1, int(t[8:10]) or 1
        if prec < 10:
            m, d = 7, 1
        elif prec < 11:
            d = 15
        return dt.date(y, m, d).isoformat()
    except (ValueError, IndexError):
        return None


def _first_time(ent, prop):
    """Most precise date first, then earliest (a festival date beats a bare year)."""
    vals = []
    for c in ent.get("claims", {}).get(prop, []):
        v = _val(c)
        t = _wb_time(v)
        if t:
            vals.append((-v.get("precision", 11), t))
    return sorted(vals)[0][1] if vals else None


def _precision(ent, prop) -> str:
    """'day' | 'month' | 'year' for the earliest date of a property."""
    best = None
    for c in ent.get("claims", {}).get(prop, []):
        v = _val(c)
        if isinstance(v, dict) and "time" in v:
            t = _wb_time(v)
            if t and (best is None or t < best[0]):
                best = (t, v.get("precision", 11), v["time"])
    for c in ent.get("claims", {}).get(prop, []):
        v = _val(c)
        if isinstance(v, dict) and "time" in v and v.get("precision", 11) > (best[1] if best else -1):
            best = (_wb_time(v), v.get("precision", 11), v["time"])
    if not best:
        return "year"
    t, prec, raw = best
    return "day" if prec >= 11 else "month" if prec == 10 else "year"


def _usd(ent, prop):
    best = None
    for c in ent.get("claims", {}).get(prop, []):
        v = _val(c)
        if isinstance(v, dict) and v.get("unit") == USD:
            best = max(best or 0.0, abs(float(v["amount"])))
    return best


def _film_entities(store, y0: int, y1: int, rows) -> list:
    """Entity-shaped film records from the store: per-film entity data where fetched
    (statement order kept), otherwise assembled from bulk SPARQL rows."""
    listed = store.films(y0 - 1, y1 + 1)
    items, meta, dates = {}, {}, {}
    for r in rows("filmitems"):
        items.setdefault(qid(r["f"]), {}).setdefault(r["prop"].rsplit("/", 1)[1], []).append(qid(r["v"]))
    for r in rows("filmmeta"):
        meta[qid(r["f"])] = r
    for r in rows("filmdates"):
        t = r["t"] if r["t"].startswith(("+", "-")) else "+" + r["t"]
        dates.setdefault(qid(r["f"]), []).append({"mainsnak": {"datavalue": {"value": {"time": t, "precision": int(r["prec"])}}}})
    out, have = [], set()
    for f, ent, src in store.entities("film"):
        if f not in listed:
            continue
        if src != "entitydata":
            ent["cast_order"] = "unordered"
            if f in dates:
                ent["claims"]["P577"] = dates[f]
        out.append(ent)
        have.add(f)
    for f in sorted(set(listed) - have):
        if f not in meta or f not in dates:
            continue
        m = meta[f]
        claims = {k: [{"mainsnak": {"datavalue": {"value": {"id": v}}}} for v in sorted(set(vs))]
                  for k, vs in items.get(f, {}).items()}
        claims["P577"] = dates[f]
        for key, prop in (("costUsd", "P2130"), ("boUsd", "P2142")):
            if m.get(key):
                claims[prop] = [{"mainsnak": {"datavalue": {"value": {"amount": m[key], "unit": USD}}}}]
        out.append({"id": f, "labels": {"en": {"value": m.get("label", "")}},
                    "descriptions": {"en": {"value": m.get("desc", "")}},
                    "sitelinks": {f"s{i}": 1 for i in range(int(float(m.get("sl", 0))))},
                    "claims": claims, "cast_order": "unordered"})
    return out


def build(y0: int, y1: int) -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from store import Store
    store = Store()

    def rows(name):
        return store.rows(name)

    labels = {qid(r["x"]): r["label"] for r in rows("labels")}
    excluded = {qid(r["f"]) for r in rows("exclude")}
    films = {}
    unordered = set()
    for ent in _film_entities(store, y0, y1, rows):
        if ent.get("cast_order") == "unordered":
            unordered.add(ent["id"])
        title = ent.get("labels", {}).get("en", {}).get("value")
        date = _first_time(ent, "P577")
        if not (title and date) or not (y0 <= int(date[:4]) <= y1) or ent["id"] in excluded:
            continue
        films[ent["id"]] = {
            "title": title, "date": date, "date_precision": _precision(ent, "P577"),
            "genres": [labels.get(g, g) for g in _ids(ent, "P136")][:5],
            "cast": _ids(ent, "P161")[:40 if ent["id"] in unordered else 12], "directors": _ids(ent, "P57")[:3],
            "distributors": [labels.get(x, x) for x in _ids(ent, "P750")][:3],
            "companies": [labels.get(x, x) for x in _ids(ent, "P272")][:3],
            "cost_usd": _usd(ent, "P2130"), "box_office_usd": _usd(ent, "P2142"),
            "follows": _ids(ent, "P155")[:1], "series": [labels.get(x, x) for x in _ids(ent, "P179")][:1],
            "sitelinks": len(ent.get("sitelinks", {})),
            "description": ent.get("descriptions", {}).get("en", {}).get("value", ""),
        }
    # films fetched in bulk have no statement order: bill by prior experience (no hindsight)
    by_date = sorted(films.items(), key=lambda kv: kv[1]["date"])
    prior = {}
    for fid, fm in by_date:
        if fid in unordered:
            fm["cast"] = sorted(fm["cast"], key=lambda p: (-prior.get(p, 0), p))[:12]
            fm["cast_order"] = "prior-credits heuristic"
        for p in fm["cast"]:
            prior[p] = prior.get(p, 0) + 1
    needed = {p for fm in films.values() for p in fm["cast"] + fm["directors"]}
    people = {}
    for r in rows("people"):
        pid = qid(r["p"])
        if pid not in needed or "label" not in r:
            continue
        birth = _iso(r["birth"])
        if not birth:
            continue
        p = people.setdefault(pid, {
            "name": r["label"], "gender": {MALE: "m", FEMALE: "f"}.get(qid(r.get("gender", "x/x")), "x"),
            "birth": birth, "death": _iso(r["death"]) if r.get("death") else None,
            "manner_of_death": [], "spouses": [], "honours": [],
            "sitelinks": int(float(r.get("sl", 0))), "description": r.get("desc", "")})
        if r.get("manner") and qid(r["manner"]) not in p["manner_of_death"]:
            p["manner_of_death"].append(qid(r["manner"]))
        p["birth"] = min(p["birth"], birth)
    for r in rows("spouses"):
        pid = qid(r["p"])
        if pid in people:
            sp = {"id": qid(r["sp"]), "start": _iso(r["start"]) if r.get("start") else None,
                  "end": _iso(r["end"]) if r.get("end") else None}
            if sp not in people[pid]["spouses"]:
                people[pid]["spouses"].append(sp)
    for r in rows("honours"):
        pid = qid(r["p"])
        if pid in people:
            h = {"award": r["awardLabel"], "result": r["kind"], "date": _iso(r["date"]) if r.get("date") else None,
                 "for": qid(r["work"]) if r.get("work") else None}
            if h not in people[pid]["honours"]:
                people[pid]["honours"].append(h)
    for p in people.values():
        p["spouses"].sort(key=lambda s: (s["start"] or "", s["id"]))
        p["honours"].sort(key=lambda h: (h["date"] or "", h["award"]))
    spouse_names = {}
    for p in people.values():
        for sp in p["spouses"]:
            if sp["id"] not in people and sp["id"] in labels:
                spouse_names[sp["id"]] = labels[sp["id"]]
    return {"version": f"wikidata-{y0}-{y1}-{dt.date.today().isoformat()}", "spouse_names": spouse_names,
            "source": "Wikidata (CC0 1.0), https://www.wikidata.org/ — facts only; no estimates stored",
            "years": [y0, y1], "films": films, "people": people}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-year", type=int, default=1975)
    ap.add_argument("--to-year", type=int, default=1984)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    pack = build(a.from_year, a.to_year)
    out = Path(a.out or ROOT / "data" / "history" / f"wikidata_{a.from_year}_{a.to_year}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(pack, separators=(",", ":"), sort_keys=True))
    n_cast = sum(len(f["cast"]) for f in pack["films"].values())
    print(f"wrote {out}: {len(pack['films'])} films ({n_cast} cast links), {len(pack['people'])} people, "
          f"{out.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
