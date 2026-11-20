"""Narrator packets: what the narrator (ChatGPT) may know and must respect.

Built from an explicit whitelist of observable facts and qualitative context.
Hidden true values (talent, true quality, satisfaction, attraction, studio
walk-away numbers, future documented events) are never included.
"""
from __future__ import annotations

import yaml

from ..core.state import WorldState
from ..core.util import add_days, age_on, days_between, money
from ..systems import decisions as D

RULES = """You are the narrator of a Hollywood career simulation. The engine is the authority.
Three levels of canon:
- HARD CANON (canon, rulings, your_work, standing, people facts): engine-confirmed. Never contradict it; never
  invent numbers (money, grosses, scores, dates), castings, audition results, awards, deals, deaths or outcomes.
- NARRATIVE CANON (narrative_canon, people[].narrative_canon): details you created earlier (dialogue beats,
  rehearsals, habits, minor characters, places). Keep them consistent. Record new ones under `narrative`.
- PROPOSED CONSEQUENTIAL CANON (initiatives): anything that should change the world (pursuing a film or a
  filmmaker, meetings, introductions, social plans with someone, publicity, career repositioning, developing
  an original project) goes under `initiatives`. Narrate the attempt, not the outcome; the engine rules
  (accepted, partial, rejected with a reason, or pending for weeks) and the next packet reports it.
- Present PENDING DECISIONS as in-story choices. End every reply with the engine block (see REPLY FORMAT).
- Use people's `why_here`, `lately` and `with_you` to ground scenes; do not invent extra social events to fill time.
- Information labelled 'rumour' may be wrong. Do not reveal anything the protagonist could not know."""

REPLY_FORMAT = """```engine
reply_to: {pid}
decisions:            # one entry per decision the player made (omit if none)
  - {{id: dec-00000, choice: accept}}            # counter needs: {{id: ..., choice: counter, fee: 60000}}
initiatives:          # consequential moves for the engine to adjudicate; target/via take a name or an id
  - {{kind: pursue_project, target: "<film title or id>", role: "<character, optional>", approach: "..."}}
  - {{kind: inquire, target: "<film or person>"}}
  - {{kind: meet, target: "<person>", approach: "why you want the meeting"}}
  - {{kind: introduction, target: "<person>", via: "<someone you know who knows them>"}}
  - {{kind: social, target: "<person you know>", approach: "dinner at their place"}}
  - {{kind: publicity, mode: publicist|interview|talk_show|charity}}
  - {{kind: reposition, details: {{genres: [drama], avoid_genres: [horror], min_role: supporting, no_tv: false, no_commercials: true}}}}
  - {{kind: develop_project, title: "...", genre: drama, logline: "one sentence"}}
proposals:            # interpersonal developments (optional)
  - {{id: p1, type: relationship_shift, with: <person id>, direction: positive|negative, severity: minor|moderate|major, cause: "..."}}
  - {{id: p2, type: romantic_overture, to: <person id>, approach: "..."}}
  - {{id: p3, type: player_intent, kind: take_class|rest|seek_agent, text: "..."}}
  - {{id: p4, type: purchase, item: car|apartment|house|gift|vacation|wardrobe, text: "..."}}
  - {{id: p5, type: reputation_moment, person: <id>, direction: positive|negative, severity: minor|moderate, public: true|false, cause: "..."}}
narrative:            # narrative canon: nonconsequential details to keep (optional `about` names or ids)
  - {{text: "Rehearsed the diner scene with Ray at his apartment; he hums Sinatra between takes.", about: ["<name>"]}}
advance: {{weeks: 4}}   # or {{until: YYYY-MM-DD}}; omit to stay at this date
```"""


# ------------------------------------------------------------- labels ---
def fame_label(f: float) -> str:
    return ("unknown to the public" if f < 0.005 else "known mostly inside the industry" if f < 0.03
            else "a recognisable face" if f < 0.10 else "well known" if f < 0.30
            else "famous" if f < 0.55 else "a household name")


def heat_label(h: float) -> str:
    return ("ice cold" if h < -40 else "cooling" if h < -12 else "steady" if h < 12
            else "warming up" if h < 35 else "hot" if h < 65 else "the hottest name in town")


def bank_label(b: float) -> str:
    return ("not a draw" if b < 15 else "a modest draw" if b < 35 else "can help open a film" if b < 55
            else "a reliable opener" if b < 75 else "a top box-office draw")


def critic_label(c: float) -> str:
    return ("dismissed by critics" if c < 30 else "unremarkable to critics" if c < 45
            else "respected" if c < 60 else "highly regarded" if c < 75 else "critically acclaimed")


