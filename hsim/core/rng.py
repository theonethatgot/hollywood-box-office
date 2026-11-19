"""Deterministic, named random streams.

Every random draw in the engine comes from a stream keyed by
(world seed, system, entity, purpose, date...). Adding a new system, person or
data record therefore never shifts any other draw: saves stay reproducible and
calibration runs stay comparable.
"""
from __future__ import annotations

import hashlib

import numpy as np


def stream(seed: int, *keys) -> np.random.Generator:
    h = hashlib.sha256("|".join(str(k) for k in (seed, *keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def unit(seed: int, *keys) -> float:
    """A single uniform [0,1) draw keyed like a stream (fast hash; for hot paths)."""
    h = hashlib.blake2b("|".join(str(k) for k in (seed, *keys)).encode(), digest_size=8).digest()
    return int.from_bytes(h, "little") / 2**64


def stable_unit(*keys) -> float:
    """Seed-independent uniform draw for latent traits that must not change
    between worlds (e.g. pairwise chemistry baseline is per-world, but
    name generation for a data record is not)."""
    h = hashlib.sha256("|".join(str(k) for k in keys).encode()).digest()
    return int.from_bytes(h[:8], "little") / 2**64


def gauss(seed: int, *keys) -> float:
    """Fast deterministic standard-normal draw for hot paths (Box-Muller on a hash)."""
    import math
    h = hashlib.blake2b("|".join(str(k) for k in (seed, *keys)).encode(), digest_size=16).digest()
    u1 = (int.from_bytes(h[:8], "little") + 1) / (2**64 + 1)
    u2 = int.from_bytes(h[8:], "little") / 2**64
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
