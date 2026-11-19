"""Command-line front end: `hsim <command> <save> ...`.

Typical loop with ChatGPT:
  hsim new career1 --name "Alex Reyes" --gender f --birth 1957-04-12 --background unknown
  hsim advance career1 --weeks 8          # stops early at decisions
  hsim packet career1                     # writes play/career1/pkt-00001.md; paste into ChatGPT
  hsim submit career1 reply.md            # paste ChatGPT's reply into a file (or use -)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from . import service as S
from .core.util import money
from .narrator import reply as RPL
from .narrator import packet as PK
from .narrator.packet import bank_label, critic_label, fame_label, heat_label
from .systems import decisions as D

SAVES = Path("saves")
PLAY = Path("play")


def _path(name: str) -> Path:
    p = Path(name)
    return p if p.suffix == ".sqlite" else SAVES / f"{name}.sqlite"


def _open(name: str) -> S.Game:
    g = S.Game.open(_path(name))
    w = g.config_warning()
    if w:
        click.secho(f"warning: {w}", fg="yellow", err=True)
    return g


@click.group()
def main():
    """Hollywood simulation engine."""


@main.command()
@click.argument("save")
@click.option("--start", default="1980-01-04", show_default=True, help="Start date (snapped to Friday).")
@click.option("--seed", default=1980, show_default=True, type=int)
@click.option("--name", default="Alex Reyes", show_default=True)
@click.option("--gender", type=click.Choice(["m", "f"]), default="f", show_default=True)
@click.option("--birth", default="1957-04-12", show_default=True)
@click.option("--background", type=click.Choice(["unknown", "working", "star"]), default="unknown", show_default=True)
@click.option("--attracted-to", default=None, help="Comma list of m,f (protagonist's own orientation).")
@click.option("--bio", default=None)
@click.option("--data-pack", default=None, help="Historical data pack JSON (see datapipe/).")
def new(save, start, seed, name, gender, birth, background, attracted_to, bio, data_pack):
    """Create a new world and protagonist."""
    params = {"seed": seed, "start": start, "data_pack": data_pack,
              "player": {"name": name, "gender": gender, "birth": birth, "background": background}}
    if attracted_to:
        params["player"]["attracted_to"] = attracted_to.split(",")
    if bio:
        params["player"]["bio"] = bio
    g = S.Game.new(_path(save), params)
    st = g.state
    click.echo(f"Created {_path(save)}: {len(st.people)} people, {len(st.projects)} projects, start {st.date}.")
    click.echo(f"Protagonist: {st.player.name} ({background}).")


@main.command()
@click.argument("save")
def status(save):
    """Show the protagonist's situation (observable values only)."""
    g = _open(save)
    st, p = g.state, g.state.player
    click.echo(f"{st.date} — {p.name}")
    click.echo(f"  public profile: {fame_label(p.fame)} | momentum: {heat_label(p.heat)} | "
               f"draw: {bank_label(p.bankability)} | critics: "
               f"{critic_label(p.critical_rep) if PK._reviewed(st, p) else 'no reviewed work yet'}")
    click.echo(f"  quote: {money(p.quote)} | cash: {money(p.cash)} | monthly costs: {money(p.monthly_costs)}")
    click.echo(f"  agent: {st.agencies[p.agent_id].name if p.agent_id else 'none'} | partner: "
               f"{st.people[p.partner_id].name if p.partner_id else (p.partner_status or 'single')}")
    for d in D.pending(st):
        click.echo(f"  PENDING {d.id} [{d.kind}] {d.summary}\n      options: {d.options} (deadline {d.deadline})")


@main.command()
@click.argument("save")
@click.option("--weeks", type=int, default=None)
@click.option("--until", default=None)
def advance(save, weeks, until):
    """Advance time; stops early when a decision is needed."""
    g = _open(save)
    cmd = {"type": "advance"}
    if until:
        cmd["until"] = until
    else:
        cmd["weeks"] = weeks or 1
    r = g.command(cmd)
    click.echo(f"Advanced {r['weeks']} week(s): {r['from']} → {r['to']} ({r['stopped']}).")
    for d in D.pending(g.state):
        click.echo(f"  PENDING {d.id} [{d.kind}] {d.summary}\n      options: {d.options}")


@main.command()
@click.argument("save")
@click.argument("decision_id")
@click.argument("choice")
@click.option("--fee", type=float, default=None)
def decide(save, decision_id, choice, fee):
    """Resolve a pending decision directly."""
    g = _open(save)
    params = {"fee": fee} if fee else {}
    r = g.command({"type": "decide", "id": decision_id, "choice": choice, "params": params})
    click.echo(r["text"])


