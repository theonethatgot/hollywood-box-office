"""Narrator boundary: no hidden values, idempotent replies, adjudication rules."""
from hsim import models as M
from hsim import service as S
from hsim.narrator import adjudicate as ADJ
from hsim.narrator import reply as RPL
from hsim.systems import personal
from hsim.systems import tick as T

HIDDEN_KEYS = {"talent", "craft", "presence", "satisfaction", "attraction_ab", "attraction_ba", "studio_max",
               "script_quality", "hook", "reception_shock", "breadth", "segment_tilt", "personality", "performance",
               "affinity", "bankability", "quality", "goals_raw"}


def _keys(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.add(str(k))
            _keys(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _keys(v, out)
    return out


def _game(tmp_path, cfg, params, weeks=12):
    g = S.Game.new(tmp_path / "n.sqlite", params, cfg)
    g.command({"type": "orders", "orders": {"interrupt_on": [], "let_agent_negotiate": ["lead", "colead", "supporting"]}})
    g.command({"type": "advance", "weeks": weeks})
    return g


def test_packet_contains_no_hidden_values(tmp_path, cfg, params):
    g = _game(tmp_path, cfg, params, weeks=30)
    r = g.command({"type": "packet"})
    text = r["text"]
    keys = _keys(r["packet"], set())
    assert not (keys & HIDDEN_KEYS), keys & HIDDEN_KEYS
    pl = g.state.player
    assert f"{pl.talent}" not in text and f"{pl.craft}" not in text


def test_reply_parsing_and_idempotency(tmp_path, cfg, params):
    g = _game(tmp_path, cfg, params)
    pid = g.command({"type": "packet"})["packet_id"]
    reply = f"Lovely scene...\n\n```engine\nreply_to: {pid}\nnotes:\n  - \"Lives in a Silver Lake bungalow.\"\n```\n"
    block = RPL.extract(reply)
    r1 = g.command({"type": "submit", "block": block})
    r2 = g.command({"type": "submit", "block": block})
    assert r1["status"] == "applied" and r2["status"] == "duplicate"
    assert sum("Silver Lake" in n["text"] for n in g.state.notes) == 1


def test_stale_reply_refused(tmp_path, cfg, params):
    g = _game(tmp_path, cfg, params)
    p1 = g.command({"type": "packet"})["packet_id"]
    g.command({"type": "packet"})
    r = g.command({"type": "submit", "block": {"reply_to": p1, "notes": ["x"]}})
    assert r["status"] == "stale"


def test_forbidden_and_unmet_proposals_rejected(tmp_path, cfg, params):
    g = _game(tmp_path, cfg, params)
    st = g.state
    stranger = next(p for p in st.actors() if p.id != st.player_id and st.rel(st.player_id, p.id, create=False) is None)
    r = ADJ.adjudicate(st, cfg, {"id": "a", "type": "player_intent", "kind": "rest", "fee": 1e6}, 0)
    assert r["result"] == "rejected"
    r = ADJ.adjudicate(st, cfg, {"id": "b", "type": "romantic_overture", "to": stranger.id}, 1)
    assert r["result"] == "rejected"
    r = ADJ.adjudicate(st, cfg, {"id": "c", "type": "relationship_shift", "with": stranger.id,
                                 "direction": "negative", "severity": "major"}, 2)
    assert r["result"] == "rejected"


def test_no_damaging_public_claims_about_real_people(tmp_path, cfg, params):
    g = _game(tmp_path, cfg, params, weeks=1)
    st = g.state
    real = next(p for p in st.actors() if p.id != st.player_id)
    real.historical = True
    r = ADJ.adjudicate(st, cfg, {"id": "d", "type": "reputation_moment", "person": real.id, "direction": "negative",
                                 "severity": "moderate", "public": True, "cause": "x"}, 0)
    assert r["result"] == "rejected"


def test_documented_marriage_depends_on_meeting(cfg, params):
    st = S.genesis_state(cfg, params)
    a, b = [p for p in st.actors() if p.id != st.player_id and p.partner_status is None][:2]
    for p in (a, b):
        p.historical = True
    ev = M.HistoricalEvent(id="hx-1", people=[a.id, b.id], type="marriage", date=st.date, summary="A married B.",
                           dependency={"kind": "relationship", "base_rate_if_never_met": 0.0})
    st.hist_events[ev.id] = ev
    personal._documented_events(st, cfg)
    assert ev.status == "voided"            # never met in this timeline → does not happen
    ev2 = M.HistoricalEvent(id="hx-2", people=[a.id, b.id], type="marriage", date=st.date, summary="A married B.",
                            dependency={"kind": "relationship", "base_rate_if_never_met": 0.0})
    st.hist_events[ev2.id] = ev2
    st.rel(a.id, b.id).contact_weeks = 6     # they worked together
    personal._documented_events(st, cfg)
    assert ev2.status == "occurred" and a.partner_id == b.id


def test_documented_independent_event_survives_divergence(cfg, params):
    st = S.genesis_state(cfg, params)
    a = next(p for p in st.actors() if p.id != st.player_id)
    a.historical = True
    a.provenance["documented_credits_after_start"] = [{"ref": "wd:Q1", "date": "1979-01-01"}]   # fully diverged
    ev = M.HistoricalEvent(id="hx-3", people=[a.id], type="death", date=st.date, summary="A died.",
                           dependency={"kind": "independent"})
    st.hist_events[ev.id] = ev
    personal._documented_events(st, cfg)
    assert ev.status == "occurred" and a.death == st.date


def test_continuity_isolated_between_saves(tmp_path, cfg, params):
    """Notes, notes-derived continuity and events of one career never appear in another's packets."""
    a = S.Game.new(tmp_path / "a.sqlite", params, cfg)
    b = S.Game.new(tmp_path / "b.sqlite", {**params, "seed": 9,
                                           "player": {**params["player"], "name": "Other Person"}}, cfg)
    pa = a.command({"type": "packet"})["packet_id"]
    a.command({"type": "submit", "block": {"reply_to": pa, "notes": ["Test Player keeps a parrot named Zanzibar."]}})
    text_a = a.command({"type": "packet"})["text"]
    text_b = b.command({"type": "packet"})["text"]
    assert "Zanzibar" in text_a
    assert "Zanzibar" not in text_b and "Test Player" not in text_b


def test_note_about_unknown_person_warns(tmp_path, cfg, params):
    g = S.Game.new(tmp_path / "w.sqlite", params, cfg)
    pid = g.command({"type": "packet"})["packet_id"]
    r = g.command({"type": "submit", "block": {"reply_to": pid,
                                               "notes": ["Zebulon shares a Silver Lake apartment with Gina."]}})
    assert r["warnings"] and "Zebulon" in r["warnings"][0]
    pid = g.command({"type": "packet"})["packet_id"]
    r = g.command({"type": "submit", "block": {"reply_to": pid, "notes": ["Test keeps a battered script on the dashboard."]}})
    assert not r["warnings"]


def test_story_profiles_for_fictional_and_real_films(cfg, params):
    from hsim.world.story import ensure_story, packet_view
    st = S.genesis_state(cfg, params)
    fic = next(p for p in st.projects.values() if not p.historical_ref and p.role_ids)
    st.roles[fic.role_ids[0]].cast_id = st.player_id
    v = packet_view(st, fic, st.roles[fic.role_ids[0]])
    assert v["provenance"].startswith("simulated screenplay") and v["beats"] and v["central_conflict"]
    assert "may be wrong" in v["your_read_of_the_script"]
    assert ensure_story(st, fic) is fic.story                     # persistent, generated once
    real = next((p for p in st.projects.values() if p.historical_ref and p.role_ids), None)
    if real is not None:
        rv = packet_view(st, real, st.roles[real.role_ids[0]])
        assert "beats" not in rv and "real film" in rv["provenance"]


def test_personas_fit_professions(cfg, params):
    from hsim.world.people import SIGNATURES_BY_ROLE
    st = S.genesis_state(cfg, params)
    for p in st.people.values():
        for role in ("agent", "casting_director"):
            if role in p.roles and p.persona.get("signature"):
                assert p.persona["signature"] in SIGNATURES_BY_ROLE[role], (p.id, p.persona["signature"])


def test_story_key_scenes_are_distinct(cfg, params):
    from hsim.systems import tick as T
    from hsim.world.story import ensure_story
    st = S.genesis_state(cfg, params)
    T.advance(st, cfg, "2100-01-01", max_weeks=2)
    for p in list(st.projects.values())[:40]:
        ensure_story(st, p)
        for scenes in p.story.get("key_scenes", {}).values():
            assert len(set(scenes)) == len(scenes)
