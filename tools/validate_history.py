"""Historical snapshot validation report: what is documented vs simulated.

    python tools/validate_history.py --start 1980-01-04 [--weeks 26]

Reports release-date precision, distributor documentation, character-name
documentation, real directors on fictional projects, divergences, and anomalies
(people working after their documented death, films released before shooting).
"""
from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hsim.core.config import load_config  # noqa: E402
from hsim.service import genesis_state  # noqa: E402
from hsim.systems import decisions as D  # noqa: E402
from hsim.systems import tick as T  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="1980-01-04")
    ap.add_argument("--weeks", type=int, default=26)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    cfg = load_config()
    st = genesis_state(cfg, {"seed": a.seed, "start": a.start, "data_pack": cfg["history"]["default_pack"],
                             "player": {"background": "working"}})
    st.orders.update({"interrupt_on": []})
    from hsim.core.util import add_weeks
    end = add_weeks(st.date, a.weeks)
    while st.date < end:
        T.advance(st, cfg, end)
        for d in D.pending(st):
            D.resolve(st, cfg, d.id, d.default, {}, delegated_by="validate")
    hp = [p for p in st.projects.values() if p.historical_ref]
    roles = [st.roles[r] for p in hp for r in p.role_ids if st.roles[r].importance != "featured"]
    gen = [p for p in st.projects.values() if not p.historical_ref and p.director_id]
    div = collections.Counter(e["type"] for e in st.events if e["type"] == "history_diverged")
    recast = [st.roles[r] for p in hp for r in p.role_ids
              if st.roles[r].intended and st.roles[r].cast_id and st.roles[r].cast_id != st.roles[r].intended]
    dead_working = [(p.name, c["project_id"]) for p in st.people.values() if p.death
                    for c in p.calendar if c["start"] > p.death]
    bad_order = [p.title for p in st.projects.values() if p.release_date and p.shoot_end and p.release_date < p.shoot_end
                 and p.stage != "released"]
    print(f"Snapshot {a.start} + {a.weeks} weeks (seed {a.seed})")
    print(f"  real films in pipeline/release: {len(hp)}")
    print(f"    release date documented to the day: {sum(not p.date_approx for p in hp)}; approximate: {sum(p.date_approx for p in hp)}")
    print(f"    distributor documented: {sum(bool(p.distributor_note) and p.distributor_note != 'distributor not documented' for p in hp)}; "
          f"not documented: {sum(p.distributor_note == 'distributor not documented' for p in hp)}")
    print(f"    principal character names documented: {sum(r.name_documented for r in roles)} of {len(roles)} (rest simulated)")
    print(f"    principal roles recast away from the documented actor: {len(recast)} (simulated divergence)")
    print(f"  divergence events logged: {sum(div.values())}")
    print(f"  fictional projects: {len(gen)}; with a real director: {sum(st.people[p.director_id].historical for p in gen)}")
    print(f"  anomalies: commitments after death {len(dead_working)}; release before wrap {len(bad_order)}")


if __name__ == "__main__":
    main()
