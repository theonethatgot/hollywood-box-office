"""Historical snapshot loader: leakage, dependencies, intended attachments."""
import copy

from hsim.core.config import load_config
from hsim.world import genesis
from hsim.world import historical as H

CFG = load_config({"world": {"generated_actors_with_history": 300, "generated_directors_with_history": 60}})


def _pack():
    films = {
        "QF1": {"title": "Old Hit", "date": "1978-06-01", "genres": ["comedy film"], "cast": ["QA", "QB", "QC"],
                "directors": ["QD"], "distributors": ["Paramount Pictures"], "companies": [], "cost_usd": 8e6,
                "box_office_usd": 6e7, "follows": [], "series": [], "sitelinks": 40, "description": "1978 film"},
        "QF2": {"title": "Small Drama", "date": "1979-03-01", "genres": ["drama film"], "cast": ["QC", "QA"],
                "directors": ["QD"], "distributors": ["Orion Pictures"], "companies": [], "cost_usd": None,
                "box_office_usd": None, "follows": [], "series": [], "sitelinks": 8, "description": "1979 film"},
        "QF3": {"title": "Future Picture", "date": "1980-11-14", "genres": ["thriller film"], "cast": ["QB", "QA"],
                "directors": ["QD"], "distributors": ["Warner Bros."], "companies": [], "cost_usd": 1.2e7,
                "box_office_usd": 9e7, "follows": [], "series": [], "sitelinks": 60, "description": "1980 thriller"},
    }
    people = {
        "QA": {"name": "Actor A", "gender": "m", "birth": "1945-01-01", "death": None, "manner_of_death": [],
               "spouses": [{"id": "QB", "start": "1982-05-01", "end": None}], "honours": [], "sitelinks": 30,
               "description": "American actor"},
        "QB": {"name": "Actor B", "gender": "f", "birth": "1950-01-01", "death": None, "manner_of_death": [],
               "spouses": [{"id": "QA", "start": "1982-05-01", "end": None}], "honours": [], "sitelinks": 20,
               "description": "American actress"},
        "QC": {"name": "Actor C", "gender": "f", "birth": "1940-01-01", "death": "1983-02-02",
               "manner_of_death": ["Q3739104"], "spouses": [], "honours": [], "sitelinks": 10,
               "description": "American actress"},
        "QD": {"name": "Director D", "gender": "m", "birth": "1930-01-01", "death": None, "manner_of_death": [],
               "spouses": [], "honours": [], "sitelinks": 15, "description": "American film director"},
    }
    return {"version": "test", "source": "test", "years": [1975, 1984], "films": films, "people": people}


def _world(pack, seed=3):
    return genesis.new_world(CFG, seed, "1980-01-04", data_pack=pack)


OBSERVED = ("fame", "bankability", "prestige", "critical_rep", "heat", "quote", "craft")


def test_real_people_and_films_loaded():
    st = _world(_pack())
    assert {"wd:QA", "wd:QB", "wd:QC", "wd:QD"} <= set(st.people)
    fut = [p for p in st.projects.values() if p.historical_ref == "wd:QF3"]
    assert len(fut) == 1 and fut[0].director_id == "wd:QD"
    intended = [st.roles[r].intended for r in fut[0].role_ids]
    assert intended == ["wd:QB", "wd:QA"]
    assert st.people["wd:QA"].provenance["personality"].startswith("prior")


def test_no_future_leakage_into_observed_attributes():
    base = _world(_pack())
    pack = copy.deepcopy(_pack())
    pack["people"]["QA"]["honours"].append({"award": "Academy Award for Best Actor", "result": "won",
                                            "date": "1983-04-11", "for": None})
    later = _world(pack)
    for attr in OBSERVED:
        assert getattr(base.people["wd:QA"], attr) == getattr(later.people["wd:QA"], attr), attr


def test_hindsight_can_move_hidden_talent_but_not_decide_it():
    pack = copy.deepcopy(_pack())
    pack["people"]["QA"]["honours"].append({"award": "Academy Award for Best Actor", "result": "won",
                                            "date": "1983-04-11", "for": None})
    a = _world(_pack()).people["wd:QA"].talent
    b = _world(pack).people["wd:QA"].talent
    assert b >= a      # later acclaim is evidence of ability...
    assert CFG["history"]["talent_noise_sd"] > 0   # ...but noise keeps it from being destiny


def test_documented_events_created_with_dependencies():
    st = _world(_pack())
    kinds = {(e.type, e.dependency.get("kind")) for e in st.hist_events.values()}
    assert ("marriage", "relationship") in kinds
    assert ("death", "independent") in kinds
    marriage = next(e for e in st.hist_events.values() if e.type == "marriage")
    assert marriage.dependency.get("met_before_start") is True     # they co-starred in 1978


def test_studio_mapping_and_genres():
    assert H.studio_of({"distributors": ["Warner Bros."], "companies": []}) == "st-wb"
    assert H.studio_of({"distributors": ["Some Unknown Co."], "companies": []}) == "st-ind"
    assert H.genre_of(["science fiction film", "action film"]) == "scifi"
    assert H.genre_of(["romantic comedy"]) == "romance"
