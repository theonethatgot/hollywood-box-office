"""Career mobility analysis: can actors who start badly improve?

    python tools/mobility.py --seeds 4 --years 3 --processes 4

Runs historical worlds headlessly and follows every represented actor aged
20-45 at the start. Work per year = film roles booked + jobs completed.
Reports, for the bottom quarter of first-year workers, how many climb to the
first-year median or better by the final year, broken down by hidden presence,
plus how casting-director goodwill evolves for that group (to detect a
self-reinforcing negative spiral).
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hsim.core.config import load_config  # noqa: E402
from hsim.core.util import add_weeks, age_on  # noqa: E402
from hsim.service import genesis_state  # noqa: E402
from hsim.systems import decisions as D  # noqa: E402
from hsim.systems import tick as T  # noqa: E402


def run(args):
    seed, years = args
    cfg = load_config()
    st = genesis_state(cfg, {"seed": seed, "start": "1980-01-04", "data_pack": cfg["history"]["default_pack"],
                             "player": {"background": "working"}})
    st.orders.update({"interrupt_on": [], "let_agent_negotiate": ["lead", "colead", "supporting", "featured"]})
    cohort = {p.id: {"presence": p.presence, "talent": p.talent, "craft0": p.craft}
              for p in st.actors() if p.agent_id and 20 <= age_on(p.birth, st.date) <= 45 and p.controller != "player"}
    cds = {pid for pid, p in st.people.items() if "casting_director" in p.roles}
    goodwill = {}
    end = add_weeks(st.date, 52 * years)
    y0 = int(st.date[:4])
    while st.date < end:
        T.advance(st, cfg, end, max_weeks=52)
        for d in D.pending(st):
            D.resolve(st, cfg, d.id, d.default, {}, delegated_by="batch")
        yr = str(int(st.date[:4]) - 1) if st.date[5:] < "01-08" else st.date[:4]
        for r in st.rels.values():
            for a, b in ((r.a, r.b), (r.b, r.a)):
                if a in cds and b in cohort:
                    goodwill.setdefault(b, {})[yr] = goodwill.get(b, {}).get(yr, 0.0) + r.affinity
    work = {pid: {str(y0 + k): 0 for k in range(years)} for pid in cohort}
    for e in st.events:
        if e["type"] == "cast":
            for a in e["actors"]:
                if a in work and e["date"][:4] in work[a]:
                    work[a][e["date"][:4]] += 1
    for pid in cohort:
        for c in st.people[pid].credits:
            if c.get("kind") == "job" and str(c.get("year")) in work[pid]:
                work[pid][str(c["year"])] += 1
        cohort[pid]["craft1"] = st.people[pid].craft
        cohort[pid]["work"] = work[pid]
        cohort[pid]["goodwill"] = goodwill.get(pid, {})
    return cohort


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--years", type=int, default=3)
    ap.add_argument("--processes", type=int, default=4)
    a = ap.parse_args()
    with ProcessPoolExecutor(a.processes) as ex:
        results = list(ex.map(run, [(s, a.years) for s in range(1, a.seeds + 1)]))
    rows = [v for r in results for v in r.values()]
    ys = sorted(rows[0]["work"])
    first, last = ys[0], ys[-1]
    w1 = np.array([r["work"][first] for r in rows])
    q25, med = np.percentile(w1, 25), np.median(w1)
    low = [r for r in rows if r["work"][first] <= q25]
    out = {"actors": len(rows), "years": ys, "first_year_work_q25": float(q25), "first_year_work_median": float(med)}
    out["low_group"] = len(low)
    out["low_reached_median_by_final_year"] = round(float(np.mean([r["work"][last] >= med for r in low])), 3)
    out["low_any_work_in_final_year"] = round(float(np.mean([r["work"][last] > 0 for r in low])), 3)
    out["low_no_work_any_year"] = round(float(np.mean([all(v == 0 for v in r["work"].values()) for r in low])), 3)
    out["low_craft_change_mean"] = round(float(np.mean([r["craft1"] - r["craft0"] for r in low])), 2)
    pres = np.array([r["presence"] for r in rows])
    t1, t2 = np.percentile(pres, [33, 67])
    for name, sel in (("presence_low", lambda r: r["presence"] <= t1), ("presence_mid", lambda r: t1 < r["presence"] <= t2),
                      ("presence_high", lambda r: r["presence"] > t2)):
        grp = [r for r in low if sel(r)]
        if grp:
            out[f"{name}_low_group_n"] = len(grp)
            out[f"{name}_reached_median"] = round(float(np.mean([r["work"][last] >= med for r in grp])), 3)
    gw = {y: [r["goodwill"].get(y, 0.0) for r in low] for y in ys}
    out["low_group_mean_cd_goodwill_by_year"] = {y: round(float(np.mean(v)), 2) for y, v in gw.items()}
    out["low_group_share_negative_goodwill_by_year"] = {y: round(float(np.mean([x < 0 for x in v])), 3) for y, v in gw.items()}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
