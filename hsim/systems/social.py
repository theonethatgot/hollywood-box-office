"""Ordinary social life in the industry.

Relationships deepen (or fade) through everyday contact, not only through work:
lunches with an agent, running into a former co-star, a premiere party. Every
encounter is with someone the person genuinely knows or is plausibly placed near
(the cast of a film actually premiering this week). Most weeks nothing happens;
quiet stretches are normal. Encounters feed relationships and can create the
contact that romance needs. NPC friendships follow the same rule.
"""
from __future__ import annotations

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_days, clamp

VENUES = ["over lunch at Musso & Frank Grill", "at a party in Laurel Canyon", "at the Formosa Café",
          "between classes at an acting workshop", "at a Sunday barbecue in Studio City", "at Dan Tana's",
          "at a screening at the Directors Guild", "at the Improv on Melrose", "at a friend's opening night",
          "in the waiting room at a casting office", "on the beach in Santa Monica", "at a charity softball game"]


def step(st: WorldState, cfg: dict) -> None:
    sc = cfg["social"]
    _player_encounters(st, cfg, sc)
    _premieres(st, cfg, sc)
    _npc_friendships(st, cfg, sc)


def _known(st, pid, min_affinity=0.0):
    out = []
    for key, r in st.rels.items():
        if pid in (r.a, r.b) and (r.contact_weeks > 0 or r.history) and r.affinity >= min_affinity:
            other = r.b if r.a == pid else r.a
            if other in st.people and not st.people[other].death:
                out.append((other, r))
    return sorted(out, key=lambda x: x[0])


def _player_encounters(st, cfg, sc) -> None:
    p = st.player
    if not p:
        return
    def established(other_id, r):
        """Catch-ups need a real connection: worked together, genuine goodwill, or your own agent."""
        worked = any("worked together" in h["text"] or "clashed on the set" in h["text"] or "rehears" in h["text"]
                     for h in r.history) or r.contact_weeks >= 2
        return "agent" in st.people[other_id].roles or worked or r.affinity >= 8
    contacts = [(o, r) for o, r in _known(st, p.id, min_affinity=-5) if established(o, r)]
    if not contacts:
        return
    sociability = 0.5 + p.personality.get("openness", 50) / 100
    breadth = min(1.0, len(contacts) / sc["contacts_for_full_social_life"])    # fewer friends, fewer outings
    if R.unit(st.seed, "social-week", p.id, st.date) > sc["player_weekly"] * sociability * breadth:
        return
    def access(other):            # a working actor doesn't casually socialise with stars they met once
        gap = st.people[other].fame - p.fame
        return 1.0 if gap < 0.1 else max(0.05, 1 - gap * 2.5)
    weights = [max(0.5, r.affinity + 10) * (2.0 if "agent" in st.people[o].roles else 1.0) * access(o)
               for o, r in contacts]
    u = R.unit(st.seed, "social-who", p.id, st.date) * sum(weights)
    acc = 0.0
    for (other_id, r), w in zip(contacts, weights):
        acc += w
        if u <= acc:
            break
    other = st.people[other_id]
    venue = VENUES[int(R.unit(st.seed, "social-venue", p.id, st.date) * len(VENUES))]
    if "agent" in other.roles:
        venue = "over lunch with your agent"
    warmth = (p.personality.get("warmth", 50) + other.personality.get("warmth", 50)) / 200
    delta = round(1 + 3 * warmth * R.unit(st.seed, "social-delta", p.id, st.date), 1)
    r.affinity = round(clamp(r.affinity + delta, -100, 100), 2)
    r.contact_weeks += 1
    r.history.append({"date": st.date, "text": f"caught up {venue}", "delta": delta})
    st.market.setdefault("contacts", []).append([r.a, r.b, "social"])
    st.log("social", f"You caught up with {other.name} {venue}." if "agent" not in other.roles
           else f"You had lunch with your agent, {other.name}.",
           actors=[p.id, other.id], salience=1, public=False)


def _premieres(st, cfg, sc) -> None:
    """Represented actors are sometimes invited to premieres of films opening this week."""
    p = st.player
    if not p or not p.agent_id:
        return
    opening = [q for _, q in sorted(st.projects.items()) if q.release_date == st.date and q.stage == "released"]
    if not opening:
        return
    if R.unit(st.seed, "premiere", p.id, st.date) > sc["premiere_invite_weekly"] * (1 + p.fame * 10):
        return
    reasons = []
    for q in opening:
        crew = [st.roles[x].cast_id for x in q.role_ids if st.roles[x].cast_id] + ([q.director_id] if q.director_id else [])
        clients = [c for c in crew if st.people[c].agent_id == p.agent_id and c != p.id]
        friends = [c for c in crew if (rr := st.rel(p.id, c, create=False)) and rr.affinity >= 5]
        worked_for = any(c.get("project_id") in st.projects and st.projects[c["project_id"]].studio_id == q.studio_id
                         for c in p.credits)
        if friends:
            reasons.append((q, f"{st.people[friends[0]].name}, whom you know, got you on the list"))
        elif clients:
            reasons.append((q, f"your agency represents {len(clients)} of the film's cast"))
        elif worked_for:
            reasons.append((q, f"you've worked for {st.studios[q.studio_id].name}"))
    if not reasons:
        return
    film, why = reasons[int(R.unit(st.seed, "premiere-film", p.id, st.date) * len(reasons))]
    cast = [st.roles[x].cast_id for x in film.role_ids if st.roles[x].cast_id] + ([film.director_id] if film.director_id else [])
    met = []
    for c in cast[:3]:
        if c == p.id:
            continue
        r = st.rel(p.id, c)
        gap = max(0.0, st.people[c].fame - p.fame)
        if R.unit(st.seed, "premiere-meet", p.id, c, st.date) < 0.5 * max(0.15, 1 - gap * 2):
            r.affinity = round(clamp(r.affinity + 2, -100, 100), 2)
            r.history.append({"date": st.date, "text": f"met at the premiere of '{film.title}'", "delta": 2})
            met.append(st.people[c].name)
    text = f"You were invited to the premiere of '{film.title}' ({why})"
    st.log("premiere", text + (f", where you met {', '.join(met)}." if met else "."),
           actors=[p.id] + cast[:3], refs={"project": film.id}, salience=1, public=False)


def _npc_friendships(st, cfg, sc) -> None:
    for key, r in sorted(st.rels.items()):
        if r.affinity < 20 or st.player_id in (r.a, r.b):
            continue
        if R.unit(st.seed, "npc-social", key, st.date) < sc["npc_friend_weekly"]:
            r.contact_weeks += 1
            r.affinity = round(clamp(r.affinity + 0.5, -100, 100), 2)
            st.market.setdefault("contacts", []).append([r.a, r.b, "social"])
