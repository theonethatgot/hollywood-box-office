"""The narrator-to-engine interface (hard / narrative / proposed canon), agent initiative,
and the packet context that exposes them."""
import copy
import datetime as dt
import re

from hsim import service as S
from hsim.core.util import add_days
from hsim.narrator import packet as PKT
from hsim.systems import agents as A
from hsim.systems import initiatives as INI
from hsim.systems import tick as T

DELEGATE_ALL = {"interrupt_on": [], "let_agent_negotiate": ["lead", "colead", "supporting"]}


def _world(cfg, params, weeks=12):
    st = S.genesis_state(cfg, params)
    st.orders.update(DELEGATE_ALL)
    T.advance(st, cfg, "2100-01-01", max_weeks=weeks)
    return st


def _reply(g, **block):
    pk = g.command({"type": "packet"})
    return g.command({"type": "submit", "block": {"reply_to": pk["packet_id"], **block}})


# ------------------------------------------------------------ technical ---
def test_not_quiet_while_shooting(cfg, params):
    st = _world(cfg, params, weeks=6)
    S.export_packet(st, cfg)
    proj = next(p for p in st.projects.values() if p.stage in ("prepro", "development"))
    st.player.calendar.append({"project_id": proj.id, "start": add_days(st.date, -3), "end": add_days(st.date, 60),
                               "kind": "shoot"})
    T.advance(st, cfg, "2100-01-01", max_weeks=3)
    st.market["jobs"] = [j for j in st.market.get("jobs", []) if j["person"] != st.player_id]
    summary = PKT.build(st, cfg, "pkt-test")["period_summary"]
    assert summary["quiet_period"] is False
    assert any(proj.title in w for w in summary["working"])


def test_event_weekdays_match_event_dates(cfg, params):
    st = _world(cfg, params, weeks=40)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for e in st.events:
        text = e["text"].split("Premise:")[0]          # fictional premises may mention days in their plots
        for name in days:
            if re.search(rf"\b{name}\b", text):
                assert dt.date.fromisoformat(e["date"]).strftime("%A") == name, e


def test_engine_does_not_invent_player_social_life(cfg, params):
    st = _world(cfg, params, weeks=40)
    assert not [e for e in st.events if e["type"] == "social" and st.player_id in e["actors"]]


# ---------------------------------------------------- narrative canon ---
def test_narrative_canon_persists_and_reaches_people_cards(tmp_path, cfg, params):
    g = S.Game.new(tmp_path / "n.sqlite", params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 4})
    agent = g.state.people[g.state.player.agent_person_id]
    r = _reply(g, narrative=[{"text": f"{agent.name.split()[0]} keeps a bowl of butterscotch on the desk.",
                              "about": [agent.name]},
                             {"text": "You got the part in a big studio film."}])
    assert any("consequential" in w for w in r["warnings"])        # flagged, stored only as detail
    assert not any(e["type"] == "cast" and e["actors"] == [g.state.player_id] for e in g.state.events[-3:])
    pk = g.command({"type": "packet"})["packet"]
    assert any("butterscotch" in x for x in pk["narrative_canon"])
    card = next(c for c in pk["people"] if c["id"] == agent.id)
    assert card["why_here"] == "your agent"
    assert any("butterscotch" in x for x in card["narrative_canon"])
    assert g.replay_check()["match"]


def test_narrative_about_unknown_person_warns(tmp_path, cfg, params):
    g = S.Game.new(tmp_path / "u.sqlite", params, cfg)
    r = _reply(g, narrative=[{"text": "Lunch with an old friend.", "about": ["Gina Moretti-Zzyzx"]}])
    assert any("nobody" in w for w in r["warnings"])


# --------------------------------------------------------- initiatives ---
def test_initiatives_cannot_grant_outcomes(tmp_path, cfg, params):
    g = S.Game.new(tmp_path / "i.sqlite", params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 3})
    proj = next(p for p in g.state.projects.values() if p.stage == "prepro")
    _reply(g, initiatives=[{"kind": "pursue_project", "target": proj.title, "result": "cast as the lead"},
                           {"kind": "meet", "target": "Nobody Atall Person"},
                           {"kind": "teleport"}])
    rulings = g.state.rulings
    assert [r["result"] for r in rulings] == ["rejected", "rejected", "rejected"]
    assert "engine decides" in rulings[0]["text"] and "nobody" in rulings[1]["text"]


