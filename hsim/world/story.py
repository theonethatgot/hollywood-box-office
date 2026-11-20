"""Film story profiles: a persistent screenplay outline for productions the protagonist
auditions for, is offered or works on.

Generated once (deterministically) and stored on the project. It gives the narrator
the film's dramatic substance (central conflict, characters and arcs, relationships,
major beats, the protagonist's key scenes, the director's intentions) without
predetermining quality, reviews or box office. The protagonist's "read of the script"
comes from the same noisy perception the engine uses for their decisions.

Real films never get an invented plot: the profile tells the narrator to use the real
film's actual story and marks the protagonist's character as a simulated addition.
"""
from __future__ import annotations

from ..core import rng as R

FUNCTIONS = {
    "drama": ("the protagonist", ["the estranged sibling", "the spouse", "the old friend", "the parent"],
              ["the employer", "the lawyer", "the neighbour", "the mentor", "the rival"]),
    "comedy": ("the protagonist", ["the reluctant partner-in-crime", "the love interest", "the best friend"],
               ["the boss", "the nosy neighbour", "the con man", "the in-law"]),
    "action": ("the hero", ["the partner", "the witness under protection", "the ex-lover"],
               ["the villain", "the commanding officer", "the informant", "the crooked cop"]),
    "romance": ("the protagonist", ["the love interest"], ["the rival suitor", "the confidante", "the disapproving parent"]),
    "thriller": ("the investigator", ["the only ally", "the person who knows too much"],
                 ["the powerful suspect", "the handler", "the killer", "the editor"]),
    "horror": ("the final survivor", ["the friend who doesn't believe", "the sibling"],
               ["the local who warns them", "the first victim", "the sheriff"]),
    "family": ("the young hero", ["the unlikely friend"], ["the grumpy guardian", "the villain", "the wise elder"]),
    "scifi": ("the reluctant leader", ["the second-in-command"], ["the corporate liaison", "the android", "the commander"]),
}
LINK = {"the estranged sibling": "estranged siblings", "the spouse": "a marriage under strain",
        "the old friend": "old friends with unfinished business", "the parent": "parent and child",
        "the reluctant partner-in-crime": "an odd-couple partnership", "the love interest": "a romance",
        "the best friend": "best friends", "the partner": "partners who don't trust each other",
        "the witness under protection": "protector and witness", "the ex-lover": "former lovers forced together",
        "the only ally": "uneasy allies", "the person who knows too much": "a dangerous alliance",
        "the friend who doesn't believe": "friends split by fear", "the sibling": "siblings",
        "the unlikely friend": "an unlikely friendship", "the second-in-command": "a command partnership"}
WANTS = ["to prove they still matter", "to protect the one person they love", "to get out of town for good",
         "to finally tell the truth", "to win back respect they lost", "to keep a promise", "to be left alone",
         "to belong somewhere", "to make things right"]
FLAWS = ["pride", "a temper they can't control", "a habit of running from trouble", "an old lie",
         "blind loyalty", "fear of being ordinary", "drinking", "trusting the wrong people", "ambition"]
CONFLICTS = {
    "drama": "{L} must face what tore the family apart, and {C} is the one person who remembers it differently",
    "comedy": "{L}'s simple plan spirals out of control, and {C} keeps making it worse and funnier",
    "action": "{L} has one chance to stop {S} before the deadline, and can't do it without {C}",
    "romance": "{L} and {C} are wrong for each other on paper and right for each other in every scene",
    "thriller": "{L} uncovers something {S} will kill to keep hidden, and {C} may be in on it",
    "horror": "something is hunting {L}'s group, and {C} refuses to believe it until it's too late",
    "family": "{L} sets out on an adventure no adult will approve of, with {C} as the most unlikely companion",
    "scifi": "far from help, {L} must hold the crew together while {S} hides the truth about the mission",
}
SCENES = ["a late-night confrontation in a kitchen", "an argument in a moving car", "a quiet confession on a rooftop",
          "a crowded party where everything comes out", "a long single take at a hospital bedside",
          "a showdown in the rain", "a phone call that changes everything", "a dinner that goes badly wrong",
          "a goodbye at a bus station", "a chase through a crowded market"]
INTENT = {
    "vision": "wants long, unbroken takes and room for actors to find moments",
    "technical": "is planning elaborate camera moves and needs precise marks",
    "actor_direction": "rehearses the relationships for days before blocking a single scene",
    "discipline": "runs a tight, efficient set and expects lines cold on the day",
    "commercial": "is focused on pace and big moments that will play in a trailer",
}


def _pick(g, seq):
    return seq[int(g.integers(len(seq)))]


