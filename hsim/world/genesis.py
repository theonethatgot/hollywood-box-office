"""World genesis: build the starting world for a given date.

The slice builds a fictional-but-era-faithful population (generated actors and
directors, real 1980 studio and agency names) and seeds a production pipeline
whose stages are inferred from release dates, exactly as the historical
snapshot compiler will do for real films (DESIGN.md §4). When a historical data
pack is supplied (datapipe/), its people and events are loaded alongside.
"""
from __future__ import annotations

import math

import numpy as np

from .. import models as M
from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_days, add_weeks, age_on, clamp, iso, next_friday, d, year
from ..systems import market
from . import names as N


def _pick(g, seq):
    return seq[int(g.integers(len(seq)))]


# ------------------------------------------------------------------ people ---
def _personality(g: np.random.Generator) -> dict:
    return {k: float(clamp(g.normal(50, 18))) for k in
            ("temperament", "warmth", "ego", "discipline", "ambition", "risk", "openness")}


def traits_from_personality(p: dict, g: np.random.Generator) -> list:
    out = []
    for k, (low, high) in N.TRAITS.items():
        v = p.get(k, 50)
        if v >= 68:
            out.append(high[int(g.integers(len(high)))])
        elif v <= 32:
            out.append(low[int(g.integers(len(low)))])
    return out[:4]


def _goals(g: np.random.Generator) -> dict:
    w = g.dirichlet([2, 1.5, 1.5, 1.5, 1.0])
    return {k: round(float(x), 3) for k, x in zip(("money", "fame", "prestige", "art", "stability"), w)}


def _romance(g: np.random.Generator, gender: str) -> dict:
    u = g.random()
    other = "f" if gender == "m" else "m"
    if u < 0.92:
        to = [other]
    elif u < 0.96:
        to = [gender]
    else:
        to = ["m", "f"]
    return {"attracted_to": to, "openness": round(float(g.beta(3, 3)), 3)}


def _pick_archetype(cfg: dict, g: np.random.Generator) -> str:
    arch = cfg["archetypes"]
    keys = list(arch)
    p = np.array([arch[k]["share"] for k in keys], dtype=float)
    return keys[int(g.choice(len(keys), p=p / p.sum()))]


def _logu(g, lo, hi):
    if lo <= 0:
        return float(g.uniform(lo, hi))
    return float(math.exp(g.uniform(math.log(lo), math.log(hi))))


