# Hollywood Simulator: Technical Design (v0.3, pre-code)

A persistent, historically grounded entertainment-industry simulation (1980–2026),
starting with film acting careers. A Python engine owns all state, numbers and
outcomes. ChatGPT (or any LLM) is the narrator: it turns engine outcomes into
scenes and can *propose* consequential developments, which the engine adjudicates.

**Status legend:** `[S]` = in the first playable vertical slice. `[P2]`…`[P6]` =
later phases (§11). **Nothing in this document is implemented yet** except two
throwaway prototypes in `prototypes/` (§7.6).

All historical figures quoted are approximate reference values to be verified
during data collection. None is used as a target outcome or ceiling.

### What changed from v0.2
- Start year is a **parameter**. Any year with data can be loaded as a historical
  snapshot without simulating earlier decades (§4).
- Population comes from a tiered, **automatically built historical database** plus
  generated professionals, with no hand-managed careers (§3).
- Real personal-life history is **included** with provenance and causal
  dependencies, replacing the v0.2 blanket exclusion (§3.6).
- Time advancement is **interruptible**, with delegation of routine matters (§6.2).
- The upper box-office tail is modelled through audience behaviour and physical
  capacity, with no historical ceilings and no jackpot rolls (§7).
- **Narrator integration is part of the first playable slice**, not Phase 6 (§8).

---

## 1. Principles → engineering rules

| Principle | Rule |
|---|---|
| Engine owns canon | All quantities and consequential outcomes are engine state. The narrator receives packets and returns *choices* and *proposals*; nothing it writes changes state without adjudication. |
| One rulebook | **The player is an NPC with a human controller.** No outcome function takes "is player" as an input. Undecided player choices are made by the player character's own NPC utility, using their stated goals. |
| Causal randomness | Random draws only perturb causes (reception, audition-day form), drawn from the same distributions for everyone, and every draw is logged with its inputs. |
| History is the starting point, not a script | Real history supplies initial state, baseline future intentions and documented events. Outcomes are simulated, and documented events re-check their causal preconditions (§3.6). |
| No ceilings | The only hard limits are physical and economic: population, seats, screens, time, money. No historical record is referenced by any outcome formula. |
| Imperfect information | Hidden *true* values vs *observed* estimates. Players, studios and the narrator see observations only. |
| Provenance | Every fact about a real person carries a source and a verification status. Rumours stay labelled as rumours, and **no damaging allegation about a real person is ever generated**. |
| Configurable and reproducible | Coefficients live in versioned YAML. `state = f(seed, data_version, config_version, command_log)`. |

---

## 2. Architecture

```
hollywood-box-office/
  engine/
    core/        clock.py rng.py events.py state.py ledger.py config.py commands.py
    models/      person.py project.py film.py studio.py agency.py market.py history.py
    systems/     market development studio_ai packaging casting negotiation
                 production post release box_office reception ancillary awards
                 careers finance relationships personal_life npc_ai intel news
    service.py   ← the ONLY entry point for front ends (JSON in/JSON out)
    narrator/    packet.py  response_parser.py  adjudicator.py  continuity.py
    io/          save.py (SQLite) snapshot.py
  datapipe/      # build-time only; turns public sources into a historical DB
    fetch_wikidata.py  fetch_imdb.py  normalize.py  estimate.py  compile_snapshot.py
  data/
    history/     # built historical DB (see §3.4 on what may be committed)
    overrides/   # human/LLM corrections with provenance (YAML)
    eras/        # year-indexed market tables
    reference/   # calibration statistics (CSV + source notes)
  config/        default.yaml
  cli/           hsim (command line front end)
  tools/         batch.py calibrate.py replay.py inspect.py
  tests/
```

**Service layer.** Every front end (the CLI, the file-based ChatGPT workflow and,
later, an MCP server or web app) calls the same `service.py` functions with JSON:
`new_game`, `load`, `advance`, `decide`, `submit_response`, `packet`, `rewind`,
`query`. That is what keeps the CLI and file workflow in the slice from becoming
throwaway code.

**Time:** dates have day resolution, and the world simulates in weekly ticks
(Friday to Thursday, matching box-office weeks). A scheduled-event queue handles
mid-week items (offer deadlines, start dates).

**Determinism:** every draw comes from a named stream,
`rng(seed, system, entity_id, purpose, date)`, as in the prototypes. Adding
systems, people or data never reshuffles other draws. Entities are always
iterated in sorted-id order.

