"""
Box-office prototype sketch (NOT the real engine).

Purpose: show that the proposed audience-compartment model produces
causally driven, seeded, reproducible outcomes. Parameters are
UNCALIBRATED placeholders chosen to be in a plausible 1984 range.

Model per audience segment s:
    Unaware -> Aware -> Interested -> Watched
               (Aware-but-uninterested and Interested-but-lapsed drop out)

Drivers: marketing spend, star fame, IP familiarity, hidden true quality,
segment appeal, word of mouth, critic score, seasonality, competition,
screen count (exhibitors drop the film as per-screen gross falls).
"""
from __future__ import annotations

import argparse
import hashlib
import math
from dataclasses import dataclass, field

import numpy as np

# ---------------------------------------------------------------- config ---
ERA_1984 = {
    "ticket_price": 3.36,                 # approx. US avg ticket, 1984
    "segments": {                         # moviegoing population (millions)
        "youth_m": 22.0, "youth_f": 22.0, "adult_m": 60.0, "adult_f": 62.0,
    },
    "base_watch_rate": 0.30,              # weekly P(interested -> buys ticket)
    "interest_lapse": 0.07,               # weekly P(interested -> gives up)
    "wom_contacts": 2.2,                  # conversations per new viewer
    "marketing_k": 0.045,                 # awareness per $M (diminishing)
    "opening_weekend_share": 0.62,        # share of week-1 gross on Fri-Sun
    "screen_drop_threshold": 900.0,       # $/screen/week below which screens are cut
    "dom_rental_by_week": [0.55, 0.50, 0.45, 0.40, 0.38, 0.35],
    "intl_ratio_mean": 0.70,              # intl gross / domestic (1980s-ish)
    "intl_rental": 0.40,
    "ancillary_coef": 0.55,               # video + pay TV + network TV vs dom gross
    "ancillary_floor": 1.5,               # $M minimum ancillary
    "overhead_rate": 0.10,
}


@dataclass
class FilmSpec:
    title: str
    genre: str
    production_budget: float              # $M negative cost
    pa_budget: float                      # $M prints & advertising
    true_quality: float                   # 0-100 hidden
    critic_appeal: float                  # 0-100 hidden (art/craft dimension)
    star_fame: float                      # 0-1 share of public aware of lead
    ip_familiarity: float                 # 0-1
    segment_appeal: dict = field(default_factory=dict)   # base P(interest|aware)
    screens: int = 1200
    season: float = 1.0                   # 1.0 neutral, >1 summer/holiday