def test_pursue_project_only_gets_you_seen(cfg, params):
    st = _world(cfg, params, weeks=3)
    pl = st.player
    results = []
    for proj in [p for p in st.projects.values() if p.stage in ("prepro", "development")][:12]:
        before = {r: st.roles[r].cast_id for r in proj.role_ids}
        res = INI.adjudicate(st, cfg, {"kind": "pursue_project", "target": proj.id}, len(results))
        results.append(res["result"])
        assert {r: st.roles[r].cast_id for r in proj.role_ids} == before   # nobody is cast by a push
        if res["result"] in ("accepted", "partial"):
            assert any(pl.id in st.roles[r].requested for r in proj.role_ids)
    assert set(results) <= {"accepted", "partial", "rejected", "pending"}
    assert "rejected" in results                                           # pushes fail too


def test_requested_actor_is_seen_but_must_win(cfg, params):
    from hsim.systems import casting as C
    st = _world(cfg, params, weeks=2)
    for proj in st.projects.values():
        role = next((st.roles[r] for r in proj.role_ids if st.roles[r].importance in ("supporting", "colead")), None)
        if proj.stage not in ("prepro", "development") or role is None:
            continue
        pool = [p for p in C.candidate_pool(st, cfg, proj, role) if C.fit(p, role, st.date) > 0.3]
        if len(pool) > cfg["casting"]["audition_size"] + 5:
            break
    rm = INI.room(st, cfg, proj, role, pool)
    outsider = st.people[rm["order"][-1]]                                  # the CD's last choice
    role.requested.append(outsider.id)
    ranked = [st.people[i] for i in rm["order"]]
    invited = A.build_audition_list(st, cfg, proj, role, pool, ranked, rm["u"])
    assert outsider in invited


def test_meeting_resolves_later_with_a_reason(tmp_path, cfg, params):
    g = S.Game.new(tmp_path / "m.sqlite", params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 3})
    target = max((p for p in g.state.people.values() if "director" in p.roles and not p.death), key=lambda p: p.prestige)
    _reply(g, initiatives=[{"kind": "meet", "target": target.id, "approach": "wants to talk about his next film"}])
    ruling = g.state.rulings[-1]
    assert ruling["result"] == "pending"
    iid = ruling["initiative"]
    g.command({"type": "advance", "weeks": 5})
    ini = g.state.initiatives[iid]
    assert ini["status"] in ("succeeded", "failed") and len(ini["steps"]) == 2
    pk = g.command({"type": "packet"})["packet"]
    assert any(x["id"] == iid for x in pk["initiatives"])
    assert g.replay_check()["match"]


def test_reposition_directive_changes_agent_behaviour(cfg, params):
    st = _world(cfg, params, weeks=2)
    pl = st.player
    res = INI.adjudicate(st, cfg, {"kind": "reposition", "details": {"no_tv": True, "no_commercials": True}}, 0)
    assert res["result"] == "accepted" and pl.directives["no_tv"]
    mark = len(st.market.get("player_submissions", []))
    jobs_before = {j["id"] for j in st.market.get("jobs", [])}
    T.advance(st, cfg, "2100-01-01", max_weeks=30)
    tv = [s for s in st.market.get("player_submissions", [])[mark:] if s.get("kind") == "tv" or "network" in str(s.get("studio"))]
    new_jobs = [j for j in st.market.get("jobs", []) + st.market.get("jobs_done", [])
                if j["person"] == pl.id and j["id"] not in jobs_before]
    assert not [j for j in new_jobs if j["kind"] in ("tv_guest", "commercial") and j.get("booked", "") > "1980-01-18"]
    assert not tv


def test_develop_project_takes_time_money_and_studio_judgement(cfg, params):
    st = _world(cfg, params, weeks=2)
    st.player.cash = 200000.0
    res = INI.adjudicate(st, cfg, {"kind": "develop_project", "title": "Night Ferry", "genre": "drama",
                                   "logline": "A ferry pilot hides a fugitive brother on the last crossing of the year."}, 0)
    assert res["result"] == "pending" and st.player.cash < 200000.0
    ini = st.initiatives[res["initiative"]]
    T.advance(st, cfg, "2100-01-01", max_weeks=40)
    assert ini["status"] in ("pitching", "greenlit", "turnaround")
    assert "quality" not in str(PKT.build(st, cfg, "pkt-x")["initiatives"])  # hidden script quality never shown


