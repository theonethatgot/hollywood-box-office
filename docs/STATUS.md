# Status: implemented vs planned

Engine version 0.1.x, the first playable slice. "Implemented" means working,
covered by tests or the batch and validation reports, and usable from the CLI.

## Implemented
| Area | What works |
|---|---|
| Core | Named deterministic RNG streams, weekly tick, event log with hash chain, YAML config with hashing, flat serialisable state |
| Persistence | SQLite saves: genesis params, command log, events, snapshots per packet; `verify` replays to an identical state hash; `rewind` branches at any packet |
| **Historical snapshot** | Wikidata (CC0) pack of 4,996 US films (1975–89) and 10,517 people; loader builds the world for a start date (1980–1987 supported); ingestion v2 (bulk SPARQL + persistent store, see docs/INGESTION.md); real studios mapped from distributors; real films become projects with stages inferred from release dates (schedules fitted so documented films don't collide); real casts as *intended* attachments with agent holds; observed attributes from pre-start facts only; hidden talent from partial hindsight plus noise; personality and orientation priors marked as such in provenance |
| **Documented history** | Marriages, divorces and deaths as events with dependencies (independent / relationship / circumstance / production); widowhood is not read as divorce; divergences logged |
| Fictional population | ~700 generated actors and 80 directors alongside real people (1,400/240 in fictional-only worlds); yearly debutants |
| Studios | Weekly greenlights at slate rates, reduced by documented films in the pipeline; pitch selection on the studio's noisy read of quality |
| Casting | Historical attachment offered first; candidate pools; casting utility on observed values plus per-role taste; direct offers; auditions with open-call slots; offers, acceptance utility, rejection cascades; delays and shelving |
| Negotiation | Fees from role budget, quote and heat; studio walk-away; counter-offers with agency leverage; gross/net points |
| **Jobbing work v0** | TV guest spots, commercials, bit parts, TV movies, stage work through agents (same rules for everyone); pay, craft, a little fame |
| Production | Shoot weeks, overruns, energy, on-set bonding and clashes, performances and hidden quality vector at wrap, craft growth |
| Release | Dating, P&A, tracking that sees films in release plus films dated within ±2 weeks, studio boosts/cuts after tracking and test screenings |
| Box office | Audience compartments, word of mouth with social proof, repeat viewing, seat capacity, exhibitor screen decisions, shared competition, seasonality, weekly chart |
| Economics | Rentals, international ratio by era, ancillary, overhead, gross participations, net-profit statements |
| Careers | Heat, bankability (attribution), fame, appeal, critical reputation, prestige, typecasting, decay, retirement, agency signing |
| Finance | Fees in two halves, commission, era tax, monthly costs, day-job income for idle low-fame actors, participations |
| Awards v0 | Academy-style nominations and winners (acting, picture, director) |
| Personal life | Hidden pairwise attraction, romance from contact, minimum courtship before marriage, breakups/divorce; real people may form simulated relationships (config); no generated illness, death, crime or scandal for real people |
| Player | Unknown / working / star starts; decisions (audition, offer, counter, romance, agency offer, job); standing orders; interruptible advance |
| Narrator | Packets (canon, rulings, delegated, projects with premises, people cards with traits, motivation, real-person flag and shared history, industry chart and news, pending decisions, continuity with recent scenes and threads, era note, notes); reply parser; adjudication; idempotent, stale-safe submission |
| Tools/tests | `tools/batch.py` (fictional or `--historical`), `tools/validate_snapshot.py` (anchor ranks); 22 tests |

## Experience pass (v0.2): living professional ecosystem
| Area | What works |
|---|---|
| Agents and casting directors | Named agents (per agency) and casting directors (per studio + independents) with personas. Agents **submit** clients for roles based on hustle, fit and a **strategy derived from the client's goals**; CDs bring in people they know, screen submissions and pass with reasons from the actual scoring; auditions leave lasting impressions on CDs and directors; monthly agent check-ins summarise real activity |
| Episodic TV | 48 fictional series on real networks (format, premise, regulars, producer, episode directors); guest parts cast through the same submission/audition process in season; bookings carry show, character, episode, director and co-stars |
| Featured parts | Every film has 6–12 smaller speaking parts open to submissions (historical films keep documented billing 5–8 as attachments) |
| Jobbing | Commercials, bit parts in real productions in the pipeline, TV movies and stage productions of real plays, each with named colleagues |
| Relationships | Co-workers, casting rooms, premieres and ordinary social encounters create and deepen contacts; access respects fame gaps; NPC friendships deepen by the same rule |
| Feedback | Audition feedback derived from the biggest real gap to the chosen actor (presence, craft, type, name), so players can respond without seeing numbers |
| Characters | Fictional people have persistent personas (background, home town, signature habit, style); real people get reputation and goals inferred from their documented careers and honours (personality remains a marked prior) |
| Projects | Studio genre identities (Disney family, New World exploitation, Orion adult drama...), tone and selling point per project; richer titles; grammatical premises; directors accept or decline by genre fit, budget versus standing and recent activity, and studios weigh affordability |
| Narrator packets | New sections: `period_summary` (with explicit quiet periods), `career_activity`, `your_work` (films + jobs), `network`, `open_threads` (including goal versus reality); people cards with profession, reputation, persona, ambition and shared history; real films carry a `historical_record` (documented vs simulated) |
| Protagonist | `--goals`, `--hometown`, `--training`; new `notable` background |
| Historical data | Documented character names (Wikidata P453/P4633, ~7% of roles; the rest are generated and flagged); multilingual (`mul`) names recovered 194 films and 380 people (e.g. *The Empire Strikes Back*, Meryl Streep); original release year preferred over later foreign releases; later rights-holders, TV networks, adult films and cast-less real films excluded; real independent distributors become studios; `tools/validate_history.py` reports documented vs simulated |

Example packets: `docs/examples/`.

### Measured after the pass
- Working actor: ~100–150 agent submissions a year, a handful of call-ins, several bookings, film roles rare.
- Established actor: 50+ auditions a year, mostly episodic TV; a film co-lead after ~13 months in the example career.
- Snapshot validation: 7 of 10 anchor stars in the top 50 by bankability (median rank 19, was 49).
- 1980 calibration (4 worlds, 1 year): admissions 0.91–0.98 billion (reference ~1.02); about 238 releases; tracking bias +1%; 44% profitable. A full recalibration pass is due after this many structural changes.
- Performance: ~40 seconds per simulated year (was ~5), because every submission, audition, job and encounter is now simulated industry-wide. Fine for play (a few seconds per month); a target for the next optimisation pass.

### Known gaps after the pass
- Some real-director pairings on fictional projects are still unusual (e.g. a prestige drama director on a horror film), though rarer.
- Packets run ~5–8k tokens; compaction controls are planned.
- Wikidata documents character names for only ~7% of roles.

## Mobility and provenance pass
- **Negative-spiral fix:** casting-director/director impressions were zero-sum against the room's median,
  so frequent auditioners accumulated bad standing just by showing up, and nothing faded. Now an ordinary
  read leaves no mark, a clearly weak read a small mark, a strong read real goodwill; bad impressions fade
  (half-life ~11 months), good ones last (~5 years). Measured with `tools/mobility.py` (4 worlds, 9,528
  represented actors, 1980–82): struggling actors' mean CD goodwill went from **−6 → −10 → −13** (share negative
  74% → 81%) to **+1.3 → +3.0 → +4.5** (share negative ~50%, stable). Work mobility (bottom quartile reaching the
  first-year median by year 3) stays ~44%.
