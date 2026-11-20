"""Engine integrity: determinism, persistence, fairness, conservation, scheduling."""
import copy
import dataclasses

from hsim import service as S
from hsim.core.util import overlaps
from hsim.systems import casting as C
from hsim.systems import tick as T

DELEGATE_ALL = {"interrupt_on": [], "let_agent_negotiate": ["lead", "colead", "supporting"]}


def _world(cfg, params, weeks=20, orders=DELEGATE_ALL):
    st = S.genesis_state(cfg, params)
    st.orders.update(orders)
    T.advance(st, cfg, "2100-01-01", max_weeks=weeks)
    return st


def test_same_seed_same_world(cfg, params):
    a = _world(cfg, params)
    b = _world(cfg, params)
    assert a.state_hash() == b.state_hash()
    assert a.event_chain == b.event_chain


def test_different_seed_different_world(cfg, params):
    a = _world(cfg, params)
    b = _world(cfg, {**params, "seed": 6})
    assert a.state_hash() != b.state_hash()


def test_serialisation_roundtrip(cfg, params):
    st = _world(cfg, params, weeks=8)
    again = type(st).from_dict(copy.deepcopy(st.to_dict()), events=list(st.events))
    assert again.state_hash() == st.state_hash()


def test_save_replay_matches(tmp_path, cfg, params):
    g = S.Game.new(tmp_path / "w.sqlite", params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 10})
    pk = g.command({"type": "packet"})
    g.command({"type": "submit", "block": {"reply_to": pk["packet_id"], "notes": ["Has a cat named Biscuit."],
                                           "advance": {"weeks": 3}}})
    g.close()
    g2 = S.Game.open(tmp_path / "w.sqlite", cfg)
    r = g2.replay_check()
    assert r["match"], r


def test_rewind_restores_packet_state(tmp_path, cfg, params):
    path = tmp_path / "w.sqlite"
    g = S.Game.new(path, params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 4})
    pk = g.command({"type": "packet"})
    at_packet = g.state.state_hash()
    g.command({"type": "submit", "block": {"reply_to": pk["packet_id"], "advance": {"weeks": 6}}})
    assert g.state.state_hash() != at_packet
    g.close()
    branch = S.rewind(path, pk["packet_id"])
    g3 = S.Game.open(branch, cfg)
    assert g3.state.state_hash() == at_packet
    assert g3.replay_check()["match"]


def test_player_and_npc_scored_identically(cfg, params):
    """No outcome function may depend on who controls the character."""
    st = _world(cfg, params, weeks=2)
    pl = st.player
    proj = next(p for p in st.projects.values() if p.stage in ("prepro", "development"))
    role = st.roles[proj.role_ids[0]]
    before = (C.casting_utility(st, cfg, proj, role, pl), C.accept_utility(st, cfg, proj, role, pl, 50000.0),
              C.audition_score(st, cfg, proj, role, pl, 0.0), C.perceived_talent(st, cfg, proj, pl))
    pl.controller = "npc"
    after = (C.casting_utility(st, cfg, proj, role, pl), C.accept_utility(st, cfg, proj, role, pl, 50000.0),
             C.audition_score(st, cfg, proj, role, pl, 0.0), C.perceived_talent(st, cfg, proj, pl))
    assert before == after


def test_money_is_conserved(cfg, params):
    st = _world(cfg, params, weeks=40)
    m = st.market["money"]
    assert abs(m["gross"] - (m["net"] + m["commission"] + m["tax"])) < 1e-3 * max(1.0, m["gross"])


def test_no_one_shoots_two_films_at_once(cfg, params):
    st = _world(cfg, params, weeks=40)
    for p in st.people.values():
        shoots = [c for c in p.calendar if c["kind"] == "shoot"]
        for i, a in enumerate(shoots):
            for b in shoots[i + 1:]:
                assert not overlaps(a["start"], a["end"], b["start"], b["end"]), (p.id, a, b)


def test_stage_values_valid(cfg, params):
    st = _world(cfg, params, weeks=30)
    ok = {"development", "prepro", "shooting", "post", "awaiting_release", "released", "dead"}
    assert all(p.stage in ok for p in st.projects.values())
    for p in st.projects.values():
        if p.stage in ("shooting", "post", "awaiting_release", "released"):
            principal = [st.roles[r] for r in p.role_ids if st.roles[r].importance != "featured"]
            assert all(r.cast_id for r in principal), p.id
            assert all(st.roles[r].cast_id or st.roles[r].status == "filled locally" or p.stage == "released"
                       for r in p.role_ids if st.roles[r].importance == "featured"), p.id


