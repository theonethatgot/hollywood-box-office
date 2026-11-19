"""Packaging and casting: directors, shortlists, auditions, offers, negotiation.

Everything is decided on OBSERVED values (bankability, critics' view, a noisy
read of talent), never on true talent. Player and NPC candidates are scored by
the same functions; only the *response* to an invitation/offer differs, and
even that falls back to NPC utility when delegated.
"""
from __future__ import annotations

import math

from .. import models as M
from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_days, add_weeks, age_on, clamp, money, overlaps, year
from . import decisions as D
from . import market


# --------------------------------------------------------------- helpers ---
def available(p: M.Person, start: str, end: str, ignore_project: str | None = None) -> bool:
    if p.death or not p.active:
        return False
    return not any(overlaps(c["start"], c["end"], start, end) for c in p.calendar
                   if c["project_id"] != ignore_project)


def commit(p: M.Person, proj: M.Project, kind: str = "shoot") -> None:
    p.calendar = [c for c in p.calendar if c["project_id"] != proj.id]
    p.calendar.append({"project_id": proj.id, "start": proj.shoot_start, "end": add_weeks(proj.shoot_end, 1),
                       "kind": kind})


def window(proj: M.Project):
    return proj.shoot_start, add_weeks(proj.shoot_end, 1)


def principal_roles(st: WorldState, proj: M.Project):
    return [st.roles[r] for r in proj.role_ids]


def scale_total(cfg, proj: M.Project, date: str) -> float:
    return market.sag_scale_week(cfg, date) * (proj.shoot_weeks + 1)


def role_budget(cfg, proj: M.Project, role: M.Role) -> float:
    pool = proj.budget * cfg["genres"][proj.genre]["atl_share"]
    return pool * cfg["casting"]["atl_role_share"][role.importance]


def star_weight(cfg, proj: M.Project, role: M.Role, date: str) -> float:
    base = cfg["casting"]["star_weight_by_role"][role.importance]
    real_m = proj.budget / 1e6 / market.infl(cfg, year(date))
    return base * clamp(real_m / cfg["casting"]["budget_star_pivot_m"], 0.3, 2.5) * max(0.3, 1 - 0.3 * proj.delays)


def perceived_talent(st: WorldState, cfg, proj: M.Project, p: M.Person) -> float:
    """The industry's noisy read of an actor's ability (fixed per project/person)."""
    noise = R.gauss(st.seed, "talent-read", proj.id, p.id) * cfg["casting"]["talent_obs_noise"]
    return 0.45 * p.talent + 0.20 * p.craft + 0.35 * p.critical_rep + noise


def fit(p: M.Person, role: M.Role, date: str) -> float:
    age = age_on(p.birth, date)
    mid = (role.age_min + role.age_max) / 2
    age_fit = math.exp(-((age - mid) / max(4.0, (role.age_max - role.age_min) / 1.6)) ** 2)
    reg = p.range.get(role.register, 40) / 100
    tc = p.typecast.get(role.register, 0.0)
    return age_fit * (0.55 + 0.45 * reg) * (1 + 0.15 * tc)


def ask_fee(st, cfg, p: M.Person, proj: M.Project) -> float:
    return max(scale_total(cfg, proj, st.date), p.quote * (1 + clamp(p.heat, -50, 50) / 200))


def agency_visibility(st, p: M.Person) -> float:
    ag = st.agencies.get(p.agent_id) if p.agent_id else None
    if ag is None:
        return -12.0
    return {1: 6.0, 2: 0.0, 3: -5.0}[ag.tier] + (ag.hustle - 50) / 10


def casting_utility(st: WorldState, cfg, proj: M.Project, role: M.Role, p: M.Person,
                    sw: float | None = None, rb: float | None = None) -> float:
    sw = star_weight(cfg, proj, role, st.date) if sw is None else sw
    rb = role_budget(cfg, proj, role) if rb is None else rb
    f = fit(p, role, st.date)
    talent = perceived_talent(st, cfg, proj, p)
    cost_ratio = ask_fee(st, cfg, p, proj) / max(1.0, rb)
    rel = 0.0
    for who in (proj.director_id, proj.casting_director_id):
        if who:
            r = st.rel(who, p.id, create=False)
            rel += r.affinity / 3 if r else 0.0         # directors and CDs remember people
    taste = cfg["casting"]["shortlist_noise"] * R.gauss(st.seed, "casting-taste", role.id, p.id)
    return (sw * p.bankability * 0.6 + 0.5 * talent + 45 * f + rel + agency_visibility(st, p)
            - 25 * max(0.0, cost_ratio - 1.2) + taste)


