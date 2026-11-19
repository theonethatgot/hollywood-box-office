"""Player decisions, standing orders and delegation.

The player character is an NPC with a human controller. When a choice arises:
  1. Standing orders may resolve it (logged as delegated).
  2. Otherwise a Decision is created; interrupting decisions stop time.
Delegated choices use exactly the same utility functions NPCs use.
"""
from __future__ import annotations

from .. import models as M
from ..core.state import WorldState
from ..core.util import add_days

HANDLERS: dict = {}   # kind -> fn(st, cfg, decision, choice, params) -> str (summary)


def handler(kind):
    def wrap(fn):
        HANDLERS[kind] = fn
        return fn
    return wrap


def create(st: WorldState, cfg: dict, kind: str, summary: str, options: list, *, deadline_days: int,
           default: str, refs: dict, interrupt: bool = True, context: str = "") -> M.Decision:
    did = st.new_id("dec")
    dec = M.Decision(id=did, kind=kind, summary=summary, options=options,
                     deadline=add_days(st.date, deadline_days), default=default, refs=refs,
                     created=st.date, interrupt=interrupt)
    if context:
        dec.refs["context"] = context
    st.decisions[did] = dec
    st.log("decision_created", summary, actors=[st.player_id], refs={"decision": did}, salience=4, public=False)
    return dec


def pending(st: WorldState, interrupting_only: bool = False) -> list:
    return [d for _, d in sorted(st.decisions.items())
            if d.status == "pending" and (d.interrupt or not interrupting_only)]


def resolve(st: WorldState, cfg: dict, decision_id: str, choice: str, params: dict | None = None,
            delegated_by: str | None = None) -> str:
    dec = st.decisions.get(decision_id)
    if dec is None:
        raise ValueError(f"unknown decision {decision_id}")
    if dec.status != "pending":
        raise ValueError(f"decision {decision_id} is already {dec.status}")
    base = choice.split("(")[0]
    valid = [o.split("(")[0] for o in dec.options]
    if base not in valid:
        raise ValueError(f"'{choice}' is not an option for {decision_id}; options: {dec.options}")
    dec.status = "resolved"
    dec.resolution = {"choice": base, "params": params or {}, "date": st.date, "delegated_by": delegated_by}
    text = HANDLERS[dec.kind](st, cfg, dec, base, params or {})
    if delegated_by:
        st.delegated.append({"rule": delegated_by, "decision": dec.id, "text": text})
    return text


def expire(st: WorldState, cfg: dict) -> None:
    """Non-interrupting decisions past their deadline take their documented default."""
    for dec in pending(st):
        if dec.deadline < st.date:
            resolve(st, cfg, dec.id, dec.default, {}, delegated_by="deadline_default")
            dec.status = "expired"
