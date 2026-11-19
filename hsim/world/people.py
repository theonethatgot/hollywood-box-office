"""Professionals as people: personas, agents, casting directors, producers.

Fictional people get a distinctive, persistent persona (background, home town,
a signature habit, a professional reputation, a current ambition). Real people
get ONLY what the record supports: a reputation derived from documented credits
and honours, plus the Wikidata description. No biographical facts are invented
for real people; their ambitions are derived from simulated goals and labelled
as simulation characterisation.
"""
from __future__ import annotations

from .. import models as M
from ..core import rng as R
from ..core.state import WorldState
from ..core.util import age_on, clamp, d, iso, year
from . import names as N

TRAINING = ["trained at a New York acting studio", "came up through Chicago improv", "a former model",
            "a stage actor from regional repertory theatre", "a former child actor", "a drama-school graduate",
            "came to acting from stand-up comedy", "a former dancer", "a stuntman turned actor",
            "discovered in a community-theatre production", "studied theatre at a state university",
            "spent years doing summer stock"]
HOMETOWNS = ["Brooklyn", "Chicago", "Dallas", "a small town in Ohio", "Boston", "New Orleans", "Philadelphia",
             "San Francisco", "rural Georgia", "Detroit", "Phoenix", "Seattle", "Toronto", "London", "Miami",
             "the San Fernando Valley", "Pittsburgh", "Minneapolis", "Kansas City", "Baltimore"]
SIGNATURES = ["keeps a battered notebook of character ideas", "famous for practical jokes on set",
              "never eats before a performance", "quotes Brando at every opportunity",
              "always first to arrive and last to leave", "carries a thermos of terrible coffee everywhere",
              "remembers every crew member's name", "chain-smokes between takes", "reads tarot for the cast",
              "obsessive about getting the period details right", "plays guitar in the trailer between setups",
              "runs lines with anyone who will listen", "talks openly about wanting to direct",
              "collects vintage cars", "swears by a strict macrobiotic diet"]
AGENT_STYLES = ["a fast-talking deal-maker", "a patient career-builder", "a protective, old-school agent",
                "an ambitious young agent hungry for a breakout client", "a blunt pragmatist",
                "a well-connected charmer who works the phones all day"]
CD_STYLES = ["known for championing unknowns", "trusts theatre actors over TV faces", "notoriously hard to impress",
             "likes to see actors take risks in the room", "values preparation above all",
             "has a long memory for actors who impressed her once", "casts quickly and decisively"]

GOAL_AMBITION = {
    "money": "wants bigger paydays and financial security",
    "fame": "wants a breakout role and a recognisable name",
    "prestige": "wants serious, respected work that gets noticed at awards time",
    "art": "wants challenging material over safe paychecks",
    "stability": "wants steady work and a sustainable life",
}


def _pick(g, seq):
    return seq[int(g.integers(len(seq)))]


def reputation(st: WorldState, p: M.Person) -> str:
    """Professional reputation from (simulated or documented) credits and honours."""
    films = [c for c in p.credits if c.get("kind") in ("film", "prior") and c.get("role") != "director"]
    wins = [a for a in p.awards if a.get("result") == "won"]
    noms = [a for a in p.awards if a.get("result") == "nominated"]
    if "director" in p.roles and "actor" not in p.roles:
        n = sum(1 for c in p.credits if c.get("role") == "director")
        genres = _top_genres(p.credits, director=True)
        return f"director{(' of ' + genres) if genres else ''}" + (f" with {n} films" if n > 1 else "")
    if not films:
        return "an unknown"
    leads = sum(1 for c in films if c.get("role") == "lead")
    genres = _top_genres(films)
    kind = ("leading actor" if leads >= max(2, len(films) // 3) else
            "character actor" if len(films) >= 8 else "working actor")
    honour = ""
    if wins:
        honour = " and award winner"
    elif noms:
        honour = " with award nominations"
    return f"{kind}{(' in ' + genres) if genres else ''}{honour}"


def _top_genres(credits, director=False) -> str:
    counts = {}
    for c in credits:
        if director and c.get("role") != "director":
            continue
        g = c.get("genre")
        if g:
            counts[g] = counts.get(g, 0) + 1
    top = [g for g, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:2]]
    return " and ".join(top)


def ambition(p: M.Person) -> str:
    if not p.goals:
        return ""
    top = max(p.goals, key=p.goals.get)
    return GOAL_AMBITION[top]


def give_persona(st: WorldState, p: M.Person, key: str) -> None:
    g = R.stream(st.seed, "persona", key)
    if p.historical:
        p.persona = {"source": "documented record; personality and ambition are simulation characterisation"}
        return
    persona = {"hometown": _pick(g, HOMETOWNS), "signature": _pick(g, SIGNATURES)}
    if "actor" in p.roles:
        persona["background"] = _pick(g, TRAINING)
    p.persona = persona