def affinity_label(a: float) -> str:
    return ("bitter enemies" if a < -60 else "hostile" if a < -30 else "strained" if a < -10
            else "cordial" if a < 15 else "friendly" if a < 40 else "close" if a < 70 else "devoted")


def energy_label(e: float) -> str:
    return "exhausted" if e < 30 else "tired" if e < 55 else "fine" if e < 80 else "fresh"


def gross_label(x: float) -> str:
    return money(x)


# ------------------------------------------------------------- builder ---
def build(st: WorldState, cfg: dict, packet_id: str) -> dict:
    n = cfg["narrator"]
    pl = st.player
    since = st.packet_seq_mark
    new_events = st.events[since:]

    canon = [e for e in new_events if (pl and pl.id in e["actors"] and e["salience"] >= 1)
             or (e["public"] and e["salience"] >= 3)]
    canon = sorted(canon, key=lambda e: (e["date"], e["seq"]))[-n["max_canon_events"]:]
    world_items = [e for e in new_events if e["public"] and e["salience"] >= 1 and not (pl and pl.id in e["actors"])
                   and e["type"] not in ("chart",)]
    # variety: cap how many items of one kind crowd out the rest
    per_type, picked = {}, []
    for e in sorted(world_items, key=lambda e: (-e["salience"], -e["seq"])):
        if per_type.get(e["type"], 0) >= 3:
            continue
        per_type[e["type"]] = per_type.get(e["type"], 0) + 1
        picked.append(e)
    world_items = picked[:n["max_world_items"]]
    world_items.sort(key=lambda e: e["seq"])

    pk = {
        "packet": packet_id,
        "date": st.date,
        "covers": f"{new_events[0]['date'] if new_events else st.date} .. {st.date}",
        "state_hash": st.state_hash(),
        "protagonist": _protagonist(st, cfg) if pl else None,
        "canon": [_event_item(st, e, with_id=True) for e in canon],
        "period_summary": _period_summary(st, cfg, new_events),
        "rulings": list(st.rulings),
        "delegated": [x["text"] for x in st.delegated],
        "standing_changes": _standing_changes(st, cfg, new_events),
        "agent": _agent_plan(st, cfg, new_events),
        "initiatives": _initiatives(st, new_events),
        "career_activity": _career_activity(st, cfg, new_events),
        "your_work": _projects(st, cfg) + _jobs(st),
        "network": _network(st, cfg),
        "open_threads": _threads(st, cfg),
        "people": _people(st, cfg, canon),
        "industry": {
            "box_office_chart": _chart(st),
            "news": [_event_item(st, e) for e in world_items],
        },
        "pending_decisions": [_decision(d, st) for d in D.pending(st)],
        "continuity": _continuity(st, cfg),
        "narrative_canon": _narrative_canon(st),
        "era": _era(st, cfg),
        "narrator_notes": st.notes[-20:],
    }
    return pk


def render(pk: dict) -> str:
    body = yaml.safe_dump(pk, sort_keys=False, allow_unicode=True, width=110)
    return (f"# Narrator packet {pk['packet']} — {pk['date']}\n\n## RULES\n{RULES}\n\n"
            f"## STATE\n```yaml\n{body}```\n\n## REPLY FORMAT\n"
            f"End your reply with exactly one block like this:\n\n{REPLY_FORMAT.format(pid=pk['packet'])}\n")


def _protagonist(st, cfg) -> dict:
    p = st.player
    ag = st.agencies.get(p.agent_id) if p.agent_id else None
    partner = st.people.get(p.partner_id) if p.partner_id else None
    return {
        "id": p.id, "name": p.name, "age": age_on(p.birth, st.date),
        "background": p.bio, "traits": p.traits,
        "goals": {k: round(v, 2) for k, v in sorted(p.goals.items(), key=lambda kv: -kv[1])},
        "public_profile": fame_label(p.fame),
        "industry_view": {"momentum": heat_label(p.heat), "draw": bank_label(p.bankability),
                          "critics": critic_label(p.critical_rep) if _reviewed(st, p) else "no reviewed work yet"},
        "quote_reported_in_trades": money(p.quote) if p.quote else "no established quote",
        "agent": (f"{st.people[p.agent_person_id].name} at {ag.name}" if ag and p.agent_person_id in st.people
                  else ag.name if ag else "no agent"),
        "agent_strategy": _strategy(p) if ag else "no representation: work comes only through open calls",
        "persona": {k: v for k, v in p.persona.items() if k != "source"},
        "money": {"cash": round(p.cash, 0), "monthly_costs": round(p.monthly_costs, 0)},
        "energy": energy_label(p.energy),
        "relationship_status": (f"{p.partner_status} {partner.name}" if partner else (p.partner_status or "single")),
        "awards": [f"{a['year']} {a['category']} ({a['result']})" for a in p.awards],
    }


