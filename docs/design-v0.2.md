> **Superseded by `DESIGN.md` v0.3.** Kept for its detailed process, data-model and formula descriptions, which v0.3 references. Where they conflict, v0.3 wins.

# Hollywood Simulator — Technical Design (v0.2, pre-code)

Scope of this document: architecture, data models, simulation processes, economic
formulas, calibration strategy and implementation phases for a persistent
1980–2026 entertainment-industry simulation, starting with film acting.

**Status legend** used throughout:
`[P1]`…`[P6]` = the phase in which a feature is planned. Nothing here is
implemented yet except the throwaway box-office sketch in
`prototypes/box_office_sketch.py` (see §6.7).

All historical figures quoted below are **approximate reference values to be
verified** during Phase 0 data collection. None is hard-coded as a target result.

---

## 1. Design principles → engineering rules

| Principle | Concrete engineering rule |
|---|---|
| Engine owns the truth | All numbers live in engine state. The narrator receives a read-only *fact packet* and can only submit *commands* that the engine validates. |
| No rubber-banding | **The player is an NPC with a human controller.** Player and NPC actors go through identical code paths; no function takes `is_player` as an input to an outcome calculation. A test enforces this (§7.4). |
| Causal randomness | Randomness only enters as *realised shocks on top of causes* (e.g. audience reception shock, audition-day variance). Every random draw is logged with its inputs. |
| History as prior, not script | Real history seeds initial state and future *intentions* (projects, attachments, debuts). Outcomes are always simulated. |
| Imperfect information | Every entity attribute has a hidden **true value** and zero or more **observations** with noise/bias. The UI and narrator only see observations. |
| No single star-power number | Actor value is a vector; film demand is the sum of many segment-level mechanisms. |
| Configurable | Every coefficient lives in versioned YAML config, by era where needed. Code contains structure, not magic numbers. |
| Reproducible | `state(t) = f(seed, initial_data, config_version, ordered_command_log)`. |

---

## 2. Architecture

```
hollywood-sim/
  engine/
    core/
      clock.py          # calendar, weekly tick, scheduled-event queue
      rng.py            # named deterministic RNG streams
      events.py         # immutable event log (audit trail)
      state.py          # WorldState container, entity registries, indexes
      commands.py       # command schema + validation (player & narrator input)
      ledger.py         # double-entry money accounting
      config.py         # YAML loading, era interpolation, config hashing
    models/             # dataclasses: Person, Project, Film, Studio, ...
    systems/            # one module per simulation process (§4)
      market.py  development.py  studio_ai.py  packaging.py  casting.py
      negotiation.py  production.py  post.py  release.py  box_office.py
      reception.py  ancillary.py  awards.py  careers.py  finance.py
      npc_ai.py  relationships.py  history.py  intel.py  news.py
    io/
      save.py           # snapshot + event log, schema-versioned
      factpacket.py     # player-visible state export for the AI narrator
  data/
    eras/               # year-indexed market tables (ticket price, admissions...)
    seed_1980/          # real people, studios, agencies, projects in pipeline
    history_intents/    # future historical projects/debuts as soft priors
    names/              # generators for fictional NPCs
  config/
    default.yaml        # all formula coefficients
  cli/                  # command-line front end
  api/                  # [P6] FastAPI wrapper over the same engine
  tools/
    batch.py            # run N seeds × M years headless
    calibrate.py        # compare simulated distributions vs reference data
    replay.py           # rebuild state from command log, verify hash
    inspect.py          # query hidden state / event provenance (debug only)
  tests/
```

### 2.1 Time model
- **Date resolution: one day. Simulation tick: one week** (Friday-to-Thursday, matching
  box-office reporting). Within a tick, systems run in a fixed order (§4.1).
- A **scheduled-event queue** (priority queue keyed by date + stable sequence id)
  carries things like "principal photography wraps", "offer expires", "Oscar
  nominations announced". Projects advance on their own timelines independent of turns.
- The player chooses how far to advance: `advance 1w`, `advance until <event>`,
  or `advance 3m` with *interrupts* (an offer arrives, an audition is scheduled, a
  decision is required) that pause time.

### 2.2 Determinism and RNG
- **Named streams:** each draw uses `rng(seed, system, entity_id, purpose, date)`
  (hash-derived, as in the prototype). Adding a new system or a new NPC does
  **not** shift any other random outcome, which keeps saves and A/B calibration stable.
- Iteration over entities is always in sorted-id order; no reliance on dict/set ordering.
- Floating-point: plain Python floats/numpy float64, no parallel reductions in the
  canonical path (batch tools may parallelise *across* seeds, never within one).

