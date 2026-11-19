"""Adjudication of narrator proposals.

The narrator proposes; the engine decides. Each proposal type has
preconditions and an engine model for its consequence, so the same scene can
produce different outcomes depending on the people involved. Rulings come back
in the next packet. Proposals that try to set numbers or outcomes are rejected.
"""
from __future__ import annotations

from ..core import rng as R
from ..core.config import era_value
from ..core.state import WorldState
from ..core.util import add_days, age_on, clamp, money, year
from ..systems import market, personal

SEVERITY = {"minor": 5.0, "moderate": 14.0, "major": 30.0}
FORBIDDEN_KEYS = {"fee", "gross", "box_office", "score", "salary", "cast", "award", "result", "outcome", "amount"}
PURCHASES = {   # 1980 dollars: one-off cost, monthly cost change
    "gift": (150, 0), "wardrobe": (800, 0), "vacation": (2500, 0), "car": (7000, 0),
    "apartment": (2000, 600), "house": (40000, 1500),
}


def _rule(prop: dict, result: str, text: str) -> dict:
    return {"proposal": prop.get("id", "?"), "type": prop.get("type", "?"), "result": result, "text": text}


def adjudicate(st: WorldState, cfg: dict, prop: dict, idx: int) -> dict:
    t = prop.get("type")
    bad = FORBIDDEN_KEYS & set(prop)
    if bad:
        return _rule(prop, "rejected", f"Proposals cannot set {', '.join(sorted(bad))}; the engine determines outcomes.")
    fn = {"relationship_shift": _relationship_shift, "romantic_overture": _romantic_overture,
          "player_intent": _player_intent, "purchase": _purchase,
          "reputation_moment": _reputation_moment}.get(t)
    if fn is None:
        return _rule(prop, "rejected", f"Unknown proposal type '{t}'.")
    g = R.stream(st.seed, "adjudicate", st.packet_id, idx, t)
    return fn(st, cfg, prop, g)


def _person(st, pid):
    return st.people.get(pid) if pid else None


def _have_met(st, a, b) -> bool:
    r = st.rel(a.id, b.id, create=False)
    return r is not None and (r.contact_weeks > 0 or r.history or r.status != "acquainted")


def _relationship_shift(st, cfg, prop, g) -> dict:
    pl = st.player
    other = _person(st, prop.get("with"))
    if other is None:
        return _rule(prop, "rejected", "That person does not exist in this world.")
    if not _have_met(st, pl, other) and not _shares_project(st, pl, other):
        return _rule(prop, "rejected", f"You have not actually crossed paths with {other.name} yet.")
    base = SEVERITY.get(prop.get("severity", "minor"), 5.0)
    neg = prop.get("direction") == "negative"
    r = st.rel(pl.id, other.id)
    if neg:
        temper = (pl.personality.get("temperament", 50) + other.personality.get("temperament", 50)) / 200
        ego = other.personality.get("ego", 50) / 100
        mult = 0.5 + temper + 0.4 * ego - max(0, r.affinity) / 200
    else:
        mult = 0.5 + other.personality.get("warmth", 50) / 100 - max(0, -r.affinity) / 200
    delta = base * clamp(mult, 0.2, 1.5) * float(g.uniform(0.7, 1.15))
    delta = -delta if neg else delta
    before = r.affinity
    r.affinity = round(clamp(r.affinity + delta, -100, 100), 2)
    cause = str(prop.get("cause", "")).strip()[:200]
    r.history.append({"date": st.date, "text": cause or ("a falling-out" if neg else "grew closer"), "delta": round(delta, 1)})
    if r.affinity < -45 and r.status not in ("dating", "married"):
        r.status = "feud"
    elif r.affinity > 35 and r.status == "acquainted":
        r.status = "friends"
    scale = abs(delta) / base
    result = "accepted" if scale >= 0.85 else "partially_accepted"
    word = "worsened" if neg else "improved"
    return _rule(prop, result, f"Your relationship with {other.name} {word}: now {_aff(r.affinity)} "
                               f"(was {_aff(before)}).")


def _aff(a):
    from .packet import affinity_label
    return affinity_label(a)


def _shares_project(st, a, b) -> bool:
    for p in st.projects.values():
        ids = {st.roles[r].cast_id for r in p.role_ids} | {p.director_id}
        if a.id in ids and b.id in ids:
            return True
    return False


def _romantic_overture(st, cfg, prop, g) -> dict:
    target = _person(st, prop.get("to"))
    if target is None:
        return _rule(prop, "rejected", "That person does not exist in this world.")
    if age_on(target.birth, st.date) < 18:
        return _rule(prop, "rejected", "Not allowed.")
    out = personal.overture(st, cfg, st.player, target, approach=str(prop.get("approach", "")))
    return _rule(prop, out["result"], out["text"])


