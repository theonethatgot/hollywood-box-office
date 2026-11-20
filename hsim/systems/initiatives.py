"""Narrator-originated initiatives: proposed consequential canon, adjudicated by the engine.

The narrator (ChatGPT) can start plausible professional and social moves in the story.
Each initiative names a kind, a target (person or project, by name or id), optionally an
intermediary ("via") and an approach. The engine evaluates it with the same mechanics as
everything else (casting rank, access and fame gaps, relationships, money, studio
decisions) and answers with success, partial success (a counter-proposal), rejection
with a reason, or a multi-week process that resolves later. Nothing here grants outcomes.

Kinds
  inquire          your agent finds out where a film or person stands (observed information)
  pursue_project   your agent pushes for you on a specific film (and role)
  meet             request a meeting with a filmmaker, executive, actor or casting director
  introduction     ask someone you know to introduce you to someone they know
  social           invite someone you know to something personal (dinner, a party, a game)
  publicity        publicist, trade interview, talk show, charity appearance
  reposition       give your agent a standing directive (genres, role size, media)
  develop_project  develop an original film: hire a writer, then pitch to studios
"""
from __future__ import annotations

import difflib

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_days, age_on, clamp, money, year
from . import market

KINDS = ("inquire", "pursue_project", "meet", "introduction", "social", "publicity", "reposition", "develop_project")


# ---------------------------------------------------------------- resolve ---
def resolve(st: WorldState, ref, kind: str = "any"):
    """Resolve a narrator reference (id or name) to a person or project.
    Returns (object, None) or (None, message with candidates)."""
    if ref is None or ref == "":
        return None, "no target given"
    ref = str(ref).strip()
    if kind in ("any", "person") and ref in st.people:
        return st.people[ref], None
    if kind in ("any", "project") and ref in st.projects:
        return st.projects[ref], None
    low = ref.lower().strip("'\"")
    pool = []
    if kind in ("any", "person"):
        pool += [(p.name, p) for p in st.people.values() if not p.death]
    if kind in ("any", "project"):
        pool += [(p.title, p) for p in st.projects.values() if p.stage != "dead"]
    exact = [o for n, o in pool if n.lower() == low]
    if len(exact) == 1:
        return exact[0], None
    if len(exact) > 1:
        return None, f"'{ref}' is ambiguous: " + "; ".join(_describe(st, o) for o in exact[:5]) + " (use the id)"
    names = [n for n, _ in pool]
    close = difflib.get_close_matches(ref, names, n=4, cutoff=0.82)
    if len(close) == 1:
        return next(o for n, o in pool if n == close[0]), None
    hint = f"; did you mean: {', '.join(close)}" if close else ""
    return None, f"nobody and nothing in this world matches '{ref}'{hint}"


def _describe(st, o) -> str:
    if hasattr(o, "title"):
        return f"{o.id} '{o.title}' ({st.studios[o.studio_id].name}, {o.stage})"
    return f"{o.id} {o.name}"


# --------------------------------------------------------------- dispatch ---
def adjudicate(st: WorldState, cfg: dict, item: dict, idx: int) -> dict:
    kind = item.get("kind")
    if kind not in KINDS:
        return _ruling(item, "rejected", f"Unknown initiative kind '{kind}'. Kinds: {', '.join(KINDS)}.")
    forbidden = {"fee", "gross", "outcome", "result", "cast", "award", "score", "success"} & set(item)
    if forbidden:
        return _ruling(item, "rejected", f"Initiatives can't set {', '.join(sorted(forbidden))}; the engine decides outcomes.")
    g = R.stream(st.seed, "initiative", st.packet_id, idx, kind)
    return globals()[f"_{kind}"](st, cfg, item, g)


def _ruling(item, result, text, **extra) -> dict:
    out = {"proposal": item.get("id", "?"), "type": f"initiative:{item.get('kind')}", "result": result, "text": text}
    out.update(extra)
    return out


def _track(st, item, status, text, due=None, data=None) -> str | None:
    if item.get("_follow_up"):                     # a watched initiative re-checking: no new record
        return item["_follow_up"]
    iid = st.new_id("ini")
    st.initiatives[iid] = {"id": iid, "kind": item.get("kind"), "created": st.date, "status": status,
                           "approach": str(item.get("approach", ""))[:200], "steps": [{"date": st.date, "text": text}],
                           "due": due, "data": data or {}}
    return iid


def _step(st, iid, text, status=None):
    ini = st.initiatives[iid]
    ini["steps"].append({"date": st.date, "text": text})
    if status:
        ini["status"] = status


def _agent(st):
    pl = st.player
    return st.people.get(pl.agent_person_id) if pl.agent_person_id else None


