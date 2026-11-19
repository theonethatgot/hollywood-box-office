"""Jobbing work v0: the everyday market that keeps working actors working.

Feature-film principal roles are only part of an actor's life. Guest spots,
commercials, bit parts, TV movies and stage work pay the rent, build craft and
keep a name circulating. This is a deliberately light model (full TV careers are
Phase 5): offers arrive through agents at rates that depend on representation,
standing and craft; the same rules apply to every actor; the protagonist
decides (or delegates via standing orders).
"""
from __future__ import annotations

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_days, add_weeks, clamp, money, year
from . import decisions as D
from . import finance, market

KINDS = [  # name, weeks, pay (1980 $) low..high, craft gain, fame gain, weight
    ("a guest role on a network TV drama", 1, (2500, 6000), 0.6, 0.002, 3),
    ("a guest spot on a sitcom", 1, (2000, 5000), 0.5, 0.002, 3),
    ("a national TV commercial", 1, (1500, 9000), 0.1, 0.001, 3),
    ("a small part in a feature film", 2, (3000, 9000), 0.7, 0.001, 2),
    ("a supporting role in a TV movie", 3, (6000, 15000), 1.0, 0.004, 1.5),
    ("a stage production", 6, (3000, 8000), 1.6, 0.0005, 1),
]


def _rate(st, cfg, p) -> float:
    jc = cfg["jobbing"]
    ag = st.agencies.get(p.agent_id) if p.agent_id else None
    agent_f = {1: 1.4, 2: 1.0, 3: 0.7}[ag.tier] * (0.6 + ag.hustle / 125) if ag else jc["no_agent_factor"]
    standing = 0.5 + p.craft / 120 + min(0.6, p.fame * 8) + max(-0.3, min(0.3, p.heat / 150))
    stardom = 1.0 if p.bankability < 50 else max(0.1, 1 - (p.bankability - 50) / 40)   # stars rarely take these
    return jc["base_weekly"] * agent_f * standing * stardom


def _busy(p, start, end) -> bool:
    from .casting import available
    return not available(p, start, end)


def step(st: WorldState, cfg: dict) -> None:
    infl = market.infl(cfg, year(st.date))
    weights = [k[5] for k in KINDS]
    for pid, p in sorted(st.people.items()):
        if "actor" not in p.roles or not p.active or p.death:
            continue
        if R.unit(st.seed, "jobbing", pid, st.date) >= _rate(st, cfg, p):
            continue
        g = R.stream(st.seed, "job", pid, st.date)
        k = KINDS[int(g.choice(len(KINDS), p=[w / sum(weights) for w in weights]))]
        name, weeks, (lo, hi), craft_gain, fame_gain, _ = k
        start = add_days(st.date, 7 * int(g.integers(1, 4)))
        end = add_weeks(start, weeks)
        if _busy(p, start, end):
            continue
        pay = round(float(g.uniform(lo, hi)) * infl * (1 + min(1.0, p.fame * 5)), -2)
        job = {"name": name, "start": start, "end": end, "pay": pay, "craft": craft_gain, "fame": fame_gain}
        if p.controller == "player":
            _offer_player(st, cfg, p, job)
        else:
            _take(st, cfg, p, job)


def _offer_player(st, cfg, p, job) -> None:
    text = f"{job['name'].capitalize()}, {job['start']} to {job['end']}, paying {money(job['pay'])}."
    if st.orders.get("auto_accept_jobs", True):
        _take(st, cfg, p, job)
        st.delegated.append({"rule": "auto_accept_jobs", "decision": None, "text": f"Your agent booked you: {text}"})
        return
    D.create(st, cfg, "job", f"Work offer: {text}", ["accept", "decline"], deadline_days=6, default="decline",
             refs={"job": job}, interrupt="jobs" in st.orders.get("interrupt_on", []))


@D.handler("job")
def _job_choice(st, cfg, dec, choice, params) -> str:
    job = dec.refs["job"]
    if choice == "accept":
        if _busy(st.player, job["start"], job["end"]):
            return "The dates no longer work; your agent passed."
        _take(st, cfg, st.player, job)
        return f"Booked: {job['name']}."
    return f"You passed on {job['name']}."


def _take(st, cfg, p, job) -> None:
    jid = st.new_id("job")
    p.calendar.append({"project_id": jid, "start": job["start"], "end": job["end"], "kind": "job"})
    pending = st.market.setdefault("jobs", [])
    pending.append({"id": jid, "person": p.id, **job})
    if p.controller == "player":
        st.log("job_booked", f"Booked {job['name']} ({job['start']} to {job['end']}, {money(job['pay'])}).",
               actors=[p.id], salience=2, public=False)


def settle(st: WorldState, cfg: dict) -> None:
    """Pay and credit jobs that finished this week."""
    keep = []
    for j in st.market.get("jobs", []):
        if j["end"] > st.date:
            keep.append(j)
            continue
        p = st.people.get(j["person"])
        if p is None or p.death:
            continue
        finance.pay(st, cfg, p.id, j["pay"], j["name"])
        p.craft = round(clamp(p.craft + j["craft"] * (1 - p.craft / 110)), 2)
        p.fame = round(min(0.95, p.fame + j["fame"]), 6)
        p.last_work = st.date
        p.calendar = [c for c in p.calendar if c["project_id"] != j["id"]]
        if p.controller == "player":
            st.log("job_done", f"Wrapped {j['name']}.", actors=[p.id], salience=1, public=False)
    st.market["jobs"] = keep
