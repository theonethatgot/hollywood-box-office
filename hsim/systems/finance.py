"""Money flows for people: fees, commissions, taxes, living costs, participations.

Every payment is split into net-to-person, agency commission and tax, and the
three are tallied so tests can check that nothing is created or lost.
"""
from __future__ import annotations

from ..core.config import era_value
from ..core.state import WorldState
from ..core.util import money, year


def pay(st: WorldState, cfg: dict, person_id: str, gross: float, memo: str, *, commissionable: bool = True) -> None:
    p = st.people[person_id]
    commission = gross * cfg["finance"]["agent_commission"] if (commissionable and p.agent_id) else 0.0
    tax = (gross - commission) * era_value(cfg, "effective_tax_rate", year(st.date))
    net = gross - commission - tax
    p.cash += net
    t = st.market.setdefault("money", {"gross": 0.0, "net": 0.0, "commission": 0.0, "tax": 0.0, "costs": 0.0})
    t["gross"] += gross
    t["net"] += net
    t["commission"] += commission
    t["tax"] += tax
    if p.controller == "player":
        st.market.setdefault("player_ledger", []).append(
            {"date": st.date, "memo": memo, "gross": round(gross, 2), "commission": round(commission, 2),
             "tax": round(tax, 2), "net": round(net, 2)})
        st.log("payment", f"Payment received: {memo} — {money(gross)} gross, {money(net)} after commission and tax.",
               actors=[p.id], salience=1, public=False)


def step(st: WorldState, cfg: dict) -> None:
    """Monthly living costs on the first tick of each month."""
    if st.date[8:10] > "07":
        return
    t = st.market.setdefault("money", {"gross": 0.0, "net": 0.0, "commission": 0.0, "tax": 0.0, "costs": 0.0})
    fc = cfg["finance"]
    from .market import infl
    from ..core.util import days_between
    day_job = fc["day_job_monthly"] * infl(cfg, year(st.date))
    for pid, p in sorted(st.people.items()):
        if p.death or not p.active:
            continue
        p.cash -= p.monthly_costs
        idle = p.last_work is None or days_between(p.last_work, st.date) > fc["day_job_idle_weeks"] * 7
        working = any(c["start"] <= st.date <= c["end"] for c in p.calendar)
        if "actor" in p.roles and p.fame < fc["day_job_fame_max"] and idle and not working:
            p.cash += day_job
            if p.controller == "player":
                st.market.setdefault("player_ledger", []).append(
                    {"date": st.date, "memo": "day job (restaurant shifts, temp work)", "net": round(day_job, 2)})
        t["costs"] += p.monthly_costs
        if p.controller == "player":
            st.market.setdefault("player_ledger", []).append(
                {"date": st.date, "memo": "monthly living costs", "net": -round(p.monthly_costs, 2)})
            if p.cash < 0:
                st.log("money_trouble", f"You are {money(-p.cash)} in the red after this month's bills.",
                       actors=[p.id], salience=3, public=False)