def make_actor(state: WorldState, cfg: dict, key: str, start: str, archetype: str | None = None,
               gender: str | None = None, birth: str | None = None, name: str | None = None,
               tier: str = "G") -> M.Person:
    g = R.stream(state.seed, "genesis-actor", key)
    archetype = archetype or _pick_archetype(cfg, g)
    a = cfg["archetypes"][archetype]
    if gender is None:
        gender = "m" if g.random() < cfg["world"]["actor_gender_share_m"] else "f"
    age_lo, age_hi = {"newcomer": (18, 30), "working": (21, 66), "notable": (25, 64), "star": (24, 60)}[archetype]
    if birth is None:
        age = int(g.integers(age_lo, age_hi + 1))
        birth = iso(d(start).replace(year=year(start) - age, month=int(g.integers(1, 13)), day=int(g.integers(1, 28))))
    if name is None:
        first = (N.FIRST_M if gender == "m" else N.FIRST_F)[int(g.integers(len(N.FIRST_M if gender == "m" else N.FIRST_F)))]
        name = f"{first} {N.LAST[int(g.integers(len(N.LAST)))]}"
    age = age_on(birth, start)
    talent = clamp(g.normal(50, 14) + (6 if archetype in ("notable", "star") else 0), 5, 98)
    exp_years = {"newcomer": 0.5, "working": min(age - 18, 25) * 0.6, "notable": min(age - 18, 30) * 0.7,
                 "star": min(age - 18, 30) * 0.7}[archetype]
    craft = clamp(15 + 0.25 * talent + exp_years * 1.4 + g.normal(0, 7), 5, 95)
    presence = clamp(g.normal(50 + (14 if archetype == "star" else 5 if archetype == "notable" else 0), 14), 5, 98)
    rng_regs = {r: clamp(0.45 * talent + g.normal(25, 13)) for r in M.REGISTERS}
    strong = list(g.choice(M.REGISTERS, size=2, replace=False))
    for r in strong:
        rng_regs[r] = clamp(rng_regs[r] + 15)
    fame = _logu(g, max(a["fame"][0], 1e-4), a["fame"][1]) if a["fame"][1] > 0 else 0.0
    bank = float(g.uniform(*a["bank"]))
    quote = _logu(g, *a["quote"]) if a["quote"][1] > 0 else 0.0
    quote *= market.infl(cfg, year(start))
    n_credits = int(g.integers(a["credits"][0], a["credits"][1] + 1))
    personality = _personality(g)
    p = M.Person(
        id=f"gen-a-{key}", name=name, gender=gender, birth=birth, roles=["actor"], tier=tier,
        talent=round(talent, 2), craft=round(craft, 2), presence=round(presence, 2),
        range={k: round(v, 2) for k, v in rng_regs.items()},
        fame=round(fame, 5), appeal=round(float(g.beta(4, 4)), 3), bankability=round(bank, 2),
        critical_rep=round(clamp(g.normal(40 + 0.35 * (talent - 50) + (8 if archetype == "notable" else 0), 9)), 2),
        prestige=round(clamp(g.normal({"newcomer": 3, "working": 12, "notable": 30, "star": 45}[archetype], 8)), 2),
        heat=round(float(g.normal(0, 12)), 2), quote=round(quote, 0),
        typecast={r: 0.5 for r in strong[:1]},
        personality=personality, goals=_goals(g), traits=traits_from_personality(personality, g),
        romance=_romance(g, gender),
        cash=round(float(quote * g.uniform(0.2, 1.5) + g.uniform(500, 4000)), 0),
        monthly_costs=cfg["finance"]["default_monthly_costs"][archetype] * market.infl(cfg, year(start)),
        energy=80.0,
        debut=None if archetype == "newcomer" and n_credits == 0 else str(year(start) - max(1, int(exp_years))),
        provenance={"source": "generated", "archetype": archetype},
    )
    # off-screen spouse for some NPCs (unavailable for romance until breakup)
    married_p = {True: 0.0}.get(age < 22, min(0.65, max(0.0, (age - 22) * 0.035)))
    if g.random() < married_p:
        p.partner_status = "married_offscreen"
    # synthetic back-catalogue (fictional titles) for narrative context
    for i in range(min(n_credits, 6)):
        gen = M.GENRES[int(g.integers(len(M.GENRES)))]
        w1, w2 = N.TITLE_WORDS[gen]
        yr = year(start) - int(g.integers(1, max(2, int(exp_years) + 2)))
        billing = {"star": "lead", "notable": "colead"}.get(archetype, "supporting")
        if g.random() < 0.4:
            billing = "supporting"
        p.credits.append({"project_id": None, "title": f"{w1[int(g.integers(8))]} {w2[int(g.integers(8))]}",
                          "role": billing, "year": yr, "genre": gen, "kind": "prior"})
    p.credits.sort(key=lambda c: c["year"])
    p.bio = _bio(p, archetype, age)
    return p


def _bio(p: M.Person, archetype: str, age: int) -> str:
    lead = {"newcomer": "A newcomer still looking for a first real break",
            "working": "A working actor with a steady run of supporting parts",
            "notable": "A recognisable name with a few memorable roles",
            "star": "A bona fide star"}[archetype]
    best = max(p.range, key=p.range.get)
    t = ("; " + ", ".join(p.traits[:2])) if p.traits else ""
    return f"{lead}; most at home in {best}{t}."


def make_director(state: WorldState, cfg: dict, key: str, start: str) -> M.Person:
    g = R.stream(state.seed, "genesis-director", key)
    gender = "m" if g.random() < 0.94 else "f"   # reflects the era's skewed hiring
    age = int(g.integers(28, 72))
    birth = iso(d(start).replace(year=year(start) - age, month=int(g.integers(1, 13)), day=int(g.integers(1, 28))))
    first = _pick(g, N.FIRST_M if gender == "m" else N.FIRST_F)
    skill = {k: round(clamp(g.normal(50, 15)), 2) for k in ("vision", "technical", "actor_direction", "discipline", "commercial")}
    personality = _personality(g)
    exp = min(age - 26, 30)
    p = M.Person(
        id=f"gen-d-{key}", name=f"{first} {N.LAST[int(g.integers(len(N.LAST)))]}", gender=gender, birth=birth,
        roles=["director"], tier="G", direction=skill,
        bankability=round(clamp(g.normal(20 + exp, 15)), 2), prestige=round(clamp(g.normal(15 + exp * 0.8, 12)), 2),
        critical_rep=round(clamp(g.normal(40 + 0.4 * (skill["vision"] - 50), 10)), 2),
        personality=personality, goals=_goals(g), traits=traits_from_personality(personality, g),
        romance=_romance(g, gender), provenance={"source": "generated"},
    )
    if g.random() < 0.6:
        p.partner_status = "married_offscreen"
    style = max(skill, key=skill.get).replace("_", " ")
    p.bio = f"Director whose strongest suit is {style}" + (f"; {', '.join(p.traits[:2])}" if p.traits else "") + "."
    return p


