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
    ("st-col", ("columbia",)), ("st-fox", ("20th century", "twentieth century", "fox")),
    ("st-ua", ("united artists",)), ("st-mgm", ("metro-goldwyn", "mgm")),
    ("st-bv", ("disney", "buena vista", "touchstone")), ("st-ori", ("orion",)),
    ("st-avc", ("avco", "embassy")), ("st-nw", ("new world",)),
]
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


def studio_of(film: dict) -> str:
    low = " | ".join(x.lower() for x in film.get("distributors", []) + film.get("companies", []))
    for sid, keys in STUDIO_KEYS:
        if any(k in low for k in keys):
            return sid
    return "st-ind"


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


def load_historical(st: WorldState, cfg: dict, pack: dict) -> None:
    hc = cfg["history"]
    start = st.date
    infl = market.infl(cfg, year(start))
    films = _apply_local_billing(pack["films"])
    people = pack["people"]
    lookback = add_days(start, -int(hc["lookback_years"] * 365))
    horizon = add_days(start, int(hc["horizon_months"] * 30.5))

    # ---- who is in the world ----
    credits = {}    # pid -> list of (film_id, date, idx)
    directing = {}
    for fid, f in films.items():
        for i, pid in enumerate(f["cast"][: hc["max_billing"]]):
            credits.setdefault(pid, []).append((fid, f["date"], i))
        for pid in f["directors"]:
            directing.setdefault(pid, []).append((fid, f["date"], 0))
    in_world = {}
    for pid in sorted(set(credits) | set(directing)):
        rec = people.get(pid)
        if not rec or not rec.get("birth"):
            continue
        if rec.get("death") and rec["death"] <= start:
            continue
        age = age_on(rec["birth"], start)
        if age < hc["min_age"] or age > 90:
            continue
        cr = credits.get(pid, []) + directing.get(pid, [])
        if not any(lookback <= dt <= horizon for _, dt, _ in cr):
            continue
        in_world[pid] = rec

    # ---- evidence (pre-start for observable; all-time for hindsight) ----
    def reach(f) -> float:
        bo = f.get("box_office_usd")
        s = math.log1p(f.get("sitelinks", 0))
        if bo and bo > 1e5:
            return 0.5 * s + 0.5 * math.log1p(bo / 1e6)
        return 0.85 * s

    ev = {}
    for pid, rec in in_world.items():
        e = {"exposure": 0.0, "lead": 0.0, "recent": 0.0, "older": 0.0, "n_pre": 0, "n_all": 0,
             "first": None, "genres": {}, "lead_all": 0.0, "honours_pre": 0.0, "honours_all": 0.0}
        for fid, dt, idx in credits.get(pid, []):
            f = films[fid]
            r = reach(f)
            bw = BILLING_W[idx] if idx < len(BILLING_W) else 0.15
            e["n_all"] += 1
            if idx <= 1:
                e["lead_all"] += r
            if dt < start:
                yrs = days_between(dt, start) / 365
                dec = math.exp(-yrs / hc["recency_years"])
                e["exposure"] += r * bw * dec
                e["n_pre"] += 1
                if idx <= 1:
                    e["lead"] += r * dec
                (e.__setitem__("recent", e["recent"] + r * bw) if yrs <= 2 else e.__setitem__("older", e["older"] + r * bw))
                e["first"] = min(e["first"] or dt, dt)
                g = genre_of(f["genres"])
                e["genres"][g] = e["genres"].get(g, 0) + bw
        for h in rec.get("honours", []):
            w = _honour_weight(h)
            e["honours_all"] += w
            if h.get("date") and h["date"] < start:
                e["honours_pre"] += w
        e["tv_fame"] = sum(_honour_weight(h) for h in rec.get("honours", [])
                           if "emmy" in h["award"].lower() and h.get("date") and h["date"] < start)
        ev[pid] = e

    actors = [p for p in in_world if p in credits]
    directors = [p for p in in_world if p in directing]
    pct_exp = _pct({p: ev[p]["exposure"] + 0.5 * ev[p]["tv_fame"] for p in actors})
    pct_lead = _pct({p: ev[p]["lead"] for p in actors})
    pct_lead_among_leads = _pct({p: ev[p]["lead"] for p in actors if ev[p]["lead"] > 0})
    hind = {p: 1.0 * ev[p]["honours_all"] + 0.5 * math.log1p(in_world[p].get("sitelinks", 0))
            + 0.3 * math.log1p(ev[p]["lead_all"]) for p in actors}
    pct_hind = _pct(hind)
    pre = {p: 1.0 * ev[p]["honours_pre"] + 0.5 * math.log1p(ev[p]["exposure"]) for p in actors}
    pct_pre = _pct(pre)
    hw = hc["hindsight_weight"]

    ranking = sorted(actors, key=lambda p: -(pct_exp[p] + 0.02 * ev[p]["honours_pre"]))
    tier_a = set(ranking[: hc["tier_a_count"]])
    future_refs = {}
    for fid, f in films.items():
        if f["date"] >= start:
            for pid in f["cast"][: hc["max_billing"]] + f["directors"]:
                future_refs.setdefault(pid, []).append({"ref": f"wd:{fid}", "date": f["date"]})

    for pid in sorted(in_world):
        rec, e = in_world[pid], ev[pid]
        g = R.stream(st.seed, "historical-person", pid)
        roles = (["actor"] if pid in credits else []) + (["director"] if pid in directing else [])
        personality = G._personality(g)
        sex = rec["gender"] if rec["gender"] in ("m", "f") else ("m" if g.random() < 0.5 else "f")
        p = M.Person(id=f"wd:{pid}", name=rec["name"], gender=sex, birth=rec["birth"], roles=roles,
                     tier="A" if pid in tier_a else "B", historical=True,
                     personality=personality, goals=G._goals(g), traits=G.traits_from_personality(personality, g),
                     provenance={"source": "wikidata", "qid": pid, "credits_pre_start": e["n_pre"],
                                 "personality": "prior (not documented)", "documented_credits_after_start":
                                     future_refs.get(pid, [])})
        if "actor" in roles:
            z_h = ND.inv_cdf(min(0.999, max(0.001, pct_hind[pid])))
            z_p = ND.inv_cdf(min(0.999, max(0.001, pct_pre[pid])))
            signal = 0.6 * (hw * z_h + (1 - hw) * z_p)
            p.talent = round(clamp(50 + 14 * signal + hc["talent_noise_sd"] * g.normal(), 5, 98), 2)
            z_l = ND.inv_cdf(min(0.999, max(0.001, _pct_one(pct_lead, pid))))
            p.presence = round(clamp(50 + 14 * 0.5 * z_l + 12 * g.normal(), 5, 98), 2)
            yrs_active = days_between(e["first"], start) / 365 if e["first"] else 0
            p.craft = round(clamp(15 + 0.25 * p.talent + min(30, yrs_active) * 1.3 + min(20, e["n_pre"]) * 0.5
                                  + g.normal(0, 6), 5, 95), 2)
            p.range = {r: round(clamp(0.45 * p.talent + g.normal(25, 12) + 18 * min(1.0, e["genres"].get(r, 0))), 2)
                       for r in M.REGISTERS}
            tot = sum(e["genres"].values()) or 1
            p.typecast = {k: round(min(2.0, v / tot * 1.5), 3) for k, v in e["genres"].items() if v / tot > 0.2}
            p.fame = round(_interp(FAME_QUANTILES, pct_exp[pid]), 5) if e["n_pre"] else 0.0005
            if e["lead"] > 0:
                p.bankability = round(_lin(BANK_QUANTILES, pct_lead_among_leads[pid]), 2)
            else:
                p.bankability = round(clamp(3 + 10 * pct_exp[pid]), 2)
            p.prestige = round(clamp(6 + 25 * math.log1p(e["honours_pre"]) + 18 * pct_exp[pid]), 2)
            p.critical_rep = round(clamp(38 + 5 * e["honours_pre"] + 12 * (pct_pre[pid] - 0.5) + g.normal(0, 6)), 2)
            p.heat = round(clamp(28 * math.log((e["recent"] + 0.5) / (e["older"] / 2 + 0.5)), -60, 60), 2) if e["n_pre"] else 0.0
            p.quote = round(_interp(QUOTE_BY_BANK, p.bankability) * infl, 0) if e["n_pre"] else 0.0
            p.appeal = round(float(clamp(0.5 + 0.25 * (p.presence - 50) / 50 + g.normal(0, 0.08), 0.1, 0.95)), 3)
        if "director" in roles:
            dr = directing[pid]
            pre_n = sum(1 for _, dt, _ in dr if dt < start)
            hon = ev[pid]["honours_all"]
            base = 50 + 6 * math.log1p(hon) + 3 * math.log1p(pre_n)
            p.direction = {k: round(clamp(base + g.normal(0, 13)), 2)
                           for k in ("vision", "technical", "actor_direction", "discipline", "commercial")}
            if "actor" not in roles:
                p.bankability = round(clamp(15 + 8 * pre_n + 4 * ev[pid]["honours_pre"]), 2)
                p.prestige = round(clamp(10 + 6 * pre_n + 8 * ev[pid]["honours_pre"]), 2)
                p.critical_rep = round(clamp(42 + 5 * ev[pid]["honours_pre"] + g.normal(0, 8)), 2)
        p.romance = G._romance(g, p.gender)
        sp_genders = [people[s["id"]]["gender"] for s in rec.get("spouses", []) if s["id"] in people
                      and people[s["id"]]["gender"] in ("m", "f")]
        if sp_genders:
            p.romance["attracted_to"] = sorted(set(sp_genders))
            p.provenance["orientation"] = "from documented spouses"
        else:
            p.provenance["orientation"] = "prior (not documented)"
        p.credits = []
        for fid, dt, idx in sorted(credits.get(pid, []), key=lambda x: x[1]):
            if dt < start:
                p.credits.append({"project_id": None, "title": films[fid]["title"], "historical_ref": f"wd:{fid}",
                                  "role": "lead" if idx == 0 else "colead" if idx == 1 else "supporting",
                                  "year": year(dt), "genre": genre_of(films[fid]["genres"]), "kind": "prior"})
        best = max((c for c in p.credits), key=lambda c: (c["role"] == "lead", c["year"]), default=None)
        desc = rec.get("description") or ("director" if "director" in roles and "actor" not in roles else "actor")
        p.bio = desc[0].upper() + desc[1:] + (f"; known for '{best['title']}' ({best['year']})" if best else "") + "."
        if p.credits:
            p.last_work = add_days(start, -120)
        archetype = ("star" if p.bankability > 55 else "notable" if p.fame > 0.05 else
                     "working" if p.credits else "newcomer")
        p.monthly_costs = cfg["finance"]["default_monthly_costs"][archetype] * infl
        p.cash = round(p.quote * float(g.uniform(0.5, 2.0)) + 3000 * infl, 0)
        p.provenance["archetype"] = archetype
        st.people[p.id] = p

    _documented_relationships(st, cfg, pack, in_world, credits)
    _historical_projects(st, cfg, pack, in_world)
    st.market["history"] = {"version": pack.get("version"), "people": len(in_world),
                            "tier_a": len(tier_a), "source": pack.get("source")}