# ---------------------------------------------------------------- inquire ---
def _inquire(st, cfg, item, g) -> dict:
    obj, err = resolve(st, item.get("target"))
    if err:
        return _ruling(item, "rejected", err)
    agent = _agent(st)
    who = agent.name if agent else "A friend in the business"
    if hasattr(obj, "title"):
        return _ruling(item, "accepted", f"{who} looked into '{obj.title}': " + project_status(st, cfg, obj))
    recent = [e["text"] for e in st.events if obj.id in e["actors"] and e["public"] and e["salience"] >= 1][-3:]
    work = [c for c in obj.calendar if c["end"] >= st.date and c["project_id"] in st.projects]
    bits = [f"{obj.name} is currently " + (f"committed to '{st.projects[work[0]['project_id']].title}' until "
                                            f"{work[0]['end']}" if work else "not on a production")]
    if recent:
        bits.append("lately: " + " | ".join(recent))
    return _ruling(item, "accepted", f"{who} asked around about {obj.name}: " + "; ".join(bits) + ".")


def project_status(st, cfg, p) -> str:
    """What an agent can learn about a production (observed, not hidden values)."""
    from .casting import candidate_pool, casting_utility, fit, role_budget, star_weight
    studio = st.studios[p.studio_id].name
    d = st.people.get(p.director_id)
    parts = [f"{p.stage.replace('_', ' ')} at {studio}" + (f", directed by {d.name}" if d else ", no director yet")]
    if p.shoot_start and p.stage in ("development", "prepro"):
        parts.append(f"shooting from about {p.shoot_start}")
    pl = st.player
    open_roles = [st.roles[r] for r in p.role_ids if not st.roles[r].cast_id and st.roles[r].status in ("open", "auditioning")
                  and st.roles[r].gender == pl.gender]
    earmarked = [r for r in open_roles if r.intended and r.intended not in r.tried]
    open_roles = [r for r in open_roles if r not in earmarked]
    if earmarked:
        parts.append(f"{len(earmarked)} of the parts you could play are earmarked for attached actors "
                     f"({', '.join(r.name + ' (' + r.importance + ')' for r in earmarked[:3])})")
    if not open_roles:
        parts.append("no unattached roles for you")
    for r in open_roles[:3]:
        pool = candidate_pool(st, cfg, p, r)
        if not any(x.id == pl.id for x in pool):
            parts.append(f"{r.name} ({r.importance}) is outside your range or schedule")
            continue
        chance = chance_label(st, cfg, p, r, pool)
        parts.append(f"{r.name} ({r.importance}){' — auditions under way' if r.status == 'auditioning' else ''}: "
                     f"your agent rates you {chance}")
    return "; ".join(parts) + "."


def room(st, cfg, proj, role, pool=None) -> dict:
    """Casting utilities for everyone the casting director could consider, highest first."""
    from .casting import candidate_pool, casting_utility, role_budget, star_weight
    pool = candidate_pool(st, cfg, proj, role) if pool is None else pool
    sw, rb = star_weight(cfg, proj, role, st.date), role_budget(cfg, proj, role)
    u = {x.id: casting_utility(st, cfg, proj, role, x, sw, rb) for x in pool}
    return {"u": u, "order": sorted(u, key=lambda k: (-u[k], k))}


def estimate_rank(st, cfg, proj, role, person, sample: int = 60) -> int:
    """An agent's read of where a client stands, from a sample of the competition (cheap, imperfect)."""
    from .casting import candidate_pool, casting_utility, role_budget, star_weight
    pool = [x for x in candidate_pool(st, cfg, proj, role) if x.id != person.id]
    if not pool:
        return 1
    sw, rb = star_weight(cfg, proj, role, st.date), role_budget(cfg, proj, role)
    picks = sorted(pool, key=lambda x: R.unit(st.seed, "rank-sample", role.id, x.id))[:sample]
    mine = casting_utility(st, cfg, proj, role, person, sw, rb)
    above = sum(1 for x in picks if casting_utility(st, cfg, proj, role, x, sw, rb) > mine)
    return 1 + round(above * len(pool) / len(picks))


def rank_in_pool(st, cfg, proj, role, pool, person_id=None) -> int:
    """Where this actor stands among the candidates (1 = the casting director's first choice)."""
    pid = person_id or st.player_id
    r = room(st, cfg, proj, role, pool)
    return r["order"].index(pid) + 1 if pid in r["u"] else 10 ** 6


def chance_label(st, cfg, p, role, pool) -> str:
    rank = rank_in_pool(st, cfg, p, role, pool)
    return ("a strong contender" if rank <= 5 else "in the mix" if rank <= 15 else "a long shot" if rank <= 40
            else "very unlikely")