# ---------------------------------------------------------------- projects ---
def _title(g, genre: str, used: set) -> str:
    w1, w2 = N.TITLE_WORDS[genre]
    for _ in range(30):
        t = f"{w1[int(g.integers(len(w1)))]} {w2[int(g.integers(len(w2)))]}"
        if g.random() < 0.15:
            t = f"The {t}"
        if t not in used:
            return t
    return f"{t} {int(g.integers(2, 9))}"


def _premise(g, genre: str) -> str:
    who, what, how = N.PREMISE[genre]
    return f"{who[int(g.integers(len(who)))].capitalize()} {what[int(g.integers(len(what)))]} {how[int(g.integers(len(how)))]}."


def make_project(state: WorldState, cfg: dict, studio: M.Studio, key: str, created: str) -> M.Project:
    """Pitch → studio greenlight filter (on its own noisy read) → project with roles."""
    dev = cfg["development"]
    used = {p.title for p in state.projects.values()}
    for attempt in range(12):
        g = R.stream(state.seed, "pitch", studio.id, key, attempt)
        gw = studio.genre_weights or {}
        genres = M.GENRES
        w = np.array([gw.get(x, 1.0) for x in genres])
        genre = genres[int(g.choice(len(genres), p=w / w.sum()))]
        script = clamp(g.normal(dev["quality_mean"], dev["quality_sd"]), 5, 98)
        hook = clamp(g.normal(50, 14), 5, 98)
        noise = dev["greenlight_obs_noise"] * (1.5 - studio.exec_taste / 100)
        observed = 0.5 * script + 0.5 * hook + g.normal(0, noise)
        # reject pitches that look weak to this studio (selection on observed, not true, quality)
        if observed >= 50 - 12 * (1 - dev["greenlight_selectivity"]) - (studio.risk_appetite - 50) * 0.2 or attempt == 11:
            break
    gcfg = cfg["genres"][genre]
    budget_real = float(math.exp(g.normal(math.log(studio.budget_median), 0.55)))
    budget = budget_real * 1e6 * market.infl(cfg, year(created))
    breadth = gcfg["breadth"] * math.exp((hook - 50) / 50 * 0.6) * math.exp(g.normal(0, 0.40))
    tilt_noise = g.dirichlet([6, 6, 6, 6]) * 4
    tilt = {s: round(float(t * n), 3) for s, t, n in zip(cfg["box_office"]["segments"], gcfg["tilt"], tilt_noise)}
    sw = gcfg["shoot_weeks"]
    shoot_weeks = int(round(g.uniform(*sw) + max(0, math.log(budget_real / 8)) * 2))
    pid = state.new_id("prj")
    p = M.Project(
        id=pid, title=_title(g, genre, used), genre=genre, studio_id=studio.id, premise=_premise(g, genre),
        budget=round(budget, 0), created=created, script_quality=round(script, 2), hook=round(hook, 2),
        breadth=round(breadth, 4), segment_tilt=tilt, shoot_weeks=max(4, shoot_weeks),
        post_weeks=int(g.integers(*dev["post_weeks"])) + (8 if genre == "scifi" else 0),
        location=["Los Angeles", "New York", "Toronto", "Vancouver", "Texas", "London", "Mexico", "Chicago"][int(g.integers(8))],
    )
    _make_roles(state, cfg, p, g)
    state.projects[pid] = p
    return p


def _make_roles(state, cfg, p: M.Project, g):
    lead_m = {"action": 0.88, "romance": 0.4, "horror": 0.45, "family": 0.6, "drama": 0.6, "comedy": 0.7,
              "thriller": 0.65, "scifi": 0.75}[p.genre]
    lg = "m" if g.random() < lead_m else "f"
    center = int(g.integers(22, 52))
    specs = [("lead", lg, center)]
    if g.random() < 0.8:
        cg = ("f" if lg == "m" else "m") if g.random() < 0.7 else lg
        specs.append(("colead", cg, int(clamp(center + g.normal(-3, 7), 18, 70))))
    for _ in range(int(g.integers(1, 4))):
        specs.append(("supporting", "m" if g.random() < 0.6 else "f", int(g.integers(20, 70))))
    shares = {"lead": 0.45, "colead": 0.28, "supporting": 0.09}
    for i, (imp, gen, c) in enumerate(specs):
        rid = state.new_id("rol")
        reg = p.genre if imp != "supporting" or g.random() < 0.6 else M.REGISTERS[int(g.integers(len(M.REGISTERS)))]
        role = M.Role(id=rid, project_id=p.id, name=_role_name(g, gen), importance=imp, gender=gen,
                      age_min=max(16, c - 7), age_max=c + 7, register=reg, screen_share=shares[imp],
                      description=N.ROLE_DESC[imp])
        state.roles[rid] = role
        p.role_ids.append(rid)