def _apply_local_billing(films: dict) -> dict:
    """If data/local/imdb_billing.json exists (local-only IMDb enrichment, see
    datapipe/imdb_billing.py), reorder each film's cast to IMDb billing order."""
    from ..core.config import ROOT
    path = ROOT / "data" / "local" / "imdb_billing.json"
    if not path.exists():
        return films
    import json
    billing = json.loads(path.read_text())
    out = {}
    for fid, f in films.items():
        order = billing.get(fid)
        if order:
            rank = {q: i for i, q in enumerate(order)}
            f = dict(f, cast=sorted(f["cast"], key=lambda q: (rank.get(q, 999), f["cast"].index(q))))
        out[fid] = f
    return out


def _pct_one(pct: dict, k) -> float:
    return pct.get(k, 0.5)


# ---------------------------------------------------- relationships/events ---
def _documented_relationships(st, cfg, pack, in_world, credits) -> None:
    start = st.date
    people = pack["people"]
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
    outside = pack.get("spouse_names", {})

    def name_of(q):
        return people.get(q, {}).get("name") or outside.get(q)

    for pid in sorted(in_world):
        me = st.people[f"wd:{pid}"]
        for sp in pack["people"][pid].get("spouses", []):
            other = sp["id"]
            s0, s1 = sp.get("start"), sp.get("end")
            other_in = other in in_world
            if s0 and s0 <= start and (not s1 or s1 > start):        # married at start
                if other_in:
                    if pid < other:
                        you = st.people[f"wd:{other}"]
                        r = st.rel(me.id, you.id)
                        r.status, r.since = "married", s0
                        r.history.append({"date": s0, "text": "married", "delta": 10, "documented": True})
                        for x, y in ((me, you), (you, me)):
                            x.partner_id, x.partner_status = y.id, "married"
                elif me.partner_status is None:
                    me.partner_status = "married_offscreen"
                    me.provenance["spouse_outside_world"] = name_of(other) or "undocumented name"
                if s1 and s1 <= end and (pid < other or not other_in):
                    nm = name_of(other)
                    _event(st, [me.id] + ([f"wd:{other}"] if other_in else []), "divorce" if other_in else "divorce_outside",
                           s1, f"{me.name} and {nm} divorced." if nm else f"{me.name}'s marriage ended in divorce.",
                           {"kind": "relationship" if other_in else "independent"})
                    n += 1
            elif s0 and start < s0 <= end and (pid < other or not other_in):
                met = (min(pid, other), max(pid, other)) in coworkers
                nm = name_of(other)
                _event(st, [me.id] + ([f"wd:{other}"] if other_in else []), "marriage" if other_in else "marriage_outside",
                       s0, f"{me.name} married {nm}." if nm else f"{me.name} married.",
                       {"kind": "relationship" if other_in else "independent", "met_before_start": met,
                        "base_rate_if_never_met": cfg["history"]["marriage_base_rate_if_never_met"]})
                n += 1
        dd = pack["people"][pid].get("death")
        if dd and start < dd <= end:
            manner = set(pack["people"][pid].get("manner_of_death", []))
            kind = "circumstance" if manner & NON_NATURAL else "independent"
            _event(st, [me.id], "death", dd, f"{me.name} died.", {"kind": kind})


