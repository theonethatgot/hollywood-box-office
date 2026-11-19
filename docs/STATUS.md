# Status: implemented vs planned

Engine version 0.1.x, the first playable slice. "Implemented" means working,
covered by tests or the batch and validation reports, and usable from the CLI.

## Implemented
| Area | What works |
|---|---|
| Core | Named deterministic RNG streams, weekly tick, event log with hash chain, YAML config with hashing, flat serialisable state |
| Persistence | SQLite saves: genesis params, command log, events, snapshots per packet; `verify` replays to an identical state hash; `rewind` branches at any packet |
| **Historical snapshot** | Wikidata (CC0) pack of 2,775 US films (1975–84) and 6,814 people; loader builds the world for a start date (1980–1984 supported); real studios mapped from distributors; real films become projects with stages inferred from release dates (schedules fitted so documented films don't collide); real casts as *intended* attachments with agent holds; observed attributes from pre-start facts only; hidden talent from partial hindsight plus noise; personality and orientation priors marked as such in provenance |
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

Fictional-only worlds (no pack) remain available. Their tail is thinner (α ≈ 2.7),
because real films bring wider spreads of budget, marketability and star power.

## Snapshot validation (1980 start, vs 1979 exhibitors' poll from memory, *verify*)
Reynolds #3, Eastwood #2, Allen #22, Travolta #21, Fonda #23, Stallone #48 by
bankability; Streisand (#91), Clayburgh (#80) and Brooks (#83) rank low. Roger
Moore is effectively missing because his Bond films are British productions.
Six of ten anchors are in the top 50 of 3,595 real actors.

## Open issues (next)
1. **Coverage:** include UK/US co-productions and US-distributed foreign films (Bond, *Superman*...).
2. **Estimator:** use recorded box office more strongly where present; Tier A personality extraction from biographies (with citations).
3. **Deaths during a shoot:** roles reopen for films not yet shooting; a death mid-shoot isn't handled yet.
4. **Profitability** against era studio financials; per-era ancillary.
5. Agents as people, deeper NPC goals, awards season detail, then Phases 3–6 (DESIGN.md §11).

## Data and licensing
- Committed: `data/history/wikidata_1975_1984.json` (CC0 facts only), `data/reference/` anchors.
- Local only (gitignored): `data/raw/` downloads, `data/local/imdb_billing.json` (IMDb billing order;
  personal non-commercial use, never committed). Without the local billing file, cast order falls back
  to Wikidata statement order, or to a prior-experience rule for films fetched in bulk.

## Known simplifications
- One international bucket; TV and theatre exist only as jobbing work.
- Agents are agencies, not individuals.
- The protagonist is exempt from generated mortality (a deliberate, documented exception).
- Generated "prior credits" for fictional NPCs are fictional titles.