def _role_name(g, gender) -> str:
    first = _pick(g, N.FIRST_M if gender == "m" else N.FIRST_F)
    return first


def schedule_from_release(cfg, p: M.Project, release: str, g) -> None:
    """Infer production calendar backwards from a release date (snapshot logic)."""
    dev = cfg["development"]
    p.release_date = next_friday(release)
    p.shoot_end = add_weeks(p.release_date, -(p.post_weeks + dev["marketing_lead_weeks"]))
    p.shoot_start = add_weeks(p.shoot_end, -p.shoot_weeks)
    p.prepro_start = add_weeks(p.shoot_start, -int(g.integers(*dev["prepro_weeks"])))


def schedule_from_greenlight(cfg, p: M.Project, start: str, g) -> None:
    dev = cfg["development"]
    p.prepro_start = start
    p.shoot_start = next_friday(add_weeks(start, int(g.integers(*dev["prepro_weeks"]))))
    p.shoot_end = add_weeks(p.shoot_start, p.shoot_weeks)
    p.release_date = None   # dated by the studio during post


# ------------------------------------------------------------------- world ---
def new_world(cfg: dict, seed: int, start: str, data_pack: dict | None = None) -> WorldState:
    from ..systems import casting, boxoffice, release   # local import: avoid cycles

    start = next_friday(start)
    st = WorldState(seed=seed, date=start, start_date=start)
    st.orders = default_orders()
    for s in cfg["studios"]:
        g = R.stream(seed, "studio", s["id"])
        st.studios[s["id"]] = M.Studio(
            id=s["id"], name=s["name"], tier=s["tier"], cash=500e6 if s["tier"] == "major" else 80e6,
            slate_per_year=s["slate"], budget_median=s["budget_median"], risk_appetite=s["risk"],
            marketing_eff=float(np.clip(g.normal(1.0, 0.1), 0.7, 1.3)),
            exec_taste=float(clamp(g.normal(50, 15))), historical=True,
            genre_weights={x: float(np.clip(g.normal(1.0, 0.3), 0.3, 2.0)) for x in M.GENRES},
            provenance={"source": "config", "note": "real studio name; attributes are model estimates"})
    for a in cfg["agencies"]:
        st.agencies[a["id"]] = M.Agency(id=a["id"], name=a["name"], tier=a["tier"], hustle=a["hustle"],
                                        negotiation=a["negotiation"], info_quality=a["info"])

    w = cfg["world"]
    n_act = w["generated_actors_with_history"] if data_pack else w["generated_actors"]
    n_dir = w["generated_directors_with_history"] if data_pack else w["generated_directors"]
    for i in range(n_act):
        p = make_actor(st, cfg, f"{i:05d}", start)
        st.people[p.id] = p
    for i in range(n_dir):
        p = make_director(st, cfg, f"{i:05d}", start)
        st.people[p.id] = p
    if data_pack:
        from ..io.datapack import load_pack_into
        load_pack_into(st, cfg, data_pack)
    assign_agents(st, cfg)

    # --- seed production pipeline, stages inferred from release dates ---
    horizon = cfg["world"]["pipeline_months"]
    for sid, studio in sorted(st.studios.items()):
        n = int(round(studio.slate_per_year * (horizon + 3) / 12))
        n = max(0, n - st.market.get("historical_slate", {}).get(sid, 0) * 2)   # real films fill part of the slate
        g = R.stream(seed, "pipeline", sid)
        for k in range(n):
            rel = add_days(start, int(g.integers(-63, horizon * 30)))
            p = make_project(st, cfg, studio, f"seed-{k}", add_days(start, -400))
            schedule_from_release(cfg, p, rel, g)
            if p.prepro_start > start:
                # not yet greenlit at the start date: weekly studio greenlights create these
                for rid in p.role_ids:
                    del st.roles[rid]
                del st.projects[p.id]
                continue
            casting.attach_director(st, cfg, p, quick=True)
            if p.release_date < start:
                p.stage = "released"
            elif p.shoot_end <= start:
                p.stage = "post" if add_weeks(p.shoot_end, p.post_weeks) > start else "awaiting_release"
            elif p.shoot_start <= start:
                p.stage = "shooting"
            elif p.prepro_start <= start:
                p.stage = "prepro"
            else:
                p.stage = "development"
            if p.stage in ("released", "post", "awaiting_release", "shooting"):
                casting.quick_cast(st, cfg, p)
                if p.stage != "shooting":
                    from ..systems import production
                    production.wrap(st, cfg, p, quiet=True)
                    p.actual_cost = p.budget
    # films released shortly before the start date: run their first weeks quietly
    release.prime_recent_releases(st, cfg)
    st.log("genesis", f"The simulation begins on {start}.", public=True, salience=0,
           data={"seed": seed, "people": len(st.people), "projects": len(st.projects)})
    return st


