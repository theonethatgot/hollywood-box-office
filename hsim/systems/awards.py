"""Awards v0: Academy-style acting, directing and picture categories.

Nominees come from a simulated voter body scoring films released in the prior
calendar year: performance quality, critical standing, prestige, a late-year
release bonus (voter memory) and voter noise. Winners are a softmax draw over
nominee scores. Effects flow into prestige, heat and quote.
"""
from __future__ import annotations

import math

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import clamp, week_of_year, year

CATS = [("Best Actor", "lead", "m"), ("Best Actress", "lead", "f"),
        ("Best Supporting Actor", "supporting", "m"), ("Best Supporting Actress", "supporting", "f")]


def _eligible(st, yr):
    return [p for _, p in sorted(st.projects.items())
            if p.stage == "released" and p.release_date and year(p.release_date) == yr and p.critic_score is not None]


def step(st: WorldState, cfg: dict) -> None:
    a = cfg["awards"]
    yr = year(st.date)
    store = st.market.setdefault("awards", {})
    key = str(yr)
    wk = week_of_year(st.date)
    if wk >= a["nomination_week"] and key not in store and year(st.start_date) < yr:
        store[key] = _nominate(st, cfg, yr - 1)
    elif wk >= a["ceremony_week"] and key in store and not store[key].get("winners"):
        _ceremony(st, cfg, store[key], yr)


def _late_bonus(p) -> float:
    m = int(p.release_date[5:7])
    return 4.0 if m >= 10 else 1.5 if m >= 7 else 0.0


def _nominate(st, cfg, film_year) -> dict:
    a = cfg["awards"]
    films = _eligible(st, film_year)
    out = {"film_year": film_year, "categories": {}, "winners": None}
    for cat, imp, gender in CATS:
        cands = []
        for p in films:
            for rid in p.role_ids:
                r = st.roles[rid]
                if not r.cast_id:
                    continue
                person = st.people[r.cast_id]
                if person.gender != gender:
                    continue
                if (imp == "lead") != (r.importance in ("lead", "colead")):
                    continue
                g = R.stream(st.seed, "oscar-vote", cat, r.id)
                score = (0.55 * (r.performance or 40) + 0.3 * p.critic_score + 0.1 * person.prestige
                         + _late_bonus(p) + (3 if p.genre == "drama" else 0) + g.normal(0, a["noise_sd"]))
                cands.append((score, person.id, p.id))
        cands.sort(key=lambda x: (-x[0], x[1]))
        out["categories"][cat] = [{"person": pid, "project": prj, "score": round(s, 2)} for s, pid, prj in cands[:a["slots"]]]
    pics = []
    for p in films:
        g = R.stream(st.seed, "oscar-vote", "picture", p.id)
        s = 0.5 * p.critic_score + 0.3 * p.quality.get("overall", 50) + _late_bonus(p) + (4 if p.genre == "drama" else 0) + g.normal(0, a["noise_sd"])
        pics.append((s, p.id))
    pics.sort(key=lambda x: (-x[0], x[1]))
    out["categories"]["Best Picture"] = [{"project": prj, "score": round(s, 2)} for s, prj in pics[:a["slots"]]]
    out["categories"]["Best Director"] = [{"person": st.projects[prj].director_id, "project": prj, "score": sc}
                                          for sc, prj in [(x["score"], x["project"]) for x in out["categories"]["Best Picture"]]
                                          if st.projects[prj].director_id]
    lines = []
    for cat, noms in out["categories"].items():
        names = []
        for n in noms:
            if "person" in n:
                person = st.people[n["person"]]
                names.append(f"{person.name} ('{st.projects[n['project']].title}')")
                person.prestige = round(clamp(person.prestige + 8), 2)
                person.heat = round(clamp(person.heat + 8, -100, 100), 2)
                person.awards.append({"year": film_year + 1, "award": "Academy Award", "category": cat,
                                      "result": "nominated", "project_id": n["project"]})
                if person.controller == "player":
                    st.log("nomination", f"You were nominated for {cat} for '{st.projects[n['project']].title}'.",
                           actors=[person.id], salience=5, public=True)
            else:
                names.append(f"'{st.projects[n['project']].title}'")
        lines.append(f"{cat}: {', '.join(names)}")
    st.log("oscar_nominations", f"Academy Award nominations announced for {film_year} films. " + " | ".join(lines),
           salience=2, public=True)
    return out


def _ceremony(st, cfg, rec, yr) -> None:
    a = cfg["awards"]
    winners = {}
    for cat, noms in rec["categories"].items():
        if not noms:
            continue
        g = R.stream(st.seed, "oscar-win", yr, cat)
        w = [math.exp(n["score"] / a["win_temperature"]) for n in noms]
        tot = sum(w)
        u, acc, pick = g.random() * tot, 0.0, noms[-1]
        for n, x in zip(noms, w):
            acc += x
            if u <= acc:
                pick = n
                break
        winners[cat] = pick
        if "person" in pick:
            person = st.people[pick["person"]]
            person.prestige = round(clamp(person.prestige + 20), 2)
            person.heat = round(clamp(person.heat + 15, -100, 100), 2)
            person.quote = round(person.quote * 1.35, 0)
            for aw in person.awards:
                if aw["category"] == cat and aw["year"] == yr:
                    aw["result"] = "won"
    rec["winners"] = winners
    parts = []
    for cat, n in winners.items():
        if "person" in n:
            parts.append(f"{cat}: {st.people[n['person']].name}")
        else:
            parts.append(f"{cat}: '{st.projects[n['project']].title}'")
    st.log("oscars", f"At the Academy Awards: " + "; ".join(parts) + ".", salience=3, public=True)
    pl = st.player_id
    for cat, n in winners.items():
        if n.get("person") == pl:
            st.log("oscar_win", f"You won the Academy Award for {cat}.", actors=[pl], salience=5, public=True)
