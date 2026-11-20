"""Studio slate decisions: weekly greenlights to sustain each studio's output."""
from __future__ import annotations

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_weeks
from ..world import genesis


def roster(st: WorldState, cfg: dict) -> None:
    """First tick of each year: studios founded this year open, defunct ones stop greenlighting,
    and slates and budgets follow the era settings."""
    from ..core.util import year
    yr = year(st.date)
    if st.market.get("roster_year") == yr:
        return
    st.market["roster_year"] = yr
    for spec in cfg["studios"]:
        s = st.studios.get(spec["id"])
        if s is None:
            if genesis.studio_active(spec, yr):
                st.studios[spec["id"]] = genesis.make_studio(cfg, st.seed, spec, yr)
                st.log("studio_founded", f"{spec['name']} is now releasing films.", salience=1, public=True)
            continue
        if genesis.studio_active(spec, yr):
            s.slate_per_year = genesis.era_number(spec["slate"], yr)
            s.budget_median = genesis.era_number(spec["budget_median"], yr)
        elif s.slate_per_year > 0:
            s.slate_per_year = 0
            st.log("studio_closed", f"{s.name} has stopped developing new films.", salience=1, public=True)


def step(st: WorldState, cfg: dict) -> None:
    roster(st, cfg)
    for sid, studio in sorted(st.studios.items()):
        g = R.stream(st.seed, "greenlight", sid, st.date)
        rate = studio.slate_per_year / 52
        # documented films this studio will start within the year count toward its slate
        horizon = add_weeks(st.date, 52)
        hist = sum(1 for p in st.projects.values() if p.studio_id == sid and p.historical_ref
                   and p.stage == "development" and p.prepro_start and p.prepro_start <= horizon)
        rate *= max(0.0, 1 - hist / max(1.0, studio.slate_per_year))
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
