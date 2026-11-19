"""Data models.

Conventions
- All registries in WorldState are flat {id: object}; objects reference each
  other by id. This keeps serialisation trivial (cls(**dict)) and saves stable.
- Fields documented as HIDDEN are true values that must never reach the player
  or the narrator directly. Observable estimates live in separate fields
  (e.g. `bankability` is the industry's belief; true draw is emergent).
- Scales are 0-100 unless noted; fame/appeal are 0-1 shares.
"""
from __future__ import annotations

from dataclasses import dataclass, field

REGISTERS = ["drama", "comedy", "action", "romance", "thriller", "horror", "family", "scifi"]
GENRES = REGISTERS  # genre and register share a vocabulary in the slice


@dataclass
class Person:
    id: str
    name: str
    gender: str                      # "m" | "f" | "x"
    birth: str                       # ISO date
    roles: list                      # ["actor", "director", ...]
    tier: str = "B"                  # A | B | C | G(enerated)
    historical: bool = False
    controller: str = "npc"          # "npc" | "player"
    death: str | None = None         # simulated death date (if dead)
    active: bool = True
    debut: str | None = None

    # --- acting (HIDDEN true values) ---
    talent: float = 50.0
    craft: float = 30.0
    presence: float = 50.0
    range: dict = field(default_factory=dict)        # register -> 0..100
    # --- public career state (observable or semi-observable) ---
    fame: float = 0.0                # share of US public who recognise them (true)
    appeal: float = 0.5              # how much recognisers want to see them (true)
    bankability: float = 10.0        # industry belief about draw, 0..100 (observed)
    critical_rep: float = 40.0       # critics' running assessment (observed)
    prestige: float = 10.0           # industry standing (observed)
    heat: float = 0.0                # momentum, -100..100 (observed)
    quote: float = 0.0               # last fee in nominal dollars (observed)
    typecast: dict = field(default_factory=dict)     # genre -> weight
    # --- director skills (HIDDEN) ---
    direction: dict = field(default_factory=dict)    # vision, technical, actor_direction, discipline, commercial
    # --- personality (HIDDEN, but narrator gets qualitative traits) ---
    personality: dict = field(default_factory=dict)  # temperament, ambition, warmth, ego, discipline, risk, openness
    goals: dict = field(default_factory=dict)        # money, fame, prestige, art, stability
    traits: list = field(default_factory=list)       # short narrative descriptors
    bio: str = ""
    romance: dict = field(default_factory=dict)      # attracted_to: [genders], openness: 0..1
    partner_id: str | None = None
    partner_status: str | None = None                # dating | married
    # --- logistics ---
    agent_id: str | None = None
    cash: float = 0.0
    monthly_costs: float = 0.0
    energy: float = 80.0
    calendar: list = field(default_factory=list)     # [{project_id, start, end, kind}]
    credits: list = field(default_factory=list)      # [{project_id, title, role, billing, year, kind}]
    awards: list = field(default_factory=list)       # [{year, award, category, result, project_id}]
    last_work: str | None = None
    provenance: dict = field(default_factory=dict)   # {source, ids, confidence}
    persona: dict = field(default_factory=dict)      # background, hometown, signature, style
    employer: str | None = None                      # agency / studio id for agents, casting directors
    agent_person_id: str | None = None               # the named agent who represents this actor
    track: dict = field(default_factory=dict)        # register -> [auditions, near the top]: what agents learn


@dataclass
class Show:
    """A (fictional) television series: a workplace with recurring people."""
    id: str
    title: str
    network: str
    genre: str
    format: str
    premise: str
    regulars: list = field(default_factory=list)
    producer_id: str | None = None
    director_ids: list = field(default_factory=list)
    started: int = 1979
    active: bool = True


@dataclass
class Studio:
    id: str
    name: str
    tier: str                         # major | mini
    cash: float
    slate_per_year: float
    budget_median: float              # $M in start-year dollars
    risk_appetite: float = 50.0
    marketing_eff: float = 1.0
    genre_weights: dict = field(default_factory=dict)
    exec_taste: float = 50.0          # HIDDEN: accuracy of quality judgement
    historical: bool = False
    provenance: dict = field(default_factory=dict)


@dataclass
class Agency:
    id: str
    name: str
    tier: int                         # 1 (top) .. 3 (boutique)
    hustle: float = 50.0
    negotiation: float = 50.0
    info_quality: float = 50.0


