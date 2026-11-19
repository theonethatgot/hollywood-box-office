"""Configuration: all tunable coefficients live in YAML, never in code.

`load_config()` merges config/default.yaml, config/eras.yaml and any override
files. The resulting hash is stored in saves so a replay can detect that
formulas changed underneath it.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"


def _merge(a: dict, b: dict) -> dict:
    out = copy.deepcopy(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_config(*overrides: str | Path | dict) -> dict:
    cfg = yaml.safe_load((CONFIG_DIR / "default.yaml").read_text())
    cfg["eras"] = yaml.safe_load((CONFIG_DIR / "eras.yaml").read_text())
    for o in overrides:
        if isinstance(o, dict):
            cfg = _merge(cfg, o)
        else:
            cfg = _merge(cfg, yaml.safe_load(Path(o).read_text()))
    return cfg


def config_hash(cfg: dict) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()[:16]


def era_value(cfg: dict, key: str, yr: int) -> float:
    """Year-indexed market value with linear interpolation and edge clamping."""
    table = cfg["eras"][key]
    years = sorted(int(y) for y in table)
    if yr <= years[0]:
        return float(table[years[0]])
    if yr >= years[-1]:
        return float(table[years[-1]])
    for y0, y1 in zip(years, years[1:]):
        if y0 <= yr <= y1:
            t = (yr - y0) / (y1 - y0)
            return float(table[y0]) * (1 - t) + float(table[y1]) * t
    raise AssertionError