_INDEX: dict = {}


def _actor_index(st: WorldState) -> dict:
    """Actors by gender, rebuilt once per simulated week (cheap pre-filter)."""
    key = (st.date, len(st.people))
    if _INDEX.get("world") is not st or _INDEX.get("key") != key:   # identity check: ids can be reused
        by = {}
        for p in st.actors():
            by.setdefault(p.gender, []).append(p)
        _INDEX.clear()
        _INDEX.update({"world": st, "key": key, "by_gender": by})
    return _INDEX["by_gender"]


def candidate_pool(st: WorldState, cfg, proj: M.Project, role: M.Role) -> list:
    start, end = window(proj)
    cast_ids = {st.roles[r].cast_id for r in proj.role_ids if st.roles[r].cast_id}
    out = []
    for p in _actor_index(st).get(role.gender, []):
        if p.gender != role.gender or p.id in cast_ids or p.id in role.tried:
            continue
        age = age_on(p.birth, st.date)
        if not (role.age_min - 6 <= age <= role.age_max + 6):
            continue
        if not available(p, start, end):
            continue
        out.append(p)
    return out


# -------------------------------------------------------------- directors ---
def attach_director(st: WorldState, cfg, proj: M.Project, quick: bool = False) -> bool:
    """Studio ranks available directors; each director decides whether the project
    suits them (genre, budget level vs their standing, how active they are)."""
    if proj.director_id:
        return True
    start, end = proj.prepro_start or st.date, add_weeks(proj.shoot_end or st.date, 1)
    g = R.stream(st.seed, "director-pick", proj.id, st.date)
    real_m = proj.budget / 1e6 / market.infl(cfg, year(st.date))
    ranked = []
    for p in st.directors():
        if not available(p, start, end):
            continue
        standing = 0.6 * p.prestige + 0.4 * p.bankability
        affordability = max(0.0, standing - (30 + 2.5 * real_m)) * 0.9   # big names cost more than small films pay
        u = (p.direction.get("commercial", 50) * (0.3 + 0.05 * real_m) + p.bankability * 0.3
             + p.prestige * 0.2 + p.direction.get("vision", 50) * 0.2 + 25 * director_genre_fit(p, proj.genre)
             - affordability + g.normal(0, 12))
        ranked.append((u, p.id, p))
    ranked.sort(key=lambda x: (-x[0], x[1]))
    for u, _, p in ranked[:25]:
        if director_accepts(st, cfg, p, proj, real_m):
            proj.director_id = p.id
            p.calendar.append({"project_id": proj.id, "start": start, "end": end, "kind": "direct"})
            p.credits.append({"project_id": proj.id, "title": proj.title, "role": "director",
                              "year": year(proj.release_date or proj.shoot_end or st.date), "genre": proj.genre,
                              "kind": "film"})
            if not quick:
                st.log("director_attached", f"{p.name} will direct '{proj.title}' for {st.studios[proj.studio_id].name}.",
                       actors=[p.id], refs={"project": proj.id}, salience=1)
            return True
    return False


def director_genre_fit(p: M.Person, genre: str) -> float:
    films = [c for c in p.credits if c.get("role") == "director" and c.get("genre")]
    if not films:
        return 0.5
    return sum(1 for c in films if c["genre"] == genre) / len(films)


def director_accepts(st, cfg, p: M.Person, proj: M.Project, real_m: float) -> bool:
    """Would this director take this job? Established names turn down small generic work;
    long-idle older directors are less likely to come back for it."""
    from ..core.util import age_on
    standing = 0.6 * p.prestige + 0.4 * p.bankability
    script_read = proj.script_quality + 10 * R.gauss(st.seed, "dir-read", proj.id, p.id)
    budget_level = clamp(50 + 15 * math.log(max(real_m, 0.2) / 8))
    fit_g = director_genre_fit(p, proj.genre)
    appeal = (0.55 * script_read + 0.3 * budget_level) * (0.6 + 0.8 * fit_g)
    age = age_on(p.birth, st.date)
    idle = 1.0
    if p.historical:
        recent = [c for c in p.credits if c.get("role") == "director" and c.get("year", 0) >= year(st.date) - 6]
        if not recent:
            idle *= 0.3                    # no recent documented US directing work
        if age > 65:
            idle *= 0.35
    prob = idle / (1 + math.exp(-(appeal - standing) / 5))
    return R.unit(st.seed, "dir-accept", proj.id, p.id) < prob


