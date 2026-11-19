"""Production lifecycle: prepro → shooting → wrap → post.

Weekly shooting creates contact between cast and director (relationships,
possible conflicts, possible romance), cost overruns, energy drain. At wrap,
performances and the film's hidden quality vector are computed.
"""
from __future__ import annotations

import math

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_weeks, clamp, year
from . import finance, market


def step(st: WorldState, cfg: dict) -> None:
    st.market["contacts"] = []
    for pid, p in sorted(st.projects.items()):
        if p.stage == "development" and p.prepro_start and p.prepro_start <= st.date:
            p.stage = "prepro"
        if p.stage == "prepro" and p.shoot_start <= st.date:
            _try_start(st, cfg, p)
        elif p.stage == "shooting":
            if p.shoot_end <= st.date:
                wrap(st, cfg, p)
            else:
                _shoot_week(st, cfg, p)
        elif p.stage == "post" and add_weeks(p.shoot_end, p.post_weeks) <= st.date:
            from . import release
            release.schedule(st, cfg, p)


def _cast_people(st, p):
    return [st.people[st.roles[r].cast_id] for r in p.role_ids if st.roles[r].cast_id]


def _try_start(st, cfg, p) -> None:
    roles = [st.roles[r] for r in p.role_ids]
    if p.director_id and all(r.cast_id for r in roles):
        p.stage = "shooting"
        p.shoot_end = add_weeks(st.date, p.shoot_weeks)
        for r in roles:
            from .casting import commit
            commit(st.people[r.cast_id], p)
            finance.pay(st, cfg, r.cast_id, r.fee * cfg["finance"]["fee_paid_at_start"],
                        f"first half of fee for '{p.title}'")
        involved = any(st.people[r.cast_id].controller == "player" for r in roles)
        st.log("shoot_start", f"Principal photography began on '{p.title}' in {p.location} "
                              f"({p.shoot_weeks} weeks scheduled).",
               actors=[r.cast_id for r in roles] + [p.director_id], refs={"project": p.id},
               salience=3 if involved else 0, public=involved)
        return
    # casting not finished: slip the start date
    p.delays += 1
    p.shoot_start = add_weeks(p.shoot_start, 2)
    p.shoot_end = add_weeks(p.shoot_start, p.shoot_weeks)
    if p.delays > 8:
        p.stage = "dead"
        for r in roles:
            if r.cast_id:
                person = st.people[r.cast_id]
                person.calendar = [c for c in person.calendar if c["project_id"] != p.id]
        if p.director_id:
            d = st.people[p.director_id]
            d.calendar = [c for c in d.calendar if c["project_id"] != p.id]
        st.log("shelved", f"{st.studios[p.studio_id].name} shelved '{p.title}' after casting stalled.",
               refs={"project": p.id}, salience=1)
    else:
        for r in roles:
            if r.cast_id:
                from .casting import commit
                commit(st.people[r.cast_id], p)


def _shoot_week(st, cfg, p) -> None:
    pc = cfg["production"]
    g = R.stream(st.seed, "shoot-week", p.id, st.date)
    director = st.people.get(p.director_id)
    disc = director.direction.get("discipline", 50) if director else 50
    overrun = max(0.0, g.normal(0.002 + (50 - disc) / 5000, pc["overrun_weekly_sd"]))
    p.actual_cost += p.budget / max(1, p.shoot_weeks) * (1 + overrun)
    people = _cast_people(st, p) + ([director] if director else [])
    for x in people:
        x.energy = clamp(x.energy - pc["energy_cost_per_week"])
    for i, a in enumerate(people):
        for b in people[i + 1:]:
            r = st.rel(a.id, b.id)
            r.contact_weeks += 1
            st.market["contacts"].append([r.a, r.b, p.id])
            temper = (a.personality.get("temperament", 50) + b.personality.get("temperament", 50)) / 200
            ego = (a.personality.get("ego", 50) + b.personality.get("ego", 50)) / 200
            pc_conf = pc["conflict_base"] * (0.5 + temper + ego) * (1.3 - (r.affinity + 100) / 250)
            if g.random() < pc_conf:
                delta = -float(g.uniform(4, 14))
                r.affinity = clamp(r.affinity + delta, -100, 100)
                r.history.append({"date": st.date, "text": f"clashed on the set of '{p.title}'", "delta": round(delta, 1)})
                if a.controller == "player" or b.controller == "player":
                    other = b if a.controller == "player" else a
                    st.log("set_conflict", f"Tension on the set of '{p.title}': you clashed with {other.name}.",
                           actors=[a.id, b.id], refs={"project": p.id}, salience=3, public=False)
            else:
                warmth = (a.personality.get("warmth", 50) + b.personality.get("warmth", 50)) / 100
                r.affinity = clamp(r.affinity + pc["bond_gain"] * warmth * float(g.uniform(0.3, 1.0)), -100, 100)