**Saves:** a SQLite snapshot, plus append-only event and command logs, plus the data
and config versions. A replay must reproduce the snapshot's state hash. `[S]`
**Branches:** `rewind` to any earlier packet creates a branch save, so a bad
narrator session is recoverable.

---

## 3. Historical database and population (answers Q1, Q4, Q5)

### 3.1 Sources investigated

| Source | Gives us | Licence / access | Role |
|---|---|---|---|
| **Wikidata** (SPARQL / dumps) | People, birth/death dates, citizenship, occupations, spouses with start/end dates, awards with dates, film cast/director/producer, release dates, some budgets/grosses, studio ownership | **CC0**: free to store, commit and redistribute | **Primary backbone** `[S]` |
| **IMDb non-commercial datasets** (`name.basics`, `title.basics`, `title.principals`, `title.ratings`) | Near-complete credits with **billing order**, professions, ratings and vote counts | Personal, non-commercial use only. **Must not be republished or used to build a redistributable database.** | Optional *local* enrichment, never committed `[S]` |
| **Wikipedia** | Biographies, career narratives, documented personal events, yearly box-office lists | CC BY-SA (attribution, share-alike) | Build-time extraction of events and personality descriptors for major figures `[P2]` |
| **TMDB API** | Cast/crew, popularity, budgets/revenues (community-maintained) | Free API key, attribution, non-commercial | Optional cross-check `[P2]` |
| Box Office Mojo / The Numbers | Weekly and yearly grosses | No open licence; no bulk scraping | Manual spot-checks only; calibration uses aggregate statistics |
| Annual exhibitor-poll lists of top box-office stars, Academy database, MPA/NATO statistics | Bankability rankings by year, nominations, admissions, ticket prices | Facts are reusable; record sources | **Anchors** for validating the estimator `[S]` |

**Your repository is public**, so anything derived from IMDb must stay local
(gitignored) and be rebuilt on your machine by the pipeline. Everything committed
is built from CC0/attributed sources.

**Network note:** this cloud session currently blocks `query.wikidata.org`,
`datasets.imdbws.com` and `api.themoviedb.org`. When we build the pipeline, I'll ask
for those hosts to be allowed (or you can run the pipeline locally).

### 3.2 Tiers and realistic population size

People are tiered by **detail and simulation cost**, not by importance to the story.
Any tier can be promoted when they become relevant.

| Tier | Who | Data held | Per snapshot (est.) | Slice target |
|---|---|---|---|---|
| **A: rich** | Stars, top directors, studio heads, top agents, anyone with notable billing in recent big releases | Full attribute vector, personality, relationships, documented personal history, finances | ~300–600 | ~200 |
| **B: working** | Credited professionals active in the last ~5 years with significant roles | Full professional attributes, estimated personality priors, light personal history | ~4,000–8,000 | ~2,000 |
| **C: dormant** | Everyone else in the historical DB (minor credits, inactive, future debutants) | Name, dates, filmography; attributes computed **on demand** | tens of thousands | all available |
| **G: generated** | Fictional professionals filling gaps (unknowns, generic supporting actors, crew-level directors) | Same model as B | Tops up each role pool to realistic size | ~1,000 |

**Why these numbers:** a 1980s year had a few hundred US releases with perhaps
10–15 meaningful credited roles each, so a few thousand significant acting roles
per year spread over a few thousand working actors, plus a few hundred active
directors. Tier B covers the people who actually compete for roles. Generated
people mostly fill the "unknown newcomer" and "jobbing supporting actor" pools,
which the historical record covers thinly.

**Lazy promotion:** when a Tier C person enters a candidate pool (for example,
the casting filter needs a 25-year-old comedic actor), their attributes are
computed by the same estimator (§3.5) **using only information up to the current
simulation date**. They are seeded by person id, so the result is deterministic.

**Performance budget:** the slice should simulate one world-year in under ~2
seconds with ~3,000 active people and ~300 projects, so batch calibration of
hundreds of seeds is practical. Casting uses indexed pre-filters (age, gender,
register, availability), not full scans.

### 3.3 Identity and continuity
- Canonical ids: `wd:Q…` (Wikidata) for real people, films and studios; IMDb `nm…`
  ids kept as local cross-references; generated people use `gen:<hash>`.
