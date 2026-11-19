"""Personal lives: attraction, romance, marriage, breakups, documented history,
fictional mortality.

Rules (DESIGN.md §3.6 + user direction):
- Romance emerges from contact (working together, meeting), mutual attraction,
  compatibility, availability and each person's own choice. No scripted pairings.
- Real people may form simulated relationships (config `generated_for_real_people`),
  but the engine never generates illness, death, crime or scandal for them.
- Documented events (marriage, divorce, death...) are the baseline and occur
  unless their causal dependency no longer holds in this simulated world.
- The player's own feelings are the player's choice: the engine only simulates
  the NPC's side (attraction, availability, willingness).
"""
from __future__ import annotations

import math

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import age_on, clamp
from . import decisions as D

TAKEN = ("dating", "married")


def _attraction(st, cfg, a, b) -> float:
    """How drawn a is to b (HIDDEN). Stable per world and pair."""
    if b.gender not in a.romance.get("attracted_to", []):
        return 0.0
    if age_on(a.birth, st.date) < 18 or age_on(b.birth, st.date) < 18:
        return 0.0
    u = R.unit(st.seed, "attraction", a.id, b.id)
    gap = abs(age_on(a.birth, st.date) - age_on(b.birth, st.date))
    gap_f = math.exp(-max(0, gap - 6) / 12)
    charm = 0.6 + 0.4 * b.presence / 100
    return round(clamp((0.15 + 0.85 * u) * gap_f * charm, 0, 1), 4)


def ensure_attraction(st, cfg, r) -> None:
    if r.attraction_set:
        return
    a, b = st.people[r.a], st.people[r.b]
    r.attraction_ab = _attraction(st, cfg, a, b) if a.controller != "player" else 0.0
    r.attraction_ba = _attraction(st, cfg, b, a) if b.controller != "player" else 0.0
    r.attraction_set = True


def available_for_romance(p) -> bool:
    return p.death is None and p.partner_status not in ("dating", "married", "married_offscreen")


def allowed(cfg, p, category: str) -> bool:
    if not p.historical:
        return True
    return category in cfg["personal"]["generated_for_real_people"]


def step(st: WorldState, cfg: dict) -> None:
    _documented_events(st, cfg)
    _sparks(st, cfg)
    _progress(st, cfg)
    _mortality(st, cfg)


# ----------------------------------------------------------- romance ---
def _sparks(st, cfg) -> None:
    pc = cfg["personal"]
    seen = set()
    for a_id, b_id, proj_id in st.market.get("contacts", []):
        if (a_id, b_id) in seen:
            continue
        seen.add((a_id, b_id))
        r = st.rel(a_id, b_id)
        ensure_attraction(st, cfg, r)
        a, b = st.people[a_id], st.people[b_id]
        if r.status in TAKEN or not (available_for_romance(a) and available_for_romance(b)):
            continue
        if not (allowed(cfg, a, "romance") and allowed(cfg, b, "romance")):
            continue
        g = R.stream(st.seed, "spark", r.a, r.b, st.date)
        if a.controller == "player" or b.controller == "player":
            npc = b if a.controller == "player" else a
            att = r.attraction_ba if npc.id == r.b else r.attraction_ab
            # the player perceives signals, which are informative but imperfect
            signal_p = pc["spark_base"] * (0.4 + 2.0 * att + 0.5 * npc.personality.get("openness", 50) / 100)
            if g.random() < signal_p and not any(d.kind == "romance" and d.status == "pending" and d.refs.get("person") == npc.id
                                                 for d in st.decisions.values()) and r.status != "ex":
                st.log("chemistry", f"There is an unmistakable spark between you and {npc.name} on the set of "
                                    f"'{st.projects[proj_id].title}'.", actors=[a.id, b.id], refs={"project": proj_id},
                       salience=3, public=False)
                D.create(st, cfg, "romance", f"Chemistry with {npc.name}: pursue something, or keep it professional?",
                         ["pursue", "keep_professional"], deadline_days=21, default="keep_professional",
                         refs={"person": npc.id}, interrupt="romance" in st.orders.get("interrupt_on", []),
                         context="Pursuing is your choice; how they respond is theirs.")
            continue
        thr = pc["attraction_threshold"]
        if r.attraction_ab < thr or r.attraction_ba < thr:
            continue
        openness = (a.romance.get("openness", 0.5) + b.romance.get("openness", 0.5)) / 2
        p = pc["spark_base"] * r.attraction_ab * r.attraction_ba * 2 * openness * (1 + max(0, r.affinity) / 100)
        if g.random() < p:
            _start_dating(st, cfg, r, a, b)


@D.handler("romance")
def _romance_choice(st, cfg, dec, choice, params) -> str:
    npc = st.people[dec.refs["person"]]
    if choice == "keep_professional":
        return f"You kept things professional with {npc.name}."
    return overture(st, cfg, st.player, npc, approach=params.get("approach", ""))["text"]


