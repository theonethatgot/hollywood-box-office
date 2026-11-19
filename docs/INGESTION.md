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