- Every save records the **data-pack version** it was built from.
- **Adding real people to an existing save** (for example, after a data expansion):
  - If their real debut is after the current simulation date, they join the
    debut pipeline normally.
  - If their debut is earlier, they are inserted with estimator-derived
    attributes. Only their credits on films that **also exist in this simulated
    world** count, and missing credits become "earlier uncatalogued work", which
    lowers their fame accordingly. They never retroactively change past events.
    An event records the registration.
- Removing or renaming people never happens in-save. Corrections apply through
  overrides on the next new game, or through an explicit migration.

### 3.4 Pipeline (build-time, automated) `[S]`
1. **Fetch:** run Wikidata queries per decade (people with acting/directing/
   producing occupations linked to US-distributed films, studios, awards, spouses,
   deaths). Optionally join the local IMDb files for billing order and full credits.
2. **Normalise:** merge ids, resolve duplicates, derive each person's credits
   timeline with billing, the film's release date and the film's known gross.
3. **Estimate:** compute attributes for any requested date (§3.5).
4. **Validate:** compare against anchor lists (yearly top box-office stars,
   nominations, reported salaries) and produce an **anomaly report** (the top N
   biggest disagreements), not a review queue.
5. **Compile snapshots:** see §4.

Nobody hand-maintains careers. After the start date, every career is produced by
the engine.

### 3.5 Systematic estimation of starting attributes (answers Q5)
**Rule: public and observable attributes use only information dated on or before
the start date. Hidden innate traits may use the whole real career (hindsight), with
shrinkage.**