# ---------------------------------------------------------- pursue_project ---
def _pursue_project(st, cfg, item, g) -> dict:
    from .casting import candidate_pool
    proj, err = resolve(st, item.get("target"), "project")
    if err:
        return _ruling(item, "rejected", err)
    pl = st.player
    agent = _agent(st)
    if not agent:
        return _ruling(item, "rejected", "Without an agent there is nobody to make the call; you'd need an introduction instead.")
    if proj.stage in ("shooting", "post", "awaiting_release", "released"):
        return _ruling(item, "rejected", f"'{proj.title}' is already {proj.stage.replace('_', ' ')}; the roles are cast.")
    roles = [st.roles[r] for r in proj.role_ids if not st.roles[r].cast_id and st.roles[r].status in ("open", "auditioning")
             and st.roles[r].gender == pl.gender]
    wanted = str(item.get("role") or "").strip().lower()
    earmarked = [r for r in roles if r.intended and r.intended not in r.tried]   # an actor is already attached
    roles = [r for r in roles if r not in earmarked]
    note = ""
    if wanted and any(r.name.lower() == wanted for r in earmarked):
        note = f"{item.get('role')} is earmarked: the producers are going to another actor first. "
    ranked = []
    for r in roles:
        pool = candidate_pool(st, cfg, proj, r)
        if any(x.id == pl.id for x in pool):
            ranked.append((rank_in_pool(st, cfg, proj, r, pool), r))
    fits_earmarked = [r for r in earmarked if r in proj_roles_fitting(st, cfg, proj, earmarked)]
    if not ranked:
        if fits_earmarked:
            for r in fits_earmarked:
                if pl.id not in r.requested:
                    r.requested.append(pl.id)
            iid = _track(st, item, "watching", f"Parts on '{proj.title}' are spoken for; {agent.name} asked to be "
                                               f"called if one opens up.", data={"project": proj.id, "agent": agent.id})
            return _ruling(item, "pending", note + f"Everything on '{proj.title}' that suits you is spoken for. "
                                                   f"{agent.name} asked to be called if a part opens up.", initiative=iid)
        if not roles and proj.stage == "development" and not earmarked:
            iid = _track(st, item, "watching", f"{agent.name} will push for you when '{proj.title}' starts casting.",
                         data={"project": proj.id, "agent": agent.id})
            return _ruling(item, "pending", f"'{proj.title}' isn't casting yet; {agent.name} has it on their list "
                                            f"and will move when it does.", initiative=iid)
        return _ruling(item, "rejected", note + why_not(st, cfg, proj, roles or earmarked, pl))
    ranked.sort(key=lambda x: (x[0], x[1].id))
    target_rank, target = next(((rk, r) for rk, r in ranked if r.name.lower() == wanted), ranked[0])
    best_rank, best = ranked[0]
    asked = next((r for r in earmarked if r.name.lower() == wanted), None) or target
    if push_succeeds(st, cfg, agent, proj, target_rank, g, pl):
        request(st, cfg, proj, target, pl.id)
        result = "accepted" if asked is target else "partial"
        iid = _track(st, item, "succeeded" if result == "accepted" else "partial",
                     f"{agent.name} got you seen for {target.name} on '{proj.title}'.",
                     data={"project": proj.id, "role": target.id})
        return _ruling(item, result, note + f"{agent.name} pushed and the casting director agreed to see you for "
                                            f"{target.name} ({target.importance}). You'll still have to win the room.",
                       initiative=iid)
    if best is not target and push_succeeds(st, cfg, agent, proj, best_rank, g, pl):
        request(st, cfg, proj, best, pl.id)
        iid = _track(st, item, "partial", f"Seen for {best.name} instead of {target.name} on '{proj.title}'.",
                     data={"project": proj.id, "role": best.id})
        return _ruling(item, "partial", note + f"They won't see you for {target.name}, but they'll see you for "
                                               f"{best.name} ({best.importance}).", initiative=iid)
    from .agents import push_decline_reason
    reason = push_decline_reason(st, cfg, proj, target, pl, target_rank)
    _track(st, item, "failed", f"No traction on '{proj.title}': {reason}.", data={"project": proj.id})
    return _ruling(item, "rejected", note + f"{agent.name} made the call, but no: {reason}.")


def why_not(st, cfg, proj, roles, p) -> str:
    """The concrete reason none of a film's parts can go to this actor."""
    from .casting import fit, window
    start, end = window(proj)
    clash = [c for c in p.calendar if c["start"] <= end and start <= c["end"] and c["project_id"] != proj.id]
    if clash:
        c = clash[0]
        what = st.projects[c["project_id"]].title if c["project_id"] in st.projects else "another job"
        return (f"The dates don't work: '{proj.title}' shoots {proj.shoot_start} to {proj.shoot_end}, and you're "
                f"committed to '{what}' until {c['end']}.")
    if not roles:
        return f"There are no parts on '{proj.title}' for you to play."
    age = age_on(p.birth, st.date)
    r = roles[0]
    if not (r.age_min - 6 <= age <= r.age_max + 6):
        return f"{r.name} is written {r.age_min}-{r.age_max}; at {age} you're outside what they'll consider."
    if fit(p, r, st.date) <= 0.3:
        return f"They don't see you as {r.name}: it's a {r.register} part outside what you're known for."
    return f"Nothing on '{proj.title}' is open to you right now."


def proj_roles_fitting(st, cfg, proj, roles) -> list:
    from .casting import available, fit, window
    pl = st.player
    if not available(pl, *window(proj)):
        return []
    return [r for r in roles if fit(pl, r, st.date) > 0.3]