### 2.3 Persistence and auditability
- **Save = snapshot + event log + command log + config hash + data version.**
- Snapshot format: SQLite (one table per entity type + JSON columns for vectors).
  SQLite is chosen over JSON because a 46-year world will hold tens of thousands
  of films/people and we need queries (filmographies, weekly charts).
- **Event log:** append-only rows `{event_id, date, system, type, entity_ids,
  inputs_digest, random_draws, outputs}`. Any number shown to the player can be
  traced: `inspect why film:1043.domestic_gross` lists the contributing events.
- **Replay test:** load an older snapshot, re-apply the command log, and the final
  state hash must match the saved hash.

### 2.4 AI narrator boundary
```
 engine ──fact packet (JSON, player-visible only)──▶ LLM narrator
 engine ◀──command proposals (JSON schema)──────── LLM / player
```
- The fact packet contains only **observations** the player character could know
  (never hidden true values) plus canonical public facts (reported grosses, awards).
- Narration may invent colour (dialogue, settings, weather) but not quantities.
  `[P6]` A post-check extracts numbers and named outcomes from the narration and
  flags any that don't appear in the packet.
- Narrator-proposed actions ("call your agent and push for points") become
  commands and go through the same validation as CLI input.

---

## 3. Data models

Notation: `T` = hidden true value, `O` = observable estimate (see §3.9).
Scales are 0–100 unless noted; vectors are keyed dictionaries.

### 3.1 Person (shared base for actors, directors, writers, producers, executives)
```
Person
  id, name, birth_date, gender, nationality, is_historical, debut_date
  roles: set[{actor, director, writer, producer, executive, agent}]
  personality:       ambition, risk_tolerance, artistic_vs_commercial (−1..1),
                     loyalty, temperament, discipline, ego
  goals:             weighted {money, fame, prestige, artistic, stability, power}
  health/energy      (T) energy 0–100 (burnout from back-to-back shoots), health
  relationships      → RelationshipGraph edges
  finances           → Account
  calendar           list[Commitment] (shoots, press tours, holds, holidays)
  reputation_events  list[event_id] (professional incidents, praise)
```