# ------------------------------------------------------------- quick cast ---
def quick_cast(st: WorldState, cfg, proj: M.Project) -> None:
    """Genesis only: cast films that were already shooting/shot at the start date."""
    for role in principal_roles(st, proj):
        if role.cast_id:
            continue
        pool = candidate_pool(st, cfg, proj, role)
        if not pool:
            continue
        sw, rb = star_weight(cfg, proj, role, st.date), role_budget(cfg, proj, role)
        best = max(pool, key=lambda p: (casting_utility(st, cfg, proj, role, p, sw, rb), p.id))
        _cast(st, cfg, proj, role, best, fee=min(ask_fee(st, cfg, best, proj), role_budget(cfg, proj, role) * 1.3),
              points=0.0, points_type=None, quiet=True)


def _cast(st: WorldState, cfg, proj: M.Project, role: M.Role, p: M.Person, fee: float, points: float,
          points_type, quiet: bool = False) -> None:
    role.cast_id, role.status, role.fee = p.id, "cast", round(fee, 0)
    role.points, role.points_type = points, points_type
    commit(p, proj)
    p.quote = max(p.quote, role.fee) if role.importance in ("lead", "colead") else max(p.quote * 0.95, role.fee) if role.importance == "supporting" else p.quote
    p.credits.append({"project_id": proj.id, "title": proj.title, "role": role.importance,
                      "character": role.name, "year": year(proj.release_date or proj.shoot_end or st.date),
                      "genre": proj.genre, "kind": "film"})
    if proj.director_id:
        st.rel(proj.director_id, p.id)
    if not quiet:
        notable = p.fame > 0.08 or p.controller == "player" or p.tier == "A"
        st.log("cast", f"{p.name} was cast as {role.name} ({role.importance}) in '{proj.title}' "
                       f"({st.studios[proj.studio_id].name}).",
               actors=[p.id], refs={"project": proj.id, "role": role.id},
               public=notable, salience=3 if p.controller == "player" else (2 if notable else 0),
               data={"fee": role.fee, "points": points, "points_type": points_type})


# ---------------------------------------------------------- weekly casting ---
def step(st: WorldState, cfg) -> None:
    for pid, proj in sorted(st.projects.items()):
        if proj.stage != "prepro":
            continue
        if not proj.director_id and not attach_director(st, cfg, proj):
            continue
        for role in principal_roles(st, proj):
            if role.status == "open":
                _start_casting(st, cfg, proj, role)
            elif role.status == "auditioning" and role.audition_date <= st.date:
                _hold_auditions(st, cfg, proj, role)