def overture(st, cfg, actor, target, approach: str = "") -> dict:
    """Someone expresses romantic interest; the target decides by their own nature."""
    r = st.rel(actor.id, target.id)
    ensure_attraction(st, cfg, r)
    att = r.attraction_ab if target.id == r.a else r.attraction_ba
    if target.controller == "player":
        att = 1.0
    if r.contact_weeks == 0 and r.affinity < 5:
        return {"result": "rejected", "text": f"You haven't really met {target.name} yet; there is nothing to build on."}
    if not available_for_romance(target):
        r.history.append({"date": st.date, "text": "an unreciprocated overture", "delta": -2})
        r.affinity = clamp(r.affinity - 2, -100, 100)
        return {"result": "declined", "text": f"{target.name} is not available, and gently makes that clear."}
    if not allowed(cfg, target, "romance"):
        return {"result": "rejected", "text": "Romantic storylines with this person are disabled in configuration."}
    g = R.stream(st.seed, "overture", actor.id, target.id, st.date)
    p_yes = clamp(0.1 + 1.1 * att + r.affinity / 200 + 0.2 * (target.romance.get("openness", 0.5) - 0.5), 0, 0.95)
    if g.random() < p_yes:
        _start_dating(st, cfg, r, actor, target)
        return {"result": "accepted", "text": f"{target.name} feels the same way. You are seeing each other."}
    if att > 0.35:
        r.affinity = clamp(r.affinity + 3, -100, 100)
        return {"result": "maybe", "text": f"{target.name} is flattered but wants to take things slowly."}
    r.affinity = clamp(r.affinity - 3, -100, 100)
    return {"result": "declined", "text": f"{target.name} doesn't see you that way."}


def _start_dating(st, cfg, r, a, b) -> None:
    r.status, r.since = "dating", st.date
    for x, y in ((a, b), (b, a)):
        x.partner_id, x.partner_status = y.id, "dating"
    r.history.append({"date": st.date, "text": "started seeing each other", "delta": 10})
    r.affinity = clamp(r.affinity + 10, -100, 100)
    famous = max(a.fame, b.fame) > 0.12
    inv = st.player_id in (a.id, b.id)
    st.log("romance", f"{a.name} and {b.name} have started seeing each other." if not inv else
           f"You and {(b if a.controller == 'player' else a).name} are now a couple.",
           actors=[a.id, b.id], salience=4 if inv else (2 if famous else 0), public=famous or inv)


def _end(st, r, a, b, kind: str) -> None:
    r.status = "ex" if kind == "breakup" else "divorced"
    r.history.append({"date": st.date, "text": "broke up" if kind == "breakup" else "divorced", "delta": -15})
    r.affinity = clamp(r.affinity - 15, -100, 100)
    for x in (a, b):
        x.partner_id, x.partner_status = None, None
    famous = max(a.fame, b.fame) > 0.12
    inv = st.player_id in (a.id, b.id)
    word = "split up" if kind == "breakup" else "are divorcing"
    st.log(kind, f"{a.name} and {b.name} {word}.", actors=[a.id, b.id],
           salience=4 if inv else (2 if famous else 0), public=famous or inv)


def _progress(st, cfg) -> None:
    pc = cfg["personal"]
    for key, r in sorted(st.rels.items()):
        if r.status not in TAKEN:
            continue
        a, b = st.people[r.a], st.people[r.b]
        if a.death or b.death:
            continue
        g = R.stream(st.seed, "relationship", key, st.date)
        compat = 1 - abs(a.personality.get("temperament", 50) - b.personality.get("temperament", 50)) / 150
        apart = 1.4 if _working_apart(st, a, b) else 1.0
        if r.status == "dating":
            if a.controller != "player" and b.controller != "player" and g.random() < pc["dating_to_marriage_weekly"] * compat * 2:
                if allowed(cfg, a, "marriage") and allowed(cfg, b, "marriage"):
                    r.status = "married"
                    for x, y in ((a, b), (b, a)):
                        x.partner_status = "married"
                    r.history.append({"date": st.date, "text": "married", "delta": 10})
                    famous = max(a.fame, b.fame) > 0.12
                    st.log("marriage", f"{a.name} and {b.name} married.", actors=[a.id, b.id],
                           salience=2 if famous else 0, public=famous)
                continue
            if g.random() < pc["breakup_weekly_base"] * (1.6 - compat) * apart and allowed(cfg, a, "breakup") and allowed(cfg, b, "breakup"):
                _end(st, r, a, b, "breakup")
        else:
            protect = r.history and any(h.get("documented") for h in r.history)
            hz = pc["divorce_weekly_base"] * (1.6 - compat) * apart
            if protect:
                hz *= (1 - pc["documented_protection"]) + pc["documented_protection"] * max(_divergence(st, a), _divergence(st, b))
            if g.random() < hz and allowed(cfg, a, "breakup") and allowed(cfg, b, "breakup"):
                _end(st, r, a, b, "divorce")
    # off-screen spouses of fictional NPCs can also end
    for pid, p in sorted(st.people.items()):
        if p.partner_status == "married_offscreen" and not p.historical and p.controller != "player":
            if R.unit(st.seed, "offscreen-divorce", pid, st.date) < pc["divorce_weekly_base"] * 0.8:
                p.partner_status = None


