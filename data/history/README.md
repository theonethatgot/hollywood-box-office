# Historical data packs

| File | Source | Licence | Contents |
|---|---|---|---|
| `wikidata_1965_1992.json` (default) | [Wikidata](https://www.wikidata.org/) | CC0 1.0 (public domain) | 9,549 US-origin feature films released 1965–1992, including animated features (date with precision, genres, cast in statement order, directors, distributors, cost and box office where recorded, series), and 16,136 people (gender, birth/death, manner of death, spouses and partners with dates, major awards and nominations with dates, sitelink count). Supports start dates from about 1970 to 1992 |
| `wikidata_1975_1989.json` | Wikidata | CC0 1.0 | The previous pack, kept so saves created with it still replay. Lacks animated features typed only as "animated film" |

## Rules
- Packs hold **documented facts only**. Attribute estimates (fame, bankability,
  hidden talent...) are computed at load time for the chosen start date by
  `hsim/world/historical.py`, so one pack serves every start date it covers.
- **Only openly licensed sources are committed.** IMDb's non-commercial datasets
  may be used for *local* enrichment, but anything derived from them belongs in
  `data/local/` (gitignored) and must never be committed to this public repository.
- Raw downloads live in `data/raw/` (gitignored).

## Local IMDb enrichment (optional, never committed)
`data/local/imdb_overlay.json` adds IMDb billing order and character names to pack
films, notable foreign films released in the US that the pack lacks, and the IMDb-only
people their casts need (birth year only). The loader applies it automatically when it
exists and was built for the current pack. Without it, the simulation runs on the
committed Wikidata pack alone.

## Rebuilding
```bash
python datapipe/fetch_wikidata.py --from-year 1965 --to-year 1992 --statement-order
python datapipe/build_pack.py --from-year 1965 --to-year 1992
# optional local enrichment (downloads ~2 GB of IMDb datasets to data/raw/imdb/)
python datapipe/imdb_billing.py --stage ids --from-year 1965 --to-year 1992
python datapipe/imdb_billing.py --stage download     # title.principals; fetch the others the same way
python datapipe/imdb_index.py --from-year 1965 --to-year 1992
python datapipe/imdb_overlay.py --pack data/history/wikidata_1965_1992.json
```
Later years: fetch the new range (`--from-year 1993 --to-year 1996`), rebuild the pack with the
wider range, then rebuild the overlay. Rolling intake picks up whatever the pack covers.
The fetcher is incremental (everything is kept in `data/raw/wikidata/store.sqlite`).
See `docs/INGESTION.md` for measurements.

## Known limitations
- Cast order comes from Wikidata statement order, which usually but not always follows billing
  (the local IMDb overlay replaces it with billing order).
- Release dates: about 40% of films have a day-precise date; the rest are known to the month or
  year and are spread deterministically across that period (marked approximate). Some notable
  films are affected (*Born on the Fourth of July* is dated only "1989").
- Production dates are not documented: shoot and post-production windows are inferred from the
  release date, so long post-productions (e.g. *Dances with Wolves*) start later than they really did.
- Coverage of minor cast, budgets and grosses is uneven. Missing budgets are estimated from studio norms.
- Personality is not documented: real people get the same personality priors as fictional NPCs, marked `prior` in provenance.
- Where no spouse is documented, romantic orientation is a population prior, marked `prior (not documented)`.
