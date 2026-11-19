"""Studio slate decisions: weekly greenlights to sustain each studio's output."""
from __future__ import annotations

from ..core import rng as R
from ..core.state import WorldState
from ..world import genesis


def step(st: WorldState, cfg: dict) -> None:
    for sid, studio in sorted(st.studios.items()):
        g = R.stream(st.seed, "greenlight", sid, st.date)
        rate = studio.slate_per_year / 52
        if studio.cash < 0:
            rate *= 0.5            # distressed studios cut back
        if g.random() < rate:
            key = f"gl-{st.date}"
            p = genesis.make_project(st, cfg, studio, key, st.date)
            genesis.schedule_from_greenlight(cfg, p, st.date, g)
            p.stage = "prepro"
            from . import casting
            casting.attach_director(st, cfg, p)
            art = "an" if p.genre[0] in "aeiou" else "a"
            st.log("greenlight", f"{studio.name} greenlit '{p.title}', {art} {p.genre} picture. {p.premise}",
                   refs={"project": p.id}, salience=1, public=True)
