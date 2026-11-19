"""Weekly box office: audience compartments with shared attention competition.

Per film and audience segment:  unaware → aware → interested → watched,
plus repeat viewing, word of mouth with social proof, seat capacity, and
exhibitor screen decisions (see DESIGN.md §7, prototypes/tail_sketch.py).
All films in release compete for the same segments' attention each week.
No outcome references historical records; the hard limits are physical.
"""
from __future__ import annotations

import math

from ..core import rng as R
from ..core.config import era_value
from ..core.state import WorldState
from ..core.util import add_weeks, money, year
from . import careers, market


def _stars(st, p):
    out = []
    for rid in p.role_ids:
        r = st.roles[rid]
        if r.cast_id and r.importance in ("lead", "colead"):
            out.append((st.people[r.cast_id], 1.0 if r.importance == "lead" else 0.6))
    return out


def _awareness0(st, cfg, p) -> float:
    bo = cfg["box_office"]
    pa_real_m = p.pa_budget / 1e6 / market.infl(cfg, year(st.date))
    studio = st.studios[p.studio_id]
    mkt = 1 - math.exp(-bo["marketing_k"] * pa_real_m * studio.marketing_eff)
    fame = max([a.fame * w for a, w in _stars(st, p)] or [0.0])
    hook = (p.hook - 50) / 100
    return 1 - (1 - mkt) * (1 - bo["fame_awareness"] * fame) * (1 - max(0.0, 0.25 * hook))


def _star_mult(st, p) -> float:
    return 1 + sum(w * a.fame * (a.appeal - 0.3) * 1.5 for a, w in _stars(st, p))


def _segments(cfg, date) -> dict:
    pop = market.moviegoing_pop_m(cfg, date)
    return {s: share * pop for s, share in cfg["box_office"]["segments"].items()}


def _initial_screens(st, cfg, p) -> int:
    bo = cfg["box_office"]
    real_m = p.budget / 1e6 / market.infl(cfg, year(st.date))
    mx = era_value(cfg, "max_wide_screens", year(st.date))
    s = bo["base_screens"] + bo["screens_per_budget_m"] * real_m
    if st.studios[p.studio_id].tier == "mini":
        s *= 0.75
    return int(max(150, min(mx * 0.8, s)))


def init_run(st: WorldState, cfg: dict, p) -> None:
    g = R.stream(st.seed, "run-init", p.id)
    aware = _awareness0(st, cfg, p)
    sm = _star_mult(st, p)
    shock = p.reception_shock or 0.0
    segs = {}
    for s, pop in _segments(cfg, st.date).items():
        ap = p.breadth * p.segment_tilt.get(s, 1.0) * sm * math.exp(0.5 * shock)
        if s.startswith("adult"):
            ap *= 0.75 + 0.5 * (p.critic_score or 50) / 100
        ap = min(ap, 0.95)
        segs[s] = {"pop": pop, "unaware": pop * (1 - aware), "interested": pop * aware * ap,
                   "watched": 0.0, "repeat": 0.0, "appeal": ap}
    screens = p.run.get("planned_screens") or _initial_screens(st, cfg, p)
    p.run = {"segments": segs, "screens": screens, "week": 0, "active": True,
             "intl_ratio": era_value(cfg, "international_ratio", year(st.date)) * math.exp(g.normal(0, 0.35))}


def expected_opening(st: WorldState, cfg: dict, p, observed_quality: float) -> float:
    """What the industry expects: same model, neutral reception, no competition detail."""
    bo = cfg["box_office"]
    aware = _awareness0(st, cfg, p)
    sm = _star_mult(st, p)
    adm = 0.0
    for s, pop in _segments(cfg, p.release_date or st.date).items():
        ap = min(0.95, p.breadth * p.segment_tilt.get(s, 1.0) * sm * (1.0 if not s.startswith("adult") else 0.75 + 0.5 * observed_quality / 100))
        adm += pop * aware * ap * bo["base_watch_rate"] * bo["opening_urgency"] * market.seasonality(cfg, p.release_date or st.date) / 1.15
    # competition tracking can see: films in release now, plus films dated to open
    # within two weeks either side (release calendars are public in the trades)
    pop = sum(_segments(cfg, st.date).values())
    rel = p.release_date or st.date
    lo, hi = add_weeks(rel, -2), add_weeks(rel, 2)
    others = 0.0
    for q in st.projects.values():
        if q.id == p.id:
            continue
        if q.stage == "released" and q.run.get("active"):
            others += sum(sg["interested"] + sg["repeat"] for sg in q.run["segments"].values())
        elif q.stage == "awaiting_release" and q.release_date and lo <= q.release_date <= hi:
            others += cfg["box_office"]["dated_rival_weight"] * _expected_interest(st, cfg, q)
    adm /= 1 + bo["competition_k"] * others / pop
    screens = p.run.get("planned_screens") or _initial_screens(st, cfg, p)
    cap = screens * bo["seats_per_screen"] * bo["shows_per_week"] * bo["max_occupancy"] / 1e6
    adm = min(adm, cap)
    return adm * 1e6 * market.ticket_price(cfg, p.release_date or st.date) * bo["opening_weekend_share"]