def _start_casting(st: WorldState, cfg, proj: M.Project, role: M.Role) -> None:
    if role.intended and role.intended not in role.tried:
        # documented attachment: the producers go to the historical choice first
        person = st.people.get(role.intended)
        if person and person.active and not person.death and available(person, *window(proj), ignore_project=proj.id):
            make_offer(st, cfg, proj, role, person, path="long-standing attachment")
            return
        role.tried.append(role.intended)
        if person:
            st.log("history_diverged", f"(Divergence) {person.name} is not available for '{proj.title}'; the role is being recast.",
                   actors=[person.id], refs={"project": proj.id}, salience=1, public=person.fame > 0.1)
    pool = candidate_pool(st, cfg, proj, role)
    if not pool:
        return
    sw, rb = star_weight(cfg, proj, role, st.date), role_budget(cfg, proj, role)
    pool = [p for p in pool if fit(p, role, st.date) > 0.3]          # nobody considers a clear mismatch
    if not pool:
        return
    utilities = {p.id: casting_utility(st, cfg, proj, role, p, sw, rb) for p in pool}
    ranked = sorted(pool, key=lambda p: (-utilities[p.id], p.id))
    top = ranked[0]
    if role.importance == "lead" and top.bankability >= cfg["casting"]["direct_offer_bankability"]:
        role.shortlist = [p.id for p in ranked[1:cfg["casting"]["shortlist_size"]]]
        make_offer(st, cfg, proj, role, top, path="direct offer")
        return
    from . import agents
    invite = agents.build_audition_list(st, cfg, proj, role, pool, ranked, utilities)
    if role.importance in ("supporting", "featured") or proj.budget < 3e6 * market.infl(cfg, year(st.date)):
        # open call: casting directors also see a few unknown / unrepresented actors
        chosen = {p.id for p in invite}
        unknowns = [p for p in pool if p.id not in chosen and (p.agent_id is None or p.fame < 0.01)]
        scout = sorted(unknowns, key=lambda p: (-(0.5 * p.talent + 0.5 * p.presence
                                                  + 25 * R.gauss(st.seed, "open-call", role.id, p.id)), p.id))
        invite = invite + scout[:cfg["agents"]["open_call_slots"]]
    role.status = "auditioning"
    role.audition_date = add_days(st.date, 7)
    role.auditioners = []
    for p in invite:
        if p.controller == "player":
            _invite_player(st, cfg, proj, role, p)
        elif _npc_wants_audition(st, cfg, proj, role, p):
            role.auditioners.append({"id": p.id, "prep": 0.0})


def _npc_wants_audition(st, cfg, proj, role, p) -> bool:
    fee = min(ask_fee(st, cfg, p, proj), role_budget(cfg, proj, role) * 1.2)
    return accept_utility(st, cfg, proj, role, p, fee) > cfg["casting"]["accept_threshold"] - 0.4


def _invite_player(st, cfg, proj, role, p) -> None:
    studio = st.studios[proj.studio_id].name
    director = st.people[proj.director_id].name if proj.director_id else "TBD"
    cd = st.people.get(proj.casting_director_id) if proj.casting_director_id else None
    summary = (f"Audition: {role.name}, the {role.importance} role in '{proj.title}' "
               f"({proj.genre}, {studio}; director {director}; casting {cd.name if cd else 'in-house'}) on "
               f"{role.audition_date}. Premise: {proj.premise}")
    o = st.orders
    lead_interrupt = role.importance == "lead" and "auditions_lead" in o.get("interrupt_on", [])
    if role.importance in o.get("auto_accept_auditions", []) and not lead_interrupt:
        role.auditioners.append({"id": p.id, "prep": 0.0})
        st.delegated.append({"rule": "auto_accept_auditions", "decision": None,
                             "text": f"Your agent booked you an audition for {role.name} in '{proj.title}' on {role.audition_date}."})
        st.log("audition_booked", f"Audition booked: {role.name} in '{proj.title}' on {role.audition_date}.",
               actors=[p.id], refs={"project": proj.id, "role": role.id}, salience=2, public=False)
        return
    D.create(st, cfg, "audition", summary, ["attend", "attend_prepared", "decline"], deadline_days=7,
             default="decline", refs={"project": proj.id, "role": role.id},
             context="attend_prepared spends extra energy on preparation for a better read.")


@D.handler("audition")
def _audition_choice(st, cfg, dec, choice, params) -> str:
    role, proj = st.roles[dec.refs["role"]], st.projects[dec.refs["project"]]
    p = st.player
    if choice == "decline" or role.status != "auditioning":
        return f"You passed on the audition for '{proj.title}'."
    prep = 0.0
    if choice == "attend_prepared":
        prep = 4.0
        p.energy = clamp(p.energy - 6)
    role.auditioners.append({"id": p.id, "prep": prep})
    st.log("audition_booked", f"You will audition for {role.name} in '{proj.title}' on {role.audition_date}.",
           actors=[p.id], refs={"project": proj.id, "role": role.id}, salience=2, public=False)
    return f"Audition confirmed for '{proj.title}' ({'prepared' if prep else 'standard'})."


def audition_score(st, cfg, proj, role, p: M.Person, prep: float) -> float:
    g = R.stream(st.seed, "audition", role.id, p.id)
    form = g.normal(0, cfg["casting"]["audition_day_sd"]) * (1.2 - p.personality.get("discipline", 50) / 250)
    return (0.45 * p.talent + 0.25 * p.craft + 0.20 * p.range.get(role.register, 40) + 0.10 * p.presence
            + 12 * (fit(p, role, st.date) - 0.6) + prep + (p.energy - 70) / 10 + form)


