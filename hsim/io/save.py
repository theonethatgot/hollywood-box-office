"""SQLite save files.

Layout
  meta(k, v)               genesis parameters, config hash, data version, latest packet
  commands(seq, json)      every state-changing command, in order (replay source)
  events(seq, json)        the audit log
  snapshots(tag, json, events_count)  'current' plus one per exported packet (rewind points)

Determinism contract: genesis(meta) + commands → identical state hash.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from ..core.state import WorldState

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS commands (seq INTEGER PRIMARY KEY, json TEXT);
CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, json TEXT);
CREATE TABLE IF NOT EXISTS snapshots (tag TEXT PRIMARY KEY, json TEXT, events_count INTEGER, commands_count INTEGER);
"""


class SaveFile:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.executescript(SCHEMA)

    def close(self):
        self.db.close()

    # --- meta ---
    def set_meta(self, k: str, v) -> None:
        self.db.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", (k, json.dumps(v)))

    def get_meta(self, k: str, default=None):
        row = self.db.execute("SELECT v FROM meta WHERE k=?", (k,)).fetchone()
        return json.loads(row[0]) if row else default

    # --- commands ---
    def append_command(self, cmd: dict) -> int:
        n = self.commands_count()
        self.db.execute("INSERT INTO commands VALUES (?, ?)", (n, json.dumps(cmd, sort_keys=True)))
        return n

    def commands(self) -> list:
        return [json.loads(r[0]) for r in self.db.execute("SELECT json FROM commands ORDER BY seq")]

    def commands_count(self) -> int:
        return self.db.execute("SELECT COUNT(*) FROM commands").fetchone()[0]

    # --- state ---
    def write_state(self, st: WorldState, tag: str = "current") -> None:
        have = self.db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        if have > len(st.events):
            self.db.execute("DELETE FROM events WHERE seq >= ?", (len(st.events),))
            have = len(st.events)
        self.db.executemany("INSERT INTO events VALUES (?, ?)",
                            [(e["seq"], json.dumps(e, sort_keys=True)) for e in st.events[have:]])
        self.db.execute("INSERT OR REPLACE INTO snapshots VALUES (?, ?, ?, ?)",
                        (tag, json.dumps(st.to_dict(), sort_keys=True), len(st.events), self.commands_count()))
        self.db.commit()

    def read_state(self, tag: str = "current") -> WorldState:
        row = self.db.execute("SELECT json, events_count FROM snapshots WHERE tag=?", (tag,)).fetchone()
        if row is None:
            raise KeyError(f"no snapshot '{tag}' in {self.path}")
        events = [json.loads(r[0]) for r in
                  self.db.execute("SELECT json FROM events WHERE seq < ? ORDER BY seq", (row[1],))]
        return WorldState.from_dict(json.loads(row[0]), events)

    def snapshot_info(self, tag: str):
        return self.db.execute("SELECT events_count, commands_count FROM snapshots WHERE tag=?", (tag,)).fetchone()

    def truncate_commands(self, n: int) -> None:
        self.db.execute("DELETE FROM commands WHERE seq >= ?", (n,))

    def tags(self) -> list:
        return [r[0] for r in self.db.execute("SELECT tag FROM snapshots ORDER BY rowid")]

    def commit(self):
        self.db.commit()