def _event(st, people, etype, date, summary, dep) -> None:
    eid = st.new_id("hx")
    st.hist_events[eid] = M.HistoricalEvent(id=eid, people=people, type=etype, date=date, summary=summary,
                                            sources=["Wikidata"], dependency=dep)


# ------------------------------------------------------------- projects ---
def _historical_projects(st, cfg, pack, in_world) -> None:
    hc = cfg["history"]
    start = st.date
    films = pack["films"]
    horizon = add_days(start, int(hc["horizon_months"] * 30.5))
    recent = add_weeks(start, -hc["in_release_weeks"])
    counts = {}
    used = {p.title for p in st.projects.values()}
    sl_pct = _pct({fid: f.get("sitelinks", 0) for fid, f in films.items()})
    for fid, f in sorted(films.items(), key=lambda kv: (kv[1]["date"], kv[0])):
        if not (recent <= f["date"] < horizon):
            continue
        sid = studio_of(f)
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
                      genre=genre, studio_id=studio.id, premise=(f.get("description") or f"A {genre} film.").capitalize() + ".",
                      budget=round(float(budget), 0), created=add_days(start, -400), script_quality=round(script, 2),
                      hook=round(hook, 2), breadth=round(gcfg["breadth"] * math.exp((hook - 50) / 50 * 0.6) * math.exp(g.normal(0, 0.3)), 4),
                      historical_ref=f"wd:{fid}")
        tilt_noise = g.dirichlet([6, 6, 6, 6]) * 4
        p.segment_tilt = {s: round(float(t * n), 3) for s, t, n in zip(cfg["box_office"]["segments"], gcfg["tilt"], tilt_noise)}
        real_m = budget / 1e6 / market.infl(cfg, year(f["date"]))
        p.shoot_weeks = max(4, int(round(g.uniform(*gcfg["shoot_weeks"]) + max(0, math.log(max(real_m, 0.5) / 8)) * 2)))
        p.post_weeks = int(g.integers(*cfg["development"]["post_weeks"]))
        used.add(p.title)
        # roles from billing order
        cast = [c for c in f["cast"][: hc["max_billing"]] if c in in_world][:4]
        for i, cpid in enumerate(cast):
            person = st.people[f"wd:{cpid}"]
            imp = "lead" if i == 0 else "colead" if i == 1 else "supporting"
            age = age_on(person.birth, f["date"])
            rid = st.new_id("rol")
            role = M.Role(id=rid, project_id=pid, name=f"role {i + 1}", importance=imp, gender=person.gender,
                          age_min=max(8, age - 6), age_max=age + 6, register=genre,
                          screen_share={"lead": 0.45, "colead": 0.28, "supporting": 0.09}[imp],
                          description=G.N.ROLE_DESC[imp], intended=person.id)
            st.roles[rid] = role
            p.role_ids.append(rid)
        if not p.role_ids:
            G._make_roles(st, cfg, p, g)
        st.projects[pid] = p
        G.schedule_from_release(cfg, p, f["date"], g)
        dirs = [x for x in f["directors"] if x in in_world]
        if dirs:
            dperson = st.people[f"wd:{dirs[0]}"]
            p.director_id = dperson.id
            dperson.calendar.append({"project_id": pid, "start": p.prepro_start, "end": add_weeks(p.shoot_end, 1), "kind": "direct"})
            dperson.credits.append({"project_id": pid, "title": p.title, "role": "director", "year": year(f["date"]),
                                    "genre": genre, "kind": "film", "historical_ref": f"wd:{fid}"})
        if p.release_date < start:
            p.stage = "released"
        elif p.shoot_end <= start:
            p.stage = "post" if add_weeks(p.shoot_end, p.post_weeks) > start else "awaiting_release"
        elif p.shoot_start <= start:
            p.stage = "shooting"
        elif p.prepro_start <= start:
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
        counts[studio.id] = counts.get(studio.id, 0) + 1
    st.market["historical_slate"] = counts


def _cast_intended(st, cfg, p) -> None:
    from ..systems import casting
    for rid in p.role_ids:
        role = st.roles[rid]
        person = st.people.get(role.intended) if role.intended else None
        if person and casting.available(person, *casting.window(p)):
            fee = min(casting.ask_fee(st, cfg, person, p), casting.role_budget(cfg, p, role) * 1.5)
            casting._cast(st, cfg, p, role, person, fee=fee, points=0.0, points_type=None, quiet=True)
            person.credits[-1]["historical_ref"] = p.historical_ref
