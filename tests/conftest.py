import pytest

from hsim.core.config import load_config

SMALL = {"world": {"generated_actors": 500, "generated_directors": 110, "new_actors_per_year": 40}}


@pytest.fixture(scope="session")
def cfg():
    return load_config(SMALL)


@pytest.fixture
def params():
    return {"seed": 5, "start": "1980-01-04",
            "player": {"name": "Test Player", "gender": "f", "birth": "1955-05-05", "background": "working"}}
