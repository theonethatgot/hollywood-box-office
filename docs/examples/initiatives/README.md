# Initiatives demonstration: Daniel Brooks, 1980–82 (real engine output)

A saved career on the historical 1980 world (`hsim new ... --historical --seed 1950 --name "Daniel Brooks"
--gender m --birth 1950-03-14 --background notable --goals prestige=4,art=3,money=2,fame=2,stability=1`),
played in four-week turns through ordinary packets and reply blocks: 40 turns, January 1980 to August 1982.
Decisions followed simple rules: attend auditions prepared, accept offers, keep on-set chemistry professional.
Narrator moves (initiatives and narrative canon) were written only from what the packets said. The narration
itself is omitted. `hsim verify` replays all 81 commands from genesis to the identical state hash.

Nothing was forced. Most attempts fail or stall, which is what the industry is like for a mid-list actor.

## 1. A narrator-originated initiative, adjudicated (July–August 1980)
`1a` Daniel is shooting *Signal of the Dawn* (Columbia, dir. Bruce Beresford). The packet's `period_summary` lists
that under `working` and `quiet_period` is false. The trades report that Universal greenlit *Summer Hours*.

`1b` The reply proposes two initiatives, pursuing *Summer Hours* and a general meeting with Sydney Pollack, and
records one narrative detail about Beresford's set.

`1c` The rulings:
- *Summer Hours*: **rejected, with the concrete reason**: "The dates don't work: 'Summer Hours' shoots
  1980-10-03 to 1980-11-28, and you're committed to 'Signal of the Dawn' until 1980-10-24."
- Pollack: **pending**, then resolved a week later ("Met Sydney Pollack"), and it now shows in `network`.

`1d` Daniel (prestige- and art-driven, about $120k in the bank) develops an original drama, *The Long Field*: hiring
Ellen Lindqvist costs $17k and takes eight weeks. He also tells his agent to avoid horror and commercials; she
complies (`agent.your_directives`), and from then on she applies it to every submission.

## 2. An agent pursuing a consequential opportunity on her own (October 1980)
`2` Margaret Hayes represents 67 actors and Daniel is "mid-list". The packet says so, and that her limited calls go
where a client just missed a casting director's list on a part worth it. When MGM's *Endless Promise* went out, she
spent a call on him for the colead: "pushed for you on Luis (colead) ... because you were just outside the casting
director's list; casting declined: they want a bigger name for this part." The same packet carries an offer Daniel
won by audition (*Wild Trouble*, Disney, $99k).

The same rules apply to every client. In the last eight months of this world, agents made 600 pushes: 297 got the
client seen and 19 of those ended in a casting. Examples include Jessica Lange (colead, *Crane's Frontier*) and
Robert Duvall (colead, *Sweethearts*). Being seen is not being cast.

## 3. Negotiation and partial success: building a package (December 1980–February 1981)
`3a` *The Long Field* draft is done ("you love it"; this is Daniel's impression, and script quality stays hidden).
Columbia, Fox and Disney pass; **United Artists "liked it but wants changes or a bigger name attached"**; MGM passes too.

`3b` The narrator responds: Daniel gives the script to Beresford, his *Signal of the Dawn* director, over coffee,
and asks him to direct (`develop_project`, `action: attach`).

`3c` **Accepted**: "Bruce Beresford read it and said yes." Beresford decided on his own read, his standing versus
Daniel's and his schedule. The interested studios read the package again.

## 4. Consequences unfold over months (spring–summer 1981)
`4a` Even with Beresford attached, Orion and Paramount join UA and Warner in "liked it, wants more", and every studio
passes: **turnaround**. The initiative stays open. The packet lists the four studios that would look again "with a
stronger package or a rewrite."

`4b` The narrator commissions a rewrite ($9k).

## 5. The result becomes hard canon (October 1981)
`5a` With the new draft, Warner passes again and then **Orion says yes**: "'The Long Field' is greenlit with you
attached." `agent.doors_open`: "they'll see you for Stuart (lead) when casting opens."

`5b` The offer comes through the attachment: lead in *The Long Field*, Orion, **dir. Bruce Beresford** (the package
held), $94k plus 2 net points. Daniel still had to accept terms.

## 6. A later packet preserves the continuity (August 1982)
`6` Ten months later:
- `your_work`: *The Long Field* in post, "an original project developed by its star", directed by Beresford.
- Beresford's people card: `why_here` "directing your film 'The Long Field'"; `with_you` history "a strong audition
  for 'Signal of the Dawn' (1980-05-23)" and "agreed to attach to your project 'The Long Field' (1981-01-16)"; and
  `narrative_canon` with both details the narrator created (the soldering iron on his set, the script handed over
  at Du-par's).
- `narrative_canon`: Margaret's habit of calling Daniel "kiddo" before bad news (from the first turn), his
  Los Feliz bungalow, the Big Chief tablet, Ellen's midnight phone calls.
- `continuity.initiatives_resolved`: the Pollack meeting, and *The Long Field* from "Hired screenwriter" to "Orion
  Pictures said yes".
- `agent`: the most recent push for him (a colead at *The Thunder Justice*, declined) and his directives.

## What this run found (fixed before the final run)
Playing the career exposed real problems, each now covered by a regression test:
- At greenlight the studio replaced the attached director with its own choice. A package now keeps its attachments.
- On-set chemistry prompts ignored the protagonist's orientation and repeated weekly (four in five weeks).
- The premieres interrupt stopped time every week of a film's run, not just its opening.
- A re-gendered lead kept a woman's name ("Carol Quinlan") for a male developer.
- Closed initiatives vanished from later packets, and full film casts crowded out people with history.
- An agent's read of the room used the protagonist's rank instead of their own client's.
- Narrative canon about someone the protagonist had never met was accepted silently (my harness had named the
  wrong director). It is now flagged.

Still simple: studio pitches are sequential, and only the strongest attachment counts in a studio's read.
Financing, producers and turnaround deals are not modelled. Shoot locations are generic: this Ohio farm drama
shot in Mexico.