def test_hidden_fields_exist_but_are_dataclass_fields(cfg, params):
    st = _world(cfg, params, weeks=1)
    names = {f.name for f in dataclasses.fields(st.player)}
    assert {"talent", "craft", "presence"} <= names


def test_replay_matches_when_save_is_reopened_between_commands(tmp_path, cfg, params):
    """The CLI (and ChatGPT's Python sessions) reload the save before every command.
    A reload must not change iteration order, or floats drift from the replay."""
    path = tmp_path / "cli.sqlite"
    S.Game.new(path, params, cfg).close()
    for cmd in ({"type": "orders", "orders": DELEGATE_ALL}, {"type": "advance", "weeks": 5},
                {"type": "packet"}, {"type": "advance", "weeks": 6}, {"type": "advance", "weeks": 4}):
        g = S.Game.open(path, cfg)
        g.command(cmd)
        g.close()
    g = S.Game.open(path, cfg)
    r = g.replay_check()
    assert r["match"], r


def test_save_load_preserves_nested_dict_order(tmp_path, cfg, params):
    path = tmp_path / "order.sqlite"
    g = S.Game.new(path, params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 3})
    live = g.state
    g.close()
    loaded = S.Game.open(path, cfg).state
    assert list(loaded.projects) == list(live.projects)
    for pid, p in live.projects.items():
        if p.run.get("segments"):
            assert list(loaded.projects[pid].run["segments"]) == list(p.run["segments"])


def test_adopt_replay_repairs_only_rounding_differences(tmp_path, cfg, params):
    path = tmp_path / "old.sqlite"
    g = S.Game.new(path, params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 4})
    p = next(x for x in g.state.projects.values() if x.domestic)
    p.domestic = p.domestic * (1 + 1e-15) + 1e-8          # simulate a legacy last-bit drift
    g.save.write_state(g.state)
    assert not g.replay_check()["match"]
    r = g.adopt_replay()
    assert r["adopted"] and r["float_differences"] >= 1
    assert g.replay_check()["match"]
    p = next(x for x in g.state.projects.values() if x.domestic)
    p.domestic += 1000.0                                   # a real divergence must be refused
    g.save.write_state(g.state)
    assert not g.adopt_replay()["adopted"]


def test_rebaseline_keeps_history_and_verifies_later_commands(tmp_path, cfg, params):
    path = tmp_path / "legacy.sqlite"
    g = S.Game.new(path, params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 3})
    g.state.market["legacy_marker"] = {"b": 1, "a": 2}       # state that genesis replay can't reproduce
    g.save.write_state(g.state)
    assert not g.replay_check()["match"]
    before = g.state.state_hash()
    r = g.rebaseline("test")
    assert r["state_hash"] == before                        # nothing that happened is changed
    g.close()
    for weeks in (2, 3):
        g = S.Game.open(path, cfg)
        g.command({"type": "advance", "weeks": weeks})
        g.close()
    g = S.Game.open(path, cfg)
    chk = g.replay_check()
    assert chk["match"] and chk["replayed_from"].startswith("checkpoint")


def test_tv_guest_part_descriptions_match_role_gender():
    from hsim.core import rng as R
    from hsim.world.tv import GUEST_PARTS_GENDERED, guest_part
    for i in range(3000):
        g = R.stream(1, "gender-test", i)
        for gender, other in (("m", "f"), ("f", "m")):
            assert guest_part(g, gender) not in GUEST_PARTS_GENDERED[other]


def test_engine_change_checkpoints_save(tmp_path, cfg, params):
    path = tmp_path / "upgrade.sqlite"
    g = S.Game.new(path, params, cfg)
    g.command({"type": "orders", "orders": DELEGATE_ALL})
    g.command({"type": "advance", "weeks": 2})
    g.save.set_meta("engine_fingerprint", "older-engine")     # as if saved by a previous engine
    before_events = [dict(e) for e in g.state.events]
    g.command({"type": "advance", "weeks": 2})
    base = g.save.get_meta("replay_base")
    assert base and "older-engine" in base["reason"]
    cp = g.save.read_state("replay_base")
    assert cp.events[:len(before_events)] == before_events            # history unchanged
    assert [e["type"] for e in cp.events[len(before_events):]] == ["engine_checkpoint"]
    assert g.replay_check()["match"]
