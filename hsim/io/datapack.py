"""Historical data packs (built by datapipe/). Loader implemented with the pipeline."""
from __future__ import annotations

import json
from pathlib import Path


def read_pack(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def load_pack_into(st, cfg, pack: dict) -> None:
    from ..world.historical import load_historical
    load_historical(st, cfg, pack)