@dataclass
class Role:
    id: str
    project_id: str
    name: str
    importance: str                   # lead | colead | supporting
    gender: str
    age_min: int
    age_max: int
    register: str
    screen_share: float
    description: str = ""
    cast_id: str | None = None
    status: str = "open"              # open | auditioning | offered | cast
    fee: float = 0.0
    points: float = 0.0
    points_type: str | None = None    # gross | net
    tried: list = field(default_factory=list)        # person ids who passed/lost
    shortlist: list = field(default_factory=list)
    audition_date: str | None = None
    auditioners: list = field(default_factory=list)
    performance: float | None = None  # HIDDEN until reviews
    intended: str | None = None       # historical attachment (a prior, not a guarantee)
    name_documented: bool = False     # character name from records (else generated)


@dataclass
class Project:
    id: str
    title: str
    genre: str
    studio_id: str
    premise: str
    budget: float                     # nominal dollars (negative cost plan)
    stage: str = "development"        # development|prepro|shooting|post|awaiting_release|released|dead
    created: str = ""
    director_id: str | None = None
    role_ids: list = field(default_factory=list)
    script_quality: float = 50.0      # HIDDEN
    hook: float = 50.0                # HIDDEN premise marketability
    breadth: float = 0.07             # HIDDEN base audience appeal
    segment_tilt: dict = field(default_factory=dict) # HIDDEN
    prepro_start: str | None = None
    shoot_start: str | None = None
    shoot_weeks: int = 8
    shoot_end: str | None = None
    post_weeks: int = 24
    release_date: str | None = None
    pa_budget: float = 0.0
    actual_cost: float = 0.0
    quality: dict = field(default_factory=dict)      # HIDDEN components after wrap
    critic_score: float | None = None
    audience_grade: str | None = None
    satisfaction: float | None = None                # HIDDEN
    reception_shock: float | None = None             # logged draw
    forecast_opening: float | None = None            # studio tracking estimate (observed)
    run: dict = field(default_factory=dict)          # live box-office compartments
    weekly: list = field(default_factory=list)       # [{week, date, gross, screens, rank}]
    domestic: float = 0.0
    opening: float = 0.0
    intl: float = 0.0
    revenue: dict = field(default_factory=dict)
    profit: float | None = None
    location: str = "Los Angeles"
    historical_ref: str | None = None
    delays: int = 0
    distributor_note: str | None = None   # documented distributor label (historical films)
    date_approx: bool = False             # release date known only to month/year
    tone: str = ""                        # creative identity (e.g. "gritty", "glossy")
    logline_extra: str = ""               # selling point / context for the narrator
    casting_director_id: str | None = None


@dataclass
class Offer:
    id: str
    role_id: str
    project_id: str
    person_id: str
    fee: float
    points: float
    points_type: str | None
    made: str
    deadline: str
    status: str = "open"              # open | accepted | declined | countered | withdrawn | expired
    round: int = 1
    studio_max: float = 0.0           # HIDDEN walk-away fee


@dataclass
class Decision:
    """Something the player must decide. Time stops on interrupting decisions."""
    id: str
    kind: str                         # offer | audition | counter | romance
    summary: str
    options: list
    deadline: str
    default: str
    refs: dict = field(default_factory=dict)
    created: str = ""
    status: str = "pending"           # pending | resolved | expired
    interrupt: bool = True
    resolution: dict = field(default_factory=dict)


@dataclass
class Relationship:
    """Undirected bond between two people (a < b by id) plus directed attraction."""
    a: str
    b: str
    affinity: float = 0.0             # -100..100
    trust: float = 0.0
    attraction_ab: float = 0.0        # HIDDEN 0..1
    attraction_ba: float = 0.0        # HIDDEN 0..1
    status: str = "acquainted"        # acquainted | friends | rivals | feud | dating | married | divorced | ex
    since: str = ""
    history: list = field(default_factory=list)      # [{date, text, delta}]
    contact_weeks: int = 0
    attraction_set: bool = False


@dataclass
class HistoricalEvent:
    """A documented real-world event about real people, with causal dependency."""
    id: str
    people: list
    type: str                         # marriage | divorce | death | ...
    date: str
    summary: str
    verification: str = "documented"  # documented | disputed | rumour
    sources: list = field(default_factory=list)
    dependency: dict = field(default_factory=dict)   # {kind, requires}
    status: str = "scheduled"         # scheduled | occurred | voided
    resolution: str = ""
