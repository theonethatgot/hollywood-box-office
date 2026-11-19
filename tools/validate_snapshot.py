"""Compare the snapshot estimator's rankings with anchor lists (validation only).

    python tools/validate_snapshot.py --start 1980-01-04
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hsim.core.config import ROOT, load_config  # noqa: E402
from hsim.io.datapack import read_pack  # noqa: E402
from hsim.world import genesis  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="1980-01-04")
    ap.add_argument("--anchors", default=str(ROOT / "data/reference/anchors_1979.yaml"))
    a = ap.parse_args()
    cfg = load_config()
    st = genesis.new_world(cfg, 1, a.start, data_pack=read_pack(ROOT / cfg["history"]["default_pack"]))
    actors = [p for p in st.people.values() if p.historical and "actor" in p.roles]
    by_bank = {p.name: i + 1 for i, p in enumerate(sorted(actors, key=lambda p: -p.bankability))}
    by_fame = {p.name: i + 1 for i, p in enumerate(sorted(actors, key=lambda p: -p.fame))}
    anchors = yaml.safe_load(Path(a.anchors).read_text())["top_box_office_stars"]
    print(f"{len(actors)} real actors. Anchor ranks (bankability / fame):")
    found = []
    for name in anchors:
        b, f = by_bank.get(name), by_fame.get(name)
        found.append(b)
        print(f"  {name:<20} {b if b else '—':>5} / {f if f else '—':>5}")
    hit = [b for b in found if b]
    print(f"anchors present: {len(hit)}/{len(anchors)}; in top 50 by bankability: {sum(b <= 50 for b in hit)}; "
          f"median rank {sorted(hit)[len(hit)//2] if hit else '—'}")


if __name__ == "__main__":
    main()
