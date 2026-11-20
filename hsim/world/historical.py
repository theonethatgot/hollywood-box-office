"""Historical snapshot loader and attribute estimator (DESIGN.md §3.5, §3.6, §4).

Given a data pack of documented facts and a start date, build real people,
real films in the pipeline and documented future events, without simulating
earlier years.

Estimation rules
- PUBLIC / OBSERVED attributes (fame, bankability, prestige, critical standing,
  heat, quote, experience) use only credits and honours dated before the start.
- HIDDEN traits (talent, presence) may use the whole documented career, but only
  partly (`history.hindsight_weight`) and with substantial noise
  (`history.talent_noise_sd`). Eventual success is evidence of ability, never
  proof: stars can be merely good, and overlooked actors can be brilliant.
- Personality is NOT documented in the pack: it is drawn from the same priors as
  fictional NPCs and marked as such in provenance (Tier A extraction is planned).
- Real future films become projects whose stage is inferred from the release
  date. Their real casts are *intended attachments*, not guarantees.
- Documented marriages, divorces and deaths become HistoricalEvents with
  causal dependencies, evaluated each week by systems/personal.py.
"""
from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

from .. import models as M
from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_days, add_weeks, age_on, clamp, d, days_between, year
from ..systems import market
from . import genesis as G
from . import people as P

ND = NormalDist()
NATURAL = {"Q3739104"}
NON_NATURAL = {"Q171558", "Q149086", "Q10737"}   # accident, homicide, suicide

GENRE_KEYS = [  # priority order: first match wins
    ("horror", ("horror", "slasher", "zombie")),
    ("scifi", ("science fiction", "fantasy", "superhero", "space")),
    ("family", ("family", "children", "animated", "animation")),
    ("action", ("action", "adventure", "war film", "western", "martial arts", "disaster")),
    ("thriller", ("thriller", "crime", "mystery", "noir", "suspense", "heist", "spy")),
    ("romance", ("romance", "romantic")),
    ("comedy", ("comedy", "parody", "satire")),
    ("drama", ("drama", "biographical", "musical", "historical")),
]
STUDIO_KEYS = [
    ("st-par", ("paramount",)), ("st-uni", ("universal",)), ("st-wb", ("warner",)),
    ("st-tri", ("tristar", "tri-star")), ("st-nl", ("new line",)), ("st-mir", ("miramax",)),
    ("st-col", ("columbia",)), ("st-fox", ("20th century", "twentieth century", "fox")),
    ("st-ua", ("united artists",)), ("st-mgm", ("metro-goldwyn", "mgm")),
    ("st-bv", ("disney", "buena vista", "touchstone", "hollywood pictures")), ("st-ori", ("orion",)),
    ("st-avc", ("avco", "embassy")), ("st-nw", ("new world",)),
]
NON_FEATURE = ("documentary", "concert film", "short film", "television film", "anthology", "pornographic",
               "adult film", "hardcore")
BILLING_W = [1.0, 0.6, 0.35, 0.22, 0.15, 0.10]
FAME_QUANTILES = [(0.0, 0.0005), (0.5, 0.004), (0.75, 0.015), (0.9, 0.05), (0.95, 0.10),
                  (0.98, 0.22), (0.995, 0.45), (1.0, 0.80)]
BANK_QUANTILES = [(0.0, 6), (0.5, 18), (0.8, 35), (0.93, 55), (0.98, 72), (0.995, 85), (1.0, 93)]  # among actors with leads
QUOTE_BY_BANK = [(0, 8e3), (15, 2.5e4), (30, 8e4), (50, 3e5), (70, 9e5), (85, 2e6), (95, 4e6)]   # 1980 $


def genre_of(labels: list) -> str:
    low = " | ".join(x.lower() for x in labels)
    for g, keys in GENRE_KEYS:
        if any(k in low for k in keys):
            return g
    return "drama"


# Rights-holders that appear in Wikidata but were not 1980s theatrical distributors
LATER_RIGHTS = ("netflix", "kaspien", "amazon", "hulu", "shout! factory", "vestron video", "anchor bay", "video",
                "kino lorber", "criterion", "mgm home", "warner home", "paramount home", "lionsgate", "lions gate",
                "artisan", "image entertainment", "sony pictures home", "arrow", "scream factory")
TV_OUTLETS = ("american broadcasting company", "nbc", "cbs", "hbo", "lorimar television", "showtime", "abc",
              "fox broadcasting company", "usa network", "turner network television", "tnt", "lifetime", "cinemax")


def theatrical_distributors(film: dict) -> list:
    return [d for d in film.get("distributors", []) if not any(k in d.lower() for k in LATER_RIGHTS)]


def is_tv_film(film: dict) -> bool:
    ds = [d.lower() for d in film.get("distributors", [])]
    return bool(ds) and all(any(t == d or d.startswith(t + " ") for t in TV_OUTLETS) for d in ds)


def studio_of(film: dict) -> str:
    """Map a film to a studio: documented theatrical distributor first, then production company."""
    for source in (theatrical_distributors(film), film.get("companies", [])):
        low = " | ".join(x.lower() for x in source)
        for sid, keys in STUDIO_KEYS:
            if any(k in low for k in keys):
                return sid
    return "st-ind"


def distributor_label(film: dict) -> str | None:
    ds = theatrical_distributors(film)
    return ds[0] if ds else None


def _interp(pairs, x):
    xs, ys = zip(*pairs)
    if x <= xs[0]:
        return ys[0]
    for (x0, y0), (x1, y1) in zip(pairs, pairs[1:]):
        if x <= x1:
            t = (x - x0) / (x1 - x0) if x1 > x0 else 0
            return math.exp(math.log(max(y0, 1e-9)) * (1 - t) + math.log(max(y1, 1e-9)) * t)
    return ys[-1]


