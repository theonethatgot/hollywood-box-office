"""Reproducible statistics for a protagonist's submission record.

    python tools/career_stats.py saves/pt.sqlite --year 1982

For a target year with k call-ins from n submissions, report the probability of
observing <= k call-ins under three different reference rates, which answer
different questions:

  1. population rate: the industry-wide call-in share across ALL submissions
     (a population average; most submissions are for actors far from the role)
  2. individual rate: this actor's own rate in the earlier years, treated as known
  3. individual rate with uncertainty: a Beta-binomial posterior predictive using
     the earlier years' counts (uniform prior), which accounts for having
     estimated the rate from limited data

All three assume submissions are independent Bernoulli trials. That assumption
is optimistic: call-ins are correlated (same casting directors, the actor's
standing changes slowly), so real dispersion is larger than these models imply.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hsim.io.save import SaveFile  # noqa: E402


def binom_cdf(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def betabinom_cdf(k: int, n: int, a: float, b: float) -> float:
    def lbeta(x, y):
        return math.lgamma(x) + math.lgamma(y) - math.lgamma(x + y)
    return sum(math.exp(math.log(math.comb(n, i)) + lbeta(i + a, n - i + b) - lbeta(a, b)) for i in range(k + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("save")
    ap.add_argument("--year", required=True)
    a = ap.parse_args()
    st = SaveFile(a.save).read_state()
    subs = st.market.get("player_submissions", [])
    called = ("called in", "requested")
    by_year = {}
    for s in subs:
        y = s["date"][:4]
        n, k = by_year.get(y, (0, 0))
        by_year[y] = (n + 1, k + (s["status"] in called))
    print("submissions / call-ins by year:", {y: f"{k}/{n} ({k / n:.1%})" for y, (n, k) in sorted(by_year.items())})
    n, k = by_year[a.year]
    prior = [(yy, v) for yy, v in sorted(by_year.items()) if yy < a.year]
    pn = sum(v[0] for _, v in prior)
    pk = sum(v[1] for _, v in prior)
    stats = st.market.get("submission_stats", {})
    pop = stats["called_in"] / stats["submitted"] if stats.get("submitted") else None
    print(f"\ntarget {a.year}: {k} call-ins from {n} submissions")
    if pop is not None:
        print(f"  1. population rate {pop:.2%} (all {stats['submitted']:,} submissions in the world): "
              f"P(<= {k}) = {binom_cdf(k, n, pop):.3f}")
    if pn:
        ind = pk / pn
        print(f"  2. own earlier rate {ind:.2%} ({pk}/{pn}), treated as known: P(<= {k}) = {binom_cdf(k, n, ind):.3f}")
        print(f"  3. own earlier rate with uncertainty, Beta({pk + 1},{pn - pk + 1}) posterior predictive: "
              f"P(<= {k}) = {betabinom_cdf(k, n, pk + 1, pn - pk + 1):.3f}")
    print("\nNote: these assume independent submissions; real call-ins are positively correlated, "
          "so streaks of zeros are more likely than these figures suggest.")


if __name__ == "__main__":
    main()
