"""
Upper-tail box-office prototype (NOT the real engine; parameters UNCALIBRATED).

Question: can extreme hits emerge from audience behaviour, with no jackpot roll
and no cap, while ordinary films still fail at realistic rates?

Mechanisms added on top of box_office_sketch.py:
  1. Social proof: word-of-mouth reach grows with how many people have already
     seen the film ("everyone is talking about it"), saturating.
  2. Repeat viewing: deeply satisfied viewers can return, decaying with each visit.
  3. Seat capacity: weekly admissions cannot exceed screens x seats x shows x
     max occupancy. Excess demand stays in the queue (sell-outs lengthen runs).
  4. Exhibitor holdover: theatres keep or add screens while per-screen sales are
     strong; they drop screens when sales fall.
  5. Fat-tailed reception (Student-t): rare cultural-moment receptions are
     possible, but every film draws from the same distribution.

Nothing references historical records. The only hard limits are physical:
population, seats, and the length of time people keep wanting to see a film.
"""
from __future__ import annotations

import argparse
import hashlib
import math

import numpy as np

ERA = {
    "ticket_price": 3.36,
    "segments": {"youth_m": 22.0, "youth_f": 22.0, "adult_m": 60.0, "adult_f": 62.0},
    "base_watch_rate": 0.30,
    "interest_lapse": 0.07,
    "wom_contacts": 1.6,
    "social_proof_gain": 3.0,      # max extra multiple on WOM reach
    "social_proof_half": 0.06,     # penetration at which half that gain applies
    "repeat_base": 0.35,           # P(return) for a maximally satisfied viewer
    "repeat_decay": 0.5,           # each later visit is this much less likely
    "seats_per_screen": 280,
    "shows_per_week": 24,
    "max_occupancy": 0.45,         # sustained average fill when sold out
    "marketing_k": 0.045,
    "opening_weekend_share": 0.62,
    "screen_drop_threshold": 1100.0,
    "screen_add_threshold": 6000.0,
    "max_screens": 2200,
    "dom_rental": 0.45,
    "intl_ratio_mean": 0.70,
    "intl_rental": 0.40,
    "ancillary_coef": 0.45,
    "ancillary_floor": 1.0,
    "overhead_rate": 0.12,
}


