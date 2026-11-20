"""LOCAL-ONLY IMDb enrichment overlay for a historical pack.

    python datapipe/imdb_overlay.py --pack data/history/wikidata_1975_1992.json

IMDb's datasets are for personal, non-commercial use and may not be republished, so
the output goes to data/local/imdb_overlay.json (gitignored) and is applied at load
time by hsim/world/historical.py. Never commit it, or anything generated from it.

What it adds to the Wikidata pack:
  films[QID].billing      IMDb billing order of the cast (Wikidata QIDs where mapped, else nm ids)
  films[QID].characters   character names from IMDb principals
  extra_films[tt]         notable films released in the US that the pack lacks (mostly non-US
                          productions): IMDb type 'movie', 'US' among release regions, enough votes
  people[nm]              IMDb-only people those casts need (birth year only, so dates are approximate)
Inputs: the pack, data/local/imdb_<y0>_<y1>.json (datapipe/imdb_index.py) and the CC0
Wikidata<->IMDb id map in the Wikidata store (datapipe/imdb_billing.py --stage ids).
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from store import Store  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / "data" / "local"
ACTING = ("actor", "actress")


def q(uri: str) -> str:
    return uri.rsplit("/", 1)[1]


def build(pack: dict, index: dict, min_votes: int, max_cast: int) -> dict:
    t0 = time.time()
    T, N = index["titles"], index["people"]
    to_imdb, to_q = {}, {}
    for r in Store().rows("imdbids"):
        to_imdb[q(r["x"])] = r["imdb"]
        to_q.setdefault(r["imdb"], q(r["x"]))
    pack_people = pack["people"]
    film_tt = {fid: to_imdb[fid] for fid in pack["films"] if to_imdb.get(fid, "").startswith("tt")}
    pack_tts = set(film_tt.values())
    imdb_people = {}

    def person_id(nconst: str, category: str):
        """The pack's QID if this person is in the pack, else an IMDb-only record (needs a birth year)."""
        qid = to_q.get(nconst)
        if qid and qid in pack_people:
            return qid
        n = N.get(nconst)
        if not n or not n.get("birth"):
            return None
        if nconst not in imdb_people:
            imdb_people[nconst] = {
                "name": n["name"], "gender": {"actor": "m", "actress": "f"}.get(category, "x"),
                "birth": f"{n['birth']}-07-01", "birth_precision": "year",
                "death": f"{n['death']}-07-01" if n.get("death") else None, "manner_of_death": [],
                "spouses": [], "partners": [], "honours": [], "sitelinks": 0, "description": "",
                "source": "imdb"}
        elif imdb_people[nconst]["gender"] == "x" and category in ACTING:
            imdb_people[nconst]["gender"] = {"actor": "m", "actress": "f"}[category]
        return nconst

    def cast_of(x):
        billed, chars = [], {}
        for ordering, nconst, category, characters in sorted(x.get("principals", [])):
            if category not in ACTING:
                continue
            pid = person_id(nconst, category)
            if pid and pid not in billed:
                billed.append(pid)
                if characters:
                    chars[pid] = characters[0][:80]
            if len(billed) >= max_cast:
                break
        return billed, chars

    films = {}
    for fid, tt in sorted(film_tt.items()):
        x = T.get(tt)
        if not x:
            continue
        billed, chars = cast_of(x)
        if billed:
            films[fid] = {"billing": billed, "characters": chars}

    # sitelinks are the pack's notability signal; give extra films the sitelinks of pack films with
    # the same IMDb vote quantile (an estimate, flagged as such)
    pairs = sorted((T[tt].get("votes", 0), pack["films"][fid].get("sitelinks", 0)) for fid, tt in film_tt.items()
                   if tt in T)
    votes_sorted = [v for v, _ in pairs]

    def sitelinks_for(votes):
        i = min(len(pairs) - 1, bisect.bisect_left(votes_sorted, votes))
        window = [s for _, s in pairs[max(0, i - 25): i + 25]]
        return sorted(window)[len(window) // 2] if window else 0

    y0, y1 = pack["years"]
    extra = {}
    for tt, x in T.items():
        if (x["type"] != "movie" or x["adult"] or tt in pack_tts or not (y0 <= x["year"] <= y1)
                or "US" not in x.get("regions", []) or x.get("votes", 0) < min_votes
                or (x["runtime"] or 90) < 60 or "Documentary" in x["genres"]):
            continue
        billed, chars = cast_of(x)
        if not billed:
            continue
        directors = [p for p in (person_id(d, "director") for d in x.get("directors", [])[:2]) if p]
        extra[tt] = {"title": x["title"], "date": f"{x['year']}-07-01", "date_precision": "year",
                     "genres": [g.lower().replace("sci-fi", "science fiction") for g in x["genres"]],
                     "cast": billed, "characters": chars, "directors": directors, "distributors": [],
                     "companies": [], "cost_usd": None, "box_office_usd": None, "follows": [], "series": [],
                     "sitelinks": sitelinks_for(x.get("votes", 0)), "sitelinks_estimated": True,
                     "description": "", "cast_order": "imdb billing", "source": "imdb"}
    stats = {"films_with_billing": len(films), "extra_films": len(extra), "imdb_only_people": len(imdb_people),
             "seconds": round(time.time() - t0, 1)}
    return {"source": "IMDb non-commercial datasets (personal use; local only, never commit)",
            "pack_version": pack.get("version"), "min_votes": min_votes, "stats": stats,
            "films": films, "extra_films": extra, "people": imdb_people}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default=str(ROOT / "data" / "history" / "wikidata_1975_1992.json"))
    ap.add_argument("--index", default=None, help="IMDb index (default: data/local/imdb_<pack years>.json)")
    ap.add_argument("--min-votes", type=int, default=3000, help="notability bar for films the pack lacks")
    ap.add_argument("--max-cast", type=int, default=10)
    a = ap.parse_args()
    pack = json.loads(Path(a.pack).read_text())
    y0, y1 = pack["years"]
    index = json.loads(Path(a.index or LOCAL / f"imdb_{y0}_{y1}.json").read_text())
    out = build(pack, index, a.min_votes, a.max_cast)
    LOCAL.mkdir(parents=True, exist_ok=True)
    (LOCAL / "imdb_overlay.json").write_text(json.dumps(out))
    print(json.dumps(out["stats"]), "-> data/local/imdb_overlay.json (local only, never commit)")


if __name__ == "__main__":
    main()