def push_succeeds(st, cfg, agent, proj, rank, g, client=None) -> bool:
    """An agent's push works through relationships and credibility; it can't overcome a poor fit."""
    from ..world.people import casting_director_for
    cd = casting_director_for(st, proj)
    rel = st.rel(agent.id, cd, create=False) if cd else None
    ag = st.agencies.get(agent.employer)
    base = 0.85 if rank <= 5 else 0.6 if rank <= 15 else 0.3 if rank <= 40 else 0.06 if rank <= 120 else 0.0
    p = base * (0.6 + agent.direction.get("hustle", 50) / 150) * {1: 1.2, 2: 1.0, 3: 0.8}.get(ag.tier if ag else 3, 0.8)
    p += (rel.affinity / 200 if rel else 0.0)
    if client is not None and proj.director_id:      # a director who rates the client opens the door
        dr = st.rel(proj.director_id, client.id, create=False)
        p += max(0.0, dr.affinity) / 60 if dr else 0.0
    return g.random() < clamp(p, 0.0, 0.95)


def request(st, cfg, proj, role, person_id) -> None:
    """The casting director agreed to see this actor. If auditions are already scheduled they join the
    room (the protagonist gets an audition decision; NPCs decide as they would for any audition)."""
    from . import casting
    if person_id not in role.requested:
        role.requested.append(person_id)
    if role.status != "auditioning" or person_id in [a["id"] for a in role.auditioners]:
        return
    p = st.people[person_id]
    if p.controller == "player":
        if not any(d.status == "pending" and d.refs.get("role") == role.id for d in st.decisions.values()):
            casting._invite_player(st, cfg, proj, role, p)
    elif casting._npc_wants_audition(st, cfg, proj, role, p):
        role.auditioners.append({"id": person_id, "prep": 0.0})


# ------------------------------------------------------------------- meet ---
def _meet(st, cfg, item, g) -> dict:
    target, err = resolve(st, item.get("target"), "person")
    if err:
        return _ruling(item, "rejected", err)
    pl = st.player
    if target.id == pl.id:
        return _ruling(item, "rejected", "That's you.")
    r = st.rel(pl.id, target.id, create=False)
    known = r is not None and (r.contact_weeks > 0 or len(r.history) > 0)
    agent = _agent(st)
    access = 0.25 + (0.25 if agent else 0) + (0.3 if known else 0) + min(0.3, pl.fame * 2) - max(0.0, target.fame - pl.fame) * 1.2
    if "agent" in target.roles or "casting_director" in target.roles:
        access += 0.2
    p = clamp(access, 0.03, 0.9)
    due = add_days(st.date, 7 * int(g.integers(1, 4)))
    iid = _track(st, item, "pending", f"Meeting requested with {target.name}.", due=due,
                 data={"target": target.id, "p": round(p, 3), "purpose": str(item.get("approach", ""))[:160]})
    return _ruling(item, "pending", f"Your {'agent' if agent else 'request'} reached out to {target.name}'s people; "
                                    f"an answer should come within a few weeks.", initiative=iid)


def _resolve_meet(st, cfg, ini, g) -> None:
    target = st.people.get(ini["data"]["target"])
    pl = st.player
    if not target or target.death:
        _step(st, ini["id"], "The meeting never happened.", "failed")
        return
    if g.random() < ini["data"]["p"]:
        r = st.rel(pl.id, target.id)
        delta = round(float(g.uniform(2, 7)) * (0.5 + target.personality.get("warmth", 50) / 100), 1)
        r.affinity = round(clamp(r.affinity + delta, -100, 100), 2)
        r.contact_weeks += 1
        what = ini["data"].get("purpose") or "a general meeting"
        r.history.append({"date": st.date, "text": f"a meeting: {what}", "delta": delta})
        st.market.setdefault("contacts", []).append([r.a, r.b, "meeting", 0.5])
        _step(st, ini["id"], f"Met {target.name}.", "succeeded")
        st.log("meeting", f"You met with {target.name} ({what}).", actors=[pl.id, target.id], salience=3, public=False,
               refs={"initiative": ini["id"]})
    else:
        _step(st, ini["id"], f"{target.name}'s office passed on a meeting for now.", "failed")
        st.log("meeting_declined", f"{target.name}'s office passed on a meeting for now.", actors=[pl.id, target.id],
               salience=2, public=False, refs={"initiative": ini["id"]})


