"""Jobbing work: the everyday market that keeps working actors working.

Every job is concrete: a named TV series episode with a character and colleagues,
a commercial with a director, a bit part in a real production in the pipeline, a
TV movie with a cast, or a stage production of a real play. Colleagues become
contacts (relationships with shared history). Offers arrive through agents at rates
that depend on representation, standing and craft; which kinds an agent pursues
follows the client's goals (agents.strategy_fit). The same rules apply to everyone.
"""
from __future__ import annotations

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_days, add_weeks, clamp, money, year
from . import decisions as D
from . import finance, market

KINDS = {  # weeks, pay range (1980 $), craft gain, fame gain, base weight
    "tv_guest": (1, (2500, 6000), 0.6, 0.002, 0.0),    # cast via systems/tvcasting.py
    "commercial": (1, (1500, 9000), 0.1, 0.001, 3.0),
    "film_bit": (2, (3000, 9000), 0.7, 0.001, 2.0),
    "tv_movie": (3, (6000, 15000), 1.0, 0.004, 1.5),
    "stage": (6, (3000, 8000), 1.6, 0.0005, 1.0),
}
PRODUCTS = ["a soft drink", "a family sedan", "a long-distance phone company", "a breakfast cereal", "a shampoo",
            "a fast-food chain", "a department store", "a light beer", "an airline", "a camera"]
PLAYS = [("The Seagull", "Chekhov"), ("A Doll's House", "Ibsen"), ("Twelfth Night", "Shakespeare"),
         ("Hedda Gabler", "Ibsen"), ("Uncle Vanya", "Chekhov"), ("Much Ado About Nothing", "Shakespeare"),
         ("The Importance of Being Earnest", "Wilde"), ("Arms and the Man", "Shaw"), ("Macbeth", "Shakespeare"),
         ("The Cherry Orchard", "Chekhov"), ("An Enemy of the People", "Ibsen"), ("Candida", "Shaw")]
THEATRES = ["a 99-seat theatre in Hollywood", "a respected regional company in Pasadena",
            "a small house on Theatre Row in New York", "a downtown Los Angeles repertory company",
            "a summer festival in Connecticut"]
TVM_TITLES = ["Nightmare on Route 9", "A Mother's Secret", "The Long Way Home", "Deadly Inheritance", "Summer of '62",
              "Terror at Lake Wren", "The Last Letter", "Danger in Paradise", "Fallen Star", "A Town Called Hope"]


def _rate(st, cfg, p) -> float:
    jc = cfg["jobbing"]
    ag = st.agencies.get(p.agent_id) if p.agent_id else None
    if ag:
        from .agents import agent_hustle
        agent_f = {1: 1.4, 2: 1.0, 3: 0.7}[ag.tier] * (0.6 + agent_hustle(st, p) / 125)
    else:
        agent_f = jc["no_agent_factor"]
    standing = 0.5 + p.craft / 120 + min(0.6, p.fame * 8) + max(-0.3, min(0.3, p.heat / 150))
    stardom = 1.0 if p.bankability < 50 else max(0.1, 1 - (p.bankability - 50) / 40)
    return jc["base_weekly"] * agent_f * standing * stardom


def _busy(p, start, end) -> bool:
    from .casting import available
    return not available(p, start, end)


