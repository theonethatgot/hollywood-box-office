# Historical data ingestion: measurements and design

## Where the time went in v1
Measured on this project's cloud session, November 2026.

| Cause | Effect |
|---|---|
| Wikidata Query Service outage rule ("1 request/minute") | The v1 fetcher slept 61 s after **every** SPARQL query. That was necessary during the outage, but the rule has since been lifted and the sleep remained. |
| Per-film `Special:EntityData`, sequential, with a 0.5 s sleep | ~110 films/min at best |
| HTTP 429 handling: `Retry-After` + 5 s fixed penalty | Each 429 cost 6 s or more |
| Batch entity API (`wbgetentities`, 50 ids/request) | Throttled for this session's shared address: 429 on 4 of 5 requests even at 1 request every 3 s. Not usable here, though it may work from other networks. |
| Wikidata dumps / third-party endpoints (QLever) | Dumps are ~100+ GB compressed, far too large for a few thousand films. QLever is blocked by this environment's network policy and isn't needed. |

## Benchmarks (same session, real film ids)
| Method | Throughput | Errors |
|---|---|---|
| `Special:EntityData`, 1 id per request, sequential | ~114 entities/min | none |
| `Special:EntityData`, 4 concurrent workers | ~538 entities/min | none |
| `wbgetentities`, 50 ids per request | unusable here | 429 |
| **SPARQL with `VALUES` lists (300 films, every property)** | **~36,000 entities/min** | none |

## v2 design (`datapipe/fetch_wikidata.py`)
1. **Bulk SPARQL for nearly everything:** film lists, film facts, release dates with
   precision, people, spouses, honours, labels and IMDb ids, using `VALUES` chunks of 300–2,000 ids.
2. **Adaptive pacing per host:** a minimum interval that doubles on 429 (honouring
   `Retry-After`) and decays back on success. Timeouts and 5xx responses on heavy
   queries split the chunk in half instead of retrying the same load.
3. **Optional statement order:** cast order from `Special:EntityData`, with 4 workers
   sharing a 0.1 s interval (≤ 600/min). Skip it when the local IMDb billing file is used.
4. **Persistent store** (`data/raw/wikidata/store.sqlite`, gitignored): entities, bulk
   rows, per-stage "seen" ids, and film lists per year. Every stage fetches only what
   is missing, so new year ranges and reruns are incremental. The v1 file cache was
   imported automatically.
5. **Statistics** per stage (requests, 429s, 5xx, retries, splits, waiting vs request
   time) go to `data/raw/wikidata/last_run_stats.json`.

## Results
| Run | v1 | v2 |
|---|---|---|
| Facts for ~2,500 films + ~9,000 people (1985–89, nothing cached) | ~95+ min (estimated from v1 rates: 1 query/min plus sequential entities) | **~2.5 min** (38 queries, 0 errors) |
| Statement order for ~2,100 films (1975–84) | ~19+ min (sequential, ~110/min) | **6.2 min**: ~595/min at peak, 337/min average after backing off on 19 × 429 (an earlier v2 run managed 118/min because one interval was shared by all workers; fixed) |
| Rerun of an already-fetched range | re-queries | ~30 s (only gaps) |

## Scaling estimate (1975–2026, ~30,000 US films and ~100,000 people)
- Bulk SPARQL: ~400 queries, about **10–15 minutes**.
- Statement order: ~30,000 entities at ~340–600/min, about **50–90 minutes**, and optional
  (the local IMDb billing file replaces it).
- IMDb billing (local only): one ~790 MB download plus a streaming scan of the whole file.

## Operating notes
- Be a good citizen: keep `--workers` at 4 or below and keep the per-host intervals.
  Wikimedia asks automated clients to limit concurrency and to send a descriptive User-Agent.
- If the query service imposes emergency limits again, pacing backs off automatically
  (the interval grows up to 60 s). Nothing needs changing.
- `python datapipe/fetch_wikidata.py --from-year Y0 --to-year Y1 [--statement-order]`,
  then `python datapipe/build_pack.py --from-year ... --to-year ...`.

## Source benchmark for a January 1990 campaign (November 2026)
Measured in this project's cloud session. The question: what is the fastest reliable way to get
the films in production and release around January 1990, their casts, and the people's careers,
without assuming Wikidata is required.