def wrap(st: WorldState, cfg: dict, p, quiet: bool = False) -> None:
    g = R.stream(st.seed, "wrap", p.id)
    director = st.people.get(p.director_id)
    dd = director.direction if director else {}
    perfs, shares = [], []
    for rid in p.role_ids:
        role = st.roles[rid]
        if not role.cast_id:
            continue
        a = st.people[role.cast_id]
        from .casting import fit
        base = 100 * ((a.talent / 100) ** 0.5) * ((a.craft / 100) ** 0.3) * ((a.range.get(role.register, 40) / 100) ** 0.2)
        perf = base * (0.7 + 0.3 * fit(a, role, st.date)) * (1 + 0.15 * (dd.get("actor_direction", 50) - 50) / 50)
        perf *= 0.85 + 0.15 * a.energy / 100
        perf = clamp(perf + g.normal(0, 5), 1, 100)
        role.performance = round(perf, 2)
        perfs.append(perf)
        shares.append(role.screen_share)
        if not quiet:
            gain = cfg["production"]["craft_gain"] * (role.screen_share / 0.45) * (0.6 + dd.get("actor_direction", 50) / 100)
            a.craft = round(clamp(a.craft + gain * (1 - a.craft / 110)), 2)
            a.last_work = st.date
            finance.pay(st, cfg, a.id, role.fee * (1 - cfg["finance"]["fee_paid_at_start"]),
                        f"second half of fee for '{p.title}'")
        a.calendar = [c for c in a.calendar if c["project_id"] != p.id]
    lead_perf = sum(x * s for x, s in zip(perfs, shares)) / max(1e-9, sum(shares)) if perfs else 40
    presence = [st.people[st.roles[r].cast_id].presence for r in p.role_ids if st.roles[r].cast_id] or [50]
    real_m = p.budget / 1e6 / market.infl(cfg, year(st.date))
    budget_level = clamp(50 + 15 * math.log(max(real_m, 0.2) / 8))
    q = {
        "craft": 0.6 * dd.get("technical", 50) + 0.25 * budget_level + 0.15 * dd.get("discipline", 50),
        "entertainment": 0.45 * p.script_quality + 0.2 * dd.get("commercial", 50) + 0.2 * lead_perf + 0.15 * (sum(presence) / len(presence)),
        "emotional": 0.35 * p.script_quality + 0.45 * lead_perf + 0.2 * dd.get("vision", 50),
        "originality": 0.55 * p.script_quality + 0.45 * dd.get("vision", 50),
        "spectacle": 0.5 * budget_level + 0.5 * dd.get("technical", 50),
    }
    q = {k: round(clamp(v + g.normal(0, 4)), 2) for k, v in q.items()}
    q["overall"] = round(0.33 * q["entertainment"] + 0.25 * q["emotional"] + 0.2 * q["craft"] + 0.22 * q["originality"], 2)
    p.quality = q
    if director:
        director.calendar = [c for c in director.calendar if c["project_id"] != p.id]
        director.last_work = st.date
    if not quiet:
        p.stage = "post"
        involved = any(st.people[st.roles[r].cast_id].controller == "player" for r in p.role_ids if st.roles[r].cast_id)
        st.log("wrap", f"'{p.title}' wrapped principal photography and moved into post-production.",
               actors=[st.roles[r].cast_id for r in p.role_ids if st.roles[r].cast_id], refs={"project": p.id},
               salience=3 if involved else 0, public=involved)
