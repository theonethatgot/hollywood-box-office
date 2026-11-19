"""Era-indexed market conditions (ticket prices, inflation, population...)."""
from __future__ import annotations

from ..core.config import era_value
from ..core.util import week_of_year, year

BASE_YEAR = 1980


_INFL: dict = {}


def infl(cfg: dict, yr: int) -> float:
    """Nominal-dollar multiplier relative to 1980 dollars (config amounts are 1980 $)."""
    key = (id(cfg), yr)
    v = _INFL.get(key)
    if v is None:
        v = _INFL[key] = era_value(cfg, "cpi", yr) / era_value(cfg, "cpi", BASE_YEAR)
    return v


def ticket_price(cfg: dict, date: str) -> float:
    return era_value(cfg, "ticket_price", year(date))


def moviegoing_pop_m(cfg: dict, date: str) -> float:
    return era_value(cfg, "moviegoing_pop_m", year(date))


def seasonality(cfg: dict, date: str) -> float:
    w = week_of_year(date)
    for band in cfg["box_office"]["seasonality"]:
        lo, hi = band["weeks"]
        if lo <= w <= hi:
            return float(band["mult"])
    return 1.0


def sag_scale_week(cfg: dict, date: str) -> float:
    return era_value(cfg, "sag_weekly_scale", year(date))
