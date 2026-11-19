"""The weekly tick and interruptible time advancement."""
from __future__ import annotations

from ..core.state import WorldState
from ..core.util import add_days
from . import (agents, awards, boxoffice, careers, casting, decisions, finance, jobbing, personal,
               production, release, social, studios, tvcasting)

STOP_EVENT_TYPES = {
    "premieres": {"player_film_gross"},
    "nominations": {"nomination", "oscar_win"},
    "romance": {"chemistry"},
}


def tick(st: WorldState, cfg: dict) -> None:
    """Simulate the week beginning on st.date (a Friday), then move to next Friday."""
    decisions.expire(st, cfg)
    studios.step(st, cfg)
    casting.step(st, cfg)
    tvcasting.step(st, cfg)
    jobbing.step(st, cfg)
    jobbing.settle(st, cfg)
    production.step(st, cfg)
    release.step(st, cfg)
    boxoffice.step(st, cfg)
    awards.step(st, cfg)
    social.step(st, cfg)
    personal.step(st, cfg)
    agents.step(st, cfg)
    agents.memory_fades(st, cfg)
    careers.step(st, cfg)
    finance.step(st, cfg)
    st.date = add_days(st.date, 7)


def advance(st: WorldState, cfg: dict, until: str, max_weeks: int | None = None) -> dict:
    """Run weekly ticks until `until`, stopping early at the player's decisions
    or at significant events the player asked to be interrupted for."""
    max_weeks = max_weeks or cfg["advance"]["max_weeks_per_call"]
    start, weeks = st.date, 0
    stop_types = set()
    for key in st.orders.get("interrupt_on", []):
        stop_types |= STOP_EVENT_TYPES.get(key, set())
    reason = "reached target date"
    while st.date < until and weeks < max_weeks:
        if decisions.pending(st, interrupting_only=True):
            reason = "decision required"
            break
        mark = len(st.events)
        tick(st, cfg)
        weeks += 1
        if decisions.pending(st, interrupting_only=True):
            reason = "decision required"
            break
        hit = [e for e in st.events[mark:] if e["type"] in stop_types and st.player_id in e["actors"]]
        if hit:
            reason = f"significant event: {hit[0]['type']}"
            break
    else:
        if weeks >= max_weeks:
            reason = "week limit"
    return {"from": start, "to": st.date, "weeks": weeks, "stopped": reason,
            "pending": [d.id for d in decisions.pending(st)]}