def step(st: WorldState, cfg: dict) -> None:
    from .agents import strategy_fit
    infl = market.infl(cfg, year(st.date))
    actors = [x for x in st.actors() if not x.historical and x.controller != "player"]
    pools = {"fiction": actors,
             "working": [x for x in actors if x.provenance.get("archetype") in ("working", "notable")],
             "unknown": [x for x in actors if x.fame < 0.05],
             "directors": [x.id for x in st.directors() if not x.historical]}
    for pid, p in sorted(st.people.items()):
        if "actor" not in p.roles or not p.active or p.death:
            continue
        if R.unit(st.seed, "jobbing", pid, st.date) >= _rate(st, cfg, p):
            continue
        g = R.stream(st.seed, "job", pid, st.date)
        names = sorted(KINDS)
        names = [k for k in names if KINDS[k][4] > 0]
        w = [KINDS[k][4] * (0.4 + strategy_fit(st, p, None, None, kind=k)) for k in names]
        kind = names[int(g.choice(len(names), p=[x / sum(w) for x in w]))]
        weeks, (lo, hi), craft_gain, fame_gain, _ = KINDS[kind]
        start = add_days(st.date, 7 * int(g.integers(1, 4)))
        end = add_weeks(start, weeks)
        if _busy(p, start, end):
            continue
        job = _detail(st, cfg, p, kind, g, start, end, pools)
        if job is None:
            continue
        job.update({"kind": kind, "start": start, "end": end, "craft": craft_gain, "fame": fame_gain,
                    "pay": round(float(g.uniform(lo, hi)) * infl * (1 + min(1.0, p.fame * 5)), -2)})
        if p.controller == "player":
            _offer_player(st, cfg, p, job)
        else:
            _take(st, cfg, p, job)


def _detail(st, cfg, p, kind, g, start, end, pools) -> dict | None:
    """Make the job concrete: where, what part, with whom."""
    from ..world.people import character_name
    from ..world.tv import EPISODES, GUEST_PARTS
    if kind == "tv_guest":
        shows = [s for _, s in sorted(st.shows.items()) if s.active]
        if not shows:
            return None
        s = shows[int(g.integers(len(shows)))]
        director = s.director_ids[int(g.integers(len(s.director_ids)))] if s.director_ids else None
        colleagues = [x for x in s.regulars if x != p.id] + ([director] if director else [])
        return {"name": f"a guest role on '{s.title}' ({s.network})", "show": s.title, "network": s.network,
                "format": s.format, "character": f"{character_name(g, p.gender)}, {GUEST_PARTS[int(g.integers(len(GUEST_PARTS)))]}",
                "episode": f"an episode about {EPISODES[s.genre][int(g.integers(len(EPISODES[s.genre])))]}",
                "colleagues": colleagues, "director": director}
    if kind == "commercial":
        dirs = pools["directors"]
        director = dirs[int(g.integers(len(dirs)))] if dirs else None
        product = PRODUCTS[int(g.integers(len(PRODUCTS)))]
        pool = [x for x in pools["unknown"] if x.id != p.id]
        cast = [pool[int(g.integers(len(pool)))].id for _ in range(int(g.integers(1, 3)))] if pool else []
        return {"name": f"a national commercial for {product}", "product": product, "director": director,
                "colleagues": cast + ([director] if director else [])}
    if kind == "film_bit":
        films = [q for _, q in sorted(st.projects.items()) if q.stage in ("shooting", "prepro")
                 and q.shoot_start and q.shoot_start <= end and q.shoot_end >= start]
        if not films:
            return None
        f = films[int(g.integers(len(films)))]
        cast = [st.roles[r].cast_id for r in f.role_ids if st.roles[r].cast_id]
        return {"name": f"a small part in '{f.title}' ({st.studios[f.studio_id].name})", "project": f.id,
                "film": f.title, "character": f"{character_name(g, p.gender)} (a few scenes)",
                "colleagues": cast + ([f.director_id] if f.director_id else []), "director": f.director_id}
    if kind == "tv_movie":
        title = TVM_TITLES[int(g.integers(len(TVM_TITLES)))]
        net = ["ABC", "CBS", "NBC"][int(g.integers(3))]
        pool = [x for x in pools["working"] if x.id != p.id]
        cast = [pool[int(g.integers(len(pool)))].id for _ in range(2)] if pool else []
        dirs = pools["directors"]
        director = dirs[int(g.integers(len(dirs)))] if dirs else None
        return {"name": f"a supporting role in the {net} TV movie '{title}'", "show": title, "network": net,
                "character": character_name(g, p.gender), "colleagues": cast + ([director] if director else []),
                "director": director}
    if kind == "stage":
        play, author = PLAYS[int(g.integers(len(PLAYS)))]
        where = THEATRES[int(g.integers(len(THEATRES)))]
        pool = [x for x in pools["fiction"] if x.id != p.id]
        cast = [pool[int(g.integers(len(pool)))].id for _ in range(3)] if pool else []
        return {"name": f"{author}'s '{play}' at {where}", "play": play, "venue": where,
                "colleagues": cast, "director": None}
    return None


