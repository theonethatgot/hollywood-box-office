"""Narrator packets: what the narrator (ChatGPT) may know and must respect.

Built from an explicit whitelist of observable facts and qualitative context.
Hidden true values (talent, true quality, satisfaction, attraction, studio
walk-away numbers, future documented events) are never included.
"""
from __future__ import annotations

import yaml

from ..core.state import WorldState
from ..core.util import age_on, days_between, money
from ..systems import decisions as D

RULES = """You are the narrator of a Hollywood career simulation. The engine is the authority.
- CANON below is fact. Never contradict it; never invent numbers (money, grosses, scores, dates), castings,
  audition results, awards, deals, deaths or other outcomes.
- You may freely invent dialogue, scenes, settings, minor fictional characters, moods and press colour,
  consistent with each person's traits and history.
- Consequential developments (a falling-out, a romance, a reputation moment, a purchase, a plan) must be
  PROPOSED in the engine block, not narrated as settled. Narrate them as tentative until the engine rules.
- Present PENDING DECISIONS as in-story choices. End every reply with the engine block (see REPLY FORMAT).
- Information labelled 'rumour' may be wrong. Do not reveal anything the protagonist could not know."""

REPLY_FORMAT = """```engine
reply_to: {pid}
decisions:            # one entry per decision the player made (omit if none)
  - {{id: dec-00000, choice: accept}}            # counter needs: {{id: ..., choice: counter, fee: 60000}}
proposals:            # consequential developments for the engine to rule on (optional)
  - {{id: p1, type: relationship_shift, with: <person id>, direction: positive|negative, severity: minor|moderate|major, cause: "..."}}
  - {{id: p2, type: romantic_overture, to: <person id>, approach: "..."}}
  - {{id: p3, type: player_intent, kind: take_class|rest|meet_person|seek_agent|pursue_director, target: <person id or omit>, text: "..."}}
  - {{id: p4, type: purchase, item: car|apartment|house|gift|vacation|wardrobe, text: "..."}}
  - {{id: p5, type: reputation_moment, person: <id>, direction: positive|negative, severity: minor|moderate, public: true|false, cause: "..."}}
notes:                # small narrative facts to remember (names of minor characters, places, habits)
  - "..."
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
        "canon": [{"id": f"ev-{e['seq']}", "date": e["date"], "text": e["text"]} for e in canon],
        "rulings": list(st.rulings),
        "delegated": [x["text"] for x in st.delegated],
        "your_projects": _projects(st, cfg),
        "people": _people(st, cfg, canon),
        "industry": {
            "box_office_chart": _chart(st),
            "news": [{"date": e["date"], "text": e["text"]} for e in world_items],
        },
        "pending_decisions": [_decision(d) for d in D.pending(st)],
        "continuity": _continuity(st, cfg),
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
        "agent": ag.name if ag else "no agent",
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
        costars = [f"{st.people[st.roles[x].cast_id].name} ({st.roles[x].name}, {st.roles[x].importance})"
                   for x in p.role_ids if st.roles[x].cast_id and st.roles[x].cast_id != pl]
        item = {"title": p.title, "studio": st.studios[p.studio_id].name, "genre": p.genre, "premise": p.premise,
                "your_role": f"{r.name} — {r.importance}: {r.description}",
                "director": d.name if d else "TBD", "costars": costars, "stage": p.stage,
                "location": p.location, "terms": money(r.fee) + (f" + {r.points:g} {r.points_type} points" if r.points_type else "")}
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
    pl = st.player
    ids = []
    for pid, p in sorted(st.projects.items()):
        if p.stage in ("released", "dead"):
            continue
        cast = [st.roles[r].cast_id for r in p.role_ids if st.roles[r].cast_id]
        if pl.id in cast:
            ids += [x for x in cast if x != pl.id] + ([p.director_id] if p.director_id else [])
    if pl.partner_id:
        ids.insert(0, pl.partner_id)
    for e in canon:
        ids += [a for a in e["actors"] if a != pl.id]
    for d in D.pending(st):
        if "person" in d.refs:
            ids.append(d.refs["person"])
        prj = st.projects.get(d.refs.get("project")) or (
            st.projects.get(st.offers[d.refs["offer"]].project_id) if d.refs.get("offer") in st.offers else None)
        if prj:
            ids += [prj.director_id] if prj.director_id else []
            ids += [st.roles[r].cast_id for r in prj.role_ids if st.roles[r].cast_id]
    rels = sorted((r for r in st.rels.values() if pl.id in (r.a, r.b) and (abs(r.affinity) >= 20 or r.status not in ("acquainted",))),
                  key=lambda r: -abs(r.affinity))
    ids += [r.b if r.a == pl.id else r.a for r in rels[:6]]
    seen, out = set(), []
    for i in ids:
        if i in seen or i not in st.people or i == pl.id:
            continue
        seen.add(i)
        out.append(_person_card(st, st.people[i]))
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


def _person_card(st, p) -> dict:
    pl = st.player
    r = st.rel(pl.id, p.id, create=False)
    prof = "director" if "director" in p.roles else "actor"
    recent = [c for c in p.credits if c.get("kind") in ("film", "prior")][-3:]
    card = {"id": p.id, "name": p.name, "age": age_on(p.birth, st.date), "profession": prof,
            "public_profile": fame_label(p.fame), "traits": p.traits, "motivation": motivation(p), "bio": p.bio,
            "recent_work": [f"'{c['title']}' ({c['year']}, {c['role']})" for c in recent],
            "relationship_status": ("married (outside the industry)" if p.partner_status == "married_offscreen"
                                    else (f"{p.partner_status} {st.people[p.partner_id].name}" if p.partner_id in st.people
                                          else "single"))}
    if p.historical:
        card["real_person"] = True
    if r:
        card["with_you"] = {"standing": affinity_label(r.affinity), "status": r.status,
                            "history": [h["text"] + f" ({h['date']})" for h in r.history[-4:]]}
    return card


def _chart(st) -> list:
    ch = st.market.get("chart")
    if not ch:
        return []
    return [f"{i}. '{x['title']}' ({x['studio']}) — {money(x['gross'])} this week, {money(x['total'])} total, week {x['week']}"
            for i, x in enumerate(ch["top"][:5], 1)]


def _decision(d) -> dict:
    out = {"id": d.id, "kind": d.kind, "summary": d.summary, "options": d.options, "deadline": d.deadline,
           "if_unanswered": d.default}
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
    for c in pl.credits:
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
    return {"career_so_far": credits[-12:],
            "earlier_key_moments": [f"{e['date']}: {e['text']}" for e in earlier[-cfg['narrator']['continuity_events']:]],
            "recent_scenes_and_threads": [f"{dte}: {t}" for dte, t in scenes[-12:]]}