# ----------------------------------------------------------- introduction ---
def _introduction(st, cfg, item, g) -> dict:
    target, err = resolve(st, item.get("target"), "person")
    if err:
        return _ruling(item, "rejected", err)
    via, err = resolve(st, item.get("via"), "person")
    if err:
        return _ruling(item, "rejected", f"introduction needs 'via' (someone you know): {err}")
    pl = st.player
    r1 = st.rel(pl.id, via.id, create=False)
    if not r1 or r1.affinity < 8:
        return _ruling(item, "rejected", f"You don't know {via.name} well enough to ask for introductions.")
    r2 = st.rel(via.id, target.id, create=False)
    if not r2 or (r2.contact_weeks == 0 and not r2.history):
        return _ruling(item, "rejected", f"{via.name} doesn't actually know {target.name}.")
    p = clamp(0.2 + r1.affinity / 80 + r2.affinity / 120 - max(0.0, target.fame - pl.fame), 0.05, 0.9)
    if g.random() < p:
        r = st.rel(pl.id, target.id)
        r.affinity = round(clamp(r.affinity + 3, -100, 100), 2)
        r.history.append({"date": st.date, "text": f"introduced by {via.name}", "delta": 3})
        r.contact_weeks += 1
        st.log("introduction", f"{via.name} introduced you to {target.name}.", actors=[pl.id, via.id, target.id],
               salience=3, public=False)
        return _ruling(item, "accepted", f"{via.name} made the introduction to {target.name}.")
    return _ruling(item, "rejected", f"{via.name} wasn't comfortable making that introduction right now.")


# ----------------------------------------------------------------- social ---
def _social(st, cfg, item, g) -> dict:
    target, err = resolve(st, item.get("target"), "person")
    if err:
        return _ruling(item, "rejected", err)
    pl = st.player
    r = st.rel(pl.id, target.id, create=False)
    if not r or (r.contact_weeks == 0 and not r.history):
        return _ruling(item, "rejected", f"You don't know {target.name} personally; try a meeting or an introduction.")
    away = [c for c in target.calendar if c["start"] <= st.date <= c["end"] and c["project_id"] in st.projects
            and st.projects[c["project_id"]].location != "Los Angeles"]
    if away:
        return _ruling(item, "rejected", f"{target.name} is away shooting '{st.projects[away[0]['project_id']].title}' "
                                         f"in {st.projects[away[0]['project_id']].location}.")
    p = clamp(0.35 + r.affinity / 60 + target.personality.get("warmth", 50) / 250 - max(0.0, target.fame - pl.fame), 0.05, 0.95)
    if g.random() < p:
        delta = round(float(g.uniform(1, 4)), 1)
        r.affinity = round(clamp(r.affinity + delta, -100, 100), 2)
        r.contact_weeks += 1
        what = str(item.get("approach", "spent time together"))[:120]
        r.history.append({"date": st.date, "text": what, "delta": delta})
        st.market.setdefault("contacts", []).append([r.a, r.b, "social", 0.6])
        return _ruling(item, "accepted", f"{target.name} accepted.")
    return _ruling(item, "rejected", f"{target.name} begged off this time.")


# -------------------------------------------------------------- publicity ---
def _publicity(st, cfg, item, g) -> dict:
    pl = st.player
    mode = str(item.get("mode") or item.get("details", {}).get("mode") or "interview")
    infl = market.infl(cfg, year(st.date))
    recent = [c for c in pl.credits if c.get("kind") in ("film", "job") and int(c.get("year", 0)) >= year(st.date) - 1]
    if mode == "publicist":
        fee = 1500 * infl
        if pl.directives.get("publicist"):
            return _ruling(item, "rejected", "You already have a publicist on retainer.")
        if pl.cash < 2 * fee:
            return _ruling(item, "rejected", f"A publicist costs about {money(fee)} a month; you can't carry that yet.")
        pl.directives["publicist"] = {"since": st.date, "monthly": round(fee, 0)}
        pl.monthly_costs += fee
        return _ruling(item, "accepted", f"You hired a publicist ({money(fee)}/month). It helps most when you have work to promote.")
    if mode == "talk_show":
        if pl.fame < 0.05 and not recent:
            return _ruling(item, "rejected", "The bookers aren't interested yet: not enough recognition or a current project.")
        p = clamp(0.15 + pl.fame * 2 + (0.2 if recent else 0), 0.05, 0.8)
        if g.random() > p:
            return _ruling(item, "rejected", "The show passed this time.")
        swing = (pl.presence - 50) / 50 + float(g.normal(0, 0.5))
        pl.fame = round(min(0.95, pl.fame + 0.01 * max(0.2, 1 + swing)), 5)
        pl.heat = round(clamp(pl.heat + 6 * swing, -100, 100), 2)
        st.log("talk_show", "You appeared on a network talk show" + (" and it went over well." if swing > 0 else "; it was a little flat."),
               actors=[pl.id], salience=3, public=True)
        return _ruling(item, "accepted", "Booked and aired: " + ("a good spot" if swing > 0 else "an awkward few minutes"))
    if mode in ("interview", "trade_interview", "charity"):
        if not recent and mode != "charity":
            return _ruling(item, "rejected", "There's nothing current to promote, so the trades aren't interested.")
        pl.heat = round(clamp(pl.heat + float(g.uniform(1, 4)), -100, 100), 2)
        pl.prestige = round(clamp(pl.prestige + (1.0 if mode == "charity" else 0.3)), 2)
        st.log("publicity", f"You did a {mode.replace('_', ' ')}.", actors=[pl.id], salience=2, public=True)
        return _ruling(item, "accepted", f"Done: a modest bump in visibility.")
    return _ruling(item, "rejected", "publicity mode must be publicist, interview, talk_show or charity.")