def ensure_story(st, proj) -> dict:
    if proj.story:
        return proj.story
    roles = [st.roles[r] for r in proj.role_ids]
    if proj.historical_ref:
        proj.story = {"provenance": "real film: use its actual documented story from general knowledge; "
                                    "this record does not contain its plot",
                      "characters": [{"role_id": r.id, "name": r.name, "importance": r.importance,
                                      "name_documented": r.name_documented} for r in roles
                                     if r.importance != "featured"],
                      "links": {}}
        return proj.story
    g = R.stream(st.seed, "story", proj.id)
    lead_f, co_fs, sup_fs = FUNCTIONS[proj.genre]
    lead = next((r for r in roles if r.importance == "lead"), None)
    colead = next((r for r in roles if r.importance == "colead"), None)
    sups = [r for r in roles if r.importance == "supporting"]
    chars, links = [], {}
    functions = {}
    if lead:
        functions[lead.id] = lead_f
    if colead:
        functions[colead.id] = _pick(g, co_fs)
    antagonist = None
    for i, r in enumerate(sups):
        f = sup_fs[i % len(sup_fs)] if i else _pick(g, sup_fs)
        functions[r.id] = f
        if antagonist is None and any(k in f for k in ("villain", "killer", "suspect", "liaison", "boss", "crooked")):
            antagonist = r
    antagonist = antagonist or (sups[0] if sups else None)
    principals = [x for x in (lead, colead) if x] + sups
    wants = [WANTS[i] for i in g.permutation(len(WANTS))]       # no two characters share a want or flaw
    flaws = [FLAWS[i] for i in g.permutation(len(FLAWS))]
    for k, r in enumerate(principals):
        want, flaw = wants[k % len(wants)], flaws[k % len(flaws)]
        chars.append({"role_id": r.id, "name": r.name, "importance": r.importance, "function": functions[r.id],
                      "wants": want, "flaw": flaw,
                      "arc": f"from {flaw} toward {'' if r.importance != 'supporting' else 'a reckoning with '}"
                             f"{_pick(g, ['honesty', 'courage', 'forgiveness', 'self-respect', 'letting go', 'responsibility'])}"})
    if lead and colead:
        links[f"{lead.id}|{colead.id}"] = LINK.get(functions[colead.id], "a central partnership")
    for r in sups:
        if lead:
            kind = "antagonists" if r is antagonist else ("mentor and protégé" if "mentor" in functions[r.id] or
                                                           "elder" in functions[r.id] else "a complicated alliance")
            links[f"{lead.id}|{r.id}"] = kind
    L = lead.name if lead else "the protagonist"
    C = colead.name if colead else "an unexpected ally"
    S = antagonist.name if antagonist else "the opposition"
    conflict = CONFLICTS[proj.genre].format(L=L, C=C, S=S)
    beats = [f"Setup: {L}'s ordinary life, already cracking ({proj.premise.rstrip('.')})",
             f"Inciting incident: an event forces {L} and {C} together",
             f"Midpoint: a revelation turns {S} from obstacle into real threat",
             f"Low point: {L} loses what they were fighting for, and {C} walks away",
             f"Climax: {L} confronts {S}; what {L} has become decides the ending"]
    proj.story = {"provenance": "simulated screenplay for a fictional production",
                  "logline": f"A {proj.tone} {proj.genre}: {proj.premise}", "central_conflict": conflict,
                  "characters": chars, "links": links, "beats": beats,
                  "key_scenes": {r.id: [_pick(g, SCENES) for _ in range(2)] for r in roles if r.importance != "featured"}}
    return proj.story


def creative_intent(st, proj) -> str:
    d = st.people.get(proj.director_id) if proj.director_id else None
    if not d:
        return "no director attached yet"
    skill = max(d.direction, key=d.direction.get) if d.direction else "vision"
    style = INTENT.get(skill, INTENT["vision"])
    if d.historical:
        return (f"{d.name} {style} (simulation characterisation of this production, not a documented account of "
                f"their real working methods; portray consistently with what is publicly known about them)")
    return f"{d.name} {style}" + (f"; known on sets as someone who {d.persona['signature']}"
                                   if d.persona.get("signature") else "")


def script_read(st, proj, person) -> str:
    """The protagonist's impression of the screenplay: the same noisy read their decisions use."""
    g = R.stream(st.seed, "script-read", proj.id, person.id)
    ag = st.agencies.get(person.agent_id) if person.agent_id else None
    noise_sd = 16 - (ag.info_quality / 10 if ag else 0)
    obs = proj.script_quality + g.normal(0, noise_sd)
    strength, verb = _pick(R.stream(st.seed, "read-detail", proj.id),
                           [("the dialogue", "works"), ("the central relationship", "works"), ("the structure", "works"),
                            ("the set pieces", "work"), ("the humour", "works")])
    has = "have" if verb == "work" else "has"
    if obs >= 65:
        return f"you think it's genuinely good, especially {strength}"
    if obs >= 50:
        return f"you think it's solid; {strength} {verb}, though parts feel familiar"
    if obs >= 38:
        return f"you have doubts; {strength} {has} promise but the rest needs work"
    return "privately, you think the script is weak and hope the director can save it"


def packet_view(st, proj, player_role) -> dict:
    story = ensure_story(st, proj)
    view = {"provenance": story["provenance"]}
    if proj.historical_ref:
        mine = next((c for c in story["characters"] if c["role_id"] == player_role.id), None)
        view["your_character"] = (f"{player_role.name} (simulated addition to the real film; not in its documented cast)"
                                  if not player_role.intended else player_role.name)
        view["other_principal_characters"] = [f"{c['name']} ({c['importance']}, "
                                              f"{'documented name' if c['name_documented'] else 'simulated name'})"
                                              for c in story["characters"] if c["role_id"] != player_role.id]
        return view
    by_id = {c["role_id"]: c for c in story["characters"]}
    cast = {r.id: st.people[r.cast_id].name for r in (st.roles[x] for x in proj.role_ids) if r.cast_id}
    view.update({"logline": story["logline"], "central_conflict": story["central_conflict"],
                 "characters": [f"{c['name']} ({c['function']}{', played by ' + cast[c['role_id']] if c['role_id'] in cast else ''})"
                                f": wants {c['wants']}; flaw: {c['flaw']}; arc {c['arc']}" for c in story["characters"]],
                 "relationships": [f"{by_id[a]['name']} and {by_id[b]['name']}: {kind}"
                                   for key, kind in story["links"].items() for a, b in [key.split("|")]
                                   if a in by_id and b in by_id],
                 "beats": story["beats"],
                 "creative_intent": creative_intent(st, proj)})
    if player_role.id in story.get("key_scenes", {}):
        view["your_key_scenes"] = story["key_scenes"][player_role.id]
    view["your_read_of_the_script"] = script_read(st, proj, st.player) + " (your impression; it may be wrong)"
    return view
