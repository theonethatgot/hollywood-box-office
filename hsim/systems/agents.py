"""Agents, submissions and casting directors.

How a role gets cast (for every actor, player or NPC):
  1. The casting director (CD) brings in a few people they already have in mind
     (top of the casting-utility ranking: observed standing, fit, relationships).
  2. Agents read the breakdown and SUBMIT clients. Whether an agent submits a client
     depends on the agent's hustle, the client's fit, and the agent's STRATEGY, which
     is derived from the client's goals (money, fame, prestige, art, stability).
  3. The CD screens submissions and calls in the best; the rest are passed on with a
     reason that comes from the actual scoring (wanted a name, wrong age, not the type...).
  4. Auditions leave impressions: CDs and directors remember strong and weak reads,
     which feed later casting through relationships.

The protagonist's agent also checks in monthly with a factual summary of this activity.
"""
from __future__ import annotations

import math

from .. import models as M
from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_days, age_on, clamp, days_between, money, year
from . import market
from .initiatives import allows, genre_bias

STRATEGY_TEXT = {
    "money": "the best-paying work available, including commercials",
    "fame": "high-visibility parts in wide releases and network TV",
    "prestige": "respected directors and serious dramatic material",
    "art": "interesting scripts, stage work and character parts, even for less money",
    "stability": "steady bookings and series work over long shots",
}


# --------------------------------------------------------------- strategy ---
def strategy_fit(st: WorldState, client: M.Person, proj: M.Project | None, role: M.Role | None,
                 kind: str | None = None) -> float:
    """0..1: how well an opportunity matches what the client wants (agent's view)."""
    g = client.goals or {}
    director = st.people.get(proj.director_id) if proj and proj.director_id else None
    size = {"lead": 1.0, "colead": 0.7, "supporting": 0.35, "featured": 0.15}.get(role.importance if role else "", 0.2)
    real_m = (proj.budget / 1e6) if proj else 1.0
    feats = {
        "money": min(1.0, real_m / 15) * 0.6 + size * 0.4 if proj else (0.9 if kind == "commercial" else 0.4),
        "fame": size * 0.6 + min(1.0, real_m / 15) * 0.4 if proj else (0.6 if kind in ("tv_guest", "tv_movie") else 0.2),
        "prestige": ((director.prestige / 100 if director else 0.3) * 0.6 + (0.4 if proj.genre == "drama" else 0.1))
        if proj else (0.5 if kind == "stage" else 0.1),
        "art": (0.6 if proj.genre in ("drama", "thriller") else 0.3) + 0.2 * size if proj
        else (0.9 if kind == "stage" else 0.2 if kind == "commercial" else 0.4),
        "stability": 0.5 if proj else (0.8 if kind in ("tv_guest", "commercial") else 0.5),
    }
    tot = sum(g.values()) or 1.0
    return clamp(sum(g.get(k, 0) * v for k, v in feats.items()) / tot, 0.0, 1.0)


def strategy_summary(client: M.Person) -> str:
    g = client.goals or {}
    top = sorted(g, key=g.get, reverse=True)[:2]
    low = min(g, key=g.get) if g else None
    txt = "Pursuing " + " and ".join(STRATEGY_TEXT[k] for k in top)
    if low and low not in top:
        txt += f"; not prioritising {STRATEGY_TEXT[low].split(',')[0]}"
    return txt + "."


def agent_hustle(st: WorldState, p: M.Person) -> float:
    a = st.people.get(p.agent_person_id) if p.agent_person_id else None
    if a:
        return a.direction.get("hustle", 50.0)
    ag = st.agencies.get(p.agent_id) if p.agent_id else None
    return ag.hustle if ag else 0.0


