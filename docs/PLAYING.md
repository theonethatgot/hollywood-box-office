# Playing with ChatGPT as narrator

## One-time setup
```bash
pip install -e .
```
In ChatGPT, create a **Project**, and paste `NARRATOR_GUIDE.md` into its instructions.

## Start a career
```bash
hsim new career1 --name "Nora Vance" --gender f --birth 1956-09-14 --background unknown
```
- `--background`: `unknown`, `working` or `star`. This sets your starting position:
  credits, fame, quote, agent and money. Your hidden talent is drawn from the same
  distribution as any NPC with that background.
- `--seed`: a different number gives a different world.
- Optional: `--attracted-to f` or `m` or `m,f`, and `--bio "..."`.

## The loop
```bash
hsim advance career1 --weeks 8        # stops early when a decision is yours
hsim packet career1                   # writes play/career1/pkt-0000N.md
```
1. Paste the packet into the ChatGPT Project chat (you can attach the file instead).
2. ChatGPT narrates and presents your choices. You reply in character or out.
3. When you've chosen, ChatGPT ends its message with an ` ```engine ` block.
4. Copy ChatGPT's whole reply into a file, for example `play/career1/reply.md`, then:
```bash
hsim submit career1 play/career1/reply.md
hsim packet career1
```
`submit` applies your decisions, rules on proposals and advances time if the
block asks for it. Then export the next packet.

## Useful commands
| Command | What it does |
|---|---|
| `hsim status career1` | Your situation and pending decisions |
| `hsim decide career1 dec-00012 accept` | Decide directly, without ChatGPT (`--fee 60000` for counter) |
| `hsim boxoffice career1` | This week's chart and yearly totals |
| `hsim history career1 --limit 40` | Recent events you would know about |
| `hsim orders career1` | Show standing orders |
| `hsim orders career1 --set 'let_agent_negotiate=["supporting"]'` | Delegate routine offers |
| `hsim rewind career1 pkt-00007` | Branch the save back to that packet (the original is kept) |
| `hsim verify career1` | Replay the whole save and confirm the state is reproducible |
| `hsim inspect career1 player` | **Debug only**: hidden values. Don't show this to the narrator. |

## Standing orders (delegation)
- `auto_accept_auditions`: role sizes your agent books without asking.
- `auto_decline_offers_below_quote_pct`: for example, 60 turns down lowball offers automatically.
- `let_agent_negotiate`: role sizes where offers are accepted or declined by
  your character's own goals, the same rule NPCs use.
- `interrupt_on`: what stops time. Options: `offers`, `auditions_lead`,
  `counter_offers`, `romance`, `premieres`, `nominations`.

## If something goes wrong
- **ChatGPT forgot the engine block:** ask it to "end with the engine block".
- **ChatGPT contradicted canon:** point to the packet. The engine's version stands.
- **You replied to an old packet:** `submit` refuses. Export a fresh packet, or
  `rewind` if you want to redo a turn.
- **Submitting the same reply twice:** it's detected and ignored.