def _tv_feedback(p: M.Person, winner: M.Person) -> str:
    gaps = {"presence": (winner.presence - p.presence) * 0.10, "craft": (winner.craft - p.craft) * 0.25}
    key = max(gaps, key=gaps.get)
    if gaps[key] <= 0.5:
        return "it was close; they went another way"
    return ("they liked the read but wanted someone with more screen presence" if key == "presence"
            else "they wanted a more polished read")


def audition_feedback(st, cfg, proj, role, p: M.Person, winner: M.Person) -> str:
    """What casting people actually tell agents: the biggest gap to the actor they chose."""
    gaps = {
        "presence": (winner.presence - p.presence) * 0.10,
        "craft": (winner.craft - p.craft) * 0.25,
        "type": (fit(winner, role, st.date) - fit(p, role, st.date)) * 12,
        "name": (winner.bankability - p.bankability) * 0.25 * star_weight(cfg, proj, role, st.date),
    }
    key = max(gaps, key=gaps.get)
    if gaps[key] <= 0.5:
        return "it was close; they simply preferred another read"
    return {"presence": "your read was solid, but they felt the actor they chose commanded the room more",
            "craft": "they wanted a more polished, technically confident read",
            "type": "they went with someone closer to how they saw the character",
            "name": "they went with a more established name"}[key]


def _hold_auditions(st, cfg, proj, role) -> None:
    present = [a for a in role.auditioners if a["id"] in st.people]
    if not present:
        role.status = "open"
        role.tried.extend(a["id"] for a in role.auditioners)
        return
    sw = star_weight(cfg, proj, role, st.date)
    scored = []
    for a in present:
        p = st.people[a["id"]]
        sc = audition_score(st, cfg, proj, role, p, a["prep"])
        studio_view = sc + sw * p.bankability * 0.25 + agency_visibility(st, p) * 0.3
        scored.append((studio_view, sc, p))
    scored.sort(key=lambda x: (-x[0], x[2].id))
    for rank, (_, sc, p) in enumerate(scored):
        if p.controller == "player":
            verdict = "won the part" if rank == 0 else ("made the final two" if rank == 1 else "did not get a callback")
            if rank > 0:
                fb = audition_feedback(st, cfg, proj, role, p, scored[0][2])
                st.log("audition_feedback", f"Feedback from the room on '{proj.title}' (via your agent): {fb}.",
                       actors=[p.id], refs={"project": proj.id}, salience=2, public=False)
            st.log("audition_result", f"You auditioned for {role.name} in '{proj.title}' and {verdict}.",
                   actors=[p.id], refs={"project": proj.id, "role": role.id}, salience=3, public=False,
                   data={"score": round(sc, 1), "rank": rank + 1, "of": len(scored)})
            rivals = [x[2] for x in scored if x[2].id != p.id][:3]
            if rivals:
                st.log("audition_rivals", f"Others seen for {role.name}: {', '.join(r.name for r in rivals)}.",
                       actors=[p.id] + [r.id for r in rivals], refs={"project": proj.id}, salience=1, public=False)
    from . import agents
    agents.audition_impressions(st, cfg, proj, role, scored)
    role.shortlist = [x[2].id for x in scored[1:]]
    make_offer(st, cfg, proj, role, scored[0][2], path="after auditions")


