"""Episodic television casting: where working actors actually audition.

Each active series shoots during the season (summer to early spring) and needs
guest parts every week. Guest parts are cast the same way as films: the show's
casting director brings in people they know, agents submit clients (agent hustle x
fit x the client's strategy), the CD calls in a handful, they audition, the best
read gets the part. Most auditions are lost; losing still leaves impressions and
feedback. The same rules apply to every actor.
"""
from __future__ import annotations

from ..core import rng as R
from ..core.state import WorldState
from ..core.util import add_days, add_weeks, age_on, clamp, money, year
from . import market

REGISTER = {"police": "thriller", "medical": "drama", "sitcom": "comedy", "detective": "thriller",
            "soap": "drama", "action": "action"}


def in_season(date: str) -> bool:
    m = int(date[5:7])
    return m >= 7 or m <= 3


def _show_cd(st, show) -> str | None:
    cds = sorted(pid for pid, p in st.people.items() if "casting_director" in p.roles and p.employer == "independent")
    if not cds:
        return None
    return cds[int(R.unit(st.seed, "show-cd", show.id) * len(cds))]


def step(st: WorldState, cfg: dict) -> None:
    if not in_season(st.date):
        return
    tc = cfg["tv"]
    actors = [p for p in st.actors() if p.agent_id or p.controller == "player"]
    by_gender = {}
    for p in actors:
        by_gender.setdefault(p.gender, []).append(p)
    for sid, show in sorted(st.shows.items()):
        if not show.active:
            continue
        n_parts = int(R.unit(st.seed, "tv-parts", sid, st.date) * (tc["guest_parts_per_week"] + 1))
        for k in range(n_parts):
            _cast_part(st, cfg, show, k, by_gender)


