"""Small shared helpers: dates, clamping, formatting."""
from __future__ import annotations

import datetime as dt
import math
from functools import lru_cache

ISO = "%Y-%m-%d"


def d(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def iso(x: dt.date) -> str:
    return x.isoformat()


def add_days(s: str, n: int) -> str:
    return iso(d(s) + dt.timedelta(days=n))


def add_weeks(s: str, n: float) -> str:
    return add_days(s, int(round(n * 7)))


def days_between(a: str, b: str) -> int:
    return (d(b) - d(a)).days


def next_friday(s: str) -> str:
    x = d(s)
    return iso(x + dt.timedelta(days=(4 - x.weekday()) % 7))


def year(s: str) -> int:
    return int(s[:4])


def week_of_year(s: str) -> int:
    return d(s).isocalendar()[1]


@lru_cache(maxsize=300_000)
def age_on(birth: str, on: str) -> int:
    b, o = d(birth), d(on)
    return o.year - b.year - ((o.month, o.day) < (b.month, b.day))


def overlaps(a0: str, a1: str, b0: str, b1: str) -> bool:
    return a0 <= b1 and b0 <= a1


def clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def money(x: float) -> str:
    """Format a dollar amount for humans/narrators."""
    a = abs(x)
    sign = "-" if x < 0 else ""
    if a >= 1e6:
        return f"{sign}${a/1e6:.1f}M"
    if a >= 1e3:
        return f"{sign}${a/1e3:.0f}k"
    return f"{sign}${a:.0f}"