# ------------------------------------------------------------ submissions ---
def build_audition_list(st: WorldState, cfg: dict, proj: M.Project, role: M.Role, pool: list, ranked: list,
                        utilities: dict) -> list:
    """Combine the CD's own picks with agent submissions; record outcomes."""
    from ..world.people import casting_director_for
    ac = cfg["agents"]
    cd_id = casting_director_for(st, proj)
    known = ranked[:ac["cd_known_picks"]]
    known_ids = {p.id for p in known}
    req = [p for p in ranked if p.id in role.requested and p.id not in known_ids]   # agreed after an agent's push
    known_ids |= {p.id for p in req}
    submitted = []
    for p in pool:
        if p.id in known_ids or not p.agent_id:
            continue
        from .casting import fit
        f = fit(p, role, st.date)
        hustle = agent_hustle(st, p) / 100
        strat = strategy_fit(st, p, proj, role)
        if not allows(p, "film", role, proj.genre):
            continue
        prob = (ac["submit_base"] * (0.4 + hustle) * max(0.0, f - 0.35) * 2.2 * (0.5 + strat) * niche_factor(p, role.register)
                * genre_bias(p, proj.genre))
        if R.unit(st.seed, "submit", role.id, p.id) < prob:
            submitted.append(p)
    # CD screening: same observed utility, plus what this CD remembers about the actor
    def screen(p):
        rel = st.rel(cd_id, p.id, create=False) if cd_id else None
        return utilities[p.id] + (rel.affinity / 4 if rel else 0.0) + 6 * R.gauss(st.seed, "screen", role.id, p.id)
    submitted.sort(key=lambda p: (-screen(p), p.id))
    slots = max(0, cfg["casting"]["audition_size"] - len(known))
    called = submitted[:slots]
    passed = submitted[slots:]
    st.market.setdefault("submission_stats", {"submitted": 0, "called_in": 0})
    st.market["submission_stats"]["submitted"] += len(submitted)
    st.market["submission_stats"]["called_in"] += len(called)
    pl = st.player_id
    for p in called:
        if p.id == pl:
            _record(st, proj, role, cd_id, "called in", "the casting director liked your submission")
    for p in passed:
        if p.id == pl:
            _record(st, proj, role, cd_id, "passed", pass_reason(st, cfg, proj, role, p))
    if pl and any(p.id == pl for p in known):
        _record(st, proj, role, cd_id, "requested", "the casting director asked for you by name")
    if pl and any(p.id == pl for p in req):
        _record(st, proj, role, cd_id, "requested", "seen because your agent pushed for you")
    return known + req + called


def pass_reason(st, cfg, proj, role, p) -> str:
    from .casting import fit, star_weight
    age = age_on(p.birth, st.date)
    mid = (role.age_min + role.age_max) / 2
    sw = star_weight(cfg, proj, role, st.date)
    if sw > 0.8 and p.bankability < 35:
        return "they want a bigger name for this part"
    if abs(age - mid) > (role.age_max - role.age_min) / 2:
        return f"they went {'younger' if age > mid else 'older'}"
    if p.range.get(role.register, 50) < 45:
        return f"they didn't see you as a {role.register} type"
    return "they went with other actors"


def pass_reason_tv(st, p, center: int, register: str) -> str:
    age = age_on(p.birth, st.date)
    if abs(age - center) > 6:
        return f"they went {'younger' if age > center else 'older'}"
    if p.range.get(register, 50) < 45:
        return f"they didn't see you for a {register} part"
    return "they had plenty of strong submissions"


def _record(st, proj, role, cd_id, status, reason) -> None:
    cd = st.people.get(cd_id) if cd_id else None
    rec = {"date": st.date, "project": proj.id, "title": proj.title, "role": role.name, "importance": role.importance,
           "studio": st.studios[proj.studio_id].name, "cd": cd.name if cd else None, "status": status, "reason": reason}
    st.market.setdefault("player_submissions", []).append(rec)
    if status in ("called in", "requested"):
        st.log("called_in", f"Your agent got you in the room: {role.name} in '{proj.title}' "
                            f"(casting: {cd.name if cd else 'the studio'}) — {reason}.",
               actors=[st.player_id] + ([cd.id] if cd else []), refs={"project": proj.id}, salience=2, public=False)