def _working_apart(st, a, b) -> bool:
    pa = {c["project_id"] for c in a.calendar if c["start"] <= st.date <= c["end"]}
    pb = {c["project_id"] for c in b.calendar if c["start"] <= st.date <= c["end"]}
    return bool(pa or pb) and not (pa & pb)


def _divergence(st, p) -> float:
    """How far a real person's simulated life has moved from their documented one (0..1).
    Uses documented future credits from the data pack when available."""
    hist = p.provenance.get("documented_credits_after_start")
    if not hist:
        return 0.0
    sim = {c.get("historical_ref") for c in p.credits if c.get("historical_ref")}
    due = [h for h in hist if h["date"] <= st.date]
    if not due:
        return 0.0
    kept = sum(1 for h in due if h["ref"] in sim)
    return 1 - kept / len(due)


# ------------------------------------------------- documented history ---
def _documented_events(st, cfg) -> None:
    for eid, ev in sorted(st.hist_events.items()):
        if ev.status != "scheduled" or ev.date > st.date:
            continue
        people = [st.people.get(x) for x in ev.people]
        if any(p is None for p in people):
            ev.status, ev.resolution = "voided", "person not in this world"
            continue
        dep = ev.dependency or {"kind": "independent"}
        kind = dep.get("kind", "independent")
        ok, why = True, "independent of simulated divergence"
        g = R.stream(st.seed, "documented", eid)
        if any(p.death for p in people) and ev.type != "death":
            ok, why = False, "a participant had already died in this timeline"
        elif kind == "relationship" and ev.type == "marriage":
            a, b = people[0], people[1]
            r = st.rel(a.id, b.id, create=False)
            met = r is not None and (r.contact_weeks > 0 or any(h.get("documented") for h in r.history)) or dep.get("met_before_start")
            free = all(p.partner_id in (None, q.id) and p.partner_status != "married" for p, q in ((a, b), (b, a)))
            if not met:
                ok = g.random() < dep.get("base_rate_if_never_met", 0.25)
                why = "they never crossed paths in this timeline" if not ok else "they met through other channels"
            elif not free:
                ok, why = False, "one of them was already committed elsewhere in this timeline"
        elif kind == "relationship" and ev.type == "divorce":
            a, b = people[0], people[1]
            r = st.rel(a.id, b.id, create=False)
            ok = r is not None and r.status == "married"
            why = "they were never married in this timeline" if not ok else "documented"
        elif kind == "circumstance":
            div = max(_divergence(st, p) for p in people)
            ok = g.random() >= div
            why = "circumstances diverged" if not ok else "circumstances held"
        elif kind == "production":
            ref = dep.get("project_ref")
            ok = any(c.get("historical_ref") == ref for p in people for c in p.calendar)
            why = "the production it depended on did not happen with them" if not ok else "production held"
        if not ok:
            ev.status, ev.resolution = "voided", why
            st.log("history_diverged", f"(Divergence) {ev.summary} — did not occur: {why}.", actors=ev.people,
                   salience=0, public=False, data={"event": eid})
            continue
        ev.status, ev.resolution = "occurred", why
        _apply_documented(st, cfg, ev, people)


def _apply_documented(st, cfg, ev, people) -> None:
    if ev.type == "death":
        p = people[0]
        p.death, p.active = st.date, False
        if p.partner_id and p.partner_id in st.people:
            q = st.people[p.partner_id]
            q.partner_id, q.partner_status = None, None
    elif ev.type == "marriage":
        a, b = people
        r = st.rel(a.id, b.id)
        r.status, r.since = "married", st.date
        r.history.append({"date": st.date, "text": "married", "delta": 10, "documented": True})
        for x, y in ((a, b), (b, a)):
            x.partner_id, x.partner_status = y.id, "married"
    elif ev.type == "divorce":
        a, b = people
        r = st.rel(a.id, b.id)
        r.status = "divorced"
        r.history.append({"date": st.date, "text": "divorced", "delta": -15, "documented": True})
        for x in (a, b):
            x.partner_id, x.partner_status = None, None
    famous = max(p.fame for p in people) > 0.05
    st.log("documented_" + ev.type, ev.summary, actors=ev.people, salience=2 if famous else 1, public=True,
           data={"event": ev.id, "verification": ev.verification, "sources": ev.sources})


# ------------------------------------------------------------ mortality ---
def _mortality(st, cfg) -> None:
    gz = cfg["personal"]["fictional_mortality_gompertz"]
    for pid, p in sorted(st.people.items()):
        if p.death or p.historical or p.controller == "player":
            continue
        age = age_on(p.birth, st.date)
        hz_week = gz["a"] * math.exp(gz["b"] * age) / 52
        if R.unit(st.seed, "mortality", pid, st.date) < hz_week:
            p.death, p.active = st.date, False
            if p.partner_id and p.partner_id in st.people:
                q = st.people[p.partner_id]
                q.partner_id, q.partner_status = None, None
            if p.fame > 0.1:
                st.log("death", f"{p.name} has died at {age}.", actors=[pid], salience=2, public=True)