def _person(st, g, key: str, role: str, employer: str | None, age_lo=28, age_hi=64, female_share=0.45) -> M.Person:
    from .genesis import _goals, _personality, _romance, traits_from_personality
    gender = "f" if g.random() < female_share else "m"
    age = int(g.integers(age_lo, age_hi))
    birth = iso(d(st.date).replace(year=year(st.date) - age, month=int(g.integers(1, 13)), day=int(g.integers(1, 28))))
    first = _pick(g, N.FIRST_F if gender == "f" else N.FIRST_M)
    personality = _personality(g)
    p = M.Person(id=f"gen-{role[:2]}-{key}", name=f"{first} {_pick(g, N.LAST)}", gender=gender, birth=birth,
                 roles=[role], tier="G", personality=personality, goals=_goals(g),
                 traits=traits_from_personality(personality, g), romance=_romance(g, gender),
                 provenance={"source": "generated"}, employer=employer)
    if g.random() < 0.55:
        p.partner_status = "married_offscreen"
    return p


def make_agents(st: WorldState, cfg: dict) -> None:
    per_tier = cfg["people"]["agents_per_agency_tier"]
    for aid, ag in sorted(st.agencies.items()):
        for i in range(per_tier[str(ag.tier)]):
            g = R.stream(st.seed, "agent-person", aid, i)
            p = _person(st, g, f"{aid}-{i}", "agent", aid, 26, 62, female_share=0.35)
            p.persona = {"style": _pick(g, AGENT_STYLES), "hometown": _pick(g, HOMETOWNS),
                         "signature": _pick(g, SIGNATURES)}
            p.bio = f"Agent at {ag.name}; {p.persona['style']}."
            p.direction = {"hustle": round(clamp(ag.hustle + g.normal(0, 10)), 1)}
            st.people[p.id] = p
    assign_agent_people(st)


def assign_agent_people(st: WorldState) -> None:
    """Every represented actor has a named agent inside their agency (balanced load)."""
    by_agency = {}
    for p in st.people.values():
        if "agent" in p.roles and p.employer:
            by_agency.setdefault(p.employer, []).append(p)
    for lst in by_agency.values():
        lst.sort(key=lambda x: x.id)
    load = {}
    for pid, p in sorted(st.people.items()):
        if "actor" not in p.roles or not p.agent_id:
            continue
        if p.agent_person_id and st.people.get(p.agent_person_id) and st.people[p.agent_person_id].employer == p.agent_id:
            continue
        agents = by_agency.get(p.agent_id, [])
        if not agents:
            continue
        a = min(agents, key=lambda x: (load.get(x.id, 0), R.unit(st.seed, "agent-pick", pid, x.id)))
        load[a.id] = load.get(a.id, 0) + 1
        p.agent_person_id = a.id


def make_casting_directors(st: WorldState, cfg: dict) -> None:
    c = cfg["people"]
    for sid, studio in sorted(st.studios.items()):
        if studio.slate_per_year <= 0:
            continue
        n = c["casting_directors_major"] if studio.tier == "major" else c["casting_directors_mini"]
        for i in range(n):
            _make_cd(st, f"{sid}-{i}", sid)
    for i in range(c["casting_directors_independent"]):
        _make_cd(st, f"ind-{i}", "independent")


def _make_cd(st, key, employer) -> None:
    g = R.stream(st.seed, "cd-person", key)
    p = _person(st, g, key, "casting_director", employer, 30, 66, female_share=0.7)   # the field skewed female
    p.persona = {"style": _pick(g, CD_STYLES), "hometown": _pick(g, HOMETOWNS)}
    where = st.studios[employer].name if employer in st.studios else "an independent casting office"
    p.bio = f"Casting director ({where}); {p.persona['style']}."
    st.people[p.id] = p


def casting_director_for(st: WorldState, proj: M.Project) -> str | None:
    if proj.casting_director_id:
        return proj.casting_director_id
    own = sorted(pid for pid, p in st.people.items() if "casting_director" in p.roles and p.employer == proj.studio_id)
    pool = own or sorted(pid for pid, p in st.people.items() if "casting_director" in p.roles and p.employer == "independent")
    if not pool:
        return None
    proj.casting_director_id = pool[int(R.unit(st.seed, "cd-assign", proj.id) * len(pool))]
    return proj.casting_director_id


def character_name(g, gender: str) -> str:
    first = _pick(g, N.FIRST_M if gender == "m" else N.FIRST_F)
    return f"{first} {_pick(g, N.LAST)}" if g.random() < 0.6 else first
