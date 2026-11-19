# Status: implemented vs planned

Engine version 0.1.0, the first playable slice. "Implemented" means working, covered
by the test suite or the batch report, and usable from the CLI.

## Implemented
| Area | What works |
|---|---|
| Core | Named deterministic RNG streams, weekly tick, event log with hash chain, config in YAML with hashing, flat serialisable state |
| Persistence | SQLite saves: genesis params, command log, events, snapshots per packet; `verify` replays to an identical state hash; `rewind` branches at any packet |
| World genesis | Real 1980 studio/agency names; ~1,400 generated actors (newcomer/working/notable/star), ~240 directors; production pipeline with stages inferred from release dates; films released just before the start already in theatres |
| Studios | Weekly greenlights at slate rates; pitch selection on the studio's *noisy* read of quality |
| Casting | Director attachment; candidate pools (age, gender, availability); casting utility on observed values (bankability, a noisy read of talent, fit, relationships, agency visibility, cost) plus per-role casting taste; direct offers for bankable leads; auditions with open-call slots for unknowns; offers, NPC acceptance utility, rejections cascade down the shortlist; delays and shelving when casting stalls |
| Negotiation | Fees from the role budget and the actor's quote/heat; studio walk-away limit; player counter-offers with leverage from agency strength; final counter; gross/net points |
| Production | Shoot weeks, overruns, energy drain, on-set bonding and clashes (temperament/ego), performances and the film's hidden quality vector at wrap, craft growth |
| Release | Release dating (season, crowding), P&A, tracking forecasts that account for visible competition, studio boosts/cuts after tracking and test screenings |
| Box office | Audience compartments across 4 segments, word of mouth with social proof, repeat viewing, seat capacity, exhibitor screen decisions, shared attention competition across all films, seasonality, weekly chart |
| Economics | Rentals, international ratio by era, ancillary, overhead, gross participations, net-profit statements ("Hollywood accounting") |
| Careers | Heat (surprise vs expectation), bankability (industry attribution), fame, appeal, critical reputation, prestige, typecasting, fame decay, retirement, yearly fictional debutants, agency signing |
| Finance | Fees in two halves, agent commission, era tax rate, monthly costs, day-job income for idle unknowns, participations |
| Awards v0 | Academy-style nominations and winners (4 acting categories, Picture, Director) |
| Personal life | Attraction (hidden, pairwise, orientation-aware), romance from on-set contact, dating, marriage, breakups/divorce; documented historical events with dependency checks (independent / relationship / circumstance / production); fictional mortality; config controls which generated categories apply to real people |
| Player | Unknown / working / star starts; decisions (audition, offer, counter, romance, agency offer); standing orders and delegation via the same utilities as NPCs; interruptible advance |
| Narrator | Packets (canon, rulings, delegated, projects with premises, people cards with traits and shared history, industry chart and news, pending decisions, continuity, notes); reply parser; adjudication of relationship shifts, romantic overtures, intents, purchases and reputation moments; idempotent submission; stale-reply refusal |
| Tools/tests | `tools/batch.py` calibration report; 17 tests (determinism, replay, rewind, fairness, money conservation, scheduling, hidden-value leakage, adjudication, documented-event dependencies) |

## Planned next (in order)
1. **Historical data pipeline** (Wikidata → data pack → estimator → snapshot). Real people and films, starting from 1980.
2. Calibration pass 2 (see open issues below).
3. Deeper NPC agency: actors pursuing goals, agents switching, studio finances and executive changes.
4. Awards season detail (precursors, campaigns), critic outlets.
5. Phases 3–6 from DESIGN.md §11.

## Calibration report (4 worlds × 2 years, 1980–81; 1980 dollars)
| Metric | Simulated | Reference / note |
|---|---|---|
| Annual admissions | 0.97–1.26 billion | ~1.02–1.07 billion (1980–81, verify) |
| Wide releases per year | ~128 | ~150–200 incl. independents |
| Domestic gross p50 / p90 / p99 | $13.6M / $56.8M / $172M | — |
| Yearly #1 film (median) | $208M | 1980 *The Empire Strikes Back* ~$181M (initial run); 1981 *Raiders* ~$212M |
| Top-10% share of gross | 41% | — |
| Hill tail index (top 5%) | 2.7 | Literature suggests < 2: **tail still too thin** |
| Opening→total multiplier p50 | 8.3× | **Probably too high**: legs too long |
| Tracking bias / error | +6% / 26% | — |
| Profitable films | 66% | **Probably too high** |
| Profitable, quality < 45 vs ≥ 65 | 64% vs 73% | Direction right; effect possibly weak |

### Open calibration issues
- Thin upper tail and long legs (see DESIGN.md §7.6): add pre-release event cascades and stronger cross-film attention dynamics.
- Profitability rate high: revisit ancillary coefficients, P&A, overhead and interest against the era's studio financials.
- Release count below the real total: independents and foreign films are not yet modelled.
- Performance: about 6 CPU-seconds per simulated year with ~1,600 people; batch runs parallelise across worlds.

## Known simplifications in the slice
- One international bucket; no TV, streaming or theatre work yet.
- Agents are agencies, not individual people.
- The protagonist is exempt from generated mortality (a deliberate, documented exception).
- Generated "prior credits" for starting NPCs are fictional titles.