### 3.2 ActorProfile (the multidimensional career, requirement 4)
| Field | T/O | Meaning |
|---|---|---|
| `talent` | T | Innate expressive ability. Mostly stable; no ceiling enforced. |
| `craft` | T | Learned technique; grows with work, training, strong directors; slow decay when idle. |
| `range` | T | vector over registers `{drama, comedy, action, romance, horror, period, musical, character}`: competence per register. |
| `presence` | T | Screen charisma; drives audience appeal more than critic response. |
| `look_market_value` | T | How the *market* currently values their appearance for leading roles; follows an age curve whose shape is configurable by era and gender (models real industry bias, not a judgement). |
| `fame` | T | vector per region `{US, EU, JP, LATAM, CN, ROW}`: share of the population who recognise them. |
| `appeal` | T | vector per audience segment: how much a recogniser wants to see them. |
| `loyalty` | T | per segment: fanbase that turns out regardless of reviews (front-loads openings). |
| `true_draw` | T | **Not stored.** Emerges from fame × appeal × loyalty in the demand model. |
| `bankability` | O | The **industry's belief** about draw: a Bayesian estimate from attributed track record. It can diverge from reality (overrated or underrated stars). |
| `critical_rep` | O-ish | Critics' running assessment (EWMA of reviewed performances). |
| `prestige` | O-ish | Industry standing: awards, prestige collaborators, guild respect. |
| `typecasting` | T | vector over persona/genre tags; high values raise fit for similar roles and lower casting odds against type (studios' perception). |
| `momentum` (heat) | O | Recency-weighted *surprise*: outcomes vs expectations. Beating expectations creates heat, not just success. |
| `quote` | O | Last fee: the anchor for negotiation. |
| `professionalism` | T | Reliability on set; leaks into the industry as rumours. |
| `scandal_risk` | T | Hazard of reputation events (**disabled by default for real living people**, §4.15). |

### 3.3 Director / Writer / Producer profiles
- **Director:** `vision, technical, actor_direction` (improves performances and
  craft growth), `budget_discipline`, `commercial_instinct`, `genre_skill` vector,
  `auteur_power` (final-cut leverage), `bankability`, `prestige`.
- **Writer:** `structure, dialogue, originality, genre_skill`; drafts carry quality.
- **Producer/Executive:** `taste` (accuracy of quality judgement), `risk_appetite`,
  `network`, `packaging_skill`.

### 3.4 Agency / Agent
```
Agency: id, tier (CAA-type to boutique), clients, packaging_power, info_quality
Agent:  person_id, agency_id, hustle, negotiation_skill, relationships,
        client_list (capacity), commission (10% default)
```
The agent's quality affects which offers reach the client, how accurate the
client's information is, and leverage in negotiation. NPC agents also drop
clients with low return on time.

### 3.5 Studio / Distributor
```
Studio: id, name, parent_company, cash, debt, credit_line, overhead_per_year,
        distribution_reach {region: 0..1}, marketing_efficiency,
        slate_strategy {tentpole_share, genre_weights, budget_bands},
        exec_regime (head of production person_id; tastes shift with changes),
        risk_appetite, library_value, relationships, output_deals
```
Studios can expand, shrink, fall into distress, be sold or merge. Historical
mergers are **pressures with probability**, not forced (§4.14).

### 3.6 Project (lifecycle state machine)
```
Project
  id, title, source {original, novel, remake, sequel, IP: franchise_id}
  genre (primary + secondary), rating_target, premise_hook (T)
  script: {draft_no, quality (T), structure, dialogue, originality, writers[]}
  stage: IDEA → DEVELOPMENT → PACKAGING → GREENLIT → PREPRO → SHOOTING
         → POST → AWAITING_RELEASE → RELEASED → (ANCILLARY windows)
         ↘ TURNAROUND / SHELVED / DEAD   (any stage)
  owner_studio, producers[], director, roles[], attachments[]
  budget: {planned, ATL, BTL, contingency, actual_to_date}
  schedule: {prepro_start, shoot_start, shoot_weeks, wrap, post_weeks, release_date}
  stage_history (audit), dev_hell_counter
Role
  id, project_id, name, importance {lead, co-lead, supporting, cameo}
  screen_time_share, age_range, gender, persona_tags, register_demands vector,
  star_requirement (from budget & studio), cast: person_id?, contract_id?
```

### 3.7 Contracts, offers, auditions
```
Offer:    role_id, to_person, from {studio, director}, type {direct, audition_invite,
          screen_test}, terms_proposed, expires, pay_or_play?, exclusivity_window
Audition: role_id, person_id, date, prep_days, result_score (T), feedback (O)
Contract: role_id, fixed_fee, pay_schedule, backend {type: gross|adjusted_gross|
          net|cash_breakeven, points, triggers}, bonuses {box_office, awards},
          billing, perks, options (sequel options with escalators), holds
```

### 3.8 Film (released) and box-office records
```
Film: project_id, release_plan {date, pattern: wide|platform|limited, screens_by_region},
      marketing {spend_by_week, creative_quality}, true_quality vector
      {craft, entertainment, emotional, originality, spectacle},
      critic_score, audience_score_by_segment, reception_shock (logged)
BoxOfficeWeek: film_id, region, week_no, date, screens, gross, admissions, rank
Revenue/CostLine: film_id, stream (theatrical_dom, intl, video, payTV, TV, SVOD...),
      amount, date, counterparty → posted to Ledger
```

### 3.9 Information layer
```
Observation: subject (entity.attr), observer (person/studio/"public"),
             value, uncertainty (σ), bias, source {tracking, trades, agent,
             rumour, test_screening, official}, date, decays_after
```
- `intel.py` generates observations each tick: trade-press projections, NRG-style
  tracking (awareness/interest with sampling noise), test-screening scores,
  agent gossip about competing actors and offers, salary rumours.
- **Who sees what:** the player sees `public` observations plus those of their
  own agent/manager (quality depends on agent `info_quality` and relationships).
- Studios make decisions on **their own observations**, never on true values.
  This is what produces believable misjudgements.

### 3.10 Relationships
Directed weighted edges: `affinity (−100..100), trust, respect, history[]`
(worked together, outcome, conflict, favour owed). Updated by shared projects
(good shoot or success → up; overruns, ego clashes or flops → down), negotiations
(hardball costs affinity), and introductions. Directors and producers re-hire
people they trust (a real and powerful career mechanism).

### 3.11 Money
Double-entry `Ledger` with `Account`s for every person, studio, agency and
the government (tax). Every transfer is a balanced entry, so total money is
conserved except for explicit sources/sinks (consumer spending in, taxes out,
which is what makes the conservation test possible).

### 3.12 Market state (per year/week)
```
MarketState: date, region tables {population_by_segment, admissions_trend,
             avg_ticket_price, screens_total, inflation_index},
             genre_appetite vector (evolving; see §4.2), tech_era flags
             {vhs, dvd, bluray, svod, pvod}, window_lengths, union_rates,
             disruptions {strike, pandemic} (structural history, §4.14)
```

---

## 4. Simulation processes

### 4.1 Weekly tick order
1. `market` — macro update, genre appetites drift, structural events.
2. `npc_ai` — goal re-evaluation (people & studios choose intentions).
3. `development` — scripts progress, rewrites, stalls, turnarounds.
4. `studio_ai` — greenlight committee, slate balancing, release dating.
5. `packaging` / `casting` — director attachment, casting calls, auditions, offers.
6. `negotiation` — open deals advance one round.
7. `production` — shoot days elapse; on-set events; overruns.
8. `post` — editing, VFX, test screenings, reshoots.
9. `release` — marketing spend, screen bookings, openings.
10. `box_office` — weekly demand for all films in release, all regions.
11. `reception` — reviews on release; audience scores; word of mouth.
12. `ancillary` — window revenues for older titles.
13. `awards` — season calendar (precursors → nominations → winners).
14. `finance` — payments, commissions, residuals, expenses, interest.
15. `careers` — stat updates from completed events.
16. `relationships`, `intel`, `news` — observations and headlines generated.

### 4.2 Market and genre cycles
Each segment's `genre_appetite[g]` follows a mean-reverting random walk **plus
endogenous feedback**: a run of hits in a genre raises appetite briefly, then
saturation lowers it (`appetite += α·recent_hit_signal − β·recent_supply`).
Studios chase the *observed* trend, which naturally produces cycles of boom and
glut (slasher boom, superhero era) without scripting them.

### 4.3 Development
- Ideas are spawned by writers, producers, studios, IP acquisitions and
  historical intents. Each has a hidden `premise_hook` and initial script quality.
- Per draft: `quality_new = quality + writer_skill_gain + N(0, σ_draft)`, with
  diminishing returns. Too many cooks (multiple rewriters) adds variance and a
  slight penalty to originality.
- **Development hell** hazard per week rises with time in development, key
  departures and exec-regime changes. Projects can go to turnaround and be picked
  up by another studio (with their prior attachments partially intact).

### 4.4 Studio greenlight (studio_ai)
A studio greenlights if its **own estimate** of risk-adjusted value clears a hurdle:
```
EV_studio = E_obs[ultimate_revenue] − budget − E[P&A] − overhead
Greenlight if  EV_studio / (budget + P&A) > hurdle(risk_appetite, cash_position)
           and  slate constraints (genre mix, release slots, capital) hold
```
`E_obs` comes from the studio's forecasting model, which uses *observed*
bankability, genre trend observations and comparable films, plus exec taste
noise. Good execs (high `taste`) have smaller error. This is where "nobody knows
anything" emerges.

### 4.5 Packaging and casting (requirement 2)
1. **Director attaches** first (usually): director's utility for the project vs
   studio's preference for the director.
2. **Role requirements** generate a candidate pool: everyone whose age, gender,
   persona and register match within tolerance, filtered by availability
   (calendar overlap → excluded or marked "would need to drop X").
3. **Shortlisting:** casting director scores candidates per decision-maker:
   - Studio utility: `w_b·bankability_obs + w_c·(−cost_obs) + w_r·(−risk) + w_t·trend`
   - Director utility: `w_f·fit + w_tal·perceived_talent + w_rel·affinity + w_v·vision_match`
   - The power balance between studio and director depends on the director's
     `auteur_power` and the budget (bigger budget → more studio control).
4. **Path by status:** top-bankability actors get *direct offers*. Mid-tier get
   *meetings / offers with conditions*. Others **audition**:
   ```
   audition_score = 0.45·talent + 0.25·craft + 0.20·range[reg] + 0.10·presence
                    + prep_bonus(prep_days) + fit_bonus(persona) + N(0, σ_day)
   ```
   `σ_day` is meaningful (an off day is real), but talent dominates over many auditions.
   Leads may require a **chemistry read / screen test** with the co-lead
   (pairwise chemistry is a hidden value drawn once per pair, which makes it persistent).
5. **Actor's decision** (players choose; NPCs evaluate the same utility):
   ```
   U_offer = g_money·log(fee/quote) + g_prestige·prestige_value(project)
           + g_fame·exposure(project) + g_art·perceived_script_quality
           + rel(director) − typecasting_risk − schedule_cost − energy_cost
   ```
   Perceived values come from the actor's/agent's observations, not truth.
6. Rejections cascade: if the first choice passes, the shortlist moves on; if the
   whole shortlist passes, the role's star requirement may be lowered or the
   project stalls.

### 4.6 Negotiation (requirement 8)
Alternating-offer bargaining over a bundle (fee, backend, billing, perks):
```
studio_max   = value_of_actor − value_of_next_best_alternative     (BATNA, studio view)
actor_min    = max(quote·(1 − flexibility(goals)), best_competing_offer_value)
leverage     = f(bankability_obs, heat, # competing interested parties,
                 agent.negotiation_skill, studio urgency (start date pressure))
deal_fee     = actor_min + leverage_share · (studio_max − actor_min)    if studio_max ≥ actor_min
```
- Each round has a breakdown hazard that grows with hardball moves and lowers
  affinity. Deals can die, and the role goes back to casting.
- **Backend:** points are traded against fixed fee. Gross points only become
  available above a bankability threshold (era-configurable). Net points are
  offered freely because their expected payout is low (§5.6).
- Contracts record **quote** updates. A fee becomes public through trade
  observations with noise, which feeds future anchors.

### 4.7 Calendar and scheduling (requirement 3)
- Shoot length ~ `f(budget, genre, VFX share, director discipline)`, roughly
  5–8 weeks for low budgets and 12–24 weeks for large ones, with a lognormal overrun.
- Post length ~ 16–52+ weeks depending on VFX. Release date is chosen by the
  studio among open slots (avoids competing tentpoles, chases seasons).
- Actors hold multiple commitments: press tours (around release), reshoots
  (unscheduled, can collide), holds and options. A **conflict resolver** applies
  contract priorities (pay-or-play, holds), so a slip on one film can cost an
  actor another role. That is emergent, not scripted.

### 4.8 Production quality
```
perf(actor, role) = talent^0.5 · craft^0.3 · range[reg]^0.2   (geometric, 0–100)
                    × fit(persona, role) × (1 + d·director.actor_direction)
                    × chemistry_factor × energy_factor + N(0, σ_perf)
film.true_quality vector:
  craft        = h(director.technical, BTL budget per minute, crew tier)
  entertainment= h(script.structure, genre delivery, pacing (editor), spectacle)
  emotional    = h(script.dialogue, lead perfs, ensemble)
  originality  = h(script.originality, director.vision, − interference)
  spectacle    = h(VFX budget, director.technical, era tech level)
```
On-set events (illness, conflict, weather, studio interference, script rewrites on
the fly) adjust components and the budget. Probabilities depend on the people
involved (temperament, discipline, relationships).

### 4.9 Reception
- **Critics:** `critic_score = Σ w_c·quality_components + prestige_halo + N(0, σ)`,
  weighted toward craft, originality and emotion. Each critic outlet is its own
  lightweight agent `[P3]`, and the aggregate is shown RT/Metacritic-style by era.
- **Audiences:** satisfaction per segment, weighted toward entertainment,
  spectacle, genre delivery and star appeal. Exit scores (CinemaScore-like) are observed.
- **Test screenings** (pre-release) give noisy satisfaction estimates and can
  trigger reshoots or a changed release plan.

### 4.10 Awards
Season calendar: festivals → critics' groups → guilds → nominations → ceremony.
Each voting body is a population of voters with preference weights (for example,
Academy: drama, transformation, period and "career narrative" captured by real
state such as prior nominations without wins). Inputs: performance quality,
film prestige, campaign spend (distributor decision), release timing (memory decay),
precursor wins (bandwagon). Nominees = top-k of simulated vote tallies with
voter noise. Awards feed prestige, quote and offers.

### 4.11 Career updates (requirements 4 & 9)
After each project or event:
- `craft += η · challenge(role) · director.actor_direction · (1 − craft/100)^γ`
  (asymptotic, but not capped, and challenge matters: easy roles teach little).
- `fame[region] ← 1 − (1 − fame)·(1 − reach_film[region] · screen_share · memorability)`;
  fame decays slowly without new exposure.
- `appeal[segment]` shifts with how satisfied that segment was **with them**
  (performance × presence), so stars can grow or alienate specific audiences.
- `bankability` = Bayesian update of the industry's draw estimate from openings,
  using the industry's **attribution heuristic** (over-credits leads, under-credits
  IP and marketing, a realistic bias that creates "overrated" stars).