def publicity_week(st, cfg) -> None:
    pl = st.player
    if not pl or not pl.directives.get("publicist"):
        return
    recent = any(c.get("kind") in ("film", "job") and int(c.get("year", 0)) >= year(st.date) - 1 for c in pl.credits)
    pl.fame = round(min(0.95, pl.fame + (0.0008 if recent else 0.0002)), 6)


# ------------------------------------------------------------- reposition ---
def _reposition(st, cfg, item, g) -> dict:
    """A standing directive to the agent. The agent complies, but says what it will cost."""
    pl = st.player
    d = dict(item.get("details") or {})
    for k in ("genres", "avoid_genres", "min_role", "no_tv", "no_commercials", "stage_ok"):
        if k in item:
            d[k] = item[k]
    if not d:
        return _ruling(item, "rejected", "reposition needs details: genres, avoid_genres, min_role "
                                         "(featured|supporting|colead|lead), no_tv, no_commercials.")
    pl.directives.update({k: v for k, v in d.items() if k in ("genres", "avoid_genres", "min_role", "no_tv",
                                                               "no_commercials", "stage_ok")})
    agent = _agent(st)
    warn = []
    if d.get("min_role") in ("lead", "colead") and pl.bankability < 45:
        warn.append("your standing doesn't yet command leads, so expect far fewer auditions")
    if d.get("no_tv") and pl.fame < 0.05:
        warn.append("turning down television will cut both income and visibility")
    if d.get("genres"):
        weak = [x for x in d["genres"] if pl.range.get(x, 50) < 45 and pl.track.get(x, [0, 0])[0] >= 3]
        if weak:
            warn.append(f"you haven't been landing {', '.join(weak)} parts")
    st.log("directive", f"You told {agent.name if agent else 'your agent'}: " + ", ".join(f"{k}={v}" for k, v in d.items()) + ".",
           actors=[pl.id] + ([agent.id] if agent else []), salience=2, public=False)
    return _ruling(item, "accepted", (f"{agent.name if agent else 'Your agent'} will follow it"
                                      + (f", but warns that {'; '.join(warn)}" if warn else "") + "."))


def allows(p, kind: str, role=None, genre: str | None = None) -> bool:
    """Do the client's directives allow this kind of work? (Used by agents for everyone.)"""
    d = p.directives or {}
    if kind in ("tv_guest", "tv_movie") and d.get("no_tv"):
        return False
    if kind == "commercial" and d.get("no_commercials"):
        return False
    if role is not None and d.get("min_role"):
        order = ["featured", "supporting", "colead", "lead"]
        if order.index(role.importance) < order.index(d["min_role"]):
            return False
    if genre and genre in (d.get("avoid_genres") or []):
        return False
    return True


def genre_bias(p, genre: str) -> float:
    g = (p.directives or {}).get("genres")
    return 1.4 if g and genre in g else (0.8 if g else 1.0)


# -------------------------------------------------------- develop_project ---
def _develop_project(st, cfg, item, g) -> dict:
    """An original film: hire a writer (weeks, money), then your agent pitches it to studios,
    who decide on their own read of the script, your standing and their slate."""
    pl = st.player
    details = dict(item.get("details") or {})
    if item.get("project") or item.get("action"):
        return _develop_follow_up(st, cfg, item, g)
    logline = str(item.get("logline") or details.get("logline") or item.get("approach") or "").strip()
    genre = str(item.get("genre") or details.get("genre") or "drama")
    from .. import models as M
    if genre not in M.GENRES:
        return _ruling(item, "rejected", f"genre must be one of {', '.join(M.GENRES)}.")
    if len(logline) < 20:
        return _ruling(item, "rejected", "develop_project needs a logline (a sentence describing the film).")
    infl = market.infl(cfg, year(st.date))
    fee = round(15000 * infl * float(g.uniform(0.7, 1.4)), -2)
    if pl.cash < fee:
        return _ruling(item, "rejected", f"Hiring a screenwriter would cost about {money(fee)}; you have {money(pl.cash)}.")
    pl.cash -= fee
    details["fee"] = fee
    skill = clamp(float(g.normal(50, 13)), 10, 95)
    weeks = int(g.integers(8, 17))
    due = add_days(st.date, 7 * weeks)
    writer = f"{['Paul', 'Ellen', 'Marty', 'Sandra', 'Jules', 'Nina'][int(g.integers(6))]} {['Kessler', 'Ruiz', 'Hale', 'Brandt', 'Okafor', 'Lindqvist'][int(g.integers(6))]}"
    iid = _track(st, item, "writing", f"Hired screenwriter {writer} ({money(fee)}); first draft due about {due}.", due=due,
                 data={"logline": logline, "genre": genre, "writer": writer, "skill": round(skill, 2),
                       "title": str(item.get("title") or details.get("title") or "Untitled project"), "pitched": [],
                       "interested": [], "attached": [], "fee": fee})
    st.log("development", f"You hired {writer} to write '{st.initiatives[iid]['data']['title']}' ({money(fee)}).",
           actors=[pl.id], salience=3, public=False, refs={"initiative": iid})
    return _ruling(item, "pending", f"{writer} is writing it; expect a draft around {due}. Then your agent can pitch it.",
                   initiative=iid)