- **Ways to improve:** on-camera experience builds screen presence (small, diminishing, capped at +12 per career);
  craft from work and classes; agents learn each client's niche (where they land near the top of the room) and
  steer submissions there, and say so in check-ins.
- **Schedule conflicts:** a slipped shoot that collides with work booked in the meantime now releases the actor
  (role recast) instead of double-booking them (a latent bug exposed by the tests).
- **Provenance labels** in packets: real film record vs simulated production; documented vs simulated character
  names; documented vs simulated casting; event provenance for real people; documented vs simulated relationships.
- **Statistics:** `tools/career_stats.py` reports call-in probabilities under the population rate, the actor's
  own earlier rate, and a Beta-binomial posterior predictive, with the independence assumption stated.

### Known gaps
- Documented *unmarried* partnerships (Wikidata P451) aren't fetched yet, so real couples who never married
  (e.g. Sondra Locke and Clint Eastwood) can be split up by simulated romances. Labelled "simulated", but should
  be protected like marriages.
- Real people's personality traits are still priors; only goals and reputation come from their documented careers.

## Narrative integrity pass
- **Continuity isolation:** the cross-protagonist "Gina" note came from the playtest harness (it added Nora's
  note to every career), not the engine. Regression test added; `submit` now warns when a note's subject
  matches nobody in the world.