def _player_intent(st, cfg, prop, g) -> dict:
    pl = st.player
    kind = prop.get("kind")
    infl = market.infl(cfg, year(st.date))
    if kind == "take_class":
        cost = 400 * infl
        if pl.cash < cost:
            return _rule(prop, "rejected", f"You can't afford the class ({money(cost)}).")
        pl.cash -= cost
        gain = 2.5 * (1 - pl.craft / 110) * float(g.uniform(0.6, 1.2))
        pl.craft = round(clamp(pl.craft + gain), 2)
        st.log("training", f"You enrolled in an acting class ({money(cost)}).", actors=[pl.id], salience=2, public=False)
        return _rule(prop, "accepted", f"You took the class ({money(cost)}). It sharpened your technique a little.")
    if kind == "rest":
        pl.energy = clamp(pl.energy + 15)
        return _rule(prop, "accepted", "You took real time off and feel restored.")
    if kind in ("meet_person", "pursue_director"):
        target = _person(st, prop.get("target"))
        if target is None:
            return _rule(prop, "rejected", "Name a real person id from the packet as 'target'.")
        reach = 0.25 + pl.fame * 2 + (0.25 if pl.agent_id else 0) + (0.2 if _have_met(st, pl, target) else 0)
        reach -= target.fame * 0.8
        if g.random() < clamp(reach, 0.05, 0.95):
            r = st.rel(pl.id, target.id)
            r.contact_weeks += 1
            r.affinity = round(clamp(r.affinity + float(g.uniform(2, 8)), -100, 100), 2)
            r.history.append({"date": st.date, "text": str(prop.get("text", "met socially"))[:160], "delta": 4})
            return _rule(prop, "accepted", f"You got time with {target.name}; it went reasonably well.")
        return _rule(prop, "declined", f"You couldn't get access to {target.name} this time.")
    if kind == "seek_agent":
        tiers = sorted({a.tier for a in st.agencies.values()})
        cur = st.agencies[pl.agent_id].tier if pl.agent_id else 4
        want = cur - 1 if cur > 1 else 1
        chance = clamp(0.15 + pl.bankability / 120 + max(0, pl.heat) / 150 + pl.critical_rep / 300 - (3 - want) * 0.1, 0.05, 0.9)
        pool = [a for a in sorted(st.agencies.values(), key=lambda a: a.id) if a.tier == max(want, tiers[0])]
        if pool and g.random() < chance:
            ag = pool[int(g.integers(len(pool)))]
            pl.agent_id = ag.id
            st.log("new_agent", f"You signed with {ag.name}.", actors=[pl.id], salience=3, public=False)
            return _rule(prop, "accepted", f"{ag.name} agreed to represent you.")
        return _rule(prop, "declined", "The agencies you approached passed for now.")
    return _rule(prop, "rejected", f"Unknown intent kind '{kind}'.")


def _purchase(st, cfg, prop, g) -> dict:
    pl = st.player
    item = prop.get("item")
    if item not in PURCHASES:
        return _rule(prop, "rejected", f"Unknown purchase '{item}'. Options: {', '.join(PURCHASES)}.")
    one_off, monthly = PURCHASES[item]
    infl = market.infl(cfg, year(st.date))
    scale = 1 + min(3.0, pl.fame * 6)              # what you buy scales with status
    cost = one_off * infl * scale
    if pl.cash < cost:
        return _rule(prop, "rejected", f"You can't afford that right now (about {money(cost)}).")
    pl.cash -= cost
    pl.monthly_costs += monthly * infl * scale
    st.log("purchase", f"You bought a {item}: {str(prop.get('text', ''))[:120]} ({money(cost)}).", actors=[pl.id],
           salience=2, public=False)
    extra = f" Monthly costs rise by {money(monthly * infl * scale)}." if monthly else ""
    return _rule(prop, "accepted", f"Purchased ({money(cost)}).{extra}")


def _reputation_moment(st, cfg, prop, g) -> dict:
    who = _person(st, prop.get("person"))
    if who is None:
        return _rule(prop, "rejected", "That person does not exist in this world.")
    neg = prop.get("direction") == "negative"
    sev = prop.get("severity", "minor")
    if who.historical and neg and (sev != "minor" or prop.get("public")):
        return _rule(prop, "rejected", "The engine does not create damaging public claims about real people. "
                                       "Private, minor professional friction is allowed.")
    if sev not in ("minor", "moderate"):
        return _rule(prop, "rejected", "Reputation moments may be minor or moderate.")
    size = {"minor": 3.0, "moderate": 7.0}[sev] * float(g.uniform(0.6, 1.1))
    if prop.get("public"):
        who.heat = round(clamp(who.heat + (-size if neg else size), -100, 100), 2)
    who.critical_rep = round(clamp(who.critical_rep + (-size if neg else size) * 0.3), 2)
    st.log("reputation", f"{'A setback' if neg else 'A boost'} for {who.name}'s reputation: {str(prop.get('cause',''))[:160]}",
           actors=[who.id], salience=2, public=bool(prop.get("public")))
    return _rule(prop, "accepted", f"Recorded. Effect on {who.name}'s standing: {'slightly negative' if neg else 'slightly positive'}.")