def _develop_follow_up(st, cfg, item, g) -> dict:
    """Build the package: attach a director or actor, or commission a rewrite. Interested studios
    then read it again."""
    pl = st.player
    ref = str(item.get("project") or "")
    ini = st.initiatives.get(ref) or next((x for x in st.initiatives.values() if x["kind"] == "develop_project"
                                           and x["data"].get("title", "").lower() == ref.lower()), None)
    if not ini or ini["kind"] != "develop_project":
        return _ruling(item, "rejected", f"No project in development matches '{ref}' (use its initiative id or title).")
    data, action = ini["data"], item.get("action")
    if ini["status"] in ("greenlit", "writing"):
        return _ruling(item, "rejected", f"'{data['title']}' is {ini['status']}; there's nothing to change right now.")
    if action == "revise":
        fee = round(data.get("fee", 15000 * market.infl(cfg, year(st.date))) * 0.5, -2)
        if pl.cash < fee:
            return _ruling(item, "rejected", f"A rewrite would cost about {money(fee)}; you have {money(pl.cash)}.")
        pl.cash -= fee
        data["quality"] = round(clamp(data["quality"] + float(g.normal(4, 6)), 5, 95), 2)
        ini["status"], ini["due"] = "writing", add_days(st.date, 7 * int(g.integers(5, 10)))
        data["rewrite"] = True
        _step(st, ini["id"], f"Commissioned a rewrite from {data['writer']} ({money(fee)}); due about {ini['due']}.")
        return _ruling(item, "pending", f"{data['writer']} is rewriting '{data['title']}' ({money(fee)}).", initiative=ini["id"])
    if action != "attach":
        return _ruling(item, "rejected", "develop_project follow-ups: action attach (with target) or revise.")
    person, err = resolve(st, item.get("target"), "person")
    if err:
        return _ruling(item, "rejected", err)
    if person.id in data["attached"]:
        return _ruling(item, "rejected", f"{person.name} is already attached.")
    if not ({"actor", "director"} & set(person.roles)):
        return _ruling(item, "rejected", f"{person.name} isn't an actor or director.")
    # they read the script and decide for themselves: the read, their standing versus yours, how busy they are
    read = data["quality"] + float(g.normal(0, 10))
    r = st.rel(pl.id, person.id, create=False)
    busy = sum(1 for c in person.calendar if c["end"] >= st.date)
    want = (read - 50) / 25 + (r.affinity / 30 if r else 0) - max(0.0, person.prestige - pl.prestige) / 30 \
        - max(0.0, person.fame - pl.fame) * 3 - 0.5 * busy + (person.goals.get("art", 0.2) - 0.2) * 2
    if want > float(g.normal(0.4, 0.5)):
        data["attached"].append(person.id)
        data["pitched"] = [x for x in data["pitched"] if x not in data["interested"]]   # interested studios re-read
        ini["status"], ini["due"] = "pitching", add_days(st.date, 14)
        _step(st, ini["id"], f"{person.name} read '{data['title']}' and agreed to attach.")
        st.log("development", f"{person.name} agreed to attach to '{data['title']}'.", actors=[pl.id, person.id],
               salience=3, public=False, refs={"initiative": ini["id"]})
        return _ruling(item, "accepted", f"{person.name} read it and said yes. Your agent will take the package back "
                                         f"to the studios that were interested.", initiative=ini["id"])
    why = ("the script didn't grab them" if read < 50 else "they're committed elsewhere" if busy
           else "they want to see more traction first")
    _step(st, ini["id"], f"{person.name} passed on attaching ({why}).")
    return _ruling(item, "rejected", f"{person.name} passed: {why}.", initiative=ini["id"])