# -------------------------------------------------------------- agents ---
def test_agent_pushes_do_not_depend_on_who_is_the_player(cfg, params):
    st = _world(cfg, params, weeks=6)
    a, b = copy.deepcopy(st), copy.deepcopy(st)
    b.people[b.player_id].controller = "npc"
    A.plan_week(a, cfg)
    A.plan_week(b, cfg)
    strip = lambda s: [{k: v for k, v in x.items()} for x in s.market.get("agent_pushes", [])]
    assert strip(a) == strip(b)


def test_agents_push_clients_and_some_pushes_fail(cfg, params):
    st = _world(cfg, params, weeks=30)
    pushes = st.market.get("agent_pushes", [])
    assert len(pushes) > 20
    results = {p["result"] for p in pushes}
    assert results == {"agreed to see", "declined"}
    won = sum(1 for p in pushes if st.roles[p["role"]].cast_id == p["client"])
    agreed = sum(1 for p in pushes if p["result"] == "agreed to see")
    assert won < agreed                                  # being seen is not being cast


def test_packet_exposes_agent_plan_and_standing(tmp_path, cfg, params):
    g = S.Game.new(tmp_path / "p.sqlite", params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 6})
    g.command({"type": "packet"})
    g.command({"type": "advance", "weeks": 20})
    pk = g.command({"type": "packet"})["packet"]
    assert pk["agent"]["attention"] and pk["agent"]["strategy"]
    assert set(pk["standing_changes"]["now"]) >= {"momentum", "draw", "industry_standing"}
    for ch in pk["standing_changes"]["changes"]:
        assert "->" in ch
    if pk["standing_changes"]["changes"]:
        assert pk["standing_changes"]["causes"]
    assert all("why_here" in c for c in pk["people"])


def test_pursuing_an_attached_part_is_answered_honestly(cfg, params):
    """A documented (or otherwise attached) part goes to its person first; the agent says so."""
    st = _world(cfg, params, weeks=3)
    pl = st.player
    for proj in st.projects.values():
        mine = [st.roles[r] for r in proj.role_ids if st.roles[r].gender == pl.gender and not st.roles[r].cast_id
                and st.roles[r].status == "open"]
        if proj.stage in ("development", "prepro") and mine:
            break
    role = mine[0]
    role.intended = next(p.id for p in st.actors() if p.id != pl.id and p.gender == pl.gender)
    res = INI.adjudicate(st, cfg, {"kind": "pursue_project", "target": proj.title, "role": role.name}, 0)
    assert "earmarked" in res["text"] and res["result"] != "accepted"
    assert role.cast_id is None


def test_development_package_follow_ups(cfg, params):
    st = _world(cfg, params, weeks=2)
    st.player.cash = 300000.0
    res = INI.adjudicate(st, cfg, {"kind": "develop_project", "title": "Night Ferry", "genre": "drama",
                                   "logline": "A ferry pilot hides a fugitive brother on the last crossing of the year."}, 0)
    iid = res["initiative"]
    early = INI.adjudicate(st, cfg, {"kind": "develop_project", "project": iid, "action": "attach",
                                     "target": st.directors()[0].id}, 1)
    assert early["result"] == "rejected"                        # nothing to attach to until a draft exists
    T.advance(st, cfg, "2100-01-01", max_weeks=20)
    ini = st.initiatives[iid]
    if ini["status"] in ("pitching", "turnaround"):
        before = st.player.cash
        r = INI.adjudicate(st, cfg, {"kind": "develop_project", "project": "Night Ferry", "action": "revise"}, 2)
        assert r["result"] == "pending" and st.player.cash < before and ini["status"] == "writing"
        d = max(st.directors(), key=lambda p: p.prestige)
        T.advance(st, cfg, "2100-01-01", max_weeks=12)
        r = INI.adjudicate(st, cfg, {"kind": "develop_project", "project": iid, "action": "attach", "target": d.name}, 3)
        assert r["result"] in ("accepted", "rejected")
        assert (d.id in ini["data"]["attached"]) == (r["result"] == "accepted")
