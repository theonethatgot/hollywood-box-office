"""1990 expansion: rolling historical intake, era studio roster, local overlay, documented
casting as a prior (auditions for parts that weren't star vehicles), actor-directors."""
import copy
import json

from hsim import service as S
from hsim.core.config import load_config
from hsim.systems import casting as C
from hsim.systems import studios as STU
from hsim.systems import tick as T
from hsim.world import genesis
from hsim.world import historical as H

CFG = load_config({"world": {"generated_actors_with_history": 300, "generated_directors_with_history": 60}})


def _person(name, g, birth, **kw):
    base = {"name": name, "gender": g, "birth": birth, "death": None, "manner_of_death": [], "spouses": [],
            "honours": [], "sitelinks": 10, "description": "American actor"}
    base.update(kw)
    return base


def _film(title, date, cast, directors=("QD",), dist="Paramount Pictures", sl=20):
    return {"title": title, "date": date, "genres": ["drama film"], "cast": list(cast), "directors": list(directors),
            "distributors": [dist], "companies": [], "cost_usd": 1e7, "box_office_usd": None, "follows": [],
            "series": [], "sitelinks": sl, "description": ""}


def _pack():
    films = {
        "QF1": _film("Early Work", "1987-05-01", ["QA", "QB"]),
        "QF2": _film("Near Film", "1990-09-01", ["QA", "QB"]),
        "QF3": _film("Far Film", "1993-03-05", ["QN", "QA"], sl=30),        # beyond the 24-month horizon
        "QF4": _film("Directed and Starring", "1990-12-01", ["QD", "QB"], directors=("QD",)),
    }
    people = {"QA": _person("Actor A", "m", "1950-01-01"), "QB": _person("Actor B", "f", "1960-01-01"),
              "QN": _person("Newcomer N", "f", "1970-01-01", sitelinks=40,
                            honours=[{"award": "Academy Award for Best Actress", "result": "won", "date": "1992-03-30",
                                      "for": "QF9"}]),
              "QD": _person("Director D", "m", "1940-01-01", description="American actor and film director")}
    return {"version": "test-1990", "source": "test", "years": [1985, 1994], "films": films, "people": people}


def _game(tmp_path, pack=None, path=None):
    if path is None:
        path = tmp_path / "pack.json"
        path.write_text(json.dumps(pack or _pack()))
    params = {"seed": 4, "start": "1990-01-05", "data_pack": str(path),
              "player": {"name": "P", "gender": "m", "birth": "1962-01-01", "background": "working"}}
    return S.Game.new(tmp_path / "w.sqlite", params, CFG)


def test_rolling_intake_brings_in_later_films_and_people_without_leakage(tmp_path):
    g = _game(tmp_path)
    st = g.state
    titles = {p.title for p in st.projects.values()}
    assert "Near Film" in titles and "Far Film" not in titles
    assert "wd:QN" not in st.people
    g.command({"type": "orders", "orders": {"interrupt_on": [], "let_agent_negotiate": ["lead", "colead", "supporting"]}})
    g.command({"type": "advance", "until": "1991-04-19"})
    st = g.state
    far = next(p for p in st.projects.values() if p.title == "Far Film")
    assert far.historical_ref == "wd:QF3" and far.stage in ("development", "prepro")
    n = st.people["wd:QN"]
    assert n.provenance.get("entered") and n.awards == [] and "Academy Award" not in n.bio      # 1992 win is future
    assert all(c.get("kind") != "prior" or c["year"] < 1990 for c in n.credits)
    assert any(e["type"] == "history_intake" for e in st.events)
    assert g.replay_check()["match"]


def test_intake_is_deterministic(tmp_path):
    path = tmp_path / "pack.json"
    path.write_text(json.dumps(_pack()))
    (tmp_path / "a").mkdir(), (tmp_path / "b").mkdir()
    a, b = _game(tmp_path / "a", path=path), _game(tmp_path / "b", path=path)
    for g in (a, b):
        T.advance(g.state, CFG, "1991-03-01")
    assert a.state.state_hash() == b.state.state_hash()