def _cast_part(st, cfg, show, k, by_gender) -> None:
    from ..world.people import character_name
    from ..world.tv import EPISODES, guest_part
    from .agents import agent_hustle, pass_reason_tv, strategy_fit
    from .casting import agency_visibility
    g = R.stream(st.seed, "tv-part", show.id, st.date, k)
    gender = "m" if g.random() < 0.55 else "f"
    center = int(g.integers(20, 62))
    reg = REGISTER[show.genre]
    part = guest_part(g, gender)               # the description always matches the role's gender
    episode = f"an episode about {EPISODES[show.genre][int(g.integers(len(EPISODES[show.genre])))]}"
    start = add_days(st.date, 14)
    end = add_weeks(start, 1)
    cd_id = _show_cd(st, show)
    cd = st.people.get(cd_id) if cd_id else None
    regulars = set(show.regulars)

    def tv_fit(p):
        age = age_on(p.birth, st.date)
        age_f = max(0.0, 1 - abs(age - center) / 9)
        return age_f * (0.55 + 0.45 * p.range.get(reg, 40) / 100)

    def known_u(p):
        rel = st.rel(cd_id, p.id, create=False) if cd_id else None
        return (0.25 * p.critical_rep + 0.25 * p.craft + 30 * tv_fit(p) + 40 * min(0.5, p.fame) + agency_visibility(st, p)
                + (rel.affinity / 3 if rel else 0) + 10 * R.gauss(st.seed, "tv-known", show.id, st.date, k, p.id))

    from .casting import available
    pool = [p for p in by_gender.get(gender, []) if p.id not in regulars and tv_fit(p) > 0.35 and p.bankability < 60
            and available(p, start, end)]
    if not pool:
        return
    known = sorted(pool, key=lambda p: (-known_u(p), p.id))[:cfg["tv"]["cd_known_picks"]]
    known_ids = {p.id for p in known}
    submitted = []
    for p in pool:
        if p.id in known_ids or not p.agent_id:
            continue
        from .agents import niche_factor
        prob = cfg["tv"]["submit_base"] * (0.4 + agent_hustle(st, p) / 100) * (tv_fit(p) - 0.3) * 2 * \
            (0.5 + strategy_fit(st, p, None, None, kind="tv_guest")) * niche_factor(p, reg)
        if R.unit(st.seed, "tv-submit", show.id, st.date, k, p.id) < prob:
            submitted.append(p)
    submitted.sort(key=lambda p: (-known_u(p), p.id))
    slots = cfg["tv"]["audition_size"] - len(known)
    called, passed = submitted[:slots], submitted[slots:]
    room = known + called
    pl = st.player_id
    title = f"'{show.title}' ({show.network})"
    for p in passed:
        if p.id == pl:
            _record(st, show, part, cd, "passed", pass_reason_tv(st, p, center, reg))
    attending = []
    for p in room:
        if p.id == pl:
            _record(st, show, part, cd, "called in" if p in called else "requested",
                    "the show's casting director wanted to see you")
            if "guest" not in st.orders.get("skip_auditions", []):
                attending.append(p)
        else:
            attending.append(p)
    if not attending:
        return
    scored = []
    for p in attending:
        form = R.gauss(st.seed, "tv-audition", show.id, st.date, k, p.id) * cfg["casting"]["audition_day_sd"]
        sc = (0.45 * p.talent + 0.25 * p.craft + 0.20 * p.range.get(reg, 40) + 0.10 * p.presence
              + 12 * (tv_fit(p) - 0.6) + (p.energy - 70) / 10 + form)
        scored.append((sc, p))
    scored.sort(key=lambda x: (-x[0], x[1].id))
    median = scored[len(scored) // 2][0]
    from .agents import impression, record_track
    for rank, (sc, p) in enumerate(scored):  # the room remembers
        record_track(p, reg, rank, len(scored))
        if cd_id:
            r = st.rel(cd_id, p.id)
            r.affinity = round(clamp(r.affinity + impression(cfg, sc, median), -100, 100), 2)
            if p.id == pl:
                r.history.append({"date": st.date, "text": f"read for a guest part on {title}", "delta": 0})
    winner = scored[0][1]
    for rank, (sc, p) in enumerate(scored):
        if p.id == pl:
            verdict = "booked it" if rank == 0 else "were not picked"
            st.log("audition_result", f"You read for {part} on {title} ({episode}) and {verdict}"
                                      + (f"; casting: {cd.name}" if cd else "") + ".",
                   actors=[p.id] + ([cd.id] if cd else []), salience=2, public=False,
                   data={"rank": rank + 1, "of": len(scored)})
            if rank > 0:
                from .casting import _tv_feedback
                st.log("audition_feedback", f"Feedback on {title} (via your agent): {_tv_feedback(p, winner)}.",
                       actors=[p.id], salience=1, public=False)
    _book(st, cfg, show, winner, part, episode, start, end, g, character_name)


def _book(st, cfg, show, p, part, episode, start, end, g, character_name) -> None:
    from .jobbing import KINDS, _offer_player, _take
    weeks, (lo, hi), craft_gain, fame_gain, _ = KINDS["tv_guest"]
    director = show.director_ids[int(g.integers(len(show.director_ids)))] if show.director_ids else None
    job = {"name": f"a guest role on '{show.title}' ({show.network})", "show": show.title, "network": show.network,
           "format": show.format, "character": f"{character_name(g, p.gender)}, {part}", "episode": episode,
           "colleagues": list(show.regulars) + ([director] if director else []), "director": director,
           "kind": "tv_guest", "start": start, "end": end, "craft": craft_gain, "fame": fame_gain,
           "pay": round(float(g.uniform(lo, hi)) * market.infl(cfg, year(st.date)) * (1 + min(1.0, p.fame * 5)), -2)}
    if p.controller == "player":
        _offer_player(st, cfg, p, job)
    else:
        _take(st, cfg, p, job)


def _record(st, show, part, cd, status, reason) -> None:
    st.market.setdefault("player_submissions", []).append({
        "date": st.date, "project": show.id, "title": show.title, "role": part, "importance": "guest",
        "studio": show.network, "cd": cd.name if cd else None, "status": status, "reason": reason})
    if status in ("called in", "requested"):
        st.log("called_in", f"Your agent got you a read for {part} on '{show.title}' ({show.network})"
                            + (f", casting {cd.name}" if cd else "") + ".",
               actors=[st.player_id] + ([cd.id] if cd else []), salience=1, public=False)