def describe(st, job) -> str:
    who = [st.people[c].name for c in job.get("colleagues", []) if c in st.people and c != job.get("director")][:4]
    bits = [job["name"]]
    if job.get("character"):
        bits.append(f"playing {job['character']}")
    if job.get("episode"):
        bits.append(job["episode"])
    if job.get("director") in st.people:
        bits.append(f"directed by {st.people[job['director']].name}")
    if who:
        bits.append("with " + ", ".join(who))
    return "; ".join(bits)


def _offer_player(st, cfg, p, job) -> None:
    text = f"{describe(st, job)} — {job['start']} to {job['end']}, paying {money(job['pay'])}."
    if st.orders.get("auto_accept_jobs", True):
        _take(st, cfg, p, job)
        agent = st.people.get(p.agent_person_id) if p.agent_person_id else None
        st.delegated.append({"rule": "auto_accept_jobs", "decision": None,
                             "text": f"{agent.name if agent else 'Your agent'} booked you: {text}"})
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
    st.market.setdefault("jobs", []).append({"id": jid, "person": p.id, "booked": st.date, **job})
    if p.controller == "player":
        st.log("job_booked", f"Booked {describe(st, job)} ({job['start']} to {job['end']}, {money(job['pay'])}).",
               actors=[p.id] + [c for c in job.get("colleagues", []) if c in st.people][:6], salience=2, public=False)


def settle(st: WorldState, cfg: dict) -> None:
    """Shoot/perform jobs that are under way; pay and credit those that finished."""
    keep = []
    for j in st.market.get("jobs", []):
        p = st.people.get(j["person"])
        if p is None or p.death:
            continue
        if j["start"] <= st.date:
            colleagues = j.get("colleagues", [])
            if p.controller != "player":
                colleagues = colleagues[:2]          # keep NPC-NPC links bounded at scale
            for c in colleagues:                     # working together builds relationships
                if c in st.people and c != p.id:
                    r = st.rel(p.id, c)
                    r.contact_weeks += 1
                    if not any(h.get("job") == j["id"] for h in r.history):
                        r.history.append({"date": st.date, "text": f"worked together on {j['name']}", "delta": 1,
                                          "job": j["id"]})
                        r.affinity = round(clamp(r.affinity + 2, -100, 100), 2)
                    st.market.setdefault("contacts", []).append([r.a, r.b, j["id"]])
        if j["end"] > st.date:
            keep.append(j)
            continue
        finance.pay(st, cfg, p.id, j["pay"], j["name"])
        p.craft = round(clamp(p.craft + j["craft"] * (1 - p.craft / 110)), 2)
        p.fame = round(min(0.95, p.fame + j["fame"]), 6)
        p.last_work = st.date
        p.calendar = [c for c in p.calendar if c["project_id"] != j["id"]]
        p.credits.append({"project_id": None, "title": j.get("show") or j.get("film") or j.get("play") or j["name"],
                          "role": "guest" if j["kind"] == "tv_guest" else j["kind"], "year": year(st.date),
                          "genre": None, "kind": "job"})
        if p.controller == "player":
            st.log("job_done", f"Wrapped {j['name']}.", actors=[p.id], salience=1, public=False)
            st.market.setdefault("jobs_done", []).append({k: v for k, v in j.items()})
    st.market["jobs"] = keep