def _reviewed(st, p) -> bool:
    return any(c.get("kind") == "prior" or (c.get("project_id") in st.projects
               and st.projects[c["project_id"]].critic_score is not None) for c in p.credits)


def _projects(st, cfg) -> list:
    out = []
    pl = st.player_id
    for pid, p in sorted(st.projects.items()):
        mine = [st.roles[r] for r in p.role_ids if st.roles[r].cast_id == pl]
        if not mine or p.stage == "dead":
            continue
        if p.stage == "released" and not p.run.get("active") and (not p.weekly or days_between(p.weekly[-1]["date"], st.date) > 35):
            continue
        r = mine[0]
        d = st.people.get(p.director_id)
        costars = [f"{st.people[st.roles[x].cast_id].name} as {st.roles[x].name} ({st.roles[x].importance}"
                   + (", character name documented" if st.roles[x].name_documented else ", character name simulated")
                   + (", documented casting" if p.historical_ref and st.roles[x].intended == st.roles[x].cast_id else "")
                   + ")" for x in p.role_ids if st.roles[x].cast_id and st.roles[x].cast_id != pl]
        item = {"title": p.title, "studio": st.studios[p.studio_id].name, "genre": p.genre, "premise": p.premise,
                "your_role": f"{r.name} — {r.importance}: {r.description}",
                "director": d.name if d else "TBD", "costars": costars, "stage": p.stage,
                "location": p.location, "terms": money(r.fee) + (f" + {r.points:g} {r.points_type} points" if r.points_type else "")}
        if p.tone:
            item["identity"] = f"{p.tone} {p.genre}; {p.logline_extra}"
        from ..world.story import packet_view
        item["story"] = packet_view(st, p, r)
        if not p.historical_ref:
            item["provenance"] = "simulated production: not a real film; its cast and characters are part of this timeline"
        if p.historical_ref:
            item["historical_record"] = {
                "real_film": True,
                "release_date": "approximate (only the year or month is documented)" if p.date_approx else "documented",
                "distributor": p.distributor_note or st.studios[p.studio_id].name,
                "your_character_name": "documented" if r.name_documented else "simulated (not in the record)",
                "note": "You are in this real film because the simulated world diverged from history." }
        if p.stage in ("prepro", "shooting"):
            item["shoot"] = f"{p.shoot_start} to {p.shoot_end}"
        if p.release_date:
            item["release_date"] = p.release_date
        if p.forecast_opening and p.stage == "awaiting_release":
            item["tracking_opening"] = money(p.forecast_opening)
        if p.stage == "released":
            item["box_office"] = {"opening": money(p.opening), "domestic_to_date": money(p.domestic),
                                  "weeks": p.run.get("week"), "critics": f"{p.critic_score:.0f}/100",
                                  "audience_grade": p.audience_grade}
        out.append(item)
    return out


def _people(st, cfg, canon) -> list:
    """The people who matter to this stretch of the story, each with the reason they're here."""
    pl = st.player
    ids = []                                        # (person id, why they're in this packet)
    def add(pid, why):
        if pid:
            ids.append((pid, why))
    if pl.partner_id:
        add(pl.partner_id, "your partner")
    if pl.agent_person_id:
        add(pl.agent_person_id, "your agent")
    featured = []                                   # small-part co-stars come after people with real history
    for pid, p in sorted(st.projects.items()):
        if p.stage in ("released", "dead"):
            continue
        cast = [st.roles[r].cast_id for r in p.role_ids if st.roles[r].cast_id]
        if pl.id in cast:
            add(p.director_id, f"directing your film '{p.title}'")
            for r in p.role_ids:
                x = st.roles[r].cast_id
                if x and x != pl.id:
                    item = (x, f"in the cast of your film '{p.title}' ({st.roles[r].importance})")
                    (featured.append(item) if st.roles[r].importance == "featured" else ids.append(item))
    for ini in st.initiatives.values():               # people your plans are built around
        for x in ini["data"].get("attached", []):
            add(x, f"attached to your project '{ini['data'].get('title')}'")
    for n in reversed(st.narrative[-30:]):
        for a_ in n.get("about", []):
            add(a_, f"in your story's narrative canon ({n['date']})")
    for d in D.pending(st):
        prj = st.projects.get(d.refs.get("project")) or (
            st.projects.get(st.offers[d.refs["offer"]].project_id) if d.refs.get("offer") in st.offers else None)
        add(d.refs.get("person"), f"part of a decision waiting for you ({d.kind})")
        if prj:
            add(prj.director_id, f"directing '{prj.title}', which a pending decision is about")
            for r in prj.role_ids:
                add(st.roles[r].cast_id, f"already cast in '{prj.title}', which a pending decision is about")
    for ini in st.initiatives.values():
        if ini["status"] in ("pending", "writing", "pitching", "watching") and ini["data"].get("target"):
            add(ini["data"]["target"], f"the person your {ini['kind']} initiative is aimed at")
    for j in st.market.get("jobs", []):
        if j["person"] == pl.id:
            for c in j.get("colleagues", [])[:5]:
                add(c, f"working with you on {j.get('show') or j.get('film') or j.get('play') or j['name']}")
    for e in canon:
        for a_ in e["actors"]:
            if a_ != pl.id:
                add(a_, f"in this period's events ({e['type'].replace('_', ' ')}, {e['date']})")
    ids += featured
    rels = sorted((r for r in st.rels.values() if pl.id in (r.a, r.b) and (r.history or r.contact_weeks)),
                  key=lambda r: (r.history[-1]["date"] if r.history else "", abs(r.affinity)), reverse=True)
    for r in rels[:8]:
        add(r.b if r.a == pl.id else r.a, "someone you've been in touch with recently")
    seen, out = set(), []
    for i, why in ids:
        if i in seen or i not in st.people or i == pl.id:
            continue
        seen.add(i)
        card = _person_card(st, st.people[i])
        card = {"why_here": why, **card}
        out.append(card)
        if len(out) >= cfg["narrator"]["max_people"]:
            break
    return out