# ------------------------------------------------------------------ offers ---
def make_offer(st: WorldState, cfg, proj: M.Project, role: M.Role, p: M.Person, path: str) -> None:
    rb = role_budget(cfg, proj, role)
    ask = ask_fee(st, cfg, p, proj)
    fee = max(scale_total(cfg, proj, st.date), min(ask, rb * 1.2))
    studio_max = max(fee, rb * cfg["negotiation"]["studio_max_mult"])
    neg = cfg["negotiation"]
    g = R.stream(st.seed, "points", role.id, p.id)
    pts, ptype = 0.0, None
    if role.importance in ("lead", "colead") and p.bankability >= neg["gross_points_bankability"]:
        pts, ptype = round(float(g.uniform(*neg["gross_points"])), 1), "gross"
    elif role.importance == "lead":
        pts, ptype = round(float(g.uniform(*neg["net_points"])), 1), "net"
    oid = st.new_id("off")
    off = M.Offer(id=oid, role_id=role.id, project_id=proj.id, person_id=p.id, fee=round(fee, 0), points=pts,
                  points_type=ptype, made=st.date, deadline=add_days(st.date, cfg["casting"]["offer_response_days"]),
                  studio_max=round(studio_max, 0))
    st.offers[oid] = off
    role.status = "offered"
    if p.controller == "player":
        _offer_to_player(st, cfg, proj, role, off, path)
    else:
        u = accept_utility(st, cfg, proj, role, p, off.fee)
        _respond(st, cfg, off, "accept" if u > cfg["casting"]["accept_threshold"] else "decline")


def _offer_terms(off: M.Offer) -> str:
    t = money(off.fee)
    if off.points_type:
        t += f" + {off.points:g} {off.points_type} points"
    return t


def _offer_to_player(st, cfg, proj, role, off: M.Offer, path: str) -> None:
    p = st.player
    o = st.orders
    studio = st.studios[proj.studio_id].name
    director = st.people[proj.director_id].name if proj.director_id else "TBD"
    summary = (f"Offer ({path}): {role.name}, {role.importance} in '{proj.title}' — {proj.premise} "
               f"{studio}, dir. {director}. Terms {_offer_terms(off)}. Shoots {proj.shoot_start} to {proj.shoot_end} "
               f"({proj.location}).")
    pct = o.get("auto_decline_offers_below_quote_pct", 0)
    if pct and p.quote and off.fee < p.quote * pct / 100:
        _respond(st, cfg, off, "decline", delegated="auto_decline_offers")
        return
    if role.importance in o.get("let_agent_negotiate", []) or "offers" not in o.get("interrupt_on", []):
        u = accept_utility(st, cfg, proj, role, p, off.fee)
        _respond(st, cfg, off, "accept" if u > cfg["casting"]["accept_threshold"] else "decline",
                 delegated="let_agent_negotiate")
        return
    D.create(st, cfg, "offer", summary, ["accept", "decline", "counter(fee)"],
             deadline_days=cfg["casting"]["offer_response_days"], default="decline", refs={"offer": off.id},
             context=f"Your quote is {money(p.quote)}. Countering risks the studio walking away.")


@D.handler("offer")
def _offer_choice(st, cfg, dec, choice, params) -> str:
    off = st.offers[dec.refs["offer"]]
    if choice == "counter":
        fee = float(params.get("fee", 0))
        if fee <= 0:
            raise ValueError("counter requires a positive 'fee'")
        return _studio_considers_counter(st, cfg, off, fee)
    return _respond(st, cfg, off, choice)


@D.handler("counter")
def _counter_choice(st, cfg, dec, choice, params) -> str:
    return _respond(st, cfg, st.offers[dec.refs["offer"]], choice)


def _studio_considers_counter(st, cfg, off: M.Offer, fee: float) -> str:
    proj, role = st.projects[off.project_id], st.roles[off.role_id]
    p = st.people[off.person_id]
    g = R.stream(st.seed, "counter", off.id, off.round)
    ag = st.agencies.get(p.agent_id) if p.agent_id else None
    leverage = (ag.negotiation - 50) / 200 if ag else -0.1
    limit = off.studio_max * (1 + leverage)
    st.log("counter_sent", f"You countered on '{proj.title}' asking {money(fee)}.", actors=[p.id],
           refs={"offer": off.id}, salience=2, public=False)
    if fee <= limit:
        off.fee = round(fee, 0)
        return _respond(st, cfg, off, "accept", note="The studio agreed to your number.")
    if g.random() < cfg["negotiation"]["walkaway_hazard"] * (fee / limit):
        off.status = "withdrawn"
        _reopen(st, cfg, proj, role, p)
        st.log("offer_withdrawn", f"The studio walked away from negotiations for '{proj.title}'.", actors=[p.id],
               refs={"offer": off.id}, salience=3, public=False)
        if proj.director_id:
            st.rel(proj.director_id, p.id).affinity -= 3
        return f"The studio withdrew the offer for '{proj.title}'."
    new_fee = round(off.fee + cfg["negotiation"]["counter_split"] * (min(fee, limit) - off.fee), 0)
    off.fee, off.round, off.status = new_fee, off.round + 1, "countered"
    D.create(st, cfg, "counter", f"The studio came back on '{proj.title}' with a final {_offer_terms(off)}.",
             ["accept", "decline"], deadline_days=5, default="decline", refs={"offer": off.id})
    return f"The studio countered at {money(new_fee)} for '{proj.title}'."