- **No future information:** real people's bios are built only from facts dated before the start (nationality,
  profession, birth year, best-known pre-start credit, pre-start honours). Wikidata descriptions (which carry
  death years and later careers in ~4,200 of ~11,000 people) are no longer shown. Film descriptions that
  mention later years are dropped. Test added.
- **Documented partnerships:** Wikidata P451 with dates (497 people, 481 dated partnerships). Ongoing ones load as
  documented relationships; future starts and ends are events with dependencies. Documented relationships
  (married or not) are protected against simulated breakups unless **relational strain in this timeline** exists
  (clashes, cooling, long separations); a divergent career alone no longer weakens them. Verified: Sondra Locke
  and Clint Eastwood stay together through 1983; Keaton and Beatty separate in 1981 as documented.
- **Film story profiles:** persistent outline for productions the protagonist auditions for or works on:
  central conflict, characters with functions, wants, flaws and arcs, relationships, beats, key scenes, director's
  intent (real directors' intent labelled as characterisation), and the protagonist's noisy read of the script.
  Real films get no invented plot. Character relationships feed on-set closeness (friction and chemistry).
- **Contextual social life:** profession-appropriate personas; on-set friction needs a concrete circumstance
  (billing rivalry, director vs ego, schedule pressure, exhaustion, two volatile temperaments); chemistry scales
  with how closely people work; catch-ups need a real connection and scale with how many you have; premiere
  invitations need a reason that the packet states.

### Still open
- Real auteurs occasionally direct fictional projects (e.g. Antonioni on an Orion drama): plausible in an
  alternate timeline but unusual; needs a stronger "documented-career fit" for real directors.
- Real people's personalities remain priors (labelled). Biography-derived traits with citations are planned.

## Bug-fix pass: replay determinism and guest-part gender
- **Replay drift (root cause):** saves were written with sorted keys, so a reloaded state iterated nested
  dictionaries (e.g. a film's audience segments) in a different order from the original run. Weekly
  admissions are summed in that loop and float addition depends on order, so cumulative grosses drifted by
  last-bit amounts (~$0.00000002) and award announcements listed categories in a different order. Saves now
  preserve order exactly; hashes stay canonical. Regression tests reopen the save between every command.
- **Legacy saves:** `hsim verify --rebaseline` keeps everything exactly as it happened and makes the current
  state a verified checkpoint; `hsim verify --adopt-replay` adopts the replay only when event histories are
  identical and every difference is float rounding (refuses anything else).
- **Engine updates:** saves record an engine fingerprint; the first command after an update checkpoints the
  save automatically (replay is only meaningful within one engine version).
- **Guest-part gender:** TV guest parts drew gender and description independently ("the suspect's girlfriend"
  as a male role). Candidate filtering already respected the role's gender; descriptions now match it.
  Neutral parts stay gender-flexible. Film roles were unaffected (0 of 52 checked mismatched).

## Initiative and continuity pass
Priorities: technical correctness, a flexible narrator-to-engine interface, agents with initiative,
and consequential context without busywork.

**Three levels of canon** (reply block; see NARRATOR_GUIDE.md):
- *Hard canon*: engine-confirmed facts (unchanged).
- *Narrative canon* (`narrative`): nonconsequential details the narrator creates, optionally `about`
  people (names or ids). Persisted, returned in `narrative_canon` and on people cards. Entries that read
  like outcomes ("got the part", money, "married") are flagged and change nothing.
- *Proposed consequential canon* (`initiatives`): `inquire`, `pursue_project`, `meet`, `introduction`,
  `social`, `publicity`, `reposition`, `develop_project` (with `attach` / `revise` follow-ups). Targets
  resolve by name or id (ambiguity and unknown names are reported). The engine answers `accepted`,
  `partial` (a counter), `rejected` with the concrete reason (dates, age range, type, "a bigger name",
  "pays below your quote", "earmarked for an attached actor"), or `pending` over weeks; initiatives keep a
  history. Initiatives can't set outcomes; a successful push only gets you seen.

**Agents with initiative** (same rules for every client; a test swaps the protagonist's controller and
compares): weekly calls are limited by hustle. Agents push clients who just missed a casting director's
list on parts worth it (size, film, the client's goals, proven niche, earnings), and clients whose
director already rates them on films casting soon. A director's regard and the agent's credibility with
the CD help; failed pushes cost credibility; placements build it. CDs add at most three pushed actors per
session. Client directives (`reposition`) constrain submissions, TV and commercials. Agents no longer
submit clients for parts far below their quote unless the part suits their goals. In a 40-week test world
about half of ~435 pushes were agreed and ~10 led to a casting: being seen is not being cast.

**Context, not busywork:** packets add `standing_changes` (labels before → after, with the events that
moved them, or "momentum fades on its own"), `agent` (strategy, how much attention you get and why,
directives, pushes this period, doors left open), `initiatives`, people cards with `why_here` and
`lately` (what they did on their own that you could know). The engine no longer invents the
protagonist's casual social life; premieres (with reasons) and NPC friendships remain.

**Fixes (with regression tests):** `quiet_period` is false while shooting or on any job (`working` lists
them); weekday words in event text must match the event date (a "Sunday barbecue" logged on Fridays and a
comedy premise "the wedding on Saturday" were removed); on-set chemistry for the protagonist respects
their own orientation and waits 26 weeks before re-prompting about the same person (a demo career got four
prompts in five weeks, one with a man for a protagonist attracted only to women); the premieres
interrupt stops on an opening, not every weekend of the run; a character's key scenes are distinct; an
agent's read of the room used the protagonist's rank instead of their client's (caught before release).
Replay determinism and guest-part gender (previous pass) keep their tests; all saves replay.

**Demonstration:** `docs/examples/initiatives/` (see its README) is a real saved career: Daniel Brooks, a
notable actor on the historical 1980 world, 40 turns through August 1982, which replays exactly (81 commands).
It shows a narrator-originated pursuit rejected for its real date conflict; a meeting arranged; his agent spending
a call on a colead for him (declined: "they want a bigger name"); and an original drama developed, passed on,
packaged with Bruce Beresford, put in turnaround, rewritten and greenlit at Orion. A packet ten months later still
carries all of it (Beresford's card, narrative canon, resolved initiatives). Playing it found six bugs, each fixed
with a regression test (listed in that README).

**Also fixed in this pass:** a greenlit package keeps its attached director and actors; a developed lead is
renamed when re-gendered; narrative canon about someone the protagonist never met is flagged; resolved initiatives
stay in `continuity`; people with history come before small-part co-stars on the people list.

## Calibration (4 historical worlds × 2 years, 1980–81, 1980 dollars)
| Metric | Simulated | Reference / note |
|---|---|---|
| Annual admissions | 1.01–1.23 billion | ~1.02–1.07 billion (verify); 1981 runs ~10% high |
| Releases per year | ~291 | Real count incl. independents was in the hundreds ✓ |
| Domestic gross p50 / p90 / p99 | $4.5M / $25M / $92M | Includes many small independent releases |
| Yearly #1 (median / max) | $143M / $219M | 1980 *Empire Strikes Back* ~$181M; 1981 *Raiders* ~$212M |
| Hill tail index (top 5%) | **1.86** | Literature: < 2 ✓ |
| Opening→total multiplier p50 | 9.2× | Era-plausible (1980 range ~7× to 26×) |
| Tracking bias / error | +2% / 35% | ✓ |
| Profitable films | 41% | Plausible; not yet validated against studio financials |
| Profitable, quality < 45 vs ≥ 65 | 27% vs 66% | Quality matters without guaranteeing success ✓ |

**Re-run, this pass (historical seeds 1–2 × 2 years), same seeds before and after the pass:**
| Metric | Before (e43fa75) | After | Note |
|---|---|---|---|
| Admissions 1980 / 1981 | 946–978M / 1.11–1.14B | same | ref ~1.02 / 1.07B |
| Releases per world-year | 244 | 244 | |
| Domestic p50 / p90 / p99 | $5.3M / $29.8M / $92.6M | $5.2M / $29.2M / $90.2M | |
| Yearly #1 median / max | $120M / $166M | $120M / $171M | |
| Hill tail index (top 5%) | 2.61 | 2.47 | **thinner than the < 2 target** |
| Profitable share; quality ≥ 65 profitable | 43.8%; 88% | 43.8%; 89% | |

The pass does not move the market. The table above predates the pack's exclusion of TV, adult and cast-less
films, and the current pack's tail is thinner than it reported (α ≈ 2.5 vs 1.86): an open calibration issue.

Fictional-only worlds (no pack) remain available. Their tail is thinner (α ≈ 2.7),
because real films bring wider spreads of budget, marketability and star power.

## Snapshot validation (1980 start, vs 1979 exhibitors' poll from memory, *verify*)
Reynolds #3, Eastwood #2, Allen #22, Travolta #21, Fonda #23, Stallone #48 by
bankability; Streisand (#91), Clayburgh (#80) and Brooks (#83) rank low. Roger
Moore is effectively missing because his Bond films are British productions.
Six of ten anchors are in the top 50 of 3,595 real actors.

## Open issues (next)
1. **Calibration:** the current historical pack's box-office tail is thinner than the literature (Hill α ≈ 2.5
   on seeds 1–2, target < 2) and the yearly #1 is low (~$120M vs ~$181–212M). Re-tune after coverage (item 2).
2. **Coverage:** include UK/US co-productions and US-distributed foreign films (Bond, *Superman*...).
3. **Estimator:** use recorded box office more strongly where present; Tier A personality extraction from biographies (with citations).
4. **Deaths during a shoot:** roles reopen for films not yet shooting; a death mid-shoot isn't handled yet.
5. **Profitability** against era studio financials; per-era ancillary.
6. Deeper NPC goals (NPCs don't yet originate initiatives like develop_project), awards season detail,
   then Phases 3–6 (DESIGN.md §11).
7. Generated fictional names can collide with real people (a fictional director named "Charlie Kaufman"
   appeared); filter generated names against the real-person index.
8. Packages: only one attachment affects a studio's read; financing, producers and turnaround deals
   are not modelled.

## Data and licensing
- Committed: `data/history/wikidata_1975_1989.json` (CC0 facts only), `data/reference/` anchors.
- Local only (gitignored): `data/raw/` downloads, `data/local/imdb_billing.json` (IMDb billing order;
  personal non-commercial use, never committed). Without the local billing file, cast order falls back
  to Wikidata statement order (now fetched for every film in the pack).

## Known simplifications
- One international bucket; TV and theatre exist only as jobbing work.
- Agents are named people inside agencies; their book, hustle and CD relationships are simple.
- The protagonist is exempt from generated mortality (a deliberate, documented exception).
- Generated "prior credits" for fictional NPCs are fictional titles.