def rng_for(seed: int, *keys) -> np.random.Generator:
    h = hashlib.sha256("|".join(map(str, (seed, *keys))).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def random_film(seed: int, i: int) -> dict:
    """A synthetic 1984 wide release. Inputs vary; the model is identical for all."""
    r = rng_for(seed, "film", i)
    budget = float(np.exp(r.normal(math.log(12), 0.6)))           # $M, median ~12
    pa = budget * float(np.exp(r.normal(math.log(0.6), 0.35)))
    quality = float(np.clip(r.normal(52, 13), 5, 98))
    fame = float(r.beta(1.4, 4))
    ip = float(r.choice([0.0, 0.0, 0.0, 0.2, 0.5], p=[0.5, 0.2, 0.1, 0.12, 0.08]))
    breadth = float(np.exp(r.normal(math.log(0.07), 0.45)))      # base appeal
    tilt = r.dirichlet([2, 2, 2, 2]) * 4                            # segment skew
    appeal = {s: breadth * t for s, t in zip(ERA["segments"], tilt)}
    screens = int(np.clip(400 + budget * 40 + r.normal(0, 150), 300, 1800))
    season = float(r.choice([0.9, 1.0, 1.15], p=[0.35, 0.4, 0.25]))
    return dict(budget=budget, pa=pa, quality=quality, fame=fame, ip=ip,
                appeal=appeal, screens=screens, season=season)


def simulate(f: dict, seed: int, i: int, weeks: int = 60) -> dict:
    e, r = ERA, rng_for(seed, "release", i)
    shock = float(r.standard_t(4)) * 0.16                    # fat-tailed reception
    sat = 1 / (1 + math.exp(-(f["quality"] - 55) / 7 - shock * 1.2))
    competition = float(np.clip(r.normal(1.0, 0.15), 0.6, 1.5))
    intl_ratio = e["intl_ratio_mean"] * math.exp(r.normal(0, 0.35))

    mkt = 1 - math.exp(-e["marketing_k"] * f["pa"])
    aware0 = 1 - (1 - mkt) * (1 - 0.55 * f["fame"]) * (1 - 0.6 * f["ip"])
    total_pop = sum(e["segments"].values())
    seg = {}
    for s, pop in e["segments"].items():
        ap = min(f["appeal"][s] * math.exp(0.5 * shock), 0.95)
        seg[s] = dict(pop=pop, unaware=pop * (1 - aware0), interested=pop * aware0 * ap,
                      watched=0.0, repeat_pool=0.0, appeal=ap)

    screens, weekly, visits_mult = f["screens"], [], 1.0
    for w in range(weeks):
        cap = screens * e["seats_per_screen"] * e["shows_per_week"] * e["max_occupancy"] / 1e6
        urgency = 1.25 if w == 0 else 1.0
        rate = min(0.9, e["base_watch_rate"] * urgency * f["season"] / competition)
        want = {s: (st["interested"] + st["repeat_pool"]) * rate for s, st in seg.items()}
        total_want = sum(want.values())
        fill = min(1.0, cap / total_want) if total_want > 0 else 0.0   # sell-outs
        penetration = sum(st["watched"] for st in seg.values()) / total_pop
        proof = 1 + e["social_proof_gain"] * penetration / (penetration + e["social_proof_half"])
        adm = 0.0
        for s, st in seg.items():
            pool = st["interested"] + st["repeat_pool"]
            if pool <= 0:
                continue
            go = want[s] * fill
            first = go * st["interested"] / pool
            rep = go - first
            st["interested"] -= first
            st["repeat_pool"] -= rep
            st["watched"] += first
            adm += go
            # people turned away by sell-outs mostly stay interested; others lapse
            st["interested"] *= 1 - e["interest_lapse"] * (0.4 if fill < 1 else 1.0)
            st["repeat_pool"] *= 0.8
            reached = min(st["unaware"], first * e["wom_contacts"] * proof * st["unaware"] / st["pop"])
            st["unaware"] -= reached
            st["interested"] += reached * min(st["appeal"] * (0.3 + 1.6 * sat), 0.95)
            st["repeat_pool"] += first * e["repeat_base"] * sat ** 3 + rep * e["repeat_base"] * sat ** 3 * e["repeat_decay"]
        gross = adm * e["ticket_price"]
        per_screen = gross * 1e6 / max(screens, 1)
        weekly.append(gross)
        if fill < 1.0:                                   # sold out: exhibitors pile in
            screens = min(e["max_screens"], int(screens * 1.35))
        elif per_screen > e["screen_add_threshold"]:
            screens = min(e["max_screens"], int(screens * 1.10))
        elif per_screen < e["screen_drop_threshold"]:
            screens = int(screens * 0.55)
        elif w > 3:
            screens = int(screens * 0.93)
        if screens < 15:
            break

    dom = sum(weekly)
    opening = weekly[0] * e["opening_weekend_share"]
    revenue = dom * e["dom_rental"] + dom * intl_ratio * e["intl_rental"] + max(e["ancillary_floor"], dom * e["ancillary_coef"])
    cost = (f["budget"] + f["pa"]) * (1 + e["overhead_rate"])
    return dict(dom=dom, opening=opening, mult=dom / max(opening, 1e-9), weeks=len(weekly),
                profit=revenue - cost, quality=f["quality"], shock=shock, sat=sat,
                cost=cost)


def hill_alpha(x: np.ndarray, top_frac: float = 0.05) -> float:
    """Hill estimator of the Pareto tail index on the top `top_frac` of values."""
    x = np.sort(x)[::-1]
    k = max(10, int(len(x) * top_frac))
    return float(1 / np.mean(np.log(x[:k] / x[k])))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--years", type=int, default=40, help="simulated release years")
    ap.add_argument("--per-year", type=int, default=150, help="wide releases per year")
    a = ap.parse_args()
    n = a.years * a.per_year
    res = [simulate(random_film(a.seed, i), a.seed, i) for i in range(n)]
    dom = np.array([x["dom"] for x in res])
    prof = np.array([x["profit"] for x in res])
    q = np.array([x["quality"] for x in res])
    mult = np.array([x["mult"] for x in res])
    by_year = dom.reshape(a.years, a.per_year)

    print(f"{n} synthetic 1984-style wide releases ({a.years} years x {a.per_year})\n")
    print("domestic gross ($M) percentiles")
    for p in (10, 25, 50, 75, 90, 99, 99.9):
        print(f"  p{p:<5} {np.percentile(dom, p):8.1f}")
    print(f"  max    {dom.max():8.1f}")
    print(f"\nyearly #1 film: median ${np.median(by_year.max(1)):.0f}M, "
          f"min ${by_year.max(1).min():.0f}M, max ${by_year.max(1).max():.0f}M")
    print(f"top 10% of films' share of all box office: "
          f"{np.sort(dom)[::-1][: n // 10].sum() / dom.sum():.0%}")
    print(f"Hill tail index (top 5%): {hill_alpha(dom):.2f}   (<2 means infinite-variance tail)")
    print(f"\nprofitable overall: {np.mean(prof > 0):.0%}")
    for lo, hi in ((0, 45), (45, 60), (60, 70), (70, 101)):
        m = (q >= lo) & (q < hi)
        print(f"  quality {lo:>2}-{hi:<3}: n={m.sum():5d}  profitable {np.mean(prof[m] > 0):4.0%}  "
              f"median dom ${np.median(dom[m]):6.1f}M  median multiplier {np.median(mult[m]):.1f}x")
    top = np.argsort(dom)[::-1][:5]
    print("\ntop 5 runs (what made them):")
    for i in top:
        x = res[i]
        print(f"  ${x['dom']:6.0f}M  opening ${x['opening']:5.1f}M  x{x['mult']:4.1f}  "
              f"{x['weeks']:2d} wks  quality {x['quality']:.0f}  reception shock {x['shock']:+.2f}")