@main.command()
@click.argument("save")
@click.option("--out", default=None, help="Output file (default play/<save>/<packet>.md); '-' for stdout.")
def packet(save, out):
    """Export a narrator packet for ChatGPT."""
    g = _open(save)
    r = g.command({"type": "packet"})
    if out == "-":
        click.echo(r["text"])
        return
    path = Path(out) if out else PLAY / Path(save).stem / f"{r['packet_id']}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(r["text"])
    click.echo(f"Wrote {path} ({len(r['text'])} chars). Paste it into your ChatGPT narrator project.")


@main.command()
@click.argument("save")
@click.argument("reply_file")
@click.option("--force", is_flag=True, help="Apply even if reply_to is not the latest packet.")
def submit(save, reply_file, force):
    """Apply ChatGPT's reply (file containing the ```engine block, or '-' for stdin)."""
    g = _open(save)
    text = sys.stdin.read() if reply_file == "-" else Path(reply_file).read_text()
    try:
        block = RPL.extract(text)
    except RPL.ReplyError as e:
        raise click.ClickException(str(e))
    r = g.command({"type": "submit", "block": block, "force": force})
    if r["status"] != "applied":
        raise click.ClickException(r["message"])
    for t in r["applied"]:
        click.echo(f"  decision: {t}")
    for e in r["errors"]:
        click.secho(f"  error: {e}", fg="red")
    for ru in r["rulings"]:
        click.echo(f"  ruling [{ru['proposal']}] {ru['result']}: {ru['text']}")
    if "advance" in r:
        a = r["advance"]
        click.echo(f"Advanced {a['weeks']} week(s) to {a['to']} ({a['stopped']}). Export the next packet with: "
                   f"hsim packet {save}")


@main.command()
@click.argument("save")
@click.option("--set", "pairs", multiple=True, help="key=json, e.g. --set 'let_agent_negotiate=[\"supporting\"]'")
def orders(save, pairs):
    """Show or change standing orders (delegation and interrupts)."""
    g = _open(save)
    if pairs:
        upd = {}
        for kv in pairs:
            k, v = kv.split("=", 1)
            upd[k] = json.loads(v)
        g.command({"type": "orders", "orders": upd})
    click.echo(json.dumps(g.state.orders, indent=2))


@main.command()
@click.argument("save")
def boxoffice(save):
    """This week's chart and yearly totals."""
    g = _open(save)
    ch = g.state.market.get("chart", {})
    click.echo(f"Chart for week of {ch.get('date')}")
    for i, x in enumerate(ch.get("top", []), 1):
        click.echo(f"{i:>2}. {x['title']:<28} {x['studio']:<26} {money(x['gross']):>8}  total {money(x['total']):>8}  wk {x['week']}")
    for y, v in sorted(g.state.market.get("year_totals", {}).items()):
        click.echo(f"  {y}: {money(v)} domestic, {g.state.market['year_admissions'][y]/1e6:.0f}M admissions")


@main.command()
@click.argument("save")
@click.option("--limit", default=30)
@click.option("--grep", default=None)
@click.option("--all", "show_all", is_flag=True, help="Include private NPC events (debug).")
def history(save, limit, grep, show_all):
    """Recent events from the audit log."""
    g = _open(save)
    pl = g.state.player_id
    ev = [e for e in g.state.events if show_all or e["public"] or pl in e["actors"]]
    if grep:
        ev = [e for e in ev if grep.lower() in e["text"].lower()]
    for e in ev[-limit:]:
        click.echo(f"{e['date']} [{e['type']}] {e['text']}")


@main.command()
@click.argument("save")
@click.argument("packet_id")
@click.option("--to", "new_name", default=None, help="Name of the branched save (default <save>-from-<packet>).")
@click.option("--in-place", is_flag=True, help="Discard everything after the packet in this save.")
def rewind(save, packet_id, new_name, in_place):
    """Branch (or rewind) a save to the moment a packet was exported."""
    src = _path(save)
    target = src if in_place else (_path(new_name) if new_name else None)
    out = S.rewind(src, packet_id, target)
    click.echo(f"Rewound to {packet_id}: {out}")


@main.command()
@click.argument("save")
def verify(save):
    """Replay genesis + command log and compare state hashes."""
    g = _open(save)
    r = g.replay_check()
    click.echo(json.dumps(r, indent=2))
    if not r["match"]:
        sys.exit(1)


@main.command()
@click.argument("save")
@click.argument("person_id")
def inspect(save, person_id):
    """DEBUG: show hidden values for a person. Never give this output to the narrator."""
    import dataclasses
    g = _open(save)
    p = g.state.people.get(person_id)
    if not p:
        raise click.ClickException("no such person")
    d = dataclasses.asdict(p)
    d.pop("calendar")
    click.echo(json.dumps(d, indent=2, default=str))


if __name__ == "__main__":
    main()