def stream_rng(seed: int, *keys: str) -> np.random.Generator:
    """Named, independent RNG stream: adding a new system never reshuffles others."""
    h = hashlib.sha256(("|".join([str(seed), *keys])).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def simulate(film: FilmSpec, seed: int, era=ERA_1984, weeks=16, verbose=False):
    rng = stream_rng(seed, "release", film.title)

    # --- realized uncertainty (causal, bounded by underlying conditions) ---
    reception_shock = rng.normal(0, 0.18)              # how the zeitgeist takes it
    critic_score = float(np.clip(film.critic_appeal + rng.normal(0, 8), 0, 100))
    competition = float(np.clip(rng.normal(1.0, 0.15), 0.6, 1.5))
    intl_ratio = era["intl_ratio_mean"] * math.exp(rng.normal(0, 0.35))

    # satisfaction of those who watch (drives word of mouth): 0..1
    satisfaction = 1 / (1 + math.exp(-(film.true_quality - 55) / 9 - reception_shock * 2))

    # --- pre-release awareness ---
    mkt_aware = 1 - math.exp(-era["marketing_k"] * film.pa_budget)
    base_aware = 1 - (1 - mkt_aware) * (1 - 0.55 * film.star_fame) * (1 - 0.6 * film.ip_familiarity)

    seg = {}
    for s, pop in era["segments"].items():
        appeal = film.segment_appeal.get(s, 0.15) * math.exp(reception_shock)
        if s.startswith("adult"):                      # adults read reviews
            appeal *= 0.75 + 0.5 * critic_score / 100
        appeal = min(appeal, 0.95)
        aware = pop * base_aware
        seg[s] = {"pop": pop, "unaware": pop - aware, "interested": aware * appeal,
                  "watched": 0.0, "appeal": appeal}

    screens = film.screens
    weekly, admissions_total = [], 0.0
    for w in range(weeks):
        week_adm = 0.0
        freshness = 1.25 if w == 0 else 1.0           # opening-week urgency
        avail = min(1.0, screens / film.screens)
        for s, st in seg.items():
            rate = era["base_watch_rate"] * freshness * film.season / competition * avail
            rate = min(rate, 0.9)
            new_watch = st["interested"] * rate
            lapse = (st["interested"] - new_watch) * era["interest_lapse"]
            st["interested"] -= new_watch + lapse
            st["watched"] += new_watch
            week_adm += new_watch
            # word of mouth: viewers reach unaware people; valence = satisfaction
            reached = min(st["unaware"],
                          new_watch * era["wom_contacts"] * st["unaware"] / st["pop"])
            st["unaware"] -= reached
            wom_appeal = st["appeal"] * (0.3 + 1.6 * satisfaction)
            st["interested"] += reached * min(wom_appeal, 0.95)
            # WOM also re-activates aware-but-unconvinced people a little
            st["interested"] += new_watch * 0.05 * (satisfaction - 0.5)
            st["interested"] = max(st["interested"], 0.0)
        gross = week_adm * era["ticket_price"]          # $M (pop in millions)
        per_screen = gross * 1e6 / max(screens, 1)
        weekly.append({"week": w + 1, "gross": gross, "screens": screens,
                       "per_screen": per_screen})
        admissions_total += week_adm
        if per_screen < era["screen_drop_threshold"]:
            screens = int(screens * 0.55)
        elif w > 2:
            screens = int(screens * 0.88)
        if screens < 15:
            break

    dom = sum(x["gross"] for x in weekly)
    opening_wknd = weekly[0]["gross"] * era["opening_weekend_share"]
    rent = era["dom_rental_by_week"]
    dom_rentals = sum(x["gross"] * rent[min(i, len(rent) - 1)] for i, x in enumerate(weekly))
    intl = dom * intl_ratio
    intl_rentals = intl * era["intl_rental"]
    ancillary = max(era["ancillary_floor"], dom * era["ancillary_coef"])
    revenue = dom_rentals + intl_rentals + ancillary
    cost = film.production_budget + film.pa_budget
    overhead = cost * era["overhead_rate"]
    profit = revenue - cost - overhead

    out = {"opening_weekend": opening_wknd, "domestic": dom, "multiplier": dom / opening_wknd,
           "international": intl, "worldwide": dom + intl, "critic_score": critic_score,
           "satisfaction": satisfaction, "studio_revenue": revenue, "total_cost": cost + overhead,
           "profit": profit, "weeks": weekly}
    if verbose:
        print(f"\n=== {film.title} (seed {seed}) ===")
        print(f"critic score {critic_score:5.1f} | audience satisfaction {satisfaction:.2f} "
              f"| reception shock {reception_shock:+.2f} | competition x{competition:.2f}")
        for x in weekly[:8]:
            print(f"  wk{x['week']:>2}  ${x['gross']:6.2f}M  screens {x['screens']:>5}  "
                  f"per-screen ${x['per_screen']:,.0f}")
        print(f"opening wknd ${opening_wknd:.1f}M | domestic ${dom:.1f}M "
              f"(x{dom/opening_wknd:.1f}) | intl ${intl:.1f}M")
        print(f"studio revenue ${revenue:.1f}M vs cost ${cost+overhead:.1f}M "
              f"-> profit ${profit:+.1f}M")
    return out


SLEEPER = FilmSpec("Sleeper Comedy", "comedy", 11.0, 7.0, true_quality=74, critic_appeal=70,
                   star_fame=0.30, ip_familiarity=0.0,
                   segment_appeal={"youth_m": 0.12, "youth_f": 0.13, "adult_m": 0.07, "adult_f": 0.09})
HYPED = FilmSpec("Hyped Action", "action", 32.0, 18.0, true_quality=44, critic_appeal=35,
                 star_fame=0.75, ip_familiarity=0.25, screens=1800, season=1.15,
                 segment_appeal={"youth_m": 0.19, "youth_f": 0.07, "adult_m": 0.10, "adult_f": 0.04})

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1984)
    ap.add_argument("--batch", type=int, default=2000)
    a = ap.parse_args()
    for f in (SLEEPER, HYPED):
        simulate(f, a.seed, verbose=True)
    print(f"\n=== distribution over {a.batch} seeds (p10 / p50 / p90) ===")
    for f in (SLEEPER, HYPED):
        r = [simulate(f, s) for s in range(a.batch)]
        def q(k):
            v = np.array([x[k] for x in r])
            return "  ".join(f"{np.percentile(v, p):7.1f}" for p in (10, 50, 90))
        print(f"\n{f.title}")
        for k in ("opening_weekend", "domestic", "multiplier", "worldwide", "profit"):
            print(f"  {k:<16} {q(k)}")
        print(f"  P(profit>0)       {np.mean([x['profit'] > 0 for x in r]):.2f}")
    # determinism check
    assert simulate(SLEEPER, 7)["domestic"] == simulate(SLEEPER, 7)["domestic"]
    print("\ndeterminism check: same seed -> identical result  OK")
