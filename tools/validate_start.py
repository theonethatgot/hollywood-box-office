"""Smoke test for a historical start date (default 5 January 1990).

    python tools/validate_start.py --start 1990-01-05 [--seed 1] [--weeks 0]

Checks: stages and attachments of major films against their documented production
history, pre-start credits of anchor actors, future-information leakage, and the
casting opportunities open to a generic protagonist. Reports aggregate coverage.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hsim.core.config import load_config  # noqa: E402
from hsim.core.util import age_on  # noqa: E402
from hsim.service import genesis_state  # noqa: E402

# (title, acceptable stages on 1990-01-05 from the documented shoot, documented lead)
ANCHORS_1990 = [
    ("Born on the Fourth of July", {"released"}, "Tom Cruise"),
    ("Driving Miss Daisy", {"released"}, "Morgan Freeman"),
    ("The Little Mermaid", {"released"}, None),
    ("The Hunt for Red October", {"post", "awaiting_release"}, "Sean Connery"),
    ("Pretty Woman", {"post", "awaiting_release"}, "Richard Gere"),
    ("Total Recall", {"post", "awaiting_release"}, "Arnold Schwarzenegger"),
    ("Dick Tracy", {"post", "awaiting_release"}, "Warren Beatty"),
    ("Back to the Future Part III", {"shooting", "post"}, "Michael J. Fox"),
    ("Ghost", {"post", "shooting"}, "Patrick Swayze"),
    ("Goodfellas", {"post"}, "Robert De Niro"),
    ("Dances with Wolves", {"post"}, "Kevin Costner"),
    ("The Silence of the Lambs", {"shooting", "post", "prepro"}, "Jodie Foster"),
    ("The Godfather Part III", {"shooting", "prepro"}, "Al Pacino"),
    ("Die Hard 2", {"shooting", "prepro"}, "Bruce Willis"),
    ("Misery", {"prepro", "shooting", "development"}, "James Caan"),
    ("Edward Scissorhands", {"prepro", "development"}, "Johnny Depp"),
    ("Home Alone", {"prepro", "development"}, "Macaulay Culkin"),
    ("Terminator 2: Judgment Day", {"development"}, "Arnold Schwarzenegger"),
]
CREDIT_ANCHORS = [("Tom Cruise", ["Top Gun", "Rain Man"]), ("Jack Nicholson", ["Chinatown", "Batman"]),
                  ("Meryl Streep", ["Sophie's Choice", "Out of Africa"]), ("Al Pacino", ["The Godfather", "Scarface"]),
                  ("Michelle Pfeiffer", ["Dangerous Liaisons", "The Fabulous Baker Boys"]),
                  ("Denzel Washington", ["Glory", "Cry Freedom"])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="1990-01-05")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--pack", default=None)
    a = ap.parse_args()
    cfg = load_config()
    if a.pack:
        cfg["history"]["default_pack"] = a.pack
    t0 = time.time()
    st = genesis_state(cfg, {"seed": a.seed, "start": a.start, "data_pack": cfg["history"]["default_pack"],
                             "player": {"name": "Test Actor", "gender": "m", "birth": "1962-05-05", "background": "working"}})
    secs = time.time() - t0
    start = st.date
    hist = [p for p in st.people.values() if p.historical]
    h = st.market["history"]
    print(f"genesis {start}: {secs:.0f}s; {len(st.people)} people ({len(hist)} real: "
          f"{sum(p.id.startswith('imdb:') for p in hist)} from the local IMDb overlay), {len(st.projects)} projects")
    print(f"pack {h['version']}; overlay {h['overlay']}; real films loaded through {h['loaded_through']}")
    real = [p for p in st.projects.values() if p.historical_ref]
    print("real projects by stage:", dict(Counter(p.stage for p in real)),
          f"(of which IMDb-only: {sum(p.historical_ref.startswith('imdb:') for p in real)})")
    print("fictional projects by stage:", dict(Counter(p.stage for p in st.projects.values() if not p.historical_ref)))
    print("studios:", ", ".join(f"{s.name} ({s.slate_per_year:.0f}/yr)" for s in st.studios.values() if s.slate_per_year))

    by_title = {}
    for p in real:
        by_title.setdefault(p.title, p)
    ok = 0
    print("\nanchor films (stage on the start date vs documented production; lead attachment):")
    for title, stages, lead in ANCHORS_1990 if start.startswith("1990") else []:
        p = by_title.get(title)
        if not p:
            print(f"  MISSING  {title}")
            continue
        roles = [st.roles[r] for r in p.role_ids]
        who = [st.people[r.cast_id or r.intended].name for r in roles if (r.cast_id or r.intended)][:3]
        good_stage = p.stage in stages
        good_lead = lead is None or lead in who
        ok += good_stage and good_lead
        print(f"  {'ok ' if good_stage and good_lead else 'OFF'} {title[:30]:30s} {p.stage:16s} "
              f"(shoot {p.shoot_start}..{p.shoot_end}, release {p.release_date}) {', '.join(who)}")
    if start.startswith("1990"):
        print(f"  {ok}/{len(ANCHORS_1990)} match stage and lead")

    print("\npre-start credits of anchor actors:")
    names = {p.name: p for p in hist}
    for name, films in CREDIT_ANCHORS:
        p = names.get(name)
        if not p:
            print(f"  MISSING {name}")
            continue
        titles = [c["title"] for c in p.credits if c.get("kind") == "prior"]
        print(f"  {name}: {len(titles)} prior credits; " + ", ".join(f"{f} {'yes' if f in titles else 'NO'}" for f in films)
              + f"; latest {max((c['year'] for c in p.credits if c.get('kind') == 'prior'), default='-')}; "
              f"fame {p.fame:.2f}, draw {p.bankability:.0f}, quote ${p.quote / 1e6:.2f}M")

    # ---- leakage
    yr = int(start[:4])
    leaks = []
    for p in hist:
        for c in p.credits:
            if c.get("kind") == "prior" and c["year"] > yr:
                leaks.append(f"{p.name}: prior credit {c['title']} {c['year']}")
        for y in re.findall(r"\b(19\d\d|20\d\d)\b", re.sub(r"'[^']*'", "", p.bio)):     # not film titles
            if int(y) > yr:
                leaks.append(f"{p.name}: bio mentions {y}")
        if p.awards and any(int(x["year"]) > yr for x in p.awards):
            leaks.append(f"{p.name}: award after start")
    released_future = [p.title for p in real if p.stage == "released" and p.release_date >= start]
    print(f"\nleakage: {len(leaks)} problems" + (": " + "; ".join(leaks[:5]) if leaks else "")
          + (f"; released-in-future films: {released_future[:5]}" if released_future else ""))

    # ---- opportunities for a generic actor
    pl = st.player
    age = age_on(pl.birth, start)
    open_roles = [r for r in st.roles.values() if not r.cast_id and st.projects[r.project_id].stage in ("development", "prepro")
                  and r.status in ("open", "auditioning")]
    fits = [r for r in open_roles if r.gender == pl.gender and r.age_min - 6 <= age <= r.age_max + 6]
    print(f"\ncasting: {len(open_roles)} uncast roles in development/pre-production; {len(fits)} suit a "
          f"{age}-year-old {'man' if pl.gender == 'm' else 'woman'} "
          f"({sum(1 for r in fits if not r.intended)} not earmarked for a documented actor; "
          f"by size: {dict(Counter(r.importance for r in fits if not r.intended))})")
    bar = cfg["history"]["attached_offer_bankability"]
    auditioned = [r for r in fits if r.intended and r.importance != "featured"
                  and st.people[r.intended].bankability < bar]
    print(f"  principal parts that will be auditioned (documented actor favoured, not yet a draw): {len(auditioned)} "
          f"by size: {dict(Counter(r.importance for r in auditioned))}")


if __name__ == "__main__":
    main()
