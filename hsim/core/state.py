"""WorldState: the single container of canonical simulation state."""
from __future__ import annotations

import dataclasses
import hashlib
import json
from dataclasses import dataclass, field

from .. import models as M

REGISTRIES = {
    "people": M.Person,
    "studios": M.Studio,
    "agencies": M.Agency,
    "projects": M.Project,
    "roles": M.Role,
    "offers": M.Offer,
    "decisions": M.Decision,
    "rels": M.Relationship,
    "hist_events": M.HistoricalEvent,
    "shows": M.Show,
}


@dataclass
class WorldState:
    seed: int
    date: str
    start_date: str
    player_id: str | None = None
    config_hash: str = ""
    data_version: str = ""
    counters: dict = field(default_factory=dict)
    people: dict = field(default_factory=dict)
    studios: dict = field(default_factory=dict)
    agencies: dict = field(default_factory=dict)
    projects: dict = field(default_factory=dict)
    roles: dict = field(default_factory=dict)
    offers: dict = field(default_factory=dict)
    decisions: dict = field(default_factory=dict)
    rels: dict = field(default_factory=dict)
    hist_events: dict = field(default_factory=dict)
    shows: dict = field(default_factory=dict)
    orders: dict = field(default_factory=dict)       # player's standing orders
    notes: list = field(default_factory=list)        # narrator notes (non-mechanical canon)
    rulings: list = field(default_factory=list)      # adjudication results not yet packeted
    delegated: list = field(default_factory=list)    # delegated choices not yet packeted
    packet_id: str | None = None                     # latest exported packet
    packet_seq_mark: int = 0                         # first event seq not yet in a packet
    applied_replies: list = field(default_factory=list)  # hashes of applied reply blocks
    market: dict = field(default_factory=dict)       # rolling market stats
    events: list = field(default_factory=list)       # audit log (persisted separately)
    event_chain: str = "genesis"

    # ------------------------------------------------------------ ids ---
    def new_id(self, prefix: str) -> str:
        n = self.counters.get(prefix, 0) + 1
        self.counters[prefix] = n
        return f"{prefix}-{n:05d}"

    # --------------------------------------------------------- events ---
    def log(self, etype: str, text: str, *, actors=(), refs=None, data=None,
            public: bool = True, salience: int = 1) -> dict:
        """Append an immutable event. `text` is canonical, narrator-safe prose
        (only public facts or facts the player character knows); hidden
        quantities belong in `data` and are filtered from packets."""
        ev = {
            "seq": len(self.events),
            "date": self.date,
            "type": etype,
            "text": text,
            "actors": sorted(set(actors)),
            "refs": refs or {},
            "data": data or {},
            "public": public,
            "salience": salience,
        }
        self.event_chain = hashlib.sha256(
            (self.event_chain + json.dumps(ev, sort_keys=True)).encode()).hexdigest()[:24]
        self.events.append(ev)
        return ev

    # ---------------------------------------------------- relationships ---
    def rel(self, a: str, b: str, create: bool = True) -> M.Relationship | None:
        x, y = sorted((a, b))
        key = f"{x}|{y}"
        r = self.rels.get(key)
        if r is None and create:
            r = M.Relationship(a=x, b=y, since=self.date)
            self.rels[key] = r
        return r

    # ---------------------------------------------------- serialisation ---
    def to_dict(self, include_events: bool = False) -> dict:
        out = {}
        for f in dataclasses.fields(self):
            v = getattr(self, f.name)
            if f.name == "events" and not include_events:
                continue
            if f.name in REGISTRIES:
                v = {k: dataclasses.asdict(o) for k, o in sorted(v.items())}
            out[f.name] = v
        return out

    @classmethod
    def from_dict(cls, d: dict, events: list | None = None) -> "WorldState":
        d = dict(d)
        for name, typ in REGISTRIES.items():
            d[name] = {k: typ(**v) for k, v in d.get(name, {}).items()}
        d["events"] = events if events is not None else d.get("events", [])
        return cls(**d)

    def state_hash(self) -> str:
        blob = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()[:16]

    # ------------------------------------------------------- helpers ---
    @property
    def player(self) -> M.Person | None:
        return self.people.get(self.player_id) if self.player_id else None

    def _cached(self, name, pred):
        """Per-week memo of sorted people lists (not serialised; rebuilt when date/population change)."""
        cache = self.__dict__.setdefault("_memo", {})
        key = (name, self.date, len(self.people))
        hit = cache.get(name)
        if hit and hit[0] == key:
            return hit[1]
        lst = [p for _, p in sorted(self.people.items()) if pred(p)]
        cache[name] = (key, lst)
        return lst

    def actors(self):
        return [p for p in self._cached("actors", lambda p: "actor" in p.roles)
                if p.active and p.death is None]

    def directors(self):
        return [p for p in self._cached("directors", lambda p: "director" in p.roles)
                if p.active and p.death is None]
