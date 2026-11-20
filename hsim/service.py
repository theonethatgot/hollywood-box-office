"""Service layer: the ONLY entry point front ends use (CLI now; MCP/web later).

Every state change is a JSON command appended to the save's command log, then
applied by `apply()`. `apply()` is pure with respect to I/O, so replaying the
genesis parameters plus the command log reproduces the state exactly.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from .core.config import config_hash, load_config
from .core.state import WorldState
from .core.util import add_weeks
from .io.save import SaveFile
from .narrator import adjudicate as ADJ
from .narrator import packet as PKT
from .narrator import reply as RPL
from .systems import decisions as D
from .systems import tick as T
from .world import genesis

ENGINE_VERSION = "0.1.0"


def engine_fingerprint(cfg: dict) -> str:
    """Hash of the engine source and configuration. Replay is only meaningful within one fingerprint."""
    import hashlib
    from .core.config import ROOT
    h = hashlib.sha256(config_hash(cfg).encode())
    for path in sorted((ROOT / "hsim").rglob("*.py")):
        h.update(path.read_bytes())
    return h.hexdigest()[:16]


def genesis_state(cfg: dict, params: dict) -> WorldState:
    pack = None
    if params.get("data_pack"):
        from pathlib import Path as _P
        from .core.config import ROOT
        from .io.datapack import read_pack
        path = _P(params["data_pack"])
        pack = read_pack(path if path.is_absolute() else ROOT / path)
    st = genesis.new_world(cfg, params["seed"], params["start"], data_pack=pack)
    st.config_hash = config_hash(cfg)
    st.data_version = pack.get("version", "") if pack else "generated-only"
    genesis.create_player(st, cfg, params.get("player", {}))
    st.packet_seq_mark = 0
    return st


# ----------------------------------------------------------- commands ---
def apply(st: WorldState, cfg: dict, cmd: dict) -> dict:
    t = cmd["type"]
    if t == "advance":
        until = cmd.get("until") or add_weeks(st.date, int(cmd.get("weeks", 1)))
        return T.advance(st, cfg, until)
    if t == "decide":
        text = D.resolve(st, cfg, cmd["id"], cmd["choice"], cmd.get("params", {}))
        st.rulings.append({"proposal": cmd["id"], "type": "decision", "result": "applied", "text": text})
        return {"text": text}
    if t == "orders":
        st.orders.update(cmd["orders"])
        return {"orders": st.orders}
    if t == "packet":
        return export_packet(st, cfg)
    if t == "submit":
        return submit_reply(st, cfg, cmd["block"], cmd.get("force", False))
    raise ValueError(f"unknown command type {t}")


def export_packet(st: WorldState, cfg: dict) -> dict:
    pid = st.new_id("pkt")
    st.packet_id = pid
    pk = PKT.build(st, cfg, pid)
    if st.player:
        st.market["standing_mark"] = PKT.standing(st)
    st.rulings, st.delegated = [], []
    st.packet_seq_mark = len(st.events)
    return {"packet_id": pid, "packet": pk, "text": PKT.render(pk)}


def submit_reply(st: WorldState, cfg: dict, block: dict, force: bool = False) -> dict:
    h = RPL.block_hash(block)
    if h in st.applied_replies:
        return {"status": "duplicate", "message": "This reply was already applied; nothing changed."}
    if block.get("reply_to") != st.packet_id and not force:
        return {"status": "stale", "message": f"Reply is for {block.get('reply_to')}, but the latest packet is "
                                              f"{st.packet_id}. Export a fresh packet or rewind."}
    errors, applied = [], []
    for dec in block.get("decisions", []):
        try:
            params = {k: v for k, v in dec.items() if k not in ("id", "choice")}
            text = D.resolve(st, cfg, dec["id"], str(dec["choice"]), params)
            st.rulings.append({"proposal": dec["id"], "type": "decision", "result": "applied", "text": text})
            applied.append(text)
        except (KeyError, ValueError) as e:
            errors.append(f"decision {dec.get('id')}: {e}")
            st.rulings.append({"proposal": dec.get("id"), "type": "decision", "result": "rejected", "text": str(e)})
    for i, prop in enumerate(block.get("proposals", [])):
        if not isinstance(prop, dict):
            continue
        ruling = ADJ.adjudicate(st, cfg, prop, i)
        st.rulings.append(ruling)
    from .systems import initiatives as INI
    for i, item in enumerate(block.get("initiatives") or []):
        if not isinstance(item, dict):
            continue
        st.rulings.append(INI.adjudicate(st, cfg, {"id": f"i{i + 1}", **item}, i))
    warnings = []
    for item in block.get("narrative") or []:
        w = add_narrative(st, item)
        warnings += w
    for note in block.get("notes", []):
        text = str(note)[:300]
        w = note_warning(st, text)
        if w:
            warnings.append(w)
        st.notes.append({"date": st.date, "text": text})
    st.applied_replies.append(h)
    out = {"status": "applied", "applied": applied, "errors": errors, "warnings": warnings,
           "rulings": [r for r in st.rulings if r["type"] != "decision"]}
    adv = block.get("advance")
    if isinstance(adv, dict) and (adv.get("weeks") or adv.get("until")):
        until = adv.get("until") or add_weeks(st.date, int(adv["weeks"]))
        out["advance"] = T.advance(st, cfg, str(until))
    return out


CONSEQUENTIAL = re.compile(r"\$\s?\d|\b(cast as|signed with|got the part|was hired|married|engaged|divorced|"
                           r"won the|fired|greenlit|pregnant|died|offered)\b", re.I)


def add_narrative(st: WorldState, item) -> list:
    """Narrative canon: details the narrator created (dialogue beats, rehearsals, habits, minor
    characters, places) preserved for continuity. They carry no mechanical weight; anything that
    should change the world belongs in `initiatives`."""
    from .systems.initiatives import resolve
    if isinstance(item, str):
        item = {"text": item}
    if not isinstance(item, dict) or not str(item.get("text", "")).strip():
        return ["narrative entry without text ignored"]
    text = str(item["text"]).strip()[:400]
    warnings, about = [], []
    for ref in item.get("about") or []:
        obj, err = resolve(st, ref, "person")
        if obj:
            about.append(obj.id)
            if obj.id != st.player_id and not _connected(st, obj.id):
                warnings.append(f"narrative is about {obj.name}, whom the protagonist has no recorded contact with "
                                f"or shared work; check it belongs in this story (kept as written).")
        else:
            warnings.append(f"narrative 'about' {err}")
    if not item.get("about"):
        w = note_warning(st, text)
        if w:
            warnings.append(w)
    if CONSEQUENTIAL.search(text):
        warnings.append(f"narrative entry '{text[:60]}...' reads like a consequential fact; it is kept as narrative "
                        f"detail only and changes nothing. Propose it as an initiative if it should matter.")
    st.narrative.append({"date": st.date, "text": text, "about": about, "packet": st.packet_id,
                         "kind": str(item.get("kind", "detail"))[:30]})
    return warnings


def _connected(st: WorldState, pid: str) -> bool:
    r = st.rel(st.player_id, pid, create=False)
    if r and (r.history or r.contact_weeks):
        return True
    for proj in st.projects.values():
        ids = {st.roles[x].cast_id for x in proj.role_ids} | {proj.director_id}
        if st.player_id in ids and pid in ids:
            return True
    return any(pid in j.get("colleagues", []) for j in st.market.get("jobs", []) if j["person"] == st.player_id)


def note_warning(st: WorldState, text: str) -> str | None:
    """Catch notes that belong to a different career (e.g. pasted from another chat): the note's
    subject is a capitalised name that matches nobody in this world."""
    first = text.split()[0].strip(".,'\"’s") if text.split() else ""
    if not first[:1].isupper() or first.lower() in ("the", "a", "an", "her", "his", "their", "my", "your", "you"):
        return None
    known = {p.name.split()[0] for p in st.people.values()} | {w for p in st.people.values() for w in p.name.split()}
    if first in known:
        return None
    return (f"note begins with '{first}', who is not anyone in this world (protagonist: {st.player.name}). "
            f"If it belongs to another career, rewind or ignore it.")


# --------------------------------------------------------------- Game ---
class Game:
    """A save file + its live state. All mutations go through `command()`."""

    def __init__(self, path: str | Path, cfg: dict | None = None):
        self.path = Path(path)
        self.cfg = cfg or load_config()
        self.save = SaveFile(self.path)
        self.state: WorldState | None = None

    @classmethod
    def new(cls, path: str | Path, params: dict, cfg: dict | None = None) -> "Game":
        path = Path(path)
        if path.exists():
            raise FileExistsError(f"{path} already exists")
        g = cls(path, cfg)
        g.save.set_meta("genesis", params)
        g.save.set_meta("engine_version", ENGINE_VERSION)
        g.save.set_meta("config_hash", config_hash(g.cfg))
        g.save.set_meta("engine_fingerprint", engine_fingerprint(g.cfg))
        g.state = genesis_state(g.cfg, params)
        g.save.write_state(g.state)
        return g

    @classmethod
    def open(cls, path: str | Path, cfg: dict | None = None) -> "Game":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)
        g = cls(path, cfg)
        g.state = g.save.read_state()
        return g

    def config_warning(self) -> str | None:
        if self.save.get_meta("config_hash") != config_hash(self.cfg):
            return ("Configuration has changed since this save was created; new weeks use the new formulas "
                    "and an exact replay of old commands may differ.")
        return None

    def command(self, cmd: dict) -> dict:
        fp = engine_fingerprint(self.cfg)
        old = self.save.get_meta("engine_fingerprint")
        if old != fp:
            # the engine changed since this save last ran: earlier commands can't be replayed by this
            # engine, so checkpoint the state exactly as it is (nothing that happened changes)
            self.state.log("engine_checkpoint", "Simulation engine updated; save checkpointed for verification.",
                           salience=0, public=False, data={"from": old, "to": fp})
            self.rebaseline(f"engine changed ({old or 'unrecorded'} -> {fp})", check=False)
            self.save.set_meta("engine_fingerprint", fp)
        self.save.append_command(cmd)
        result = apply(self.state, self.cfg, cmd)
        if cmd["type"] == "packet":
            self.save.write_state(self.state, tag=result["packet_id"])
            self.save.set_meta("latest_packet", result["packet_id"])
        self.save.write_state(self.state)
        return result

    def replayed_state(self) -> WorldState:
        """Replay from genesis, or from a verified checkpoint if the save has one."""
        base = self.save.get_meta("replay_base")
        cmds = self.save.commands()
        if base:
            st = self.save.read_state(base["tag"])
            cmds = cmds[base["commands"]:]
        else:
            st = genesis_state(self.cfg, self.save.get_meta("genesis"))
        for cmd in cmds:
            apply(st, self.cfg, cmd)
        return st

    def rebaseline(self, reason: str, check: bool = True) -> dict:
        """Make a legacy save verifiable again WITHOUT changing anything that happened: the
        current state (what the narrator has seen) becomes the verified checkpoint, and all
        later commands must replay exactly from it. History before the checkpoint cannot be
        re-derived from genesis (it was written by an engine whose saves reordered keys)."""
        before = self.replay_check() if check else {"match": None}
        self.save.write_state(self.state, tag="replay_base")
        self.save.set_meta("replay_base", {"tag": "replay_base", "commands": self.save.commands_count(),
                                           "date": self.state.date, "reason": reason,
                                           "genesis_replay_matched": before["match"]})
        self.save.commit()
        return {"checkpoint_date": self.state.date, "commands_before_checkpoint": self.save.commands_count(),
                "genesis_replay_matched_before": before["match"], "state_hash": self.state.state_hash()}

    def adopt_replay(self, rel_tol: float = 1e-9) -> dict:
        """Repair a save written before order-preserving serialisation (engine <= cbc197a):
        replace the stored state with its exact replay, but ONLY if the event history is
        identical and every difference is a float last-bit difference. Anything else is refused."""
        replay = self.replayed_state()
        if replay.event_chain != self.state.event_chain or len(replay.events) != len(self.state.events):
            return {"adopted": False, "reason": "event histories differ: this is not a rounding-only divergence"}
        diffs = []

        def walk(a, b, path):
            if isinstance(a, dict) and isinstance(b, dict):
                if set(a) != set(b):
                    diffs.append((path, "keys differ", None, None))
                    return
                for k in a:
                    walk(a[k], b[k], f"{path}/{k}")
            elif isinstance(a, list) and isinstance(b, list):
                if len(a) != len(b):
                    diffs.append((path, "length differs", None, None))
                    return
                for i, (x, y) in enumerate(zip(a, b)):
                    walk(x, y, f"{path}[{i}]")
            elif isinstance(a, float) and isinstance(b, float):
                if a != b:
                    diffs.append((path, "float", a, b))
            elif a != b:
                diffs.append((path, "value", a, b))
        walk(self.state.to_dict(), replay.to_dict(), "")
        bad = [d for d in diffs if d[1] != "float" or abs(d[2] - d[3]) > rel_tol * max(1.0, abs(d[2]), abs(d[3]))]
        report = [{"path": p, "saved": a, "replayed": b} for p, _, a, b in diffs[:50]]
        if bad:
            return {"adopted": False, "reason": f"{len(bad)} non-rounding differences", "differences": report}
        self.state = replay
        self.save.write_state(replay)
        return {"adopted": True, "float_differences": len(diffs), "differences": report,
                "new_hash": replay.state_hash()}

    # read-only helpers
    def replay_check(self) -> dict:
        st = self.replayed_state()
        base = self.save.get_meta("replay_base")
        return {"replayed_hash": st.state_hash(), "saved_hash": self.state.state_hash(),
                "match": st.state_hash() == self.state.state_hash(), "commands": self.save.commands_count(),
                "replayed_from": f"checkpoint {base['date']}" if base else "genesis"}

    def close(self):
        self.save.close()


def rewind(path: str | Path, packet_id: str, new_path: str | Path | None = None) -> Path:
    """Branch a save at an exported packet. The original save is left untouched
    unless new_path is the same file (then later history is discarded)."""
    path = Path(path)
    target = Path(new_path) if new_path else path.with_name(f"{path.stem}-from-{packet_id}{path.suffix}")
    if target != path:
        if target.exists():
            raise FileExistsError(target)
        shutil.copy(path, target)
    sf = SaveFile(target)
    info = sf.snapshot_info(packet_id)
    if info is None:
        raise KeyError(f"no snapshot for packet {packet_id}")
    st = sf.read_state(packet_id)
    sf.truncate_commands(info[1])
    base = sf.get_meta("replay_base")
    if base and base["commands"] > info[1]:
        sf.db.execute("DELETE FROM meta WHERE k='replay_base'")     # checkpoint lies after the rewind point
    for tag in sf.tags():
        if tag not in ("current", packet_id):
            other = sf.snapshot_info(tag)
            if other and other[1] > info[1]:
                sf.db.execute("DELETE FROM snapshots WHERE tag=?", (tag,))
    sf.set_meta("latest_packet", packet_id)
    sf.write_state(st)
    sf.close()
    return target