### Measured
| Step | Wikidata (SPARQL, existing pipeline) | IMDb bulk datasets (local only) | TMDb |
|---|---|---|---|
| Download | n/a (queries) | 1.16 GB (basics, crew, ratings, name.basics, akas) in **47 s** at 18–28 MB/s; title.principals (791 MB) ~30 s at the same rate | ID exports (movies 28 MB, people 81 MB) in 5 s. The exports hold id, title and popularity only (no year), so they can't select a year range. |
| Fetch / process | 1990–92 from nothing: **151 s**, 59 queries, 0 errors (1,474 films, 6,961 people). Re-listing all of 1975–92 after the film-class fix: 180 s; facts for the 80 new films: seconds | Streaming index of 1985–92, every title type and country: **130 s**, 683 MB peak memory, 65,707 titles, 254,674 people | **Not measured.** The saved credential was refused (HTTP 401, "Invalid API key"), most likely a v3 key where the v4 Read Access Token is needed. Estimate: ~40 requests/s documented limit; 1 request per film (`append_to_response=credits,release_dates`) and 1 per person, so ~6 min for 15k films and ~12 min for 30k people. |
| Wikidata→IMDb id map (P345, CC0) | 5 s for 1985–92 | | |

### Coverage, release years 1989–91 (`datapipe/compare_sources.py`)
| | Wikidata pack | IMDb |
|---|---|---|
| Top 25 grossing films of 1990 | 25/25 (after the fix below) | 25/25 |
| US-released features with ≥ 25,000 / ≥ 5,000 / ≥ 1,000 votes (205 / 519 / 1,095) | 88% / 78% / 61% | 100% (it defines these tiers) |
| Why notable films are missing | Non-US productions released in the US (*La Femme Nikita*, *My Left Foot*, *Kiki's Delivery Service*): the pack keeps US-origin films only | Has them; `akas` shows US release |
| Release date | Day precision for 41% of all pack films, 87% of films with ≥ 5,000 votes, 25/25 top films | **Year only** |
| Cast | ≥ 5 cast for 47% of films (statement order approximate) | ≥ 5 billed cast for 99%, with billing order and character names |
| Distributor / budget / box office | 55% / 11% / 9% (box office for 20/25 top films) | none |
| People | Gender 96%, full birth date 96%, spouses and partners with dates, awards | Gender only through actor/actress, birth **year** for 80%, no relationships or awards |
| Licence | CC0: can be committed and shipped | Personal, non-commercial use; no republication. Local only |

**Bug found by the comparison and fixed:** the film-list query took only items typed "film" (Q11424), so
features typed only "animated film" (Q202866) or "animated feature film" (Q29168811) were missing in every
year: *The Little Mermaid*, *The Rescuers Down Under*, *Beauty and the Beast*. Now there is one query per
class (a combined `VALUES` join timed out on the endpoint). `--relist` re-runs the lists; 1975–92 gained
113 films (7,328 → 7,441).

### Decision
**Wikidata stays the backbone, and IMDb bulk becomes a local overlay. TMDb is optional, for a few hundred
targeted lookups.**
- IMDb alone can't drive the simulation. Year-only dates can't place films on a weekly release calendar
  (which films are playing on 5 January 1990). It has no distributors, budgets or grosses and no documented
  relationships or awards, and nothing from it can be committed.
- Wikidata is the fastest source of those facts (2.5 min for three new years, incremental) and the only
  one whose data can ship in the public repo with provenance.
- IMDb is the fastest way to complete what Wikidata is thin on, all of it local only: full billed casts and
  character names (99% vs 47%), and notable foreign films released in the US (160 with ≥ 5,000 votes,
  1988–91). Cost: ~1.5 min download plus 2 min processing, no rate limits.
- TMDb fills the remaining gaps for notable films: day-precision dates for ~330 films with ≥ 1,000 votes and
  box office for ~800 of them (TMDb revenue is worldwide, not domestic). That's ~1,000 requests, under a
  minute at the documented limit. Its terms require attribution and non-commercial use and restrict
  storing data beyond caching, so TMDb data would stay local like IMDb. It needs a valid Read Access Token.

Estimated end-to-end for a January 1990 pack (1985–92): Wikidata ~3 min plus IMDb ~4 min, so **under
10 minutes** from an empty cache, and seconds when incremental. Optional TMDb: about 1 more minute.

### Provenance
Each fact keeps its source: committed pack = Wikidata (CC0); `data/local/` overlays = IMDb (and TMDb if
used), tagged by source and never committed. Where sources disagree (e.g. a release date), Wikidata's dated
claim wins unless it is only month or year precise.
