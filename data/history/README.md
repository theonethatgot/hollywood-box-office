# Historical data packs

| File | Source | Licence | Contents |
|---|---|---|---|
| `wikidata_1975_1984.json` | [Wikidata](https://www.wikidata.org/) | CC0 1.0 (public domain) | US-origin films released 1975–1984 (date, genres, cast in statement order, directors, distributors, cost and box office where recorded, series); the top-billed cast and directors (gender, birth/death, manner of death, spouses with dates, major awards and nominations with dates, sitelink count) |

## Rules
- Packs hold **documented facts only**. Attribute estimates (fame, bankability,
  hidden talent...) are computed at load time for the chosen start date by
  `hsim/world/historical.py`, so one pack serves every start date it covers.
- **Only openly licensed sources are committed.** IMDb's non-commercial datasets
  may be used for *local* enrichment, but anything derived from them belongs in
  `data/local/` (gitignored) and must never be committed to this public repository.
- Raw downloads live in `data/raw/` (gitignored).

## Rebuilding
```bash
python datapipe/fetch_wikidata.py --from-year 1975 --to-year 1984 --focus-year 1980
python datapipe/build_pack.py --from-year 1975 --to-year 1984
```
The fetcher is resumable and rate-limit aware. The Wikidata query service may
restrict clients to about one query per minute, so a full fetch can take over an hour.

## Known limitations
- Cast order comes from Wikidata statement order, which usually but not always follows billing.
- Coverage of minor cast, budgets and grosses is uneven. Missing budgets are estimated from studio norms.
- Personality is not documented: real people get the same personality priors as fictional NPCs, marked `prior` in provenance.
- Where no spouse is documented, romantic orientation is a population prior, marked `prior (not documented)`.