def _lin(pairs, x):
    for (x0, y0), (x1, y1) in zip(pairs, pairs[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * ((x - x0) / (x1 - x0) if x1 > x0 else 0)
    return pairs[-1][1]


def _pct(values: dict) -> dict:
    """Rank-percentile in (0,1) with ties averaged; deterministic ordering by key."""
    items = sorted(values.items(), key=lambda kv: (kv[1], kv[0]))
    n = len(items)
    return {k: (i + 0.5) / n for i, (k, _) in enumerate(items)}


def _honour_weight(h: dict) -> float:
    a = h["award"].lower()
    won = h["result"] == "won"
    if "academy award" in a:
        return 3.0 if won else 1.5
    if "golden globe" in a:
        return 1.0 if won else 0.5
    if "bafta" in a:
        return 0.8 if won else 0.4
    if "emmy" in a:
        return 0.6 if won else 0.3
    if "tony" in a:
        return 0.6 if won else 0.3
    return 0.2


# ------------------------------------------------------------- sources ---
def pkey(pid: str) -> str:
    """Person id in the world: Wikidata QIDs as wd:Q..., IMDb-only people (local overlay) as imdb:nm..."""
    return ("imdb:" if pid.startswith("nm") else "wd:") + pid


def fkey(fid: str) -> str:
    return ("imdb:" if fid.startswith("tt") else "wd:") + fid


_SOURCES: dict = {}


def overlay_path():
    from ..core.config import ROOT
    return ROOT / "data" / "local" / "imdb_overlay.json"


def sources(pack: dict) -> dict:
    """The pack's films and people, merged with the local IMDb overlay when it exists and was
    built for this pack. Cached per process (packs are immutable; replay reloads identically)."""
    import json
    path = overlay_path()
    stamp = (pack.get("version"), path.stat().st_mtime if path.exists() else None)
    hit = _SOURCES.get("key")
    if hit == stamp and _SOURCES.get("pack") is pack:
        return _SOURCES["src"]
    films = {fid: dict(f, date=effective_date(fid, f)) for fid, f in pack["films"].items()}
    people = dict(pack["people"])
    overlay = None
    legacy = path.parent / "imdb_billing.json"
    if path.exists():
        ov = json.loads(path.read_text())
        if ov.get("pack_version") == pack.get("version"):
            overlay = {"source": "imdb", "films": len(ov["films"]), "extra_films": len(ov["extra_films"]),
                       "people": len(ov["people"])}
            people.update({k: v for k, v in ov["people"].items() if k not in people})
            for fid, add in ov["films"].items():
                f = films.get(fid)
                if not f:
                    continue
                billed = [x for x in add["billing"] if x in people]
                rest = [x for x in f["cast"] if x not in billed]
                chars = dict(add.get("characters", {}))
                chars.update(f.get("characters", {}))          # Wikidata's documented name wins
                films[fid] = dict(f, cast=billed + rest, characters=chars, cast_order="imdb billing (local)",
                                  imdb_cast=[x for x in billed if x not in f["cast"]])
            for tt, f in ov["extra_films"].items():
                films[tt] = dict(f, date=effective_date(tt, f))
    elif legacy.exists():                                       # older local file: billing order only
        billing = json.loads(legacy.read_text())
        overlay = {"source": "imdb billing (legacy)"}
        for fid, order in billing.items():
            f = films.get(fid)
            if f:
                rank = {x: i for i, x in enumerate(order)}
                films[fid] = dict(f, cast=sorted(f["cast"], key=lambda x: (rank.get(x, 999), f["cast"].index(x))))
    films = {fid: f for fid, f in films.items()
             if not any(x in g_.lower() for g_ in f["genres"] for x in NON_FEATURE) and not is_tv_film(f)}
    src = {"films": films, "people": people, "overlay": overlay,
           "sitelinks_pct": _pct({fid: f.get("sitelinks", 0) for fid, f in films.items()})}
    _SOURCES.update({"key": stamp, "pack": pack, "src": src})
    return src


def index_credits(films: dict, max_billing: int) -> tuple:
    cache = _SOURCES.get("index")
    if cache and cache[0] is films and cache[1] == max_billing:
        return cache[2]
    credits, directing = {}, {}
    for fid, f in films.items():
        for i, pid in enumerate(f["cast"][:max_billing]):
            credits.setdefault(pid, []).append((fid, f["date"], i))
        for pid in f["directors"]:
            directing.setdefault(pid, []).append((fid, f["date"], 0))
    _SOURCES["index"] = (films, max_billing, (credits, directing))
    return credits, directing


def _reach(f) -> float:
    bo = f.get("box_office_usd")
    s = math.log1p(f.get("sitelinks", 0))
    if bo and bo > 1e5:
        return 0.5 * s + 0.5 * math.log1p(bo / 1e6)
    return 0.85 * s


def evidence(hc, rec, cr: list, films: dict, as_of: str) -> dict:
    """Career evidence. Everything observable uses credits and honours dated before `as_of`;
    the *_all fields are hindsight (used only, partly, for hidden talent)."""
    e = {"exposure": 0.0, "lead": 0.0, "recent": 0.0, "older": 0.0, "n_pre": 0, "n_all": 0,
         "first": None, "genres": {}, "lead_all": 0.0, "honours_pre": 0.0, "honours_all": 0.0}
    for fid, dt, idx in cr:
        f = films[fid]
        r = _reach(f)
        bw = BILLING_W[idx] if idx < len(BILLING_W) else 0.15
        e["n_all"] += 1
        if idx <= 1:
            e["lead_all"] += r
        if dt < as_of:
            yrs = days_between(dt, as_of) / 365
            dec = math.exp(-yrs / hc["recency_years"])
            big = r ** hc["reach_power"]        # one big hit outweighs several small films
            e["exposure"] += big * bw * dec
            e["n_pre"] += 1
            if idx <= 1:
                e["lead"] += big * dec
            if yrs <= 2:
                e["recent"] += r * bw
            else:
                e["older"] += r * bw
            e["first"] = min(e["first"] or dt, dt)
            g = genre_of(f["genres"])
            e["genres"][g] = e["genres"].get(g, 0) + bw
    for h in rec.get("honours", []):
        w = _honour_weight(h)
        e["honours_all"] += w
        if h.get("date") and h["date"] < as_of:
            e["honours_pre"] += w
    e["tv_fame"] = sum(_honour_weight(h) for h in rec.get("honours", [])
                       if "emmy" in h["award"].lower() and h.get("date") and h["date"] < as_of)
    return e


def _metrics(e: dict, rec: dict) -> dict:
    return {"exp": e["exposure"] + 0.5 * e["tv_fame"], "lead": e["lead"],
            "hind": 1.0 * e["honours_all"] + 0.5 * math.log1p(rec.get("sitelinks", 0)) + 0.3 * math.log1p(e["lead_all"]),
            "pre": 1.0 * e["honours_pre"] + 0.5 * math.log1p(e["exposure"])}


class Percentiles:
    """Exact rank percentiles for the population loaded at the start; people who enter later
    are placed against the start population's quantiles (stored in the save)."""

    def __init__(self, exact: dict | None = None, quantiles: dict | None = None):
        self.exact, self.q = exact or {}, quantiles or {}

    def __call__(self, name, pid, value) -> float:
        if pid in self.exact.get(name, {}):
            return self.exact[name][pid]
        import bisect
        qs = self.q.get(name)
        if not qs:
            return 0.5
        lo, hi = bisect.bisect_left(qs, value), bisect.bisect_right(qs, value)
        return min(0.995, max(0.005, (lo + hi) / 2 / (len(qs) - 1)))

    @staticmethod
    def quantiles(values) -> list:
        v = sorted(values)
        if not v:
            return []
        return [round(v[min(len(v) - 1, int(i * (len(v) - 1) / 100))], 6) for i in range(101)]


def eligible(hc, rec, now: str) -> bool:
    if not rec or not rec.get("birth"):
        return False
    if rec.get("death") and rec["death"] <= now:
        return False
    return hc["min_age"] <= age_on(rec["birth"], now) <= 90


def make_person(st, cfg, pid, rec, cr, dr, films, pct, as_of, now, tier_a=False, future_refs=None) -> M.Person:
    """A real person as the industry sees them at `as_of` (the campaign start: nothing that
    happened later in real history is visible). `now` is the date they enter the world."""
    hc = cfg["history"]
    infl = market.infl(cfg, year(now))
    e = evidence(hc, rec, cr, films, as_of)
    m = _metrics(e, rec)
    g = R.stream(st.seed, "historical-person", pid)
    roles = (["actor"] if cr else []) + (["director"] if dr else [])
    personality = G._personality(g)
    sex = rec["gender"] if rec["gender"] in ("m", "f") else ("m" if g.random() < 0.5 else "f")
    p = M.Person(id=pkey(pid), name=rec["name"], gender=sex, birth=rec["birth"], roles=roles,
                 tier="A" if tier_a else "B", historical=True,
                 personality=personality, goals=_documented_goals(e, G._goals(g)),
                 traits=G.traits_from_personality(personality, g),
                 provenance={"source": rec.get("source", "wikidata"), "id": pid, "credits_pre_start": e["n_pre"],
                             "personality": "prior (not documented)",
                             "documented_credits_after_start": (future_refs or {}).get(pid, [])})
    if rec.get("birth_precision") == "year":
        p.provenance["birth"] = "year only (approximate date)"
    hw = hc["hindsight_weight"]
    if "actor" in roles:
        z_h = ND.inv_cdf(min(0.999, max(0.001, pct("hind", pid, m["hind"]))))
        # no record before the start means unknown, not untalented: neutral rather than bottom-percentile
        z_p = ND.inv_cdf(min(0.999, max(0.001, pct("pre", pid, m["pre"])))) if e["n_pre"] else 0.0
        signal = 0.6 * (hw * z_h + (1 - hw) * z_p)
        p.talent = round(clamp(50 + 14 * signal + hc["talent_noise_sd"] * g.normal(), 5, 98), 2)
        z_l = ND.inv_cdf(min(0.999, max(0.001, pct("lead", pid, m["lead"])))) if e["n_pre"] else 0.0
        p.presence = round(clamp(50 + 14 * 0.5 * z_l + 12 * g.normal(), 5, 98), 2)
        yrs_active = days_between(e["first"], as_of) / 365 if e["first"] else 0
        p.craft = round(clamp(15 + 0.25 * p.talent + min(30, yrs_active) * 1.3 + min(20, e["n_pre"]) * 0.5
                              + g.normal(0, 6), 5, 95), 2)
        p.range = {r: round(clamp(0.45 * p.talent + g.normal(25, 12) + 18 * min(1.0, e["genres"].get(r, 0))), 2)
                   for r in M.REGISTERS}
        tot = sum(e["genres"].values()) or 1
        p.typecast = {k: round(min(2.0, v / tot * 1.5), 3) for k, v in e["genres"].items() if v / tot > 0.2}
        p_exp = pct("exp", pid, m["exp"])
        p.fame = round(_interp(FAME_QUANTILES, p_exp), 5) if e["n_pre"] else 0.0005
        if e["lead"] > 0:
            p.bankability = round(_lin(BANK_QUANTILES, pct("leadL", pid, m["lead"])), 2)
        else:
            p.bankability = round(clamp(3 + 10 * p_exp), 2)
        p.prestige = round(clamp(6 + 25 * math.log1p(e["honours_pre"]) + 18 * p_exp), 2)
        p.critical_rep = round(clamp(38 + 5 * e["honours_pre"] + 12 * (pct("pre", pid, m["pre"]) - 0.5) + g.normal(0, 6)), 2)
        p.heat = round(clamp(28 * math.log((e["recent"] + 0.5) / (e["older"] / 2 + 0.5)), -60, 60), 2) if e["n_pre"] else 0.0
        p.quote = round(_interp(QUOTE_BY_BANK, p.bankability) * infl, 0) if e["n_pre"] else 0.0
        p.appeal = round(float(clamp(0.5 + 0.25 * (p.presence - 50) / 50 + g.normal(0, 0.08), 0.1, 0.95)), 3)
    if "director" in roles:
        pre_n = sum(1 for _, dt, _ in dr if dt < as_of)
        hon = e["honours_all"]
        base = 50 + 6 * math.log1p(hon) + 3 * math.log1p(pre_n)
        p.direction = {k: round(clamp(base + g.normal(0, 13)), 2)
                       for k in ("vision", "technical", "actor_direction", "discipline", "commercial")}
        if "actor" not in roles:
            p.bankability = round(clamp(15 + 8 * pre_n + 4 * e["honours_pre"]), 2)
            p.prestige = round(clamp(10 + 6 * pre_n + 8 * e["honours_pre"]), 2)
            p.critical_rep = round(clamp(42 + 5 * e["honours_pre"] + g.normal(0, 8)), 2)
    p.romance = G._romance(g, p.gender)
    people = sources_people(st)
    sp_genders = [people[s["id"]]["gender"] for s in rec.get("spouses", []) if s["id"] in people
                  and people[s["id"]]["gender"] in ("m", "f")]
    if sp_genders:
        p.romance["attracted_to"] = sorted(set(sp_genders))
        p.provenance["orientation"] = "from documented spouses"
    else:
        p.provenance["orientation"] = "prior (not documented)"
    p.credits = []
    for fid, dt, idx in sorted(cr, key=lambda x: x[1]):
        if dt < as_of:
            p.credits.append({"project_id": None, "title": films[fid]["title"], "historical_ref": fkey(fid),
                              "role": "lead" if idx == 0 else "colead" if idx == 1 else "supporting",
                              "year": year(dt), "genre": genre_of(films[fid]["genres"]), "kind": "prior"})
    for fid, dt, _ in sorted(dr, key=lambda x: x[1]):
        if dt < as_of:
            p.credits.append({"project_id": None, "title": films[fid]["title"], "historical_ref": fkey(fid),
                              "role": "director", "year": year(dt), "genre": genre_of(films[fid]["genres"]),
                              "kind": "prior"})
    best = max((c for c in p.credits if c["role"] != "director"), key=lambda c: (c["role"] == "lead", c["year"]),
               default=None) or max((c for c in p.credits), key=lambda c: c["year"], default=None)
    p.bio = dated_bio(rec, roles, best, e, as_of)
    if p.credits:
        p.last_work = add_days(as_of, -120)
    archetype = ("star" if p.bankability > 55 else "notable" if p.fame > 0.05 else
                 "working" if p.credits else "newcomer")
    p.monthly_costs = cfg["finance"]["default_monthly_costs"][archetype] * infl
    p.cash = round(p.quote * float(g.uniform(0.5, 2.0)) + 3000 * infl, 0)
    p.provenance["archetype"] = archetype
    if now != as_of:
        p.provenance["entered"] = now
    return p


def sources_people(st) -> dict:
    return _SOURCES.get("src", {}).get("people", {})


def load_historical(st: WorldState, cfg: dict, pack: dict) -> None:
    hc = cfg["history"]
    start = st.date
    src = sources(pack)
    films, people = src["films"], src["people"]
    lookback = add_days(start, -int(hc["lookback_years"] * 365))
    horizon = add_days(start, int(hc["horizon_months"] * 30.5))
    credits, directing = index_credits(films, hc["max_billing"])

    # ---- who is in the world: active recently or documented to work within the horizon ----
    in_world = {}
    for pid in sorted(set(credits) | set(directing)):
        rec = people.get(pid)
        if not eligible(hc, rec, start):
            continue
        cr = credits.get(pid, []) + directing.get(pid, [])
        if any(lookback <= dt <= horizon for _, dt, _ in cr):
            in_world[pid] = rec

    ev = {pid: evidence(hc, rec, credits.get(pid, []), films, start) for pid, rec in in_world.items()}
    actors = [p for p in in_world if p in credits]
    mets = {p: _metrics(ev[p], in_world[p]) for p in actors}
    exact = {"exp": _pct({p: mets[p]["exp"] for p in actors}), "lead": _pct({p: mets[p]["lead"] for p in actors}),
             "leadL": _pct({p: mets[p]["lead"] for p in actors if mets[p]["lead"] > 0}),
             "hind": _pct({p: mets[p]["hind"] for p in actors}), "pre": _pct({p: mets[p]["pre"] for p in actors})}
    quant = {"exp": Percentiles.quantiles(mets[p]["exp"] for p in actors),
             "lead": Percentiles.quantiles(mets[p]["lead"] for p in actors),
             "leadL": Percentiles.quantiles(mets[p]["lead"] for p in actors if mets[p]["lead"] > 0),
             "hind": Percentiles.quantiles(mets[p]["hind"] for p in actors),
             "pre": Percentiles.quantiles(mets[p]["pre"] for p in actors)}
    pct = Percentiles(exact, quant)
    ranking = sorted(actors, key=lambda p: -(exact["exp"][p] + 0.02 * ev[p]["honours_pre"]))
    tier_a = set(ranking[: hc["tier_a_count"]])
    future_refs = {}
    for fid, f in films.items():
        if f["date"] >= start:
            for pid in f["cast"][: hc["max_billing"]] + f["directors"]:
                future_refs.setdefault(pid, []).append({"ref": fkey(fid), "date": f["date"]})

    for pid in sorted(in_world):
        st.people[pkey(pid)] = make_person(st, cfg, pid, in_world[pid], credits.get(pid, []), directing.get(pid, []),
                                           films, pct, start, start, pid in tier_a, future_refs)

    _documented_relationships(st, cfg, people, pack.get("spouse_names", {}), in_world, credits)
    st.market["history"] = {"version": pack.get("version"), "pack": pack.get("_path"), "years": pack.get("years"),
                            "people": len(in_world), "tier_a": len(tier_a), "source": pack.get("source"),
                            "overlay": src["overlay"], "loaded_through": horizon, "quantiles": quant,
                            "intake": []}
    _historical_projects(st, cfg, src, in_world, start, horizon, add_weeks(start, -hc["in_release_weeks"]), start)


NATIONALITIES = {"American", "British", "English", "Scottish", "Welsh", "Irish", "Canadian", "Australian", "French",
                 "Italian", "German", "Swiss", "Austrian", "Mexican", "Swedish", "Danish", "Norwegian", "Dutch",
                 "Belgian", "Spanish", "Greek", "Polish", "Russian", "Soviet", "Japanese", "Chinese", "Indian", "Israeli",
                 "Brazilian", "Argentine", "Cuban", "Hungarian", "Czech", "Jamaican", "Filipino", "Korean", "Finnish",
                 "Icelandic", "Turkish", "Egyptian", "Lebanese", "Iranian", "Chilean", "Colombian", "Portuguese"}


def dated_bio(rec: dict, roles: list, best: dict | None, e: dict, start: str) -> str:
    """A biography using ONLY facts dated before the start: nationality (first word of the
    description), profession from pre-start credits, birth year, best-known pre-start credit
    and pre-start honours. Wikidata descriptions are written with hindsight (death years,
    later careers), so their remainder is never shown."""
    first = (rec.get("description") or "").split(" ")[0]
    nat = first if first in NATIONALITIES else ""
    acts = "actor" in roles
    prof = "actor-director" if acts and "director" in roles else "actor" if acts else "film director"
    if acts and rec.get("gender") == "f":
        prof = prof.replace("actor", "actress")
    born = rec["birth"][:4]
    bits = [f"{nat + ' ' if nat else ''}{prof} (born {born})"]
    if best:
        bits.append(f"known for '{best['title']}' ({best['year']})")
    pre = [h for h in rec.get("honours", []) if h.get("date") and h["date"] < start]
    oscar_win = any("academy award" in h["award"].lower() and h["result"] == "won" for h in pre)
    oscar_nom = any("academy award" in h["award"].lower() for h in pre)
    if oscar_win:
        bits.append("Academy Award winner")
    elif oscar_nom:
        bits.append("Academy Award nominee")
    elif any("golden globe" in h["award"].lower() or "emmy" in h["award"].lower() for h in pre):
        bits.append("award-nominated")
    text = "; ".join(bits)
    return text[0].upper() + text[1:] + "."


def _premise_text(f: dict, genre: str) -> str:
    """Film descriptions are only used if they say nothing dated after the release year."""
    import re
    t = (f.get("description") or "").strip().rstrip(".")
    ry = int(f["date"][:4])
    if not t or "released in" in t or any(int(y) > ry for y in re.findall(r"\b(19\d\d|20\d\d)\b", t)):
        t = f"{ry} {genre} film"
    return t[0].upper() + t[1:] + "."


def effective_date(fid: str, f: dict) -> str:
    """Release dates known only to the year or month are spread deterministically
    across that period (marked approximate) instead of piling onto one weekend."""
    prec = f.get("date_precision", "day")
    y, m = int(f["date"][:4]), int(f["date"][5:7])
    u = R.stable_unit("release-date", fid)
    if prec == "year":
        return (d(f"{y}-02-01") + __import__("datetime").timedelta(days=int(u * 300))).isoformat()
    if prec == "month":
        return (d(f"{y}-{m:02d}-01") + __import__("datetime").timedelta(days=int(u * 27))).isoformat()
    return f["date"]


def _documented_goals(e: dict, prior: dict) -> dict:
    """Career priorities inferred from the documented record (what kind of work they
    actually pursued and were honoured for), blended with a weak prior."""
    gen = e["genres"]
    tot = sum(gen.values()) or 1.0
    serious = (gen.get("drama", 0) + 0.5 * gen.get("thriller", 0)) / tot
    popular = (gen.get("action", 0) + gen.get("comedy", 0) + gen.get("horror", 0) + gen.get("scifi", 0)) / tot
    honours = math.log1p(e["honours_all"])
    ev = {"prestige": 0.12 + 0.12 * honours + 0.35 * serious, "art": 0.12 + 0.45 * serious + 0.04 * honours,
          "fame": 0.12 + 0.5 * popular, "money": 0.12 + 0.4 * popular, "stability": 0.12}
    blend = {k: 0.7 * ev[k] / sum(ev.values()) + 0.3 * prior.get(k, 0.2) for k in ev}
    s = sum(blend.values())
    return {k: round(v / s, 3) for k, v in blend.items()}


def _pct_one(pct: dict, k) -> float:
    return pct.get(k, 0.5)


# ---------------------------------------------------- relationships/events ---
def _documented_relationships(st, cfg, people, outside, in_world, credits, start=None, pair_ok=None) -> None:
    """Documented marriages, divorces, partnerships and deaths become HistoricalEvents.
    `pair_ok(pid, other)` limits which pairs are handled (people entering mid-campaign only add
    events that the people already in the world haven't)."""
    start = start or st.date
    end = add_days(start, int(cfg["history"]["events_horizon_years"] * 365))
    pre_together = {}
    for pid, cr in credits.items():
        for fid, dt, _ in cr:
            if dt < start:
                pre_together.setdefault(fid, []).append(pid)
    coworkers = set()
    for fid, ids in pre_together.items():
        for a in ids:
            for b in ids:
                if a < b:
                    coworkers.add((a, b))
    n = 0

    def name_of(q):
        return people.get(q, {}).get("name") or outside.get(q)

    pair_ok = pair_ok or (lambda a, b: True)
    for pid in sorted(in_world):
        me = st.people[pkey(pid)]
        for sp in people[pid].get("spouses", []):
            other = sp["id"]
            if not pair_ok(pid, other):
                continue
            s0, s1 = sp.get("start"), sp.get("end")
            other_in = other in in_world
            if s0 and s0 <= start and (not s1 or s1 > start):        # married at start
                if other_in:
                    if pid < other:
                        you = st.people[pkey(other)]
                        r = st.rel(me.id, you.id)
                        r.status, r.since = "married", s0
                        r.history.append({"date": s0, "text": "married", "delta": 10, "documented": True})
                        for x, y in ((me, you), (you, me)):
                            x.partner_id, x.partner_status = y.id, "married"
                elif me.partner_status is None:
                    me.partner_status = "married_offscreen"
                    me.provenance["spouse_outside_world"] = name_of(other) or "undocumented name"
                deaths = [people.get(x, {}).get("death") for x in (pid, other)]
                widowed = s1 and any(dd and abs(days_between(dd, s1)) <= 10 for dd in deaths)
                if s1 and s1 <= end and not widowed and (pid < other or not other_in):
                    nm = name_of(other)
                    _event(st, [me.id] + ([pkey(other)] if other_in else []), "divorce" if other_in else "divorce_outside",
                           s1, f"{me.name} and {nm} divorced." if nm else f"{me.name}'s marriage ended in divorce.",
                           {"kind": "relationship" if other_in else "independent"})
                    n += 1
            elif s0 and start < s0 <= end and (pid < other or not other_in):
                met = (min(pid, other), max(pid, other)) in coworkers
                nm = name_of(other)
                _event(st, [me.id] + ([pkey(other)] if other_in else []), "marriage" if other_in else "marriage_outside",
                       s0, f"{me.name} married {nm}." if nm else f"{me.name} married.",
                       {"kind": "relationship" if other_in else "independent", "met_before_start": met,
                        "base_rate_if_never_met": cfg["history"]["marriage_base_rate_if_never_met"]})
                n += 1
        _documented_partnerships(st, cfg, people, pid, me, in_world, coworkers, name_of, start, end, pair_ok)
        dd = people[pid].get("death")
        if dd and start < dd <= end and pair_ok(pid, None):
            manner = set(people[pid].get("manner_of_death", []))
            kind = "circumstance" if manner & NON_NATURAL else "independent"
            _event(st, [me.id], "death", dd, f"{me.name} died.", {"kind": kind})


def _documented_partnerships(st, cfg, people, pid, me, in_world, coworkers, name_of, start, end, pair_ok) -> None:
    """Documented unmarried partnerships (Wikidata P451). Undated ones are skipped (they can't be
    placed in time). If records overlap at the start, the most recently begun one is current."""
    partners = [x for x in people[pid].get("partners", []) if x.get("start") and pair_ok(pid, x["id"])]
    ongoing = [x for x in partners if x["start"] <= start and (not x.get("end") or x["end"] > start)]
    married = me.partner_status in ("married", "married_offscreen")
    if ongoing and not married:
        cur = max(ongoing, key=lambda x: (x["start"], x["id"]))
        other = cur["id"]
        if other in in_world:
            you = st.people[pkey(other)]
            if you.partner_status not in ("married", "married_offscreen") and you.partner_id in (None, me.id):
                r = st.rel(me.id, you.id)
                if not any(h.get("documented") for h in r.history):
                    r.status, r.since = "dating", cur["start"]
                    r.history.append({"date": cur["start"], "text": "in a relationship", "delta": 10,
                                      "documented": True})
                for x, y in ((me, you), (you, me)):
                    x.partner_id, x.partner_status = y.id, "dating"
        elif me.partner_status is None:
            me.partner_status = "partnered_offscreen"
            me.provenance["partner_outside_world"] = name_of(other) or "undocumented name"
    for x in partners:
        other = x["id"]
        other_in = other in in_world
        if not (pid < other or not other_in):
            continue                                   # each in-world pair handled once
        nm = name_of(other)
        if start < x["start"] <= end:
            met = (min(pid, other), max(pid, other)) in coworkers
            _event(st, [me.id] + ([pkey(other)] if other_in else []),
                   "partnership" if other_in else "partnership_outside", x["start"],
                   f"{me.name} and {nm} began a relationship." if nm else f"{me.name} began a relationship.",
                   {"kind": "relationship" if other_in else "independent", "met_before_start": met,
                    "base_rate_if_never_met": cfg["history"]["marriage_base_rate_if_never_met"]})
        if x.get("end") and start < x["end"] <= end:
            _event(st, [me.id] + ([pkey(other)] if other_in else []),
                   "separation" if other_in else "separation_outside", x["end"],
                   f"{me.name} and {nm} separated." if nm else f"{me.name}'s relationship ended.",
                   {"kind": "relationship" if other_in else "independent"})


def _event(st, people, etype, date, summary, dep) -> None:
    eid = st.new_id("hx")
    st.hist_events[eid] = M.HistoricalEvent(id=eid, people=people, type=etype, date=date, summary=summary,
                                            sources=["Wikidata"], dependency=dep)


# ------------------------------------------------------------- projects ---
# ---------------------------------------------------------- rolling intake ---
_PACKS: dict = {}


def _pack_for(st):
    """The save's historical pack, by the path recorded at genesis (cached per process)."""
    h = st.market["history"]
    path = h.get("pack")
    if not path:
        return None
    if path not in _PACKS:
        from ..core.config import ROOT
        from ..io.datapack import read_pack
        from pathlib import Path
        pth = Path(path)
        pack = read_pack(pth if pth.is_absolute() else ROOT / pth)
        pack["_path"] = path
        _PACKS[path] = pack
    return _PACKS[path]


class _InWorld:
    """Membership test for pack ids against the people currently in the world."""

    def __init__(self, st):
        self.people = st.people

    def __contains__(self, pid) -> bool:
        return pkey(pid) in self.people


def intake(st: WorldState, cfg: dict) -> None:
    """Monthly, deterministic: real films whose release date enters the rolling horizon become
    projects (usually in development), and the real people they need who aren't in the world yet
    arrive, judged only on their record before the campaign started (no later history leaks in)."""
    h = st.market.get("history")
    if not h or not h.get("pack") or st.date[8:10] > "07":
        return
    hc = cfg["history"]
    target = add_days(st.date, int(hc["horizon_months"] * 30.5))
    if target <= h["loaded_through"]:
        return
    pack = _pack_for(st)
    src = sources(pack)
    if (pack.get("version") != h["version"] or src["overlay"] != h["overlay"]) and not h.get("sources_changed"):
        h["sources_changed"] = st.date
        st.log("history_sources_changed", "The historical pack or local overlay differs from the one this world "
               "was created with; later intake uses the current files (replay needs the original ones).",
               public=False, salience=0)
    films, people = src["films"], src["people"]
    credits, directing = index_credits(films, hc["max_billing"])
    window = [(fid, f) for fid, f in sorted(films.items(), key=lambda kv: (kv[1]["date"], kv[0]))
              if h["loaded_through"] <= f["date"] < target]
    arrivals = {}
    for fid, f in window:
        for pid in f["cast"][: hc["max_billing"]] + f["directors"]:
            if pid not in arrivals and pkey(pid) not in st.people and eligible(hc, people.get(pid), st.date):
                arrivals[pid] = people[pid]
    pct = Percentiles(None, h["quantiles"])
    for pid in sorted(arrivals):
        st.people[pkey(pid)] = make_person(st, cfg, pid, arrivals[pid], credits.get(pid, []), directing.get(pid, []),
                                           films, pct, st.start_date, st.date)
    if arrivals:
        before = {pid for pid in people if pid not in arrivals}
        _documented_relationships(st, cfg, people, pack.get("spouse_names", {}), arrivals, credits, start=st.date,
                                  pair_ok=lambda a, b: b is None or b not in before or pkey(b) not in st.people)
        from . import genesis as GEN
        from . import people as PEOPLE
        ids = {pkey(pid) for pid in arrivals}
        GEN.assign_agents(st, cfg, only=ids)
        for i in sorted(ids):
            PEOPLE.give_persona(st, st.people[i], i)
        PEOPLE.assign_agent_people(st)
    n_before = len(st.projects)
    _historical_projects(st, cfg, src, _InWorld(st), st.start_date, target, h["loaded_through"], st.date)
    h["loaded_through"] = target
    rec = {"date": st.date, "films": len(st.projects) - n_before, "people": len(arrivals), "through": target}
    h["intake"] = (h.get("intake", []) + [rec])[-60:]
    if rec["films"] or rec["people"]:
        st.log("history_intake", f"{rec['films']} documented productions and {rec['people']} real people entered "
               f"the world (releases up to {target}).", public=False, salience=0, data=rec)


def _independent_studios(st, cfg, films: dict) -> dict:
    """Real independent distributors become mini studios (historical releases only,
    no generated slate). Returns label -> studio id."""
    from collections import Counter
    counts = Counter(distributor_label(f) for f in films.values() if studio_of(f) == "st-ind" and distributor_label(f))
    out = {}
    for label, n in sorted(counts.items()):
        if n < 3:
            continue
        sid = "st-x-" + "".join(ch for ch in label.lower() if ch.isalnum())[:24]
        if sid not in st.studios:
            st.studios[sid] = M.Studio(id=sid, name=label, tier="mini", cash=20e6, slate_per_year=0, budget_median=2.0,
                                       risk_appetite=65, historical=True,
                                       provenance={"source": "wikidata distributor", "films_in_pack": n})
        out[label] = sid
    return out


def _historical_projects(st, cfg, src, in_world, start, horizon, recent, now) -> None:
    """Real films released in [recent, horizon) become projects; stages are inferred at `now`."""
    films = src["films"]
    indie = _independent_studios(st, cfg, films)
    used = {p.title for p in st.projects.values()}
    counts = st.market.setdefault("historical_slate", {})
    for fid, f in sorted(films.items(), key=lambda kv: (kv[1]["date"], kv[0])):
        if not (recent <= f["date"] < horizon):
            continue
        p = film_project(st, cfg, fid, f, src, in_world, indie, used, now)
        if p:
            counts[p.studio_id] = counts.get(p.studio_id, 0) + 1


def film_project(st, cfg, fid, f, src, in_world, indie, used, now):
    hc = cfg["history"]
    sl_pct = src["sitelinks_pct"]
    if not any(c in in_world for c in f["cast"][: hc["max_billing"]]):
        return None       # never invent a cast for a real film (catches untagged documentaries too)
    sid = studio_of(f)
    if sid == "st-ind" and distributor_label(f) in indie:
        sid = indie[distributor_label(f)]
    studio = st.studios.get(sid) or st.studios["st-ind"]
    g = R.stream(st.seed, "historical-film", fid)
    genre = genre_of(f["genres"])
    gcfg = cfg["genres"][genre]
    z = ND.inv_cdf(min(0.999, max(0.001, sl_pct[fid])))
    hw = hc["hindsight_weight"]
    script = clamp(50 + 14 * (hw * 0.6 * z + 0.8 * g.normal()), 5, 98)       # hidden, partly hindsight
    hook = clamp(50 + 14 * (hw * 0.7 * z + 0.7 * g.normal()), 5, 98)
    if f.get("follows") or f.get("series"):
        hook = clamp(hook + hc["sequel_hook_bonus"])
    budget = f.get("cost_usd") or float(math.exp(g.normal(math.log(studio.budget_median), 0.5))) * 1e6 * market.infl(cfg, year(f["date"]))
    pid = st.new_id("prj")
    p = M.Project(id=pid, title=f["title"] if f["title"] not in used else f"{f['title']} ({year(f['date'])})",
                  genre=genre, studio_id=studio.id, premise=_premise_text(f, genre),
                  budget=round(float(budget), 0), created=add_days(now, -400), script_quality=round(script, 2),
                  hook=round(hook, 2), breadth=round(gcfg["breadth"] * math.exp((hook - 50) / 50 * 0.6) * math.exp(g.normal(0, 0.3)), 4),
                  historical_ref=fkey(fid))
    p.distributor_note = distributor_label(f) or ("distributor not documented" if studio.id == "st-ind" else None)
    p.date_approx = f.get("date_precision", "day") != "day"
    tilt_noise = g.dirichlet([6, 6, 6, 6]) * 4
    p.segment_tilt = {s: round(float(t * n), 3) for s, t, n in zip(cfg["box_office"]["segments"], gcfg["tilt"], tilt_noise)}
    real_m = budget / 1e6 / market.infl(cfg, year(f["date"]))
    p.shoot_weeks = max(4, int(round(g.uniform(*gcfg["shoot_weeks"]) + max(0, math.log(max(real_m, 0.5) / 8)) * 2)))
    p.post_weeks = int(g.integers(*cfg["development"]["post_weeks"]))
    used.add(p.title)
    # roles from billing order
    cast = [c for c in f["cast"][: hc["max_billing"]] if c in in_world]
    for i, cpid in enumerate(cast):
        person = st.people[pkey(cpid)]
        imp = "lead" if i == 0 else "colead" if i == 1 else "supporting" if i < 4 else "featured"
        age = age_on(person.birth, f["date"])
        rid = st.new_id("rol")
        char = f.get("characters", {}).get(cpid)
        role = M.Role(id=rid, project_id=pid, name=char or P.character_name(g, person.gender), importance=imp,
                      gender=person.gender, name_documented=bool(char),
                      age_min=max(8, age - 6), age_max=age + 6, register=genre,
                      screen_share={"lead": 0.45, "colead": 0.28, "supporting": 0.09, "featured": 0.03}[imp],
                      description=G.N.ROLE_DESC[imp], intended=person.id)
        st.roles[rid] = role
        p.role_ids.append(rid)
    if not p.role_ids:
        G._make_roles(st, cfg, p, g)
    else:
        lo, hi = cfg["casting"]["featured_roles"]
        for _ in range(max(0, int(g.integers(lo, hi + 1)) - max(0, len(cast) - 4))):   # undocumented parts
            gen = "m" if g.random() < 0.55 else "f"
            c = int(g.integers(18, 70))
            rid = st.new_id("rol")
            st.roles[rid] = M.Role(id=rid, project_id=pid, name=P.character_name(g, gen), importance="featured",
                                   gender=gen, age_min=max(16, c - 8), age_max=c + 8, register=genre,
                                   screen_share=0.03, description=G.N.ROLE_DESC["featured"])
            p.role_ids.append(rid)
    st.projects[pid] = p
    G.schedule_from_release(cfg, p, f["date"], g)
    _fit_schedule(cfg, p, [st.people[st.roles[r].intended] for r in p.role_ids if st.roles[r].intended], f["date"], g)
    dirs = [x for x in f["directors"] if x in in_world]
    if dirs:
        dperson = st.people[pkey(dirs[0])]
        p.director_id = dperson.id
        dperson.calendar.append({"project_id": pid, "start": p.prepro_start, "end": add_weeks(p.shoot_end, 1), "kind": "direct"})
        dperson.credits.append({"project_id": pid, "title": p.title, "role": "director", "year": year(f["date"]),
                                "genre": genre, "kind": "film", "historical_ref": fkey(fid)})
    if p.release_date < now:
        p.stage = "released"
    elif p.shoot_end <= now:
        p.stage = "post" if add_weeks(p.shoot_end, p.post_weeks) > now else "awaiting_release"
    elif p.shoot_start <= now:
        p.stage = "shooting"
    elif p.prepro_start <= now:
        p.stage = "prepro"
    else:
        p.stage = "development"
    if p.stage in ("released", "post", "awaiting_release", "shooting"):
        _cast_intended(st, cfg, p)
        from ..systems import casting, production
        if not p.director_id:
            casting.attach_director(st, cfg, p, quick=True)
        casting.quick_cast(st, cfg, p)
        if p.stage != "shooting":
            production.wrap(st, cfg, p, quiet=True)
            p.actual_cost = p.budget
    elif p.stage in ("prepro", "development"):
        for rid in p.role_ids:     # agents place holds on the documented cast's dates
            person = st.people.get(st.roles[rid].intended)
            if person:
                person.calendar.append({"project_id": pid, "start": p.shoot_start, "end": add_weeks(p.shoot_end, 1),
                                        "kind": "hold"})
    return p


def _fit_schedule(cfg, p, people, release, g) -> None:
    """Inferred shoot windows are estimates. Use post-production slack so a person's
    documented films do not collide; if no fit exists, keep the estimate (the
    simulation will then treat it as a genuine scheduling conflict)."""
    from ..core.util import overlaps

    def clashes():
        s0, s1 = p.shoot_start, add_weeks(p.shoot_end, 1)
        return any(overlaps(c["start"], c["end"], s0, s1) for x in people for c in x.calendar
                   if c["project_id"] != p.id and c["kind"] in ("shoot", "hold"))
    if not people or not clashes():
        return
    base = p.post_weeks
    for delta in (-2, 2, -4, 4, -6, 6, -8, 8, -10, 10, -12, 12, -14, 14, -16, 16):
        pw = base + delta
        if not 10 <= pw <= 48:
            continue
        p.post_weeks = pw
        G.schedule_from_release(cfg, p, release, g)
        if not clashes():
            return
    p.post_weeks = base
    G.schedule_from_release(cfg, p, release, g)


def _cast_intended(st, cfg, p) -> None:
    from ..systems import casting
    for rid in p.role_ids:
        role = st.roles[rid]
        person = st.people.get(role.intended) if role.intended else None
        if person and casting.available(person, *casting.window(p), ignore_project=p.id):   # actor-directors
            fee = min(casting.ask_fee(st, cfg, person, p), casting.role_budget(cfg, p, role) * 1.5)
            casting._cast(st, cfg, p, role, person, fee=fee, points=0.0, points_type=None, quiet=True)
            person.credits[-1]["historical_ref"] = p.historical_ref