This is what makes the historical world behave plausibly while still diverging.
A 1980 unknown who later became a great actor starts unknown, but with high hidden
talent. Whether that potential is realised depends on simulated opportunities.
`hindsight_weight` is configurable (default 0.5; 0 means "everyone is judged only
by what was known").

| Attribute | Evidence (only up to the start date, except where marked H) |
|---|---|
| `fame[region]` | Σ credits × film admissions × billing weight × recency decay; TV-series regular exposure |
| `bankability` (industry belief) | Openings/grosses of films they headlined vs comparable films; anchor-list rank (yearly top-star polls) |
| `critical_rep` | Ratings/critic reception of their films weighted by role size; critics' awards |
| `prestige` | Major nominations/wins (time-decayed); prestige collaborators |
| `heat` (momentum) | Last 2–3 years' outcomes vs expectations |
| `craft` / experience | Credit count and size, years active, stage background where recorded |
| `quote` | Reported fees if documented; otherwise derived from bankability and era pay scale |
| `typecasting` | Genre/persona distribution of past roles weighted by billing |
| `talent`, `presence` (H) | Career-wide quality signals (awards, ratings of lead work, longevity), shrunk toward the population prior |
| Personality, goals | Priors by profile; for Tier A, build-time extraction from biographies into a fixed schema with a citation per trait `[P2]` |

Raw evidence scores are converted to **within-year percentiles**, then mapped onto
configured target distributions, so the 1980 and 2004 worlds have comparable scales.

**Corrections:** `data/overrides/*.yaml` entries
`{id, field, value | delta, reason, source, author}` are applied after estimation
and versioned. Typical use: a handful of famous figures whose estimates look wrong
in the anomaly report. Neither you nor I are expected to review hundreds.

### 3.6 Real personal lives and historical events (answers Q4) `[S basic, P2 full]`

**HistoricalEvent record**
```
id, people[], type (marriage, divorce, child, death, illness, legal, scandal,
                    public statement, relocation, ...)
date, public_date (when it became publicly known; drives the information layer)
verification: documented | disputed | rumour
sources[] (url/title/date), summary (neutral wording)
dependency: { kind: independent | production | relationship | career | circumstance,
              requires: [conditions] }
```

**How documented events play out in an alternate history.** Each tick, the engine
checks upcoming documented events against their dependencies:

| Dependency | Example | Engine behaviour |
|---|---|---|
| independent | A death from long-term illness; a birth to an established couple | Occurs on schedule. A divergent career is not a reason to remove it. |
| production | An accident on a specific film set | Occurs only if that production exists with that person on set at that time. It is **never relocated** to another production. |
| relationship | A marriage between two people who met on a film | If they met in the simulation, it proceeds with its hazard. If not, probability falls to a base rate of meeting through other channels (shared agency, social circle, other projects). |
| career / circumstance | An event documented as tied to sudden fame or financial pressure | Hazard is scaled by whether the circumstance holds in-sim. |

- **Rumours** enter only the information layer, labelled as rumours, with their
  real circulation dates. They never become canon for mechanics.
- **Generation rules for real people:** the engine may generate *neutral or
  professional* developments (friendships, professional feuds arising from simulated
  interactions, new collaborations, and romantic relationships between real people
  only when they arise from simulated contact and the configuration allows it).
  It **never generates** crimes, abuse or misconduct allegations, addiction, illness
  or deaths for real people. Those occur only when documented.
- Fictional NPCs get the full generated personal-life system (hazards driven by
  personality, stress, money and fame).
- **World context timeline** `[S light]`: documented non-film events (elections,
  recessions, cultural moments) affect the market (for example, recession demand
  elasticity) and are passed to the narrator as atmosphere.

---

## 4. Start-year snapshots (answers Q2)

`compile_snapshot(date)` builds an initial world **directly from the historical DB**,
without simulating earlier decades:

1. **People:** everyone alive with a career by that date gets a tier. Attributes
   come from §3.5 as of that date. Relationships are seeded from collaboration
   history (worked together and the outcomes), shared agencies and documented marriages.
2. **Studios and agencies:** ownership, executives, approximate finances and
   output deals as of that date.
3. **Recent past (read-only canon):** films released in roughly the prior 3 years,
   with real grosses and reception, so bankability, heat and genre trends have context.
4. **Pipeline in progress:** films historically released in the next roughly 2–3
   years become projects whose **stage is inferred** from the release date minus
   typical durations (or real production dates when known), with real attachments
   as high-prior intentions. A film shooting in March 1980 is mid-production at
   start, but a slipped schedule or recasting can still change it.
5. **Future intentions:** later historical films are soft seeds that appear near
   their real development dates (see `docs/design-v0.2.md` §4.14). Future people
   enter through the debut pipeline.
6. **Market and era:** ticket prices, admissions, screens, windows, technology
   flags, union scales, genre appetites (estimated from recent genre performance)
   and world context.

**Slice support:** the first data build covers people and films around 1975–1990,
so **any start date from Jan 1980 to about 1985 works**. Adding 1990, 2004 or 2015
later is a data expansion, not an engine change `[P4]`.

**Protagonist creation** `[S]`: choose a background (birth year, training, origin),
a starting position, and goals that the delegation logic uses:
- **Unknown:** no credits; some stage/commercial background; a small agency.
- **Working actor:** generated back-catalogue of supporting roles in fictional
  films, with modest fame, a mid-tier agent and a quote to match.
- **Established star:** generated hit history, high bankability, a top agent and
  existing relationships with real figures, all consistent with that year's market.
- **Take over a real person** (cheap, because the player is just a controller):
  e.g. play as a real 1980 working actor. `[S optional]`

Generated back-history uses the **same estimator path** (synthetic credits, then
evidence, then attributes), so a "star" start is internally consistent rather than
having numbers assigned.

---

## 5. Data models (condensed; full field lists in `docs/design-v0.2.md` §3)

- **Person:** id, tier, provenance, birth/death, roles, personality,
  goals, energy/health, calendar, relationships, account, `controller: npc | player`.
- **ActorProfile:** talent(T), craft(T), range vector(T), presence(T),
  look_market_value(T, era/gender/age curve configurable), fame per region(T),
  appeal per segment(T), loyalty per segment(T), bankability(O), critical_rep,
  prestige, typecasting vector, heat(O), quote(O), professionalism(T).
  T means hidden true value, O means an observed estimate.
- **Director, Writer, Producer, Executive, Agent profiles:** as in v0.2.
- **Studio, Agency:** as in v0.2, plus ownership history.
- **Project:** stage machine IDEA → DEVELOPMENT → PACKAGING → GREENLIT → PREPRO →
  SHOOTING → POST → AWAITING_RELEASE → RELEASED (or TURNAROUND, SHELVED, DEAD),
  plus `historical_ref` and `divergence` flags.
- **Role, Offer, Audition, Contract** (fee, backend type and points, bonuses, billing, holds).
- **Film, BoxOfficeWeek, Revenue/Cost lines** posted to a double-entry Ledger.
- **Observation** (subject, observer, value, σ, bias, source, date).
- **HistoricalEvent** (§3.6), **WorldContextEvent**.
- **Decision** `{id, owner, kind, options[], deadline, default_policy, context_refs}`.
- **Proposal and Ruling** (§8.4).
- **NarrativeNote** (non-mechanical continuity: names of minor fictional people,
  places, running jokes), submitted by the narrator and stored verbatim.

---

## 6. Simulation processes

### 6.1 Weekly tick order
Market and context → historical events check → NPC goals → development → studio
slate/greenlight → packaging and casting → negotiations → production → post →
release scheduling → box office (all films, shared competition) → reception →
ancillary → awards → finance → careers → relationships → information and news.
The process descriptions in `docs/design-v0.2.md` §4.2–4.12 are retained (casting utilities,
negotiation bargaining, production quality, career updates, NPC utility agents).

### 6.2 Interruptible advancement and delegation (answers Q3) `[S]`
`advance --until 1980-06-30` runs week by week and **stops early** when:
- A **decision** the player owns is created with `interrupt: true` (offers,
  counter-offers, audition invitations for significant roles, scheduling conflicts,
  contract options, major personal choices).
- A **narratively significant** event involving the player occurs, if enabled
  (a film's opening, nominations, a major relationship event). This is configurable.

**Standing orders** (`orders.yaml`, per save) delegate routine matters, for example:
```yaml
auto_accept_auditions: {min_role: supporting, genres_excluded: [horror]}
auto_decline_offers: {fee_below_quote_pct: 60}
let_agent_negotiate: {up_to_role: supporting}     # agent uses its own skill
finances: auto                                    # bills, commissions, taxes
interrupt_on: [lead_offers, conflicts, counter_offers, nominations, premieres]
```
Delegated choices are made by the **same utility functions** that NPCs use, with the
player character's stated goals. They are logged as `delegated(rule=…)` and listed
in the next packet. Offers with a deadline freeze time until answered. If a decision
is explicitly ignored, its documented default applies at the deadline.

---

## 7. Box office: extraordinary outcomes without ceilings (answers Q6 / your Q3)

### 7.1 What limits success (and what doesn't)
**Hard limits are physical and economic only:** population by segment, seats ×
shows × occupancy (capacity), screens available, ticket prices, run time before
interest decays or windows open, and marketing money. **No outcome formula
references historical records**, so a film can beat any record if the simulated
audience behaviour gets it there.

### 7.2 Mechanisms that create a heavy upper tail `[S]`
Economists De Vany & Walls found that box-office revenue has a Pareto-type upper
tail (variance effectively infinite) and attributed it to **information cascades**:
word of mouth and observing other people's choices. The model builds those causes directly:

1. **Audience compartments** per segment and region: unaware → aware → interested →
   watched, with lapse (`docs/design-v0.2.md` §5.1).
2. **Social proof:** word-of-mouth reach grows with penetration ("everyone is
   talking about it") and saturates.
3. **Repeat viewing:** return probability rises steeply with satisfaction
   (`∝ sat³` in the prototype) and decays per visit.
4. **Capacity and holdover:** demand beyond weekly seats stays queued (sell-outs
   lengthen runs). Exhibitors add screens when films sell out and drop them when
   per-screen sales fall. Era parameters control screen totals and windows.
5. **Breadth:** four-quadrant appeal reaches more segments; niche appeal saturates
   its segment quickly.
6. **Event status** `[S, to build]`: pre-release tracking feeds media coverage,
   which feeds awareness (a cascade before opening). The prototype lacks this (§7.6).
7. **Cultural-moment reception:** a fat-tailed (Student-t) reception shock drawn
   identically for every film. It modulates satisfaction and appeal; it never sets
   a gross directly. A phenomenon needs several of these mechanisms to align, and
   the event log shows which did.
8. **International echo** `[P3]`: regional markets with their own fame and genre appetites.

### 7.3 Failure calibration
Profitability depends on cost discipline, marketing efficiency, concept breadth,
release-date competition and genre cycles, as well as quality. Targets: a
substantial share of wide releases lose money, and well-made films often fail,
but noticeably less often than poorly made ones.

### 7.4 Calibration targets (distributional, never per-film)
- Yearly gross distribution by era: percentiles, top-10% share, **Hill tail index** of the top 5%
- Ratio of the yearly #1 to the median film; spread of the yearly #1 across years
- Opening-to-total multipliers overall and **for the top grossers specifically**
- Profitability rate overall and by quality band; budget vs gross relationship
- Frequency of new all-time admissions records over long simulated spans, as a
  *soft* plausibility check (historically rare, not never). It is a diagnostic, not a cap.
- Historical coverage test: simulate real films 500× from their real inputs. The
  real result should fall inside the simulated 10–90% band about 80% of the time.

No fixed "±25%" tolerance. Sign-off is a reviewed calibration report showing each
target's simulated distribution next to the reference.

### 7.5 Methods
Batch runs over hundreds of seeds; loss = weighted quantile/KS distances; parameter
search (coordinate, then Bayesian) with held-out years; ±20% sensitivity analysis;
emergence counts per simulated decade (sleepers, breakouts, collapses, comebacks).

### 7.6 Prototype evidence (uncalibrated; `prototypes/tail_sketch.py`)
6,000 synthetic 1984-style wide releases (40 simulated years × 150):

| Metric | Result |
|---|---|
| Domestic gross p10 / p50 / p90 / p99 | $6.6M / $15.9M / $39.3M / $85M |
| Yearly #1 film: median / max | $103M / $252M (beats the real 1984 #1 with no special rule) |
| Profitable overall | 41% |
| Profitable, quality < 45 vs ≥ 70 | 35% vs 56% |
| Top 5 runs | quality 64–83; mostly ordinary reception shocks, so they are driven by quality and word of mouth, not luck |
| Hill tail index (top 5%) | 3.0 |

**What calibration must fix (findings):**
1. **The tail is too thin:** α ≈ 3.0, while the literature points to α < 2. The likely
   missing pieces are the pre-release event cascade, cross-film attention competition
   and IP/star-driven event openings.
2. **Hits rely on implausibly long legs:** the top runs opened at $4–8M with
   28–53× multipliers. Real 1980s megahits opened bigger and still had long legs,
   so distributor widening and pre-release buzz need modelling.
3. Quality's effect on profitability is plausible in direction, but its size needs
   checking against reference data.

The first sketch (`box_office_sketch.py`) also produced an impossible $38M 1984
opening before tuning, which shows why the batch calibration tooling is part of the slice.

---

## 8. Narrator integration with ChatGPT (answers your Q4) `[S]`

### 8.1 The loop
```
hsim load career1                       # canonical save
hsim advance career1 --until 1980-06-30 # stops at decisions/interrupts
hsim packet career1 > packet.md         # narrator packet (player-visible only)
  → paste into ChatGPT (a ChatGPT Project holding the Narrator Guide)
  → ChatGPT narrates, presents the pending choices, the player chooses in-story
  → ChatGPT ends its reply with a fenced ```engine block
hsim submit career1 reply.md            # parse → validate → adjudicate → apply → autosave
  (repeat; the next packet includes the rulings)
```
You can also decide directly from the CLI (`hsim decide dec-0012 counter --fee 45000`)
whenever that's easier.

### 8.2 Narrator Guide (one-time document for the ChatGPT Project) `[S]`
It states the contract:
- **May invent:** dialogue, personalities consistent with packet traits, settings,
  minor fictional characters, everyday events, press colour, emotional texture.
- **Must not invent or contradict:** any number (money, grosses, scores, dates),
  casting results, audition outcomes, awards, deals, deaths or other canon. It must
  not reveal information marked `narrator_hidden`.
- **Must propose, not assert:** consequential developments (falling-outs, alliances,
  reputation moments, purchases, career intentions) go in the `engine` block.
- How to present pending decisions, and how to write the reply block.

### 8.3 Packet format (Markdown + YAML, target ≤ ~4k tokens; detail levels configurable)
```yaml
packet: pkt-000143          # unique; a reply must reference it
save: career1  state_hash: 9f3a…  date: 1980-05-09  covers: 1980-04-11..1980-05-09
canon:                      # confirmed; must not be contradicted
  - {id: ev-2231, date: 1980-04-18, text: "You were cast as Danny in 'Night Shift Blues' (Orion), supporting role."}
  - {id: ev-2240, date: 1980-05-02, text: "'Night Shift Blues' began principal photography in Toronto. Scheduled 7 weeks."}
  - {id: ev-2251, date: 1980-05-09, text: "Opening weekend for 'Harbor Lights' (rival's film): $4.1M, rank 3."}
rulings:                    # results of your last proposals
  - {proposal: pr-0031, result: partially_accepted, effect: "Relationship with director cooled (moderate, not severe)."}
delegated:
  - {rule: auto_accept_auditions, text: "Agent booked an audition for a Paramount comedy on 1980-05-14."}
status:
  career: {fame: "known to casting directors, not the public", heat: rising, quote_public: "$40k (trade estimate)"}
  money: {cash: 18450, monthly_costs: 2100}
  projects: [{title: Night Shift Blues, stage: shooting, wraps: ~1980-06-20}]
people:                     # who is on stage, with what the player knows
  - {id: wd:Q…, name: …, role: director, traits: [meticulous, short-tempered], relation: "respects your work; annoyed by your lateness", notes: "…"}
world:                      # public industry knowledge, labelled by confidence
  - {text: "Trades report Universal is chasing a big summer comedy star.", confidence: reported}
  - {text: "Rumour: a rival actor is up for the same lead as you.", confidence: rumour}
pending_decisions:
  - id: dec-0012
    kind: offer
    deadline: 1980-05-16
    summary: "Orion offers a lead in a low-budget thriller, $45k, shoots 1980-07-07."
    options: [accept, decline, counter(fee), ask_agent]
    conflicts: "Overlaps by ~1 week if 'Night Shift Blues' runs over."
    default_if_unanswered: decline
continuity: |
  Previously: … (engine-generated, salience-ranked, rolling compaction)
narrator_notes: ["Your roommate is Gina (fictional, aspiring writer)."]
```
**What packets never contain:** hidden true values (talent, true quality, future
dates of documented events not yet public, other people's private negotiations),
except as the player's observations.

### 8.4 Reply block and adjudication
````
```engine
reply_to: pkt-000143
decisions:
  - {id: dec-0012, choice: counter, fee: 60000}
proposals:
  - {id: p1, type: relationship_shift, between: [player, wd:Q…], direction: negative,
     severity: moderate, cause: "Shouting match over rewrites on day 12."}
  - {id: p2, type: player_intent, text: "Wants to meet director X about her next film."}
  - {id: p3, type: purchase, item: "used car", est_cost: 3000}
notes:
  - "Player started dating Gina's friend Marco (fictional)."
advance: {until: 1980-06-30}
```
````
Proposal types in the slice: `relationship_shift`, `reputation_moment`,
`player_intent`, `purchase/expense`, `personal_milestone` (for the player or
fictional NPCs), and `narrative_note`. More types come in `[P2]`.

**Adjudication:** each type has preconditions (were they actually together? is it
affordable? is the person real, and does the proposal touch protected categories?)
and an engine model for the consequence. For example, whether an argument becomes
a lasting falling-out depends on both temperaments, existing affinity and the
stakes, and can resolve as *accepted*, *partially accepted* (a smaller effect),
*rejected (with reason)* or *rolled* (a logged chance). Proposals that try to set
numbers or outcomes (fees, casting, grosses, awards) are rejected and converted into
intentions where possible ("wants a higher fee" becomes a counter-offer).
NPC-to-NPC developments that the narrator invents follow the same rules.

### 8.5 Continuity and safety
- **Idempotent:** a reply must reference the latest packet id and state hash.
  Re-submitting the same block is detected by its hash and ignored. A reply to an
  old packet is refused unless you `rewind`, which creates a branch.
- **Atomic and saved:** each submission is applied fully or not at all, then autosaved.
- **Continuity summary:** generated deterministically from the event log
  (salience = player involvement, size of change, recency, ongoing threads), so a
  brand-new ChatGPT chat only needs the latest packet.
- **Consistency check** `[P2]`: the parser flags numbers or named outcomes in
  ChatGPT's narration that aren't in the packet, for example a narrated gross that
  differs from canon.

### 8.6 Integration options
| Option | How | Verdict |
|---|---|---|
| **A. Copy/paste files** | Local CLI + ChatGPT Project with the Narrator Guide | **Slice default.** Works on any plan, and canon stays on your machine. |
| B. ChatGPT runs the engine in its Python sandbox | Upload engine + save each session | Not recommended as canonical: sandbox files expire and ChatGPT can edit state. |
| **C. MCP server** | Expose `service.py` as MCP tools (`get_packet`, `submit_reply`, `advance`) | `[P6]`, or earlier if you want. ChatGPT's developer mode supports custom MCP tools with write actions, but plan availability varies and the engine must be reachable over the internet. Uses the same service layer, so nothing is rewritten. |

---

## 9. Autonomous ecosystem
Unchanged in intent from `docs/design-v0.2.md` §4.12: all people and studios are bounded-rational
utility agents using their own observations. NPC careers, studio fortunes, genre
cycles, relationships and personal lives (within §3.6 rules) evolve without the
player. The packet's `world` section surfaces a salience-ranked selection of that activity.

---

## 10. Testing
- **Unit and property:** money conservation, valid stage transitions, no overlapping
  shoots, all draws logged.
- **Determinism:** same inputs give the same state hash, and replay equals the snapshot.
- **Fairness:** swap the player with an identical NPC; the outcome distributions must
  match. Delegated decisions must equal NPC utility choices.
- **Snapshot leakage:** observed attributes in a snapshot must be unchanged when
  data after the start date is deleted.
- **Narrator:** packets contain no hidden fields; the packet → reply → apply cycle
  is idempotent; rewinding and replaying gives an identical state; malformed or
  forbidden proposals are rejected with reasons.
- **Batch calibration:** `tools/batch.py` runs thousands of films and careers per
  configuration and produces the calibration report (§7.4) and career-dynamics
  report (breakout rates, career lengths, slump-recovery rates, salary
  distributions, NPC vs historical rank correlations for the first simulated years).

---

## 11. Phases

### Vertical slice (Phases 0 + 1): "a playable, narratable 1980s career" `[S]`
**Simulation integrity**
- Core: RNG streams, clock and queue, event and command logs, ledger, SQLite saves,
  replay, rewind/branch, config versioning, service layer.
- Data: Wikidata pipeline (+ optional local IMDb enrichment) for about 1975–1990;
  estimator with hindsight rule, overrides and anomaly report; snapshot compiler
  (start dates 1980–1985); tiers A/B/C plus generated fill.
- Protagonist creation: unknown, working actor or established star (+ optionally
  take over a real person).
- World loop: simplified development, studio greenlight on observed forecasts,
  casting (offers, auditions, screen tests for leads, competition, conflicts,
  rejections), negotiation (fee, quote, gross/net points), production durations
  and overruns, film quality, critic and audience reception, box office (shared
  competition, the §7.2 tail mechanisms, single international bucket), simple
  ancillary and studio P&L, participations ("Hollywood accounting"),
  career updates, personal finance, relationships v1, information layer v1.
- Awards v0: Academy acting nominations and wins via a simple voter model.
- Personal life v1: documented Wikidata events (marriages, divorces, children,
  deaths) with dependency checks; light generated life events for fictional NPCs.
- Interruptible advance, standing orders and delegation.

**Narrative usability**
- Packets (§8.3), reply parser and adjudicator (§8.4), slice proposal types,
  continuity summary, narrative notes, idempotency, rewind.
- Narrator Guide for a ChatGPT Project.
- An end-to-end test script plus one real play session with ChatGPT as acceptance.

**Calibration**
- Batch tooling, 1980s reference statistics, calibration and career reports.

### Later phases
- **P2: deeper industry and lives.** Full awards season (precursors, campaigns),
  agencies (switching, packaging), development hell and turnaround, studio finances
  and ownership changes, Wikipedia-derived documented events and personality
  extraction (with citations), critic outlets, more proposal types, the narration
  consistency checker, and a 1990 snapshot as a second start-year proof.
- **P3: full economics.** Multi-region international, full ancillary waterfall by
  era, residuals detail, platform releases, franchises and IP.
- **P4: history to 2026.** Data expansion, snapshots for 2004 and 2015 (and any year),
  structural eras (multiplexes, DVD, China, streaming, the 1988/2007/2023 strikes,
  the 2020 pandemic), and per-era calibration with held-out years.
- **P5: career breadth.** TV, streaming originals and buyouts, theatre, endorsements,
  producing, directing, production companies.
- **P6: integrated apps.** MCP server for ChatGPT, web front end.

### Implemented vs planned
| Component | Status |
|---|---|
| Design (this document) | done (v0.3) |
| `prototypes/box_office_sketch.py`, `prototypes/tail_sketch.py` | throwaway prototypes, uncalibrated |
| Everything else | planned |

---

## 12. Open items
1. Data hosts (Wikidata, optionally IMDb/TMDB) need network access in the build
   environment, or the pipeline runs on your machine.
2. Box-office reference statistics need a source we're allowed to use for full
   yearly distributions. Aggregates and Wikipedia lists are fine; bulk scraping of
   commercial sites is not.
3. Configuration default for romantic relationships between real people that arise
   from simulated contact (§3.6): proposed **on** (neutral category), but you may prefer **off**.