- `heat ← λ·heat + (1−λ)·Σ surprise`, where surprise = outcome − prior expectation
  (box office, reviews, awards, viral moments).
- `typecasting[tags] += τ · screen_share · success_weight`. Playing against type
  lowers it slowly, and a hit against type lowers it fast (reinvention).
- **Ageing:** the role supply by age and gender comes from the script generator's
  historical demographics (configurable). Talent is stable, craft can still grow,
  and `look_market_value` follows the era's curve. Older stars shift to character work,
  prestige or directing naturally because that is where their utility moves.
- **Transitions `[P5]`:** directing or producing ambitions emerge from goals plus
  prestige and network; a first directing gig is a project like any other, with
  the actor's director stats seeded from experience.

### 4.12 NPC decision-making
All NPCs (people and studios) are **utility-maximising agents with bounded
rationality**: they evaluate options with the same functions as the player, using
their own observations, with softmax choice noise (`temperature` per personality).
NPC actors pursue goals (an ambitious money-seeker takes the sequel; an artist
takes the indie). This gives the world its own stories: an NPC star can break
out, burn out or reinvent themselves without the player.

### 4.13 Player actions (CLI verbs, vertical slice)
`status`, `calendar`, `offers`, `audition <role>`, `prep <days>`,
`accept/decline/counter <offer>`, `take-class`, `network <person>`,
`ask-agent <question>`, `switch-agent`, `pitch` `[P5]`, `spend <lifestyle>`,
`invest`, `advance <period|until event>`, `news`, `trades`, `boxoffice`,
`history <entity>`, `save/load`.