# -------------------------------------------------------------- impressions ---
def audition_impressions(st: WorldState, cfg: dict, proj: M.Project, role: M.Role, scored: list) -> None:
    """CDs and directors remember auditions. scored: [(studio_view, score, person)]."""
    from ..world.people import casting_director_for
    if not scored:
        return
    scores = sorted(s for _, s, _ in scored)
    median = scores[len(scores) // 2]
    watchers = [x for x in (casting_director_for(st, proj), proj.director_id) if x]
    n = len(scored)
    for rank, (_, sc, p) in enumerate(sorted(scored, key=lambda x: -x[1])):
        delta = impression(cfg, sc, median)
        record_track(p, role.register, rank, n)
        for w in watchers:
            r = st.rel(w, p.id)
            r.affinity = round(clamp(r.affinity + delta, -100, 100), 2)
            r.contact_weeks += 0          # an audition is a meeting, not working together
            word = "a strong audition" if delta > 2 else "a solid audition" if delta > -1 else "an audition that didn't land"
            r.history.append({"date": st.date, "text": f"{word} for '{proj.title}'", "delta": round(delta, 1)})


def impression(cfg, score: float, median: float) -> float:
    """Asymmetric memory: an ordinary read leaves no mark, a clearly weak one a small
    mark, a strong one real goodwill. (A zero-sum rule made frequent auditioners sink.)"""
    im = cfg["agents"]["impressions"]
    gap = score - median
    if gap >= im["strong_margin"]:
        return round(min(im["max_gain"], gap / 3), 2)
    if gap <= -im["weak_margin"]:
        return -round(min(im["max_loss"], (-gap - im["weak_margin"]) / 6 + 0.5), 2)
    return 0.0


def record_track(p: M.Person, register: str, rank: int, n: int) -> None:
    """What an agent learns from results: where the client lands near the top of the room."""
    t = p.track.setdefault(register, [0, 0])
    t[0] += 1
    if rank < max(1, n // 3):
        t[1] += 1


def niche_factor(p: M.Person, register: str) -> float:
    """Agents steer submissions toward the kinds of parts where the client does well."""
    n, good = p.track.get(register, (0, 0))
    overall_n = sum(v[0] for v in p.track.values())
    overall_good = sum(v[1] for v in p.track.values())
    base = (overall_good + 1) / (overall_n + 3)
    here = (good + base * 3) / (n + 3)            # shrink toward the client's overall rate
    return clamp(0.6 + 1.2 * here, 0.6, 1.5)


def best_niche(p: M.Person) -> str | None:
    rated = [(r, (v[1] + 0.5) / (v[0] + 2)) for r, v in p.track.items() if v[0] >= 3]
    if len(rated) < 2:
        return None
    best = max(rated, key=lambda x: x[1])
    avg = sum(x[1] for x in rated) / len(rated)
    return best[0] if best[1] > avg * 1.3 else None


def memory_fades(st: WorldState, cfg: dict) -> None:
    """Monthly: casting directors' and directors' impressions of actors fade toward neutral
    (bad ones over months, good ones over years). Friendships and feuds are unaffected."""
    if st.date[8:10] > "07":
        return
    im = cfg["agents"]["impressions"]
    pros = {pid for pid, p in st.people.items() if "casting_director" in p.roles or "director" in p.roles}
    for r in st.rels.values():
        if r.status != "acquainted" or not ((r.a in pros) ^ (r.b in pros)):
            continue
        if r.affinity < 0:
            r.affinity = round(r.affinity * im["negative_monthly_keep"], 2)
        elif r.affinity > 0:
            r.affinity = round(r.affinity * im["positive_monthly_keep"], 2)


# ---------------------------------------------------------------- check-ins ---
def step(st: WorldState, cfg: dict) -> None:
    """Monthly agent check-in with the protagonist (first tick of the month)."""
    pl = st.player
    if not pl or not pl.agent_person_id or st.date[8:10] > "07" or st.date == st.start_date:
        return
    agent = st.people[pl.agent_person_id]
    since = add_days(st.date, -35)
    subs = [s for s in st.market.get("player_submissions", []) if s["date"] >= since]
    jobs = [j for j in st.market.get("jobs", []) + st.market.get("jobs_done", []) if j.get("person") == pl.id
            and j.get("booked", j.get("start", "")) >= since]
    called = [s for s in subs if s["status"] in ("called in", "requested")]
    passes = [s for s in subs if s["status"] == "passed"]
    reasons = {}
    for s in passes:
        reasons[s["reason"]] = reasons.get(s["reason"], 0) + 1
    parts = [f"{agent.name} checked in"]
    if subs:
        parts.append(f"they submitted you for {len(subs)} role{'s' if len(subs) != 1 else ''} this past month; "
                     f"{len(called)} got you in the room")
        if reasons:
            top = max(reasons, key=reasons.get)
            parts.append(f"the most common feedback on passes: '{top}'")
    else:
        parts.append("there was little in your range this month to submit you for")
    if jobs:
        parts.append(f"{len(jobs)} smaller booking{'s' if len(jobs) != 1 else ''} came through")
    niche = best_niche(pl)
    if niche:
        parts.append(f"they're steering you toward {niche} parts, where you've been landing near the top of the room")
    advice = _advice(st, cfg, pl)
    if advice:
        parts.append(advice)
    st.log("agent_checkin", "; ".join(parts) + ".", actors=[pl.id, agent.id], salience=2, public=False,
           data={"submitted": len(subs), "called_in": len(called)})
    r = st.rel(pl.id, agent.id)
    r.contact_weeks += 1
    r.history.append({"date": st.date, "text": "monthly check-in call", "delta": 0})


def _advice(st, cfg, p) -> str:
    """Advice grounded in the client's actual state and goals."""
    g = p.goals or {}
    top = max(g, key=g.get) if g else "money"
    if p.cash < p.monthly_costs:
        return "money is tight, so they suggest taking every commercial and guest spot that fits"
    if p.craft < 35:
        return "they think a good acting class would sharpen your auditions"
    if top in ("prestige", "art"):
        return "they want to get you seen in a respected stage production"
    if top == "fame":
        return "they're pushing to get you in front of network casting"
    return ""


# ------------------------------------------------------------ agent plans ---
# Each week every agent decides where to spend their calls. Agents are commercially
# motivated: they push for the clients whose careers pay (quote, standing, momentum) and
# for clients with a real angle on a specific film (they've worked with its director, or
# the part is squarely in their proven niche). A push asks the casting director to see the
# client; it works through the agent's credibility and relationship with that CD, and it
# can't overcome a poor fit. A successful push only gets the client into the room.
# The protagonist is one client among many: no rule here looks at who is the player.
SIZE_UPSIDE = {"lead": 1.0, "colead": 0.75, "supporting": 0.4, "featured": 0.12}


def plan_week(st: WorldState, cfg: dict) -> None:
    if st.date == st.start_date:
        return
    from .casting import available, fit, star_weight, window
    from . import initiatives as INI
    ap = cfg["agents"]["plans"]
    roles = []                                      # principal roles not yet casting, on films with a director
    for pid, proj in sorted(st.projects.items()):
        if proj.stage not in ("development", "prepro"):
            continue
        for rid in proj.role_ids:
            r = st.roles[rid]
            if r.importance == "featured" or r.cast_id or r.intended:
                continue
            if r.status == "open" or (r.status == "auditioning" and r.audition_date and r.audition_date > st.date):
                roles.append((proj, r))
    if not roles:
        return
    worked = {}                                     # director -> people they've built goodwill with
    directors = {p.director_id for p, _ in roles if p.director_id}
    for r in st.rels.values():
        if r.affinity >= ap["connection_affinity"]:
            if r.a in directors:
                worked.setdefault(r.a, set()).add(r.b)
            if r.b in directors:
                worked.setdefault(r.b, set()).add(r.a)
    clients = {}
    for p in st.actors():
        if p.agent_person_id:
            clients.setdefault(p.agent_person_id, []).append(p)
    log = st.market.setdefault("agent_pushes", [])
    rooms = {}
    for aid in sorted(clients):
        agent = st.people.get(aid)
        if not agent or agent.death:
            continue
        hustle = agent.direction.get("hustle", 50)
        info = st.agencies[agent.employer].info_quality if agent.employer in st.agencies else 50
        calls = 1 + int(hustle >= 75)
        book = sorted(clients[aid], key=lambda c: (-commission_potential(st, cfg, c), c.id))
        focus = {c.id for c in book[:ap["focus_clients"]]}
        options = []
        for c in book:
            age = age_on(c.birth, st.date)
            for proj, role in roles:
                if role.gender != c.gender or not (role.age_min - 3 <= age <= role.age_max + 3):
                    continue
                angle = c.id in worked.get(proj.director_id, ())
                if c.id not in focus and not angle:
                    continue
                if c.id in role.requested or c.id in role.tried or c.id in [a['id'] for a in role.auditioners] or not INI.allows(c, "film", role, proj.genre):
                    continue
                f = fit(c, role, st.date)
                if f < ap["min_fit"]:
                    continue
                need = star_weight(cfg, proj, role, st.date) * 60
                reach = clamp(1 - max(0.0, need - c.bankability) / 60, 0.05, 1.0)
                director = st.people.get(proj.director_id) if proj.director_id else None
                upside = (SIZE_UPSIDE[role.importance] * math.log10(max(proj.budget, 1e5) / 1e5)
                          * (0.6 + (director.prestige if director else 30) / 100))
                score = (upside * f * reach * (0.5 + strategy_fit(st, c, proj, role)) * INI.genre_bias(c, proj.genre)
                         * niche_factor(c, role.register) * (1.5 if angle else 1.0))
                options.append((score, c, proj, role, angle))
        options.sort(key=lambda x: (-x[0], x[1].id, x[3].id))
        # the agent's read of the room for the most attractive options: is a call worth spending?
        judged, per_client, shortlist = [], {}, []
        for o in options:                         # the best few options for each client, not one client's leads
            if per_client.get(o[1].id, 0) < 3:
                per_client[o[1].id] = per_client.get(o[1].id, 0) + 1
                shortlist.append(o)
        for score, c, proj, role, angle in shortlist[:ap["options_considered"]]:
            if not available(c, *window(proj)):
                continue
            if role.id not in rooms:                 # computed once per role per week, only when needed
                rooms[role.id] = INI.room(st, cfg, proj, role)
            rm = rooms[role.id]
            if c.id not in rm["u"]:
                continue
            rank = rm["order"].index(c.id) + 1
            if rank <= cfg["agents"]["cd_known_picks"] and role.status == "open":
                continue                          # the CD will call them in anyway
            read = rank * math.exp(0.5 * (1 - info / 100) * R.gauss(st.seed, "agent-read", agent.id, role.id, c.id))
            odds = 0.85 if read <= 5 else 0.6 if read <= 15 else 0.3 if read <= 40 else 0.05
            if odds < ap["min_odds"]:
                continue
            judged.append((score * odds, c, proj, role, angle, rank))
        judged.sort(key=lambda x: (-x[0], x[1].id, x[3].id))
        used = set()
        for value, c, proj, role, angle, rank in judged:
            if calls <= 0:
                break
            if c.id in used:
                continue
            used.add(c.id)
            calls -= 1
            _push(st, cfg, agent, c, proj, role, angle, rank, log)
    if len(log) > 400:
        del log[:-400]


def commission_potential(st: WorldState, cfg: dict, c: M.Person) -> float:
    """What a client is worth to an agent's book: earnings, standing, momentum."""
    infl = market.infl(cfg, year(st.date))
    return (math.log10(max(c.quote / infl, 1e4)) * 12 + c.bankability * 0.5 + max(0.0, c.heat) * 0.2
            + c.prestige * 0.1)


def _push(st, cfg, agent, c, proj, role, angle, rank, log) -> None:
    from . import initiatives as INI
    from ..world.people import casting_director_for
    g = R.stream(st.seed, "agent-push", agent.id, c.id, role.id, st.date)
    ok = INI.push_succeeds(st, cfg, agent, proj, rank, g)
    director = st.people.get(proj.director_id) if proj.director_id else None
    why = (f"{c.name} has worked well with {director.name}" if angle
           else f"{c.name} is one of their priority clients")
    rec = {"date": st.date, "agent": agent.id, "client": c.id, "project": proj.id, "role": role.id,
           "result": "agreed to see" if ok else "declined", "why": why, "rank_read": rank}
    cd_id = casting_director_for(st, proj)
    if ok:
        INI.request(st, cfg, proj, role, c.id)
    else:
        rec["reason"] = push_decline_reason(st, cfg, proj, role, c, rank)
        if cd_id:                                     # pushing poor fits costs a little credibility
            r = st.rel(agent.id, cd_id)
            r.affinity = round(clamp(r.affinity - cfg["agents"]["plans"]["failed_push_cost"], -100, 60), 2)
    log.append(rec)
    if c.controller == "player":
        cd = st.people.get(cd_id) if cd_id else None
        because = (f"you've worked well with {director.name}" if angle else "you're one of their priority clients")
        text = (f"{agent.name} pushed for you on {role.name} ({role.importance}) in '{proj.title}' "
                f"({st.studios[proj.studio_id].name}, {'director ' + director.name if director else 'no director yet'}) "
                f"because {because}; "
                + (f"{cd.name if cd else 'casting'} agreed to see you when casting opens."
                   if ok else f"casting declined: {rec['reason']}."))
        st.log("agent_push", text, actors=[c.id, agent.id] + ([cd.id] if cd else []),
               refs={"project": proj.id, "role": role.id}, salience=3 if ok else 2, public=False)


def push_decline_reason(st, cfg, proj, role, c, rank) -> str:
    """Why a casting director won't take the meeting (from the same observed values that rank the room)."""
    r = pass_reason(st, cfg, proj, role, c)
    if r != "they went with other actors":
        return r
    return ("they already have stronger candidates in mind" if rank > 40
            else "they're keeping the list short and you didn't make it")


def placement_goodwill(st: WorldState, cfg: dict, proj: M.Project, p: M.Person) -> None:
    """Agents who place clients build credibility with that casting director."""
    from ..world.people import casting_director_for
    cd = casting_director_for(st, proj)
    if cd and p.agent_person_id and p.agent_person_id in st.people:
        r = st.rel(p.agent_person_id, cd)
        r.affinity = round(clamp(r.affinity + cfg["agents"]["plans"]["placement_goodwill"], -100, 60), 2)