def test_actor_director_can_star_in_own_film(tmp_path):
    st = _game(tmp_path).state
    proj = next(p for p in st.projects.values() if p.title == "Directed and Starring")
    lead = next(st.roles[r] for r in proj.role_ids if st.roles[r].intended == "wd:QD")
    assert proj.director_id == "wd:QD"
    assert C.available(st.people["wd:QD"], *C.window(proj), ignore_project=proj.id)
    assert lead.importance == "lead"


def test_documented_part_for_a_non_star_is_auditioned_with_the_documented_actor_favoured(tmp_path):
    st = _game(tmp_path).state
    proj = next(p for p in st.projects.values() if p.title == "Directed and Starring")
    assert proj.stage in ("development", "prepro")
    role = next(st.roles[r] for r in proj.role_ids if st.roles[r].intended == "wd:QB")
    st.people["wd:QB"].bankability = 10.0
    proj.stage = "prepro"
    C._start_casting(st, CFG, proj, role)
    assert role.status == "auditioning" and "wd:QB" in [a["id"] for a in role.auditioners]
    assert C.audition_score(st, CFG, proj, role, st.people["wd:QB"], 0) > \
        C.audition_score(st, CFG, proj, copy.copy(role).__class__(**{**role.__dict__, "intended": None}), st.people["wd:QB"], 0)
    star_role = next(st.roles[r] for r in proj.role_ids if st.roles[r].intended == "wd:QD")
    st.people["wd:QD"].bankability = 80.0
    C._start_casting(st, CFG, proj, star_role)
    assert any(o.role_id == star_role.id and o.person_id == "wd:QD" for o in st.offers.values())


def test_studio_roster_follows_the_era():
    st = genesis.new_world(CFG, 2, "1990-01-05")
    ids = set(st.studios)
    assert {"st-tri", "st-nl", "st-mir"} <= ids and not {"st-avc", "st-nw"} & ids
    assert st.studios["st-wb"].budget_median > 15
    old = genesis.new_world(CFG, 2, "1983-01-07")
    assert "st-tri" not in old.studios and "st-avc" in old.studios
    old.date = "1984-01-06"
    STU.roster(old, CFG)
    assert "st-tri" in old.studios
    old.date = "1987-01-02"
    STU.roster(old, CFG)
    assert old.studios["st-avc"].slate_per_year == 0


def test_local_overlay_merges_billing_characters_and_extra_films(tmp_path, monkeypatch):
    pack = _pack()
    ov = {"pack_version": pack["version"], "films": {"QF2": {"billing": ["QB", "nm1", "QA"], "characters": {"nm1": "Sal"}}},
          "extra_films": {"tt9": {**_film("Foreign Hit", "1990-07-01", ["nm1", "QB"], directors=[], dist=None),
                                  "distributors": [], "date_precision": "year", "source": "imdb"}},
          "people": {"nm1": _person("Imdb Only", "m", "1955-07-01", source="imdb", birth_precision="year")}}
    path = tmp_path / "imdb_overlay.json"
    path.write_text(json.dumps(ov))
    monkeypatch.setattr(H, "overlay_path", lambda: path)
    H._SOURCES.clear()
    src = H.sources(pack)
    assert src["films"]["QF2"]["cast"][:3] == ["QB", "nm1", "QA"]
    assert src["films"]["QF2"]["characters"]["nm1"] == "Sal" and "tt9" in src["films"]
    st = genesis.new_world(CFG, 5, "1990-01-05", data_pack=pack)
    assert "imdb:nm1" in st.people and st.people["imdb:nm1"].provenance["source"] == "imdb"
    assert any(p.historical_ref == "imdb:tt9" for p in st.projects.values())
    H._SOURCES.clear()