def _expected_interest(st, cfg, q) -> float:
    """Neutral-reception estimate of the interested audience a dated film will open with."""
    if q.pa_budget <= 0:
        return 0.0
    aware = _awareness0(st, cfg, q)
    sm = _star_mult(st, q)
    return sum(pop * aware * min(0.95, q.breadth * q.segment_tilt.get(s, 1.0) * sm)
               for s, pop in _segments(cfg, q.release_date or st.date).items())


def step(st: WorldState, cfg: dict, quiet: bool = False) -> None:
    bo = cfg["box_office"]
    active = [p for _, p in sorted(st.projects.items()) if p.stage == "released" and p.run.get("active")]
    if not active:
        return
    # attention competition: total interest per segment across all films
    totals = {}
    for p in active:
        for s, sg in p.run["segments"].items():
            totals[s] = totals.get(s, 0.0) + sg["interested"] + sg["repeat"]
    season = market.seasonality(cfg, st.date)
    price = market.ticket_price(cfg, st.date)
    infl = market.infl(cfg, year(st.date))
    chart = []
    for p in active:
        run = p.run
        segs = run["segments"]
        sat = p.satisfaction if p.satisfaction is not None else 0.5
        screens = run["screens"]
        cap = screens * bo["seats_per_screen"] * bo["shows_per_week"] * bo["max_occupancy"] / 1e6
        urgency = bo["opening_urgency"] if run["week"] == 0 else 1.0
        want = {}
        for s, sg in segs.items():
            others = totals[s] - sg["interested"] - sg["repeat"]
            comp = 1 + bo["competition_k"] * others / sg["pop"]
            rate = min(0.9, bo["base_watch_rate"] * urgency * season / comp)
            want[s] = (sg["interested"] + sg["repeat"]) * rate
        total_want = sum(want.values())
        fill = min(1.0, cap / total_want) if total_want > 0 else 0.0
        pen = sum(sg["watched"] for sg in segs.values()) / sum(sg["pop"] for sg in segs.values())
        proof = 1 + bo["social_proof_gain"] * pen / (pen + bo["social_proof_half"])
        adm = 0.0
        for s, sg in segs.items():
            pool = sg["interested"] + sg["repeat"]
            if pool <= 0:
                continue
            go = want[s] * fill
            first = go * sg["interested"] / pool
            rep = go - first
            sg["interested"] -= first
            sg["repeat"] -= rep
            sg["watched"] += first
            adm += go
            sg["interested"] *= 1 - bo["interest_lapse"] * (0.4 if fill < 1 else 1.0)
            sg["repeat"] *= 0.8
            reached = min(sg["unaware"], first * bo["wom_contacts"] * proof * sg["unaware"] / sg["pop"])
            sg["unaware"] -= reached
            sg["interested"] += reached * min(sg["appeal"] * (0.3 + 1.6 * sat), 0.95)
            sg["repeat"] += (first + rep * bo["repeat_decay"]) * bo["repeat_base"] * sat ** 3
        gross = adm * 1e6 * price
        per_screen_real = gross / max(screens, 1) / infl
        run["week"] += 1
        wk = {"week": run["week"], "date": st.date, "gross": round(gross, 0), "screens": screens,
              "admissions": round(adm * 1e6, 0)}
        p.weekly.append(wk)
        p.domestic += gross
        if run["week"] == 1:
            p.opening = round(gross * bo["opening_weekend_share"], 0)
        chart.append(p)
        # exhibitors respond
        if fill < 1.0:
            run["screens"] = int(min(era_value(cfg, "max_wide_screens", year(st.date)), screens * 1.35))
        elif per_screen_real > bo["screen_add_threshold"]:
            run["screens"] = int(min(era_value(cfg, "max_wide_screens", year(st.date)), screens * 1.10))
        elif per_screen_real < bo["screen_drop_threshold"]:
            run["screens"] = int(screens * 0.55)
        elif run["week"] > 3:
            run["screens"] = int(screens * 0.93)
        if run["screens"] < 15 or run["week"] >= bo["max_weeks"]:
            run["active"] = False
    chart.sort(key=lambda p: -p.weekly[-1]["gross"])
    for rank, p in enumerate(chart, 1):
        p.weekly[-1]["rank"] = rank
    _record_chart(st, chart)
    if not quiet:
        _chart_events(st, cfg, chart)
    for p in chart:
        if p.run["week"] == 1 and not quiet:
            careers.on_opening(st, cfg, p)
        if not p.run["active"]:
            finalize(st, cfg, p, quiet=quiet)