### 4.14 Historical realism with divergence (requirement 6)
Three layers:
1. **Initial state (Jan 1980):** real studios, agencies, actors, directors and
   projects in development, with estimated attributes (curated data, §6.4).
2. **Structural history (default ON, toggleable):** technology and macro conditions
   arrive on schedule, such as VHS growth, multiplex expansion, DVD (1997), the China
   market opening, streaming (2007 onward, original films ~2015 onward), the 1988/2007/2023
   strikes and the 2020 pandemic. These are environmental, not outcomes for specific films.
3. **Contingent history = soft intents:** a historical film becomes a *project seed*
   that appears around its real development date, with its real creative team as
   **high-prior attachments**. Whether it gets made, who stars, how good it is and
   how it does are all simulated. If the historical star is busy, the role is recast.
   Real future actors enter via a **debut pipeline** around their real debut age,
   with estimated talent profiles, but their careers are simulated from there.
   Mergers and acquisitions are probabilistic pressures conditioned on studios' simulated
   finances (a studio that's thriving in-sim is less likely to be sold).

**Divergence persists:** once the sim deviates (Film X flops), downstream intents
read the simulated state. Sequels to flops lose their seed probability, and an actor
who already broke out gets the roles their heat earns, not their historical ones.
A `divergence report` shows how far the world has drifted.

### 4.15 Real-person content policy (config)
Scandal, health and personal-life events are **disabled for real living people by
default** (they apply to fictional NPCs). Professional outcomes such as box office,
castings and awards are simulated for everyone.

---

## 5. Economic formulas

### 5.1 Demand model: audience compartments (prototype exists)
For each film, region `r` and audience segment `s` (for example youth/adult × male/female,
family; `[P3]` adds more), people move between states:
```
Unaware ──marketing, star fame, IP, WOM──▶ Aware ──appeal──▶ Interested ──▶ Watched
                                             │                   │
                                             └─ not interested    └─ lapse ("wait for video")
```
Weekly flows:
```
aware_from_marketing = 1 − exp(−k_mkt,era · effective_spend)    # diminishing returns
baseline_aware       = 1 − (1−mkt)(1 − a_f·fame_lead)(1 − a_ip·IP_familiarity)
appeal_s             = genre_appetite_s · premise_hook · star_appeal_s · trailer_quality
                       · rating_access_s · critic_effect_s · exp(reception_shock)
watch_rate_s,t       = base_rate · urgency_t · seasonality_t · screen_availability_t
                       / competition_t                        # other films' interest
lapse_t              = base_lapse · window_pressure_era       # shorter windows → more waiting
WOM: new viewers × contacts × P(unaware) → aware, with appeal × (0.3 + 1.6·satisfaction_s)
```
- **Competition** is endogenous: films in release split a weekly moviegoing budget
  per segment (`[P1]` scalar; `[P3]` full shared-pool model across all films).
- **Screens:** the distributor books an opening count from tracking. Exhibitors
  drop screens when per-screen gross falls below a threshold (era-dependent).
- **Platform releases** start with few screens in big cities and expand if per-screen
  averages are high, which is how sleepers and awards films emerge.
- **Opening weekend** = week-1 gross × weekend share (era: about 0.6–0.7).

### 5.2 International `[P1 simplified, P3 full]`
Each region runs its own compartment model with regional fame, genre appetite,
release delay, and distribution reach. Era tables move the international share from
roughly 35–45% of worldwide gross for typical 1980s films to roughly 55–70% for 2010s
blockbusters (verify).

### 5.3 Distributor rentals
```
domestic_rentals = Σ_weeks gross_w · rental_share_w   (sliding scale, ~55% → 35%)
intl_rentals     = Σ gross · intl_share_r             (~40%; China ~25% from 2012)
```

### 5.4 Ancillary windows (era-driven)
```
ancillary_stream_i = demand_index · coefficient_i,era · genre_multiplier_i + floor_i
demand_index       = f(theatrical admissions, star fame, quality, IP)
```
Streams: home video (VHS rental pricing 1980s → sell-through → DVD boom about
1999–2007 → decline), pay-TV, network/syndication, SVOD licensing (2008+),
PVOD (2020+), library value over decades. Coefficients come from era tables. Each
stream pays out over time (dated ledger entries), not as a lump sum.
Direct-to-streaming films `[P5]` use a cost-plus buyout model instead of box office.

### 5.5 Costs and the studio P&L
```
negative_cost = ATL (talent fees) + BTL (shoot weeks × crew/day rate × era index)
                + VFX + contingency + overruns
P&A           = studio decision (planned by tracking; typical wide release
                ≈ 50–100% of negative cost; verify by era)
studio_profit = rentals + ancillary − negative_cost − P&A − overhead (≈10–15%)
                − interest − participations (gross/adjusted gross points)
```

### 5.6 Participations and "Hollywood accounting"
Two ledgers per film:
- **Economic P&L** (above): what the studio really made.
- **Participation statement:** used to compute **net points**:
  `net_receipts = rentals − distribution_fee (30–40% of rentals) − distribution
   expenses − negative_cost − interest − overhead − gross participations`.
  This rarely goes positive, matching reality, so a player who takes net points on a
  modest hit gets nothing, while gross points on the same film pay well.
- Cash-breakeven and box-office bonuses are triggers on the economic ledger.

### 5.7 Salaries
```
base_scale(year, budget_tier)   — era table (SAG minimums → star fees)
fee_target = base_scale · (bankability_obs/50)^β · heat_mult · prestige_mult
             · scarcity(available alternatives) · agent_mult
```
`fee_target` enters negotiation (§4.6) as the actor side's anchor alongside the
quote. Reference calibration: SAG scale (verify per year), the star-fee club
thresholds by era (roughly $1M in the late 1970s, $10M+ for a few stars by about 1990,
the $20M club by the late 1990s, and the 2010s shift toward backend and then
streaming buyouts; verify).

### 5.8 Personal finance
```
gross_income → agent 10% → manager 10–15% (optional) → lawyer ~5%
             → business manager ~5% (optional) → publicist (retainer)
             → union dues → taxes (era-specific effective rates, config)
residuals (TV/video/streaming, SAG-style formulas, paid quarterly)
expenses: lifestyle tier (choice; lifestyle creep raises fixed costs),
          housing, staff, training
investments: simple asset classes with era returns (index proxy), real estate `[P4]`
```
An actor can go broke, live on residuals, or build capital for a production company `[P5]`.

---

## 6. Calibration strategy

### 6.1 What "realistic" means here
We calibrate **distributions and relationships**, never individual films:
- Annual distribution of domestic grosses (heavy-tailed; top-10 share)
- Count of $100M+ (inflation-adjusted) releases per year by era
- Opening-to-total multiplier distribution by era (1980s legs longer than 2010s)
- Budget vs gross, profitability rate, and the share of wide releases losing money
- International share by era and genre
- Star salary distribution by year; how many actors are above $X
- Career dynamics: second-role rate after debut, years to breakout, length of
  leading-man/woman careers, rate of comebacks after slumps, Oscar-nomination age
- Studio-level annual market share volatility

### 6.2 Reference data (to collect in Phase 0)
Box Office Mojo / The Numbers (yearly charts, weekly runs, budgets where known),
MPA THEME reports (admissions, screens), National Association of Theatre Owners
(average ticket prices), Academy Awards database, union rate tables, and published
studio financials. Stored as CSV in `data/reference/` with source notes.

### 6.3 Methods
1. **Batch runs:** `tools/batch.py --seeds 200 --years 1980-1990` produces summary
   statistics per run.
2. **Loss function:** quantile errors and KS distance between simulated and
   reference distributions, weighted per target.
3. **Parameter search:** coordinate search first, then Bayesian optimisation
   (Optuna) over config parameters, with held-out years (fit 1980–1995, validate
   1996–2005) to avoid overfitting.
4. **Historical coverage test:** seed real films with historical inputs (budget, cast,
   release date, estimated quality) and simulate each 500 times. If calibrated, the
   real gross should fall inside the simulated 10–90% band about 80% of the time. Too
   often means the model is too wide; too rarely means it's overconfident.
5. **Sensitivity analysis:** vary each parameter ±20% and rank outcome sensitivity.
   High-sensitivity parameters get the most data attention.
6. **Emergence checks:** count sleeper hits, flop-driven studio crises, breakouts
   from nobodies, long dominant careers, and career collapses per simulated decade.
   Each should occur at roughly historical frequencies, with none forced.

### 6.4 Seed-data estimation for real people
Attributes for real 1980 people are estimated from track records (box office,
awards, critical reception, years working) via a documented rubric, then stored with
an `estimation_confidence`. Unknowns get wide priors. Curating this dataset is the
largest non-code effort; the vertical slice uses ~60 real people plus generated NPCs.

### 6.5 Known gaps found by the prototype
The box-office sketch (§6.7) produces plausible medians, but its upside tail is
too thin (sleeper p90 domestic ≈ $29M with no true breakouts). Planned fixes:
fat-tailed reception shocks (Student-t), WOM feeding the *appeal* of the unconvinced
(cultural-moment effects), platform expansion, and second-week reviews-driven boosts.

### 6.6 Tests
- **Unit:** each formula with fixed inputs.
- **Property:** money conservation, no negative stocks, no person in two overlapping
  shoots, all stage transitions valid, all random draws logged.
- **Determinism:** same seed + commands → identical state hash. Replay equals snapshot.
- **Fairness:** run the same scenario with the player's actor replaced by an
  identical NPC, then compare outcome distributions (they must match statistically).
- **Regression:** golden-seed snapshots for key metrics; config changes show diffs.

### 6.7 Prototype result (uncalibrated placeholder parameters, 1984)
`python3 prototypes/box_office_sketch.py` → 2000 seeds each:

| Film | Budget + P&A | Opening wknd p10/p50/p90 | Domestic p50 | Multiplier p50 | P(profit) |
|---|---|---|---|---|---|
| Sleeper comedy (quality 74, low fame) | $11M + $7M | $3.7 / $5.0 / $6.7M | $21M | 4.3× | 0.91 |
| Hyped action (quality 44, big star) | $32M + $18M | $7.1 / $9.5 / $12.9M | $31M | 3.3× | 0.10 |

The causal story emerges without being scripted: marketing and star fame buy the
opening, quality buys the legs, and both outcomes stay uncertain. (The first
parameter guess produced a $38M 1984 opening, above the real record of that
era, which is exactly the kind of error calibration catches.)

---

## 7. Implementation phases

Each phase ends with a playable build, passing tests, and an updated
"implemented vs planned" table.

**Phase 0: Foundations (no gameplay)**
Repo skeleton, models, RNG streams, clock and event queue, event log, ledger,
config loader with hashing, SQLite save/load, replay tool, test harness.
Start collecting reference data for 1980–1990.
*Done when:* a world with dummy entities advances 520 weeks deterministically,
and save → load → replay hashes match.

**Phase 1: Vertical slice (1980–1990, domestic + one international bucket)**
- ~60 real people + ~400 generated actors, ~60 directors, 8 studios, 4 agencies
- Development (simplified), studio greenlight with observed-value forecasts
- Casting: direct offers, auditions, availability conflicts, rejections
- Negotiation: fee + quote + simple gross/net points
- Production and post with durations and overruns; film quality vector
- Reception (critic score + segment satisfaction)
- Compartment box office with competition scalar, screens, weekly charts
- Simplified ancillary coefficients and studio P&L; participations
- Career updates (craft, fame, appeal, bankability, heat, typecasting)
- Personal finance with commissions and lifestyle expenses
- Information layer v1 (trades, tracking, agent intel)
- CLI with the verbs in §4.13; fact-packet export for narration
- Calibration v1 on 1980s gross distributions and multipliers
*Done when:* you can play a decade from unknown to (possibly) star while NPC
careers evolve, and batch stats are within agreed tolerances.

**Phase 2: Living industry**
NPC goals and decision depth, relationship graph effects on hiring, agencies and
agents (switching, packaging), holds and options, development hell and turnaround,
studio finances (distress, executive regime changes), news generation.

**Phase 3: Full economics and awards**
Multi-region international markets, shared competition pool across films,
platform releases, era-accurate ancillary waterfall, residuals, awards season with
voting bodies and campaigns, critic outlets.

**Phase 4: Historical expansion 1990–2026**
Seed data for later decades (via intents and debut pipeline), structural events
(DVD, China, streaming, strikes, pandemic), franchise/IP system, divergence report,
calibration across all eras with held-out validation.

**Phase 5: Career breadth**
Television (series regular, guest, pilots), streaming originals and buyouts,
theatre, endorsements, producing, directing, production companies.

**Phase 6: Web app and narrator integration**
FastAPI over the same engine, web front end (dashboards, calendar, trades page),
LLM narrator with fact packets, command proposals and a number-consistency checker.

---

## 8. Decisions needed before Phase 0 code

1. **Player start:** new unknown actor in Jan 1980 (recommended for the slice), or choose any year/archetype?
2. **Real people scope in slice:** ~60 real 1980 names plus generated NPCs, OK?
3. **Tick:** weekly simulation with daily dates (recommended), OK?
4. **Real-person events policy (§4.15):** keep the default (no scandals/health events for real living people)?
5. **Data help:** will you help curate/review the seed-attribute estimates for real people, or should I draft them for your review?
6. **Calibration tolerance:** how close is "close enough" for slice sign-off (e.g. simulated yearly-gross quantiles within ±25% of 1980s reference)?