def _respond(st, cfg, off: M.Offer, choice: str, delegated: str | None = None, note: str = "") -> str:
    proj, role = st.projects[off.project_id], st.roles[off.role_id]
    p = st.people[off.person_id]
    if choice == "accept":
        if not available(p, *window(proj), ignore_project=proj.id):
            choice = "decline"
        else:
            off.status = "accepted"
            _cast(st, cfg, proj, role, p, off.fee, off.points, off.points_type)
            text = f"Accepted {role.name} in '{proj.title}' for {_offer_terms(off)}. {note}".strip()
            if delegated:
                st.delegated.append({"rule": delegated, "decision": None, "text": text})
            return text
    off.status = "declined"
    p.calendar = [c for c in p.calendar if c["project_id"] != proj.id]   # release any hold
    _reopen(st, cfg, proj, role, p)
    if p.controller == "player" or p.fame > 0.15:
        st.log("offer_declined", f"{p.name} turned down {role.name} in '{proj.title}'.", actors=[p.id],
               refs={"offer": off.id}, salience=2 if p.controller == "player" else 1,
               public=p.controller != "player")
    text = f"Declined {role.name} in '{proj.title}'."
    if delegated:
        st.delegated.append({"rule": delegated, "decision": None, "text": text})
    return text


def _reopen(st, cfg, proj, role, p) -> None:
    role.tried.append(p.id)
    while role.shortlist:
        nxt = st.people.get(role.shortlist.pop(0))
        if nxt and nxt.id not in role.tried and available(nxt, *window(proj)):
            make_offer(st, cfg, proj, role, nxt, path="next choice")
            return
    role.status = "open"


# -------------------------------------------------------- actor's utility ---
def accept_utility(st: WorldState, cfg, proj: M.Project, role: M.Role, p: M.Person, fee: float) -> float:
    """How much an actor wants a role. Used by NPCs and by delegated player choices."""
    if not available(p, *window(proj), ignore_project=proj.id):
        return -99.0
    g = R.stream(st.seed, "script-read", proj.id, p.id)
    ag = st.agencies.get(p.agent_id) if p.agent_id else None
    noise_sd = 16 - (ag.info_quality / 10 if ag else 0)
    script_obs = proj.script_quality + g.normal(0, noise_sd)
    ref = max(p.quote, scale_total(cfg, proj, st.date))
    money_term = math.log(max(fee, 1) / ref)
    size = {"lead": 1.0, "colead": 0.6, "supporting": 0.25, "featured": 0.1}[role.importance]
    director = st.people.get(proj.director_id) if proj.director_id else None
    dir_pres = director.prestige if director else 30
    rel = 0.0
    if director:
        r = st.rel(director.id, p.id, create=False)
        rel = (r.affinity / 100) if r else 0.0
    idle = 0.0
    if p.last_work:
        from ..core.util import days_between
        idle = min(1.5, days_between(p.last_work, st.date) / 7 / cfg["casting"]["idle_weeks_desperation"])
    else:
        idle = 1.0
    gl = p.goals or {"money": 0.3, "fame": 0.2, "prestige": 0.2, "art": 0.2, "stability": 0.1}
    star_drop = -0.6 if (p.bankability > 60 and role.importance in ("supporting", "featured")) else 0.0
    if role.intended == p.id:
        star_drop += cfg["history"]["intended_role_bonus"]
    return (gl.get("money", 0.2) * 2.0 * money_term + gl.get("fame", 0.2) * 1.2 * size
            + gl.get("prestige", 0.2) * ((dir_pres - 30) / 40 + (script_obs - 50) / 40)
            + gl.get("art", 0.2) * (script_obs - 50) / 30 + gl.get("stability", 0.1) * 0.5
            + 0.5 * idle + rel + star_drop)