MOTIVE = {"money": "financial security and big paydays", "fame": "fame and visibility",
          "prestige": "respect and awards", "art": "challenging, meaningful work", "stability": "a steady, sane life"}


def motivation(p) -> str:
    if not p.goals:
        return ""
    top = sorted(p.goals.items(), key=lambda kv: -kv[1])[:2]
    if len(top) == 1:
        return f"driven by {MOTIVE[top[0][0]]}"
    return f"driven mostly by {MOTIVE[top[0][0]]}, and also by {MOTIVE[top[1][0]]}"


def _profession(st, p) -> str:
    if "agent" in p.roles:
        ag = st.agencies.get(p.employer)
        return f"agent at {ag.name}" if ag else "agent"
    if "casting_director" in p.roles:
        return (f"casting director at {st.studios[p.employer].name}" if p.employer in st.studios
                else "independent casting director")
    if "producer" in p.roles:
        return "television producer"
    if "director" in p.roles and "actor" in p.roles:
        return "actor-director"
    return "director" if "director" in p.roles else "actor"


def _person_card(st, p) -> dict:
    from ..world.people import ambition, reputation
    pl = st.player
    r = st.rel(pl.id, p.id, create=False)
    recent = [c for c in p.credits if c.get("kind") in ("film", "prior", "job")][-3:]
    card = {"id": p.id, "name": p.name, "age": age_on(p.birth, st.date), "profession": _profession(st, p),
            "public_profile": fame_label(p.fame), "reputation": reputation(st, p),
            "traits": p.traits, "motivation": motivation(p), "ambition": ambition(p), "bio": p.bio}
    persona = {k: v for k, v in p.persona.items() if k != "source"}
    if persona:
        card["persona"] = persona
    if recent:
        def tag(c):
            if c.get("kind") == "prior":
                return "documented" if p.historical else "backstory"
            return "this timeline"
        card["recent_work"] = [f"'{c['title']}' ({c['year']}, {c['role']}; {tag(c)})" for c in recent]
    card["relationship_status"] = _relationship_status(st, p)
    if p.historical:
        card["real_person"] = True
        card["note"] = ("Real person. Their career up to the start date is documented; their ambition is inferred from it; "
                        "personality traits are simulation characterisation, not biography. Everything they do with you, "
                        "and anything marked 'simulated', is this alternate timeline, not history.")
    if r:
        card["with_you"] = {"standing": affinity_label(r.affinity), "status": r.status,
                            "history": [h["text"] + f" ({h['date']})" for h in r.history[-4:]]}
    lately = _lately(st, p)
    if lately:
        card["lately"] = lately
    about = [f"{n['date']}: {n['text']}" for n in st.narrative if p.id in n.get("about", [])][-4:]
    if about:
        card["narrative_canon"] = about
    return card


def _lately(st, p, days: int = 120) -> list:
    """What this person has been doing on their own, as far as the protagonist could know (public events,
    plus anything the protagonist witnessed)."""
    since = add_days(st.date, -days)
    out = []
    for e in reversed(st.events):
        if e["date"] < since or len(out) >= 3:
            break
        if p.id in e["actors"] and st.player_id not in e["actors"] and e["public"] and e["salience"] >= 1 \
                and e["type"] not in ("chart", "tracking"):
            out.append(f"{e['date']}: {e['text']}")
    return out[::-1]


