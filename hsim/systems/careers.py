"""Career evolution: heat, bankability, fame, appeal, critical reputation,
typecasting, ageing, retirement and new entrants. Identical for player and NPCs.
"""
from __future__ import annotations

import math

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import age_on, clamp, days_between, year
from . import decisions as D
from . import market

IMP_W = {"lead": 1.0, "colead": 0.55, "supporting": 0.15, "featured": 0.04}


def _cast(st, p):
    for rid in p.role_ids:
        r = st.roles[rid]
        if r.cast_id:
            yield r, st.people[r.cast_id]


def on_release_reviews(st: WorldState, cfg: dict, p) -> None:
    """Critics react to performances when the film opens."""
    lr = cfg["careers"]["critical_lr"]
    for r, a in _cast(st, p):
        view = 0.6 * (r.performance or 50) + 0.4 * (p.critic_score or 50)
        a.critical_rep = round(clamp(a.critical_rep + lr * IMP_W[r.importance] * (view - a.critical_rep)), 2)
        if (p.critic_score or 0) >= 75:
            a.prestige = round(clamp(a.prestige + (p.critic_score - 70) / 5 * IMP_W[r.importance]), 2)
    d = st.people.get(p.director_id)
    if d:
        d.critical_rep = round(clamp(d.critical_rep + lr * ((p.critic_score or 50) - d.critical_rep)), 2)


def on_opening(st: WorldState, cfg: dict, p) -> None:
    """Industry reads the opening against expectations (heat) and re-estimates
    who 'opens' films (bankability). Attribution deliberately over-credits leads."""
    c = cfg["careers"]
    infl = market.infl(cfg, year(st.date))
    expected = max(p.forecast_opening or 1.0, 1.0)
    surprise = clamp(math.log(max(p.opening, 1.0) / expected), -1.5, 1.5)
    real_open_m = p.opening / 1e6 / infl
    real_budget_m = p.budget / 1e6 / infl
    signal = clamp(50 + 22 * math.log(max(real_open_m, 0.01) / max(0.35 * real_budget_m, 0.05)))
    for r, a in _cast(st, p):
        w = IMP_W[r.importance]
        a.heat = round(clamp(a.heat + 25 * surprise * w, -100, 100), 2)
        a.bankability = round(clamp(a.bankability + c["bankability_lr"] * w * (signal - a.bankability)), 2)
    d = st.people.get(p.director_id)
    if d:
        d.heat = round(clamp(d.heat + 20 * surprise, -100, 100), 2)
        d.bankability = round(clamp(d.bankability + 0.2 * (signal - d.bankability)), 2)
    if abs(surprise) > 0.45:
        word = "beat" if surprise > 0 else "fell short of"
        st.log("trade_verdict", f"Trades: '{p.title}' {word} industry expectations on its opening.",
               refs={"project": p.id}, salience=2 if any(a.controller == "player" for _, a in _cast(st, p)) else 1,
               public=True)


def on_run_end(st: WorldState, cfg: dict, p) -> None:
    c = cfg["careers"]
    pop = sum(sg["pop"] for sg in p.run["segments"].values())
    reach = sum(sg["watched"] for sg in p.run["segments"].values()) / pop
    sat = p.satisfaction or 0.5
    for r, a in _cast(st, p):
        mem = c["memorability"][r.importance] * (0.6 + 0.8 * a.presence / 100)
        a.fame = round(1 - (1 - a.fame) * (1 - min(0.9, reach * mem * 1.4)), 5)
        perf_f = ((r.performance or 50) - 50) / 50
        a.appeal = round(clamp(a.appeal + 0.12 * IMP_W[r.importance] * ((sat - 0.55) + 0.5 * perf_f), 0.05, 0.98), 4)
        tc = a.typecast
        for k in list(tc):
            tc[k] = round(tc[k] * 0.93, 4)
        tc[p.genre] = round(min(2.0, tc.get(p.genre, 0) + 0.3 * IMP_W[r.importance] * (0.6 + sat)), 4)


def step(st: WorldState, cfg: dict) -> None:
    c = cfg["careers"]
    fame_decay = 1 - c["fame_decay_yearly"] / 52
    for pid, p in sorted(st.people.items()):
        if p.death:
            continue
        p.heat = round(p.heat * c["heat_decay_weekly"], 3)
        p.fame = round(p.fame * fame_decay, 6)
        working = any(cc["start"] <= st.date <= cc["end"] for cc in p.calendar)
        if not working:
            p.energy = clamp(p.energy + cfg["production"]["energy_recovery_per_week"])
    if st.date[5:10] <= "01-07":   # first tick of the year
        _yearly(st, cfg)


def _yearly(st: WorldState, cfg: dict) -> None:
    from ..world.genesis import make_actor
    c = cfg["careers"]
    yr = year(st.date)
    if st.market.get("yearly_done") == yr:
        return
    st.market["yearly_done"] = yr
    for pid, p in sorted(st.people.items()):
        if p.death or not p.active or p.controller == "player":
            continue
        g = R.stream(st.seed, "yearly", pid, yr)
        age = age_on(p.birth, st.date)
        idle_years = days_between(p.last_work, st.date) / 365 if p.last_work else (2 if p.provenance.get("archetype") == "newcomer" else 0)
        if idle_years > c["retire_idle_years"] and p.fame < 0.05 and g.random() < 0.5:
            p.active = False
            continue
        if age > 68 and g.random() < 0.08 + (age - 68) * 0.02:
            p.active = False
            if p.fame > 0.15:
                st.log("retirement", f"{p.name} has quietly stepped away from acting.", actors=[pid], salience=1)
    # new fictional entrants keep the talent pipeline realistic
    n = cfg["world"]["new_actors_per_year"]
    for i in range(n):
        a = make_actor(st, cfg, f"y{yr}-{i:04d}", st.date, archetype="newcomer")
        st.people[a.id] = a
    from ..world.genesis import assign_agents
    from ..world import people as PEOPLE
    assign_agents(st, cfg, yearly=True)
    for pid, person in sorted(st.people.items()):
        if not person.persona:
            PEOPLE.give_persona(st, person, pid)
    PEOPLE.assign_agent_people(st)


@D.handler("agency_offer")
def _agency_offer(st, cfg, dec, choice, params) -> str:
    ag = st.agencies[dec.refs["agency"]]
    if choice == "accept":
        st.player.agent_id = ag.id
        from ..world import people as PEOPLE
        PEOPLE.assign_agent_people(st)
        agent = st.people.get(st.player.agent_person_id)
        st.log("new_agent", f"You signed with {ag.name}" + (f"; your agent is {agent.name}." if agent else "."),
               actors=[st.player_id] + ([agent.id] if agent else []), salience=3, public=False)
        return f"You signed with {ag.name}."
    return f"You declined representation from {ag.name}."
