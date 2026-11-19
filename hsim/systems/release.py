"""Release dating, tracking forecasts, reviews and openings."""
from __future__ import annotations

import math

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_weeks, clamp, money, next_friday, sigmoid, year
from . import boxoffice, careers, market


def schedule(st: WorldState, cfg: dict, p) -> None:
    """Studio dates a finished film: earliest slot after marketing lead time,
    nudged toward strong seasons and away from crowded weekends."""
    p.stage = "awaiting_release"
    earliest = next_friday(add_weeks(st.date, cfg["development"]["marketing_lead_weeks"]))
    if p.release_date and p.release_date >= earliest:
        _set_pa(st, cfg, p)
        return
    real_m = p.budget / 1e6 / market.infl(cfg, year(st.date))
    horizon = 14 if real_m > 10 else 6
    taken = {}
    for q in st.projects.values():
        if q.release_date and q.stage in ("awaiting_release", "released"):
            taken[q.release_date] = taken.get(q.release_date, 0) + 1
    g = R.stream(st.seed, "release-date", p.id)
    best, best_u = earliest, -1e9
    for k in range(horizon + 1):
        dte = add_weeks(earliest, k)
        u = market.seasonality(cfg, dte) * (1 + 0.04 * real_m) - 0.12 * taken.get(dte, 0) - 0.02 * k + g.normal(0, 0.03)
        if u > best_u:
            best, best_u = dte, u
    p.release_date = best
    _set_pa(st, cfg, p)


def _set_pa(st, cfg, p) -> None:
    if p.pa_budget:
        return
    g = R.stream(st.seed, "pa", p.id)
    dev = cfg["development"]
    p.pa_budget = round(p.budget * dev["pa_ratio_median"] * math.exp(g.normal(0, dev["pa_ratio_sd"])), 0)


def step(st: WorldState, cfg: dict) -> None:
    for pid, p in sorted(st.projects.items()):
        if p.stage != "awaiting_release" or not p.release_date:
            continue
        if p.forecast_opening is None and add_weeks(p.release_date, -3) <= st.date:
            _tracking(st, cfg, p)
        if p.release_date <= st.date:
            open_film(st, cfg, p)


def _involves_player(st, p) -> bool:
    return any(st.roles[r].cast_id == st.player_id for r in p.role_ids)


def _tracking(st, cfg, p) -> None:
    """Industry tracking: the model's own expectation (no reception luck) plus survey noise."""
    _set_pa(st, cfg, p)
    g = R.stream(st.seed, "tracking", p.id)
    test_screening = p.quality.get("overall", 50) + g.normal(0, 8)       # noisy read of the finished film
    est = boxoffice.expected_opening(st, cfg, p, observed_quality=test_screening)
    p.forecast_opening = round(est * math.exp(g.normal(0, 0.22)), 0)
    # studio reacts to its own tracking and test screenings: back winners, cut losses
    rb = cfg["release_response"]
    real_m = p.budget / 1e6 / market.infl(cfg, year(st.date))
    ratio = (p.forecast_opening / 1e6 / market.infl(cfg, year(st.date))) / max(0.2, rb["expected_open_per_budget"] * real_m)
    lift = clamp(math.log(max(ratio, 1e-3)) * rb["pa_elasticity"] + (test_screening - 55) / 100 * rb["screening_weight"],
                 -rb["max_cut"], rb["max_boost"])
    if abs(lift) > 0.05:
        p.pa_budget = round(p.pa_budget * (1 + lift), 0)
        p.run["planned_screens"] = int(boxoffice._initial_screens(st, cfg, p) * (1 + 0.6 * lift))
        est = boxoffice.expected_opening(st, cfg, p, observed_quality=test_screening)
        p.forecast_opening = round(est * math.exp(g.normal(0, 0.22)), 0)
        if _involves_player(st, p):
            word = "expanding" if lift > 0 else "scaling back"
            st.log("marketing_shift", f"Encouraged by tracking and test screenings, the studio is {word} the campaign for '{p.title}'."
                   if lift > 0 else f"After soft tracking, the studio is {word} the campaign for '{p.title}'.",
                   actors=[st.player_id], refs={"project": p.id}, salience=2, public=False)
    if _involves_player(st, p):
        st.log("tracking", f"Pre-release tracking projects '{p.title}' to open around {money(p.forecast_opening)}.",
               actors=[st.player_id], refs={"project": p.id}, salience=2, public=True)


def open_film(st: WorldState, cfg: dict, p, quiet: bool = False) -> None:
    if p.forecast_opening is None:
        _tracking(st, cfg, p)
    bo = cfg["box_office"]
    g = R.stream(st.seed, "reception", p.id)
    q = p.quality or {"overall": 50, "entertainment": 50, "emotional": 50, "craft": 50, "originality": 50, "spectacle": 50}
    shock = float(g.standard_t(bo["reception_t_df"])) * bo["reception_scale"]
    p.reception_shock = round(shock, 4)
    critic = 0.3 * q["craft"] + 0.35 * q["originality"] + 0.35 * q["emotional"] + 15 * shock + g.normal(0, 7)
    p.critic_score = round(clamp(critic + (critic - 50) * 0.6), 1)   # stretch: critics are decisive
    enjoy = 0.45 * q["entertainment"] + 0.3 * q["emotional"] + 0.25 * q["spectacle"]
    p.satisfaction = round(sigmoid((enjoy - cfg["reception"]["sat_mid"]) / cfg["reception"]["sat_width"] + shock * 1.2), 4)
    p.audience_grade = _grade(p.satisfaction)
    p.stage = "released"
    boxoffice.init_run(st, cfg, p)
    if not quiet:
        inv = _involves_player(st, p)
        st.log("reviews", f"Reviews for '{p.title}': {_review_phrase(p.critic_score)} "
                          f"(critics' aggregate {p.critic_score:.0f}/100); opening-night audiences gave it {p.audience_grade}.",
               actors=[st.roles[r].cast_id for r in p.role_ids if st.roles[r].cast_id], refs={"project": p.id},
               salience=3 if inv else 1, public=True)
        careers.on_release_reviews(st, cfg, p)


def _grade(sat: float) -> str:
    for cut, gr in ((0.9, "an A+"), (0.82, "an A"), (0.74, "an A-"), (0.66, "a B+"), (0.58, "a B"),
                    (0.5, "a B-"), (0.42, "a C+"), (0.34, "a C"), (0.25, "a C-"), (0.15, "a D")):
        if sat >= cut:
            return gr
    return "an F"


def _review_phrase(score: float) -> str:
    return ("rapturous" if score >= 85 else "strong" if score >= 70 else "mixed-to-positive" if score >= 58
            else "mixed" if score >= 45 else "poor" if score >= 30 else "savage")


def prime_recent_releases(st: WorldState, cfg: dict) -> None:
    """Genesis: films released in the weeks before the start date run their
    early weeks silently so the market isn't empty on day one."""
    start = st.date
    recent = sorted((p for p in st.projects.values() if p.stage == "released" and p.release_date < start),
                    key=lambda p: p.release_date)
    if not recent:
        return
    first = recent[0].release_date
    dte = first
    while dte < start:
        st.date = dte
        for p in recent:
            if p.release_date == dte:
                p.stage = "awaiting_release"
                open_film(st, cfg, p, quiet=True)
        boxoffice.step(st, cfg, quiet=True)
        dte = add_weeks(dte, 1)
    st.date = start