SIMULATED_PERSONAL = {"romance", "marriage", "breakup", "divorce", "chemistry"}


def _provenance(st, e) -> str | None:
    """Label events about real people as documented history or simulated divergence."""
    reals = [a for a in e["actors"] if a in st.people and st.people[a].historical]
    t = e["type"]
    if t.startswith("documented_"):
        return "documented history"
    if t == "history_diverged":
        return "simulated divergence from history"
    if not reals:
        return None
    if t in SIMULATED_PERSONAL:
        return "simulated (not historical): an alternate-timeline development"
    if t == "cast":
        prj = st.projects.get(e["refs"].get("project"))
        role = st.roles.get(e["refs"].get("role"))
        if prj and prj.historical_ref and role and role.intended in e["actors"]:
            return "documented casting (as in history)"
        if prj and prj.historical_ref:
            return "simulated casting in a real film (diverges from history)"
        return "simulated casting in a fictional production"
    if t in ("director_attached", "greenlight"):
        prj = st.projects.get(e["refs"].get("project"))
        return "documented production" if prj and prj.historical_ref else "fictional production"
    return "simulated event in this timeline"


def _event_item(st, e, with_id=False) -> dict:
    item = ({"id": f"ev-{e['seq']}"} if with_id else {}) | {"date": e["date"], "text": e["text"]}
    prov = _provenance(st, e)
    if prov:
        item["provenance"] = prov
    return item


def _relationship_status(st, p) -> str:
    if p.partner_status == "partnered_offscreen":
        return "in a relationship (partner outside the film industry)" + (" (documented)" if p.historical else "")
    if p.partner_status == "married_offscreen":
        return "married (spouse outside the film industry)" + (" (documented)" if p.historical and p.provenance.get("spouse_outside_world") else "")
    if p.partner_id in st.people:
        r = st.rel(p.id, p.partner_id, create=False)
        documented = bool(r and any(h.get("documented") for h in r.history))
        status = "in a relationship with" if (p.partner_status == "dating" and documented) else p.partner_status
        label = f"{status} {st.people[p.partner_id].name}"
        if p.historical or st.people[p.partner_id].historical:
            label += " (documented)" if documented else " (simulated, not historical)"
        return label
    return "single"


def standing(st) -> dict:
    """The protagonist's observable standing (labels, as the industry would describe it)."""
    p = st.player
    return {"public_profile": fame_label(p.fame), "momentum": heat_label(p.heat), "draw": bank_label(p.bankability),
            "critics": critic_label(p.critical_rep) if _reviewed(st, p) else "no reviewed work yet",
            "industry_standing": prestige_label(p.prestige),
            "quote": money(p.quote) if p.quote else "no established quote"}


def prestige_label(x: float) -> str:
    return ("a newcomer" if x < 15 else "a working professional" if x < 30 else "respected" if x < 50
            else "highly respected" if x < 70 else "an industry heavyweight")


STANDING_CAUSES = {"reviews", "trade_verdict", "player_film_gross", "nomination", "oscar_win", "talk_show", "publicity",
                   "reputation", "cast", "job_done", "run_end", "oscar_nominations", "audition_result"}


def _standing_changes(st, cfg, new_events) -> dict:
    """How the protagonist's standing moved since the last packet, and what moved it."""
    pl = st.player
    before = st.market.get("standing_mark")
    now = standing(st)
    if not before:
        return {"now": now, "changes": [], "causes": []}
    changes = [f"{k.replace('_', ' ')}: {before[k]} -> {now[k]}" for k in now if before.get(k) != now[k]]
    mine = {c.get("project_id") for c in pl.credits}
    causes = [f"{e['date']}: {e['text']}" for e in new_events if e["type"] in STANDING_CAUSES
              and (pl.id in e["actors"] or e["refs"].get("project") in mine)
              and not (e["type"] == "audition_result" and "won" not in e["text"])]
    if not changes:
        return {"now": now, "changes": [], "relevant_events": causes[-5:]}
    if any(c.startswith("momentum") for c in changes) and not causes:
        causes.append("no new work or press: momentum fades on its own between projects")
    if any(c.startswith("public profile") for c in changes) and not causes:
        causes.append("out of the public eye: recognition fades slowly without new releases")
    return {"now": now, "changes": changes, "causes": causes[-8:]}