def assign_agents(st: WorldState, cfg: dict | None = None, yearly: bool = False) -> None:
    """Represented actors keep their agency. Credited actors are matched to an agency
    tier by their standing; uncredited actors are signed only with some probability
    (agencies scout showcases and student films). The protagonist is never signed
    silently: they receive an offer they can accept or decline."""
    base = (cfg or {}).get("agents", {}).get("sign_newcomer_yearly", 0.3)
    by_tier = {t: [a for a in sorted(st.agencies.values(), key=lambda a: a.id) if a.tier == t] for t in (1, 2, 3)}
    for pid, p in sorted(st.people.items()):
        if p.agent_id or "actor" not in p.roles or p.death or not p.active:
            continue
        g = R.stream(st.seed, "agent-assign", pid, st.date)
        has_credits = any(c.get("kind") in ("film", "prior") for c in p.credits)
        if not has_credits:
            if p.controller == "player" and not yearly:
                continue
            showcase = 0.5 * p.talent + 0.5 * p.presence + g.normal(0, 12)
            if g.random() > base * (0.4 + showcase / 80):
                continue
        b = p.bankability
        tier = 1 if b > 50 else 2 if b > 18 else 3
        if g.random() < 0.15:
            tier = min(3, tier + 1)
        pool = by_tier[tier]
        if not pool:
            continue
        ag = pool[int(g.integers(len(pool)))]
        if p.controller == "player":
            from ..systems import decisions as D
            if any(d.kind == "agency_offer" and d.status == "pending" for d in st.decisions.values()):
                continue
            D.create(st, cfg, "agency_offer", f"{ag.name} wants to represent you (standard 10% commission).",
                     ["accept", "decline"], deadline_days=14, default="decline", refs={"agency": ag.id})
            continue
        p.agent_id = ag.id


def default_orders() -> dict:
    return {
        "auto_accept_auditions": ["supporting", "colead", "lead"],
        "auto_decline_offers_below_quote_pct": 0,
        "auto_accept_jobs": True,
        "let_agent_negotiate": [],
        "interrupt_on": ["offers", "auditions_lead", "counter_offers", "romance", "premieres", "nominations"],
    }


def create_player(st: WorldState, cfg: dict, spec: dict) -> M.Person:
    """Create the protagonist. Background sets career position; hidden talent is
    drawn from the same distribution as any NPC with that background."""
    bg = spec.get("background", "unknown")
    archetype = {"unknown": "newcomer", "working": "working", "star": "star"}[bg]
    p = make_actor(st, cfg, "player", st.date, archetype=archetype, gender=spec.get("gender"),
                   birth=spec.get("birth"), name=spec.get("name"), tier="P")
    p.id = "player"
    p.controller = "player"
    if spec.get("goals"):
        tot = sum(spec["goals"].values())
        p.goals = {k: v / tot for k, v in spec["goals"].items()}
    if spec.get("traits"):
        p.traits = list(spec["traits"])
    if spec.get("bio"):
        p.bio = spec["bio"]
    if spec.get("attracted_to"):
        p.romance["attracted_to"] = list(spec["attracted_to"])
    p.partner_status = spec.get("partner_status")   # player chooses their own starting life
    if bg == "unknown":
        p.agent_id = None
        p.cash = float(spec.get("cash", 2500))
    if bg == "star":
        p.agent_id = "ag-caa"
    st.people[p.id] = p
    st.player_id = p.id
    if p.agent_id is None and bg != "unknown":
        p.controller = "npc"          # established backgrounds come with representation, by the NPC rule
        assign_agents(st, cfg)
        p.controller = "player"
    st.log("player_created", f"{p.name} begins their story in Hollywood.", actors=[p.id], salience=3,
           data={"background": bg})
    return p