def _record_chart(st, chart) -> None:
    st.market["chart"] = {"date": st.date, "top": [
        {"project": p.id, "title": p.title, "studio": st.studios[p.studio_id].name, "week": p.run["week"],
         "gross": p.weekly[-1]["gross"], "total": round(p.domestic, 0), "screens": p.weekly[-1]["screens"]}
        for p in chart[:10]]}
    y = st.date[:4]
    yt = st.market.setdefault("year_totals", {})
    yt[y] = round(yt.get(y, 0.0) + sum(p.weekly[-1]["gross"] for p in chart), 0)
    ya = st.market.setdefault("year_admissions", {})
    ya[y] = round(ya.get(y, 0.0) + sum(p.weekly[-1]["admissions"] for p in chart), 0)


def _chart_events(st, cfg, chart) -> None:
    top = chart[0]
    wkd = top.weekly[-1]["gross"] * cfg["box_office"]["opening_weekend_share"]
    st.log("chart", f"'{top.title}' ({st.studios[top.studio_id].name}) was the #1 film this weekend with about "
                    f"{money(wkd)} (week {top.run['week']}, {money(top.domestic)} total).",
           refs={"project": top.id}, salience=1, public=True)
    for p in chart:
        cast = [st.roles[r].cast_id for r in p.role_ids if st.roles[r].cast_id]
        if st.player_id in cast and p.run["week"] <= 6:
            w = p.weekly[-1]
            label = "opened" if p.run["week"] == 1 else f"took in week {p.run['week']}"
            amt = p.opening if p.run["week"] == 1 else w["gross"]
            span = "over its opening weekend" if p.run["week"] == 1 else "this week"
            st.log("player_film_gross", f"'{p.title}' {label} with {money(amt)} {span} (rank #{w['rank']}, "
                                        f"{w['screens']} screens; {money(p.domestic)} to date).",
                   actors=[st.player_id], refs={"project": p.id}, salience=4 if p.run["week"] == 1 else 2, public=True)


def finalize(st: WorldState, cfg: dict, p, quiet: bool = False) -> None:
    bo = cfg["box_office"]
    infl = market.infl(cfg, year(st.date))
    p.intl = round(p.domestic * p.run["intl_ratio"], 0)
    dom_rentals = p.domestic * bo["dom_rental"]
    intl_rentals = p.intl * bo["intl_rental"]
    ancillary = max(bo["ancillary_floor_m"] * 1e6 * infl, p.domestic * bo["ancillary_coef"])
    cost = (p.actual_cost or p.budget) + p.pa_budget
    overhead = cost * bo["overhead_rate"]
    gross_receipts = dom_rentals + intl_rentals + ancillary
    gross_part = 0.0
    payouts = []
    for rid in p.role_ids:
        r = st.roles[rid]
        if r.cast_id and r.points_type == "gross":
            amt = gross_receipts * r.points / 100
            gross_part += amt
            payouts.append((r.cast_id, amt, "gross"))
    # "Hollywood accounting": net profit for net-point participants
    dist_fee = (dom_rentals + intl_rentals) * bo["distribution_fee"]
    interest = (p.actual_cost or p.budget) * 0.10
    net_receipts = gross_receipts - dist_fee - p.pa_budget - (p.actual_cost or p.budget) - overhead - interest - gross_part
    for rid in p.role_ids:
        r = st.roles[rid]
        if r.cast_id and r.points_type == "net" and net_receipts > 0:
            payouts.append((r.cast_id, net_receipts * r.points / 100, "net"))
    profit = gross_receipts - cost - overhead - sum(a for _, a, _ in payouts)
    p.revenue = {"domestic_rentals": round(dom_rentals), "intl_rentals": round(intl_rentals),
                 "ancillary": round(ancillary), "gross_participations": round(gross_part),
                 "net_receipts_statement": round(net_receipts), "total_cost": round(cost + overhead)}
    p.profit = round(profit, 0)
    st.studios[p.studio_id].cash += profit
    if not quiet:
        from . import finance
        for pid, amt, kind in payouts:
            finance.pay(st, cfg, pid, amt, f"{kind}-point participation in '{p.title}'")
        careers.on_run_end(st, cfg, p)
        cast = [st.roles[r].cast_id for r in p.role_ids if st.roles[r].cast_id]
        inv = st.player_id in cast
        st.log("run_end", f"'{p.title}' finished its theatrical run with {money(p.domestic)} domestic"
                          f" and an estimated {money(p.intl)} overseas.",
               actors=cast, refs={"project": p.id}, salience=3 if inv else 1, public=True,
               data={"profit": p.profit, "net_receipts": round(net_receipts)})
        if inv:
            for rid in p.role_ids:
                r = st.roles[rid]
                if r.cast_id == st.player_id and r.points_type == "net":
                    msg = ("Your net-profit statement shows the film still 'in deficit' on paper — your net points pay nothing."
                           if net_receipts <= 0 else "Your net points actually paid out — a rarity.")
                    st.log("participation", msg, actors=[st.player_id], refs={"project": p.id}, salience=2, public=False)