def _agent_plan(st, cfg, new_events) -> dict | None:
    """What your agent is doing for you, strategically, and how much of their attention you get."""
    from ..systems.agents import commission_potential
    pl = st.player
    agent = st.people.get(pl.agent_person_id) if pl.agent_person_id else None
    if not agent:
        return None
    book = sorted((c for c in st.actors() if c.agent_person_id == agent.id),
                  key=lambda c: (-commission_potential(st, cfg, c), c.id))
    rank = next((i for i, c in enumerate(book) if c.id == pl.id), len(book))
    tier = ("one of their top earners" if rank < max(3, len(book) // 10) else
            "mid-list" if rank < len(book) // 2 else "one of their smaller clients")
    attention = (f"{agent.name} represents {len(book)} actors and you are {tier}. Calls are limited: they push "
                 f"when you just miss a casting director's list on a part worth it, or when a director already rates you")
    start = new_events[0]["date"] if new_events else st.date
    pushes = [x for x in st.market.get("agent_pushes", []) if x["client"] == pl.id and x["date"] >= start]
    lines = []
    for x in pushes:
        prj, role = st.projects.get(x["project"]), st.roles.get(x["role"])
        if prj and role:
            lines.append(f"{x['date']}: pushed for {role.name} ({role.importance}) in '{prj.title}' — "
                         + ("casting agreed to see you" if x["result"] == "agreed to see" else f"declined: {x.get('reason')}"))
    waiting = []
    for r in st.roles.values():
        if pl.id in r.requested and r.status == "open" and not r.cast_id:
            prj = st.projects[r.project_id]
            waiting.append(f"'{prj.title}' ({prj.stage}): they'll see you for {r.name} ({r.importance}) when casting opens")
    out = {"agent": f"{agent.name} ({_profession(st, agent)})", "strategy": _strategy(pl), "attention": attention}
    if pl.directives:
        out["your_directives"] = {k: v for k, v in pl.directives.items()}
    if lines:
        out["pushes_this_period"] = lines
    if waiting:
        out["doors_open"] = waiting
    return out


OPEN_INITIATIVE = ("pending", "writing", "pitching", "watching", "turnaround")   # turnaround can be revived


def _initiatives(st, new_events) -> list:
    """Initiatives under adjudication (proposed consequential canon) and ones that moved this period."""
    start = new_events[0]["date"] if new_events else st.date
    out = []
    for iid, ini in st.initiatives.items():
        open_ = ini["status"] in OPEN_INITIATIVE
        moved = [s_ for s_ in ini["steps"] if s_["date"] >= start]
        if not open_ and not moved:
            continue
        out.append({"id": iid, "kind": ini["kind"], "status": ini["status"], "started": ini["created"],
                    "history": [f"{s_['date']}: {s_['text']}" for s_ in ini["steps"][-5:]],
                    **({"next_step_due": ini["due"]} if ini.get("due") and open_ else {})})
    return out


def _narrative_canon(st) -> list:
    return [f"{n['date']}: {n['text']}" for n in st.narrative[-15:]]


def _strategy(p) -> str:
    from ..systems.agents import strategy_summary
    return strategy_summary(p)


def _period_summary(st, cfg, new_events) -> dict:
    pl = st.player
    mine = [e for e in new_events if pl.id in e["actors"]]
    subs = [x for x in st.market.get("player_submissions", []) if new_events and x["date"] >= new_events[0]["date"]]
    kinds = {}
    for e in mine:
        kinds[e["type"]] = kinds.get(e["type"], 0) + 1
    weeks = max(1, days_between(new_events[0]["date"], st.date) // 7) if new_events else 0
    work = kinds.get("job_booked", 0) + kinds.get("cast", 0)
    auditions = kinds.get("audition_result", 0)
    start = new_events[0]["date"] if new_events else st.date
    busy = working_during(st, pl, start, st.date)
    quiet = work == 0 and auditions == 0 and not busy and not D.pending(st)
    pieces = [f"{weeks} week(s)"] + ([f"working on {len(busy)} job(s)"] if busy else []) + [f"{len(subs)} submission(s) by your agent",
              f"{sum(1 for x in subs if x['status'] in ('called in', 'requested'))} call-in(s)",
              f"{auditions} audition(s)", f"{work} booking(s)"]
    ledger = [x for x in st.market.get("player_ledger", []) if new_events and x["date"] >= new_events[0]["date"]]
    net = sum(x.get("net", 0) for x in ledger)
    return {"overview": ", ".join(pieces) + f"; net money {'+' if net >= 0 else ''}{money(net)}.",
            "working": busy[-8:],
            "quiet_period": quiet,
            "note": ("A quiet stretch: realistic downtime. Portray ordinary life, waiting and small moments; "
                     "do not invent career breakthroughs.") if quiet else ""}


def working_during(st, p, start: str, end: str) -> list:
    """Productions and jobs the person was committed to at any point in [start, end].
    Time on set, in rehearsal or under contract is not a quiet period."""
    from ..core.util import overlaps
    out = []
    for c in p.calendar:
        prj = st.projects.get(c["project_id"])
        if prj and overlaps(c["start"], c["end"], start, end):
            out.append(f"{'shooting' if c['kind'] == 'shoot' else c['kind']} '{prj.title}' ({c['start']} to {c['end']})")
    for j in st.market.get("jobs", []) + st.market.get("jobs_done", []):
        if j.get("person") == p.id and overlaps(j["start"], j["end"], start, end):
            what = j.get("show") or j.get("film") or j.get("play") or j.get("product") or j["name"]
            item = f"{j['kind'].replace('_', ' ')}: {what} ({j['start']} to {j['end']})"
            if item not in out:
                out.append(item)
    return out


def _career_activity(st, cfg, new_events) -> dict:
    from ..systems.jobbing import describe
    pl = st.player
    start = new_events[0]["date"] if new_events else st.date
    subs = [x for x in st.market.get("player_submissions", []) if x["date"] >= start]
    out = {}
    if subs:
        out["submissions"] = [f"{x['date']}: {x['role']} ({x['importance']}) in '{x['title']}' ({x['studio']}"
                              + (f", casting {x['cd']}" if x['cd'] else "") + f") — {x['status']}: {x['reason']}"
                              for x in subs[-10:]]
    aud = [e for e in new_events if pl.id in e["actors"] and e["type"] in ("audition_result", "audition_rivals", "called_in")]
    if aud:
        out["auditions"] = [f"{e['date']}: {e['text']}" for e in aud[-8:]]
    booked = [j for j in st.market.get("jobs", []) + st.market.get("jobs_done", [])
              if j["person"] == pl.id and j.get("booked", "") >= start]
    if booked:
        out["bookings"] = [f"{j['start']} to {j['end']}: {describe(st, j)} ({money(j['pay'])})" for j in booked]
    calls = [e for e in new_events if pl.id in e["actors"] and e["type"] == "agent_checkin"]
    if calls:
        out["agent_calls"] = [f"{e['date']}: {e['text']}" for e in calls]
    return out


def _jobs(st) -> list:
    from ..systems.jobbing import describe
    out = []
    for j in st.market.get("jobs", []):
        if j["person"] != st.player_id:
            continue
        status = "under way" if j["start"] <= st.date else "booked"
        item = {"title": j.get("show") or j.get("film") or j.get("play") or j["name"], "kind": j["kind"].replace("_", " "),
                "status": status, "dates": f"{j['start']} to {j['end']}", "details": describe(st, j),
                "pay": money(j["pay"])}
        if j.get("format"):
            item["format"] = j["format"]
        out.append(item)
    return out


def _network(st, cfg) -> list:
    pl = st.player
    rows = []
    for r in st.rels.values():
        if pl.id not in (r.a, r.b) or not (r.history or r.contact_weeks):
            continue
        other = st.people.get(r.b if r.a == pl.id else r.a)
        if not other:
            continue
        first = r.history[0]["text"] if r.history else "met"
        last = r.history[-1] if r.history else None
        rows.append((last["date"] if last else "", {
            "name": other.name, "id": other.id, "who": _profession(st, other),
            "how_you_know_them": first, "standing": affinity_label(r.affinity),
            "last_interaction": f"{last['text']} ({last['date']})" if last else ""}))
    rows.sort(key=lambda x: x[0], reverse=True)
    return [x for _, x in rows[:15]]


def _threads(st, cfg) -> list:
    from ..systems.jobbing import describe
    pl = st.player
    out = []
    for d in D.pending(st):
        out.append(f"Decision waiting: {d.summary} (by {d.deadline})")
    for j in st.market.get("jobs", []):
        if j["person"] == pl.id and j["start"] > st.date:
            out.append(f"Upcoming: {describe(st, j)} starting {j['start']}")
    for pid, p in sorted(st.projects.items()):
        mine = [st.roles[r] for r in p.role_ids if st.roles[r].cast_id == pl.id]
        if mine and p.stage in ("prepro", "shooting", "post", "awaiting_release"):
            out.append(f"'{p.title}' is in {p.stage.replace('_', ' ')}" + (f"; release {p.release_date}" if p.release_date else ""))
    yr = st.date[:4]
    year_subs = [x for x in st.market.get("player_submissions", []) if x["date"][:4] == yr]
    year_roles = [c for c in pl.credits if c.get("kind") == "film" and str(c.get("year")) >= yr]
    top_goal = max(pl.goals, key=pl.goals.get) if pl.goals else None
    if top_goal:
        from ..world.people import GOAL_AMBITION
        out.append(f"Career goal: {GOAL_AMBITION[top_goal].replace('wants', 'you want')}. So far in {yr}: "
                   f"{len(year_subs)} submissions, {sum(1 for x in year_subs if x['status'] in ('called in', 'requested'))} "
                   f"call-ins, {len(year_roles)} film role(s) booked.")
    if pl.cash < 2 * pl.monthly_costs:
        out.append(f"Money is tight: about {money(pl.cash)} against {money(pl.monthly_costs)} a month in costs.")
    if not pl.agent_id:
        out.append("No agent: work arrives only through open calls; finding representation is the main obstacle.")
    recent_shift = [r for r in st.rels.values() if pl.id in (r.a, r.b) and r.history and abs(r.history[-1].get("delta", 0)) >= 5
                    and r.history[-1]["date"] >= add_days(st.date, -35)]
    for r in recent_shift[:3]:
        other = st.people[r.b if r.a == pl.id else r.a]
        out.append(f"Relationship in motion with {other.name}: {r.history[-1]['text']}")
    return out


def _chart(st) -> list:
    ch = st.market.get("chart")
    if not ch:
        return []
    return [f"{i}. '{x['title']}' ({x['studio']}) — {money(x['gross'])} this week, {money(x['total'])} total, week {x['week']}"
            for i, x in enumerate(ch["top"][:5], 1)]


def _decision(d, st=None) -> dict:
    out = {"id": d.id, "kind": d.kind, "summary": d.summary, "options": d.options, "deadline": d.deadline,
           "if_unanswered": d.default}
    if st is not None and d.kind in ("offer", "audition"):
        from ..world.story import packet_view
        role = st.roles.get(d.refs.get("role")) or (st.roles.get(st.offers[d.refs["offer"]].role_id)
                                                    if d.refs.get("offer") in st.offers else None)
        if role:
            v = packet_view(st, st.projects[role.project_id], role)
            out["story_preview"] = {k: v[k] for k in ("provenance", "logline", "central_conflict", "your_character",
                                                      "your_key_scenes", "your_read_of_the_script") if k in v}
            mine = [c for c in v.get("characters", []) if c.startswith(role.name)]
            if mine:
                out["story_preview"]["your_character"] = mine[0]
    if d.refs.get("context"):
        out["context"] = d.refs["context"]
    return out


def _era(st, cfg) -> dict:
    from ..systems import market
    return {"year": int(st.date[:4]), "average_ticket_price": f"${market.ticket_price(cfg, st.date):.2f}",
            "note": "The blockbuster era is a few years old; theatrical release dominates and home video is small but growing fast."
            if st.date < "1983" else "Home video is becoming a real second market."}


def _continuity(st, cfg) -> dict:
    pl = st.player
    credits = []
    for c in sorted(pl.credits, key=lambda c: int(c.get("year", 0) or 0)):
        line = f"{c['year']}: '{c['title']}' ({c['role']}"
        prj = st.projects.get(c.get("project_id")) if c.get("project_id") else None
        if prj and prj.stage == "released" and prj.critic_score is not None:
            line += f"; {money(prj.domestic)} domestic, critics {prj.critic_score:.0f}"
        credits.append(line + ")")
    earlier = [e for e in st.events[:st.packet_seq_mark] if pl.id in e["actors"] and e["salience"] >= 3]
    scenes = []
    for r in sorted(st.rels.values(), key=lambda r: (r.a, r.b)):
        if pl.id in (r.a, r.b):
            other = st.people[r.b if r.a == pl.id else r.a]
            for h in r.history[-3:]:
                scenes.append((h["date"], f"with {other.name}: {h['text']}"))
    scenes += [(n["date"], n["text"]) for n in st.notes[-10:]]
    scenes.sort()
    closed = [i for i in st.initiatives.values() if i["status"] not in OPEN_INITIATIVE]
    initiatives = [f"{i['created']} {i['kind'].replace('_', ' ')}: " + " -> ".join(s_["text"] for s_ in
                   (i["steps"][:1] + i["steps"][-1:] if len(i["steps"]) > 1 else i["steps"])) for i in closed]
    return {"career_so_far": credits[-12:],
            "initiatives_resolved": initiatives[-8:],
            "earlier_key_moments": [f"{e['date']}: {e['text']}" for e in earlier[-cfg['narrator']['continuity_events']:]],
            "recent_scenes_and_threads": [f"{dte}: {t}" for dte, t in scenes[-12:]]}
