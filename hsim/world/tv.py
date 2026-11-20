"""Fictional television series of the era: recurring workplaces for working actors.

Real 1980 network names are used as setting; the series themselves are fictional
(so the simulation never misstates real shows' casts). Each show has a premise,
format, recurring regulars (fictional actors), a producer and a rotation of
episode directors, so a guest spot comes with a show, a character, an episode
and colleagues.
"""
from __future__ import annotations

from .. import models as M
from ..core import rng as R
from ..core.state import WorldState
from . import names as N

NETWORKS = ["ABC", "CBS", "NBC", "first-run syndication", "PBS"]
FORMATS = {
    "police": ("hour-long police drama", ["Precinct", "Squad", "Beat", "Patrol", "Badge", "Division"],
               ["Harbor", "Metro", "Central", "Westside", "Bay City", "Downtown"],
               "detectives of a {place} precinct work the city's toughest cases"),
    "medical": ("hour-long medical drama", ["General", "Memorial", "County", "Mercy", "St. Vincent's", "Emergency"],
                ["Lakeview", "Riverside", "City", "Oakwood", "Valley", "Northside"],
                "doctors and nurses at {place} hospital juggle emergencies and private lives"),
    "sitcom": ("half-hour sitcom", ["& Company", "Street", "Place", "Family", "Diner", "Garage"],
               ["Mulligan's", "The Kowalski", "Fifth", "Maple", "Rosie's", "Dugan's"],
               "the regulars at {place} get into weekly trouble"),
    "detective": ("hour-long private-eye series", ["Investigations", "& Associates", "P.I.", "Files", "Case", "Agency"],
                  ["Cole", "Malone", "Hart", "Santos", "Dakota", "Brennan"],
                  "a {place} private eye takes the cases nobody else will"),
    "soap": ("prime-time soap", ["Heights", "Ranch", "Estate", "Landing", "Ridge", "Point"],
             ["Golden", "Shadow", "Silver", "Crystal", "Eagle", "Paradise"],
             "a wealthy family at {place} fights over money, love and inheritance"),
    "action": ("hour-long action-adventure", ["Force", "Patrol", "Rescue", "Run", "Squadron", "Riders"],
               ["Highway", "Coast", "Sky", "Desert", "Canyon", "Mountain"],
               "a {place} rescue team takes on danger every week"),
}
EPISODES = {
    "police": ["a hostage standoff at a bank", "a string of rooftop burglaries", "a crooked councilman's murder",
               "a runaway who witnessed a killing", "a car-theft ring at the docks"],
    "medical": ["a bus crash that floods the ER", "a famous patient who refuses surgery", "a malpractice suit",
                "a mystery illness at a summer camp", "a surgeon with a secret"],
    "sitcom": ["a disastrous blind date", "a surprise inspection", "a talent show gone wrong",
               "a lottery ticket that might be a winner", "an old flame comes to town"],
    "detective": ["a missing heiress", "a blackmailed movie producer", "an insurance fraud that turns deadly",
                  "a stolen racehorse", "a nightclub singer in danger"],
    "soap": ["a contested will", "a charity ball scandal", "a secret pregnancy", "a hostile takeover",
             "a long-lost sibling arrives"],
    "action": ["a forest fire trapping hikers", "a smuggling ring on the coast", "a stranded school bus",
               "a mountain avalanche", "a sabotaged oil rig"],
}
# Neutral parts can be cast with any gender (ordinary gender-flexible casting); gendered
# descriptions only go with a role of that gender.
GUEST_PARTS_NEUTRAL = ["the witness", "a desperate parent", "a con artist", "a rookie officer", "a nightclub owner",
                       "a nervous bank teller", "a society reporter", "the new neighbour", "a hitchhiker",
                       "a hotshot lawyer", "an old friend of the lead", "a hotel clerk", "a drifter", "a young doctor",
                       "a union boss"]
GUEST_PARTS_GENDERED = {"f": ["the suspect's girlfriend", "the victim's sister", "a waitress", "a grieving widow"],
                        "m": ["the suspect's boyfriend", "the victim's brother", "a bartender", "a grieving widower"]}
GUEST_PARTS = GUEST_PARTS_NEUTRAL + GUEST_PARTS_GENDERED["f"] + GUEST_PARTS_GENDERED["m"]


def guest_part(g, gender: str) -> str:
    pool = GUEST_PARTS_NEUTRAL + GUEST_PARTS_GENDERED.get(gender, [])
    return pool[int(g.integers(len(pool)))]


def make_shows(st: WorldState, cfg: dict) -> None:
    from .genesis import make_director
    from .people import _person
    n = cfg["tv"]["shows"]
    actors = sorted((p for p in st.people.values() if "actor" in p.roles and not p.historical
                     and p.provenance.get("archetype") in ("working", "notable")), key=lambda p: p.id)
    used = set()
    kinds = sorted(FORMATS)
    for i in range(n):
        g = R.stream(st.seed, "tv-show", i)
        kind = kinds[i % len(kinds)]
        fmt, suffixes, prefixes, premise = FORMATS[kind]
        place = prefixes[int(g.integers(len(prefixes)))]
        title = f"{place} {suffixes[int(g.integers(len(suffixes)))]}".replace("The Kowalski Family", "The Kowalskis")
        if any(s.title == title for s in st.shows.values()):
            title = f"{title} {['Blues', 'Nights', 'West', 'Story'][i % 4]}"
        regulars = []
        for _ in range(int(g.integers(3, 6))):
            cand = actors[int(g.integers(len(actors)))] if actors else None
            if cand and cand.id not in used:
                used.add(cand.id)
                regulars.append(cand.id)
                cand.persona["series"] = title
        prod = _person(st, g, f"tvp-{i}", "producer", None, 32, 62, female_share=0.25)
        prod.bio = f"Executive producer of '{title}'."
        st.people[prod.id] = prod
        dirs = []
        for k in range(3):
            dp = make_director(st, cfg, f"tv-{i}-{k}", st.date)
            dp.bio = f"Television director who works regularly on '{title}'."
            st.people[dp.id] = dp
            dirs.append(dp.id)
        sid = f"tv-{i:03d}"
        st.shows[sid] = M.Show(id=sid, title=title, network=NETWORKS[int(g.integers(len(NETWORKS)))], genre=kind,
                               format=fmt, premise=premise.format(place=place), regulars=regulars,
                               producer_id=prod.id, director_ids=dirs, started=st.date and int(st.date[:4]) - int(g.integers(0, 4)))
