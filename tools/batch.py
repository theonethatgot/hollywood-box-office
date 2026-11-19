"""Headless batch runs for calibration (DESIGN.md §7.4).

    python tools/batch.py --seeds 4 --years 3 [--processes 4] [--json out.json]

Runs whole worlds with the protagonist fully delegated (an NPC in all but name)
and reports distributions: market size vs reference admissions, gross
percentiles, Hill tail index, multipliers, profitability by quality,
forecast bias, and career dynamics. Reference numbers come from config/eras.yaml.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hsim.core.config import era_value, load_config  # noqa: E402
from hsim.core.util import add_weeks, year  # noqa: E402
from hsim.service import genesis_state  # noqa: E402
from hsim.systems import market  # noqa: E402
from hsim.systems import tick as T  # noqa: E402


def run_world(args) -> dict:
    seed, years, start, pack = args
    cfg = load_config()
    st = genesis_state(cfg, {"seed": seed, "start": start, "data_pack": pack, "player": {"background": "unknown"}})
    st.orders.update({"interrupt_on": [], "let_agent_negotiate": ["lead", "colead", "supporting"],
                      "auto_accept_auditions": ["lead", "colead", "supporting"]})
    snap0 = {pid: (p.fame, p.bankability) for pid, p in st.people.items() if "actor" in p.roles}
    end = add_weeks(st.date, 52 * years + 30)   # +30 weeks so the last year's films finish their runs
    while st.date < end:
        T.advance(st, cfg, end)
        for d in list(st.decisions.values()):   # protagonist: resolve anything left like an NPC would
            if d.status == "pending":
                from hsim.systems import decisions as D
                D.resolve(st, cfg, d.id, d.default, {}, delegated_by="batch")
    y0 = year(start)
    films = []
    for p in st.projects.values():
        if p.stage != "released" or not p.release_date or not (y0 <= year(p.release_date) < y0 + years):
            continue
        infl = market.infl(cfg, year(p.release_date))
        films.append({"year": year(p.release_date), "dom": p.domestic / infl, "open": p.opening / infl,
                      "forecast": (p.forecast_opening or 0) / infl, "budget": p.budget / infl,
                      "profit": None if p.profit is None else p.profit / infl,
                      "quality": p.quality.get("overall", 50), "critic": p.critic_score,
                      "weeks": p.run.get("week", 0)})
    careers = []
    for pid, p in st.people.items():
        if "actor" not in p.roles or pid not in snap0:
            continue
        careers.append({"fame0": snap0[pid][0], "fame1": p.fame, "bank0": snap0[pid][1], "bank1": p.bankability,
                        "talent": p.talent, "films": sum(1 for c in p.credits if c.get("kind") == "film"),
                        "active": p.active})
    totals = {y: v for y, v in st.market.get("year_admissions", {}).items()}
    return {"seed": seed, "films": films, "careers": careers, "admissions": totals}


def hill(x, frac=0.05):
    x = np.sort(np.asarray(x))[::-1]
    k = max(5, int(len(x) * frac))
    if len(x) <= k + 1:
        return float("nan")
    return float(1 / np.mean(np.log(x[:k] / x[k])))


def report(results, cfg, start_year, years) -> dict:
    films = [f for r in results for f in r["films"]]
    dom = np.array([f["dom"] for f in films]) / 1e6
    out = {"worlds": len(results), "films": len(films)}
    adm = []
    for r in results:
        for y in range(start_year, start_year + years):
            if str(y) in r["admissions"]:
                adm.append((y, r["admissions"][str(y)] / 1e6, era_value(cfg, "admissions_m", y)))
    out["admissions_sim_vs_ref_m"] = [(y, round(s), round(ref)) for y, s, ref in adm]
    out["films_per_world_year"] = round(len(films) / (len(results) * years), 1)
    out["domestic_1980usd_m_percentiles"] = {p: round(float(np.percentile(dom, p)), 1) for p in (10, 25, 50, 75, 90, 99)}
    out["domestic_max_m"] = round(float(dom.max()), 1)
    yearly_top = []
    for r in results:
        for y in range(start_year, start_year + years):
            ds = [f["dom"] for f in r["films"] if f["year"] == y]
            if ds:
                yearly_top.append(max(ds) / 1e6)
    out["yearly_no1_m"] = {"median": round(float(np.median(yearly_top)), 1), "max": round(float(max(yearly_top)), 1)}
    out["top10pct_share"] = round(float(np.sort(dom)[::-1][: max(1, len(dom) // 10)].sum() / dom.sum()), 3)
    out["hill_alpha_top5pct"] = round(hill(dom), 2)
    mult = np.array([f["dom"] / f["open"] for f in films if f["open"] > 0])
    out["multiplier_percentiles"] = {p: round(float(np.percentile(mult, p)), 2) for p in (10, 50, 90)}
    fb = np.array([math.log(f["open"] / f["forecast"]) for f in films if f["open"] > 0 and f["forecast"] > 0])
    out["forecast_log_bias_median"] = round(float(np.median(fb)), 3)
    out["forecast_log_error_sd"] = round(float(np.std(fb)), 3)
    fin = [f for f in films if f["profit"] is not None]
    out["profitable_share"] = round(float(np.mean([f["profit"] > 0 for f in fin])), 3)
    bands = {}
    for lo, hi in ((0, 45), (45, 55), (55, 65), (65, 101)):
        sel = [f for f in fin if lo <= f["quality"] < hi]
        if sel:
            bands[f"{lo}-{hi}"] = {"n": len(sel), "profitable": round(float(np.mean([f["profit"] > 0 for f in sel])), 2),
                                   "median_dom_m": round(float(np.median([f["dom"] for f in sel])) / 1e6, 1)}
    out["by_quality"] = bands
    cs = [c for r in results for c in r["careers"]]
    out["careers"] = {
        "actors": len(cs),
        "unknown_to_known_rate": round(float(np.mean([c["fame1"] > 0.1 for c in cs if c["fame0"] < 0.01])), 4),
        "stars_end": int(sum(c["fame1"] > 0.3 for c in cs)),
        "stars_start": int(sum(c["fame0"] > 0.3 for c in cs)),
        "median_films_per_actor": float(np.median([c["films"] for c in cs])),
        "talent_vs_fame_gain_corr": round(float(np.corrcoef([c["talent"] for c in cs],
                                                            [c["fame1"] - c["fame0"] for c in cs])[0, 1]), 3),
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--first-seed", type=int, default=1)
    ap.add_argument("--years", type=int, default=2)
    ap.add_argument("--start", default="1980-01-04")
    ap.add_argument("--processes", type=int, default=1)
    ap.add_argument("--json", default=None)
    ap.add_argument("--historical", action="store_true", help="use the default historical data pack")
    a = ap.parse_args()
    pack = None
    if a.historical:
        from hsim.core.config import ROOT
        pack = str(ROOT / load_config()["history"]["default_pack"])
    jobs = [(s, a.years, a.start, pack) for s in range(a.first_seed, a.first_seed + a.seeds)]
    if a.processes > 1:
        with ProcessPoolExecutor(a.processes) as ex:
            results = list(ex.map(run_world, jobs))
    else:
        results = [run_world(j) for j in jobs]
    rep = report(results, load_config(), int(a.start[:4]), a.years)
    print(json.dumps(rep, indent=2))
    if a.json:
        Path(a.json).write_text(json.dumps({"report": rep, "results": results}))


if __name__ == "__main__":
    main()