def _resolve_development(st, cfg, ini, g) -> None:
    pl = st.player
    data = ini["data"]
    if ini["status"] == "writing":
        if data.get("rewrite"):
            quality = data["quality"]
            data["rewrite"] = False
            data["pitched"] = [x for x in data["pitched"] if x not in data["interested"]]
        else:
            quality = clamp(data["skill"] + float(g.normal(0, 10)), 5, 95)
        data["quality"] = round(quality, 2)                    # hidden: never shown
        read = ("you love it" if quality + float(g.normal(0, 8)) > 62 else "it's promising but uneven"
                if quality > 45 else "honestly, it isn't there yet")
        _step(st, ini["id"], f"{data['writer']} delivered the draft of '{data['title']}'; {read}.", "pitching")
        ini["due"] = add_days(st.date, 14)
        st.log("development", f"The draft of '{data['title']}' arrived; {read}.", actors=[pl.id], salience=3,
               public=False, refs={"initiative": ini["id"]})
        return
    if ini["status"] == "pitching":
        studios = [s for s in sorted(st.studios.values(), key=lambda s: s.id) if s.slate_per_year > 0
                   and s.id not in data["pitched"]]
        if not studios:
            interested = [st.studios[x].name for x in data.get("interested", [])]
            _step(st, ini["id"], "Every studio has passed; the project is in turnaround"
                  + (f" ({', '.join(interested)} would look again with a stronger package or a rewrite)." if interested else "."),
                  "turnaround")
            return
        again = [x for x in studios if x.id in data.get("interested", [])]   # those who asked to see it again first
        s = (again or studios)[int(g.integers(len(again or studios)))]
        data["pitched"].append(s.id)
        read = data["quality"] + float(g.normal(0, 12)) * (1.5 - s.exec_taste / 100)
        names = [st.people[x] for x in data.get("attached", []) if x in st.people]
        package = max([pl.bankability] + [x.bankability for x in names if "actor" in x.roles])
        package += max([0.0] + [x.prestige for x in names if "director" in x.roles]) * 0.25
        appeal = (read * 0.55 + package * 0.35 + s.genre_weights.get(data["genre"], 1.0) * 10
                  + (s.risk_appetite - 50) * 0.2)
        if appeal >= 62:
            proj = _greenlight_development(st, cfg, ini, s, g)
            _step(st, ini["id"], f"{s.name} said yes: '{proj.title}' is greenlit with you attached.", "greenlit")
            st.log("development", f"{s.name} greenlit '{proj.title}', developed by you.", actors=[pl.id], salience=4,
                   public=True, refs={"project": proj.id, "initiative": ini["id"]})
        elif appeal >= 52:
            if s.id not in data.setdefault("interested", []):
                data["interested"].append(s.id)
            _step(st, ini["id"], f"{s.name} liked it but wants changes or a bigger name attached; still pitching.")
            ini["due"] = add_days(st.date, 21)
        else:
            _step(st, ini["id"], f"{s.name} passed.")
            ini["due"] = add_days(st.date, 14)
        st.log("pitch", f"Pitched '{data['title']}' to {s.name}: " + ini["steps"][-1]["text"], actors=[pl.id],
               salience=2, public=False, refs={"initiative": ini["id"]})


def _greenlight_development(st, cfg, ini, studio, g):
    from ..world import genesis
    from . import casting
    data = ini["data"]
    p = genesis.make_project(st, cfg, studio, f"dev-{ini['id']}", st.date)
    p.title, p.genre, p.premise = data["title"], data["genre"], data["logline"].rstrip(".") + "."
    p.script_quality = data["quality"]
    p.logline_extra = "an original project developed by its star"
    genesis.schedule_from_greenlight(cfg, p, st.date, g)
    p.stage = "prepro"
    casting.attach_director(st, cfg, p)
    lead = next((st.roles[r] for r in p.role_ids if st.roles[r].importance == "lead"), None)
    if lead:
        lead.gender = st.player.gender
        age = age_on(st.player.birth, st.date)
        lead.age_min, lead.age_max = age - 5, age + 5
        lead.requested.append(st.player_id)
        lead.intended = st.player_id          # the developer is the attachment; still must accept terms
    return p


# ------------------------------------------------------------ weekly step ---
def step(st: WorldState, cfg: dict) -> None:
    publicity_week(st, cfg)
    for iid, ini in sorted(st.initiatives.items()):
        if not ini.get("due") or ini["due"] > st.date:
            continue
        g = R.stream(st.seed, "initiative-step", iid, st.date)
        if ini["kind"] == "meet" and ini["status"] == "pending":
            _resolve_meet(st, cfg, ini, g)
            ini["due"] = None
        elif ini["kind"] == "develop_project" and ini["status"] in ("writing", "pitching"):
            _resolve_development(st, cfg, ini, g)
            if ini["status"] not in ("writing", "pitching"):
                ini["due"] = None
    # agents keep watch on films a client asked them to pursue
    for iid, ini in sorted(st.initiatives.items()):
        if ini["status"] != "watching":
            continue
        proj = st.projects.get(ini["data"]["project"])
        if not proj or proj.stage in ("shooting", "post", "awaiting_release", "released", "dead"):
            _step(st, iid, "The film moved on before anything opened up.", "failed")
        elif proj.stage == "prepro":
            g = R.stream(st.seed, "initiative-watch", iid, st.date)
            res = _pursue_project(st, cfg, {"kind": "pursue_project", "target": proj.id, "_follow_up": iid}, g)
            if res["result"] == "pending":
                continue                               # still spoken for; keep watching
            _step(st, iid, "Casting opened: " + res["text"], "succeeded" if res["result"] in ("accepted", "partial") else "failed")
            st.log("agent_push", f"'{proj.title}' started casting: {res['text']}", actors=[st.player_id], salience=3,
                   public=False, refs={"project": proj.id, "initiative": iid})
