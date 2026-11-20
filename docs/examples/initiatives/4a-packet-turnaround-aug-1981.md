# Narrator packet pkt-00025 — 1981-08-14

## RULES
You are the narrator of a Hollywood career simulation. The engine is the authority.
Three levels of canon:
- HARD CANON (canon, rulings, your_work, standing, people facts): engine-confirmed. Never contradict it; never
  invent numbers (money, grosses, scores, dates), castings, audition results, awards, deals, deaths or outcomes.
- NARRATIVE CANON (narrative_canon, people[].narrative_canon): details you created earlier (dialogue beats,
  rehearsals, habits, minor characters, places). Keep them consistent. Record new ones under `narrative`.
- PROPOSED CONSEQUENTIAL CANON (initiatives): anything that should change the world (pursuing a film or a
  filmmaker, meetings, introductions, social plans with someone, publicity, career repositioning, developing
  an original project) goes under `initiatives`. Narrate the attempt, not the outcome; the engine rules
  (accepted, partial, rejected with a reason, or pending for weeks) and the next packet reports it.
- Present PENDING DECISIONS as in-story choices. End every reply with the engine block (see REPLY FORMAT).
- Use people's `why_here`, `lately` and `with_you` to ground scenes; do not invent extra social events to fill time.
- Information labelled 'rumour' may be wrong. Do not reveal anything the protagonist could not know.

## STATE
```yaml
packet: pkt-00025
date: '1981-08-14'
covers: 1981-07-17 .. 1981-08-14
state_hash: 2f503035a36e84ad
protagonist:
  id: player
  name: Daniel Brooks
  age: 31
  background: A recognisable name with a few memorable roles; most at home in scifi; volatile, generous with colleagues.
  traits:
  - volatile
  - generous with colleagues
  - vain
  goals:
    prestige: 0.33
    art: 0.25
    money: 0.17
    fame: 0.17
    stability: 0.08
  public_profile: a recognisable face
  industry_view:
    momentum: steady
    draw: a modest draw
    critics: respected
  quote_reported_in_trades: $94k
  agent: Margaret Hayes at Starling-Barr Talent (fictional)
  agent_strategy: Pursuing respected directors and serious dramatic material and interesting scripts, stage work
    and character parts, even for less money; not prioritising steady bookings and series work over long shots.
  persona:
    hometown: Columbus, Ohio
    signature: always first to arrive and last to leave
    background: trained at the Yale School of Drama
  money:
    cash: 157006.0
    monthly_costs: 6000.0
  energy: exhausted
  relationship_status: single
  awards: []
canon:
- id: ev-6936
  date: '1981-07-17'
  text: Your agent got you a read for the victim's brother on 'Desert Force' (first-run syndication), casting Kim
    Anderson.
- id: ev-6937
  date: '1981-07-17'
  text: 'You read for the victim''s brother on ''Desert Force'' (first-run syndication) (an episode about a stranded
    school bus) and were not picked; casting: Kim Anderson.'
- id: ev-6938
  date: '1981-07-17'
  text: 'Feedback on ''Desert Force'' (first-run syndication) (via your agent): they liked the read but wanted someone
    with more screen presence.'
- id: ev-6939
  date: '1981-07-17'
  text: Booked a small part in 'Warner's Motive' (New World Pictures); playing Leon Sinclair (a few scenes); directed
    by Charles Martin; with Bill Cosby, Monique Proulx, Joseph Maher, Reggie Kowalski (1981-07-31 to 1981-08-14,
    $11k).
  provenance: simulated event in this timeline
- id: ev-6941
  date: '1981-07-17'
  text: 'Payment received: second half of fee for ''The Red Run'' — $27k gross, $15k after commission and tax.'
- id: ev-6942
  date: '1981-07-17'
  text: '''The Red Run'' wrapped principal photography and moved into post-production.'
  provenance: simulated event in this timeline
- id: ev-6999
  date: '1981-07-24'
  text: You were invited to the premiere of 'Wolfen' (your agency represents 3 of the film's cast), where you met
    Albert Finney, Diane Venora.
  provenance: simulated event in this timeline
- id: ev-7011
  date: '1981-07-31'
  text: Booked Ibsen's 'An Enemy of the People' at a downtown Los Angeles repertory company; with Mitchell Warner,
    Peter Winslow, Michael Coleman (1981-08-21 to 1981-10-02, $12k).
- id: ev-7013
  date: '1981-07-31'
  text: After soft tracking, the studio is scaling back the campaign for 'Signal of the Dawn'.
- id: ev-7014
  date: '1981-07-31'
  text: Pre-release tracking projects 'Signal of the Dawn' to open around $546k.
- id: ev-7020
  date: '1981-07-31'
  text: You were invited to the premiere of 'Letters of the Wolves' (you've worked for Orion Pictures), where you
    met Candy Clark.
  provenance: simulated event in this timeline
- id: ev-7095
  date: '1981-08-07'
  text: 'Margaret Hayes checked in; they submitted you for 11 roles this past month; 1 got you in the room; the
    most common feedback on passes: ''they had plenty of strong submissions''; 2 smaller bookings came through;
    they''re steering you toward action parts, where you''ve been landing near the top of the room; they want to
    get you seen in a respected stage production.'
period_summary:
  overview: 4 week(s), working on 1 job(s), 8 submission(s) by your agent, 1 call-in(s), 1 audition(s), 2 booking(s);
    net money +$9k.
  working:
  - 'film bit: Warner''s Motive (1981-07-31 to 1981-08-14)'
  quiet_period: false
  note: ''
rulings: []
delegated:
- 'Margaret Hayes booked you: a small part in ''Warner''s Motive'' (New World Pictures); playing Leon Sinclair (a
  few scenes); directed by Charles Martin; with Bill Cosby, Monique Proulx, Joseph Maher, Reggie Kowalski — 1981-07-31
  to 1981-08-14, paying $11k.'
- 'Margaret Hayes booked you: Ibsen''s ''An Enemy of the People'' at a downtown Los Angeles repertory company; with
  Mitchell Warner, Peter Winslow, Michael Coleman — 1981-08-21 to 1981-10-02, paying $12k.'
standing_changes:
  now:
    public_profile: a recognisable face
    momentum: steady
    draw: a modest draw
    critics: respected
    industry_standing: a working professional
    quote: $94k
  changes: []
  relevant_events: []
agent:
  agent: Margaret Hayes (agent at Starling-Barr Talent (fictional))
  strategy: Pursuing respected directors and serious dramatic material and interesting scripts, stage work and character
    parts, even for less money; not prioritising steady bookings and series work over long shots.
  attention: 'Margaret Hayes represents 68 actors and you are mid-list. Calls are limited: they push when you just
    miss a casting director''s list on a part worth it, or when a director already rates you'
  your_directives:
    avoid_genres:
    - horror
    no_commercials: true
initiatives:
- id: ini-00002
  kind: develop_project
  status: turnaround
  started: '1980-08-22'
  history:
  - '1981-03-27: Orion Pictures liked it but wants changes or a bigger name attached; still pitching.'
  - '1981-04-17: Paramount Pictures liked it but wants changes or a bigger name attached; still pitching.'
  - '1981-05-08: Universal Pictures passed.'
  - '1981-05-22: New World Pictures passed.'
  - '1981-06-05: Every studio has passed; the project is in turnaround (United Artists, Warner Bros., Orion Pictures,
    Paramount Pictures would look again with a stronger package or a rewrite).'
career_activity:
  submissions:
  - '1981-07-17: Desmond Wyatt (supporting) in ''Vance''s Bridges'' (Orion Pictures, casting Lori Wade) — passed:
    they didn''t see you as a drama type'
  - '1981-07-17: Barry Harper (featured) in ''Vance''s Bridges'' (Orion Pictures, casting Lori Wade) — passed: the
    part pays well below your quote'
  - '1981-07-17: a hotel clerk (guest) in ''Westside Patrol'' (ABC, casting Leslie Yates) — passed: they had plenty
    of strong submissions'
  - '1981-07-17: the victim''s brother (guest) in ''Desert Force'' (first-run syndication, casting Kim Anderson)
    — called in: the show''s casting director wanted to see you'
  - '1981-07-17: a hotel clerk (guest) in ''Dakota Investigations'' (CBS, casting Kim Anderson) — passed: they had
    plenty of strong submissions'
  - '1981-07-17: a desperate parent (guest) in ''Highway Patrol'' (CBS, casting Lena Brooks) — passed: they had
    plenty of strong submissions'
  - '1981-07-17: a drifter (guest) in ''Santos Files'' (CBS, casting Margaret Merrick) — passed: they had plenty
    of strong submissions'
  - '1981-07-31: Ellis (lead) in ''Frontier of the Damned'' (Orion Pictures, casting Lori Wade) — passed: they want
    a bigger name for this part'
  auditions:
  - '1981-07-17: Your agent got you a read for the victim''s brother on ''Desert Force'' (first-run syndication),
    casting Kim Anderson.'
  - '1981-07-17: You read for the victim''s brother on ''Desert Force'' (first-run syndication) (an episode about
    a stranded school bus) and were not picked; casting: Kim Anderson.'
  bookings:
  - '1981-07-31 to 1981-08-14: a small part in ''Warner''s Motive'' (New World Pictures); playing Leon Sinclair
    (a few scenes); directed by Charles Martin; with Bill Cosby, Monique Proulx, Joseph Maher, Reggie Kowalski ($11k)'
  - '1981-08-21 to 1981-10-02: Ibsen''s ''An Enemy of the People'' at a downtown Los Angeles repertory company;
    with Mitchell Warner, Peter Winslow, Michael Coleman ($12k)'
  agent_calls:
  - '1981-08-07: Margaret Hayes checked in; they submitted you for 11 roles this past month; 1 got you in the room;
    the most common feedback on passes: ''they had plenty of strong submissions''; 2 smaller bookings came through;
    they''re steering you toward action parts, where you''ve been landing near the top of the room; they want to
    get you seen in a respected stage production.'
your_work:
- title: Signal of the Dawn
  studio: Columbia Pictures
  genre: scifi
  premise: A teenage hacker wakes up decades after the launch before first contact turns to war.
  your_role: 'Leon — supporting: a key supporting part'
  director: Bruce Beresford
  costars:
  - Hal Keating as Luis (lead, character name simulated)
  - Natalie Rhodes as Susan Wyatt (colead, character name simulated)
  - Elizabeth Taylor as Lena Tierney (supporting, character name simulated)
  - Ward Costello as Timothy Dalton (featured, character name simulated)
  - Joanne Linville as Natalie (featured, character name simulated)
  - Ben Vereen as Lionel (featured, character name simulated)
  - Alan Okonkwo as Trevor Petrakis (featured, character name simulated)
  - Carl Ballantine as Vincent (featured, character name simulated)
  - Rachel Thorne as Gloria Gallagher (featured, character name simulated)
  - Joyce Halloran as Joan Sterling (featured, character name simulated)
  - Barry Sinclair as Dean Irving (featured, character name simulated)
  - Gail Tierney as Maxine Garrison (featured, character name simulated)
  - Buck Henry as Russell (featured, character name simulated)
  - Don Adams as Bruce (featured, character name simulated)
  stage: awaiting_release
  location: Los Angeles
  terms: $99k
  identity: effects-driven scifi; a mid-budget studio picture looking for a marketable lead
  story:
    provenance: simulated screenplay for a fictional production
    logline: 'A effects-driven scifi: A teenage hacker wakes up decades after the launch before first contact turns
      to war.'
    central_conflict: far from help, Luis must hold the crew together while Lena Tierney hides the truth about the
      mission
    characters:
    - 'Luis (the reluctant leader, played by Hal Keating): wants to win back respect they lost; flaw: an old lie;
      arc from an old lie toward responsibility'
    - 'Susan Wyatt (the second-in-command, played by Natalie Rhodes): wants to keep a promise; flaw: fear of being
      ordinary; arc from fear of being ordinary toward forgiveness'
    - 'Lena Tierney (the corporate liaison, played by Elizabeth Taylor): wants to prove they still matter; flaw:
      a temper they can''t control; arc from a temper they can''t control toward a reckoning with self-respect'
    - 'Leon (the android, played by Daniel Brooks): wants to make things right; flaw: trusting the wrong people;
      arc from trusting the wrong people toward a reckoning with courage'
    relationships:
    - 'Luis and Susan Wyatt: a command partnership'
    - 'Luis and Lena Tierney: antagonists'
    - 'Luis and Leon: a complicated alliance'
    beats:
    - 'Setup: Luis''s ordinary life, already cracking (A teenage hacker wakes up decades after the launch before
      first contact turns to war)'
    - 'Inciting incident: an event forces Luis and Susan Wyatt together'
    - 'Midpoint: a revelation turns Lena Tierney from obstacle into real threat'
    - 'Low point: Luis loses what they were fighting for, and Susan Wyatt walks away'
    - 'Climax: Luis confronts Lena Tierney; what Luis has become decides the ending'
    creative_intent: Bruce Beresford wants long, unbroken takes and room for actors to find moments (simulation
      characterisation of this production, not a documented account of their real working methods; portray consistently
      with what is publicly known about them)
    your_key_scenes:
    - a quiet confession on a rooftop
    - a showdown in the rain
    your_read_of_the_script: you have doubts; the central relationship has promise but the rest needs work (your
      impression; it may be wrong)
  provenance: 'simulated production: not a real film; its cast and characters are part of this timeline'
  release_date: '1981-08-21'
  tracking_opening: $546k
- title: Wild Trouble
  studio: Buena Vista (Disney)
  genre: comedy
  premise: A stuffy accountant inherits a failing nightclub and everything goes wrong.
  your_role: 'Dean Wyatt — supporting: a key supporting part'
  director: Michael Nankin
  costars:
  - Maxine Keating as Teresa Yates (lead, character name simulated)
  - Glenn Anderson as Richard Calloway (colead, character name simulated)
  - Ingrid Emerson as Vanessa (supporting, character name simulated)
  - John Altman as Dale (featured, character name simulated)
  - Maxine Stuart as Pamela (featured, character name simulated)
  - Katy Jurado as Karen Kessler (featured, character name simulated)
  - Richard Widmark as Jeffrey Emerson (featured, character name simulated)
  - David Opatoshu as Curtis (featured, character name simulated)
  - Red Buttons as Barry Yates (featured, character name simulated)
  - Reggie Bannister as Richard Whitaker (featured, character name simulated)
  - Ava Gardner as Daphne Wolcott (featured, character name simulated)
  stage: post
  location: Los Angeles
  terms: $99k
  identity: screwball comedy; a big-budget event picture the studio is building its year around
  story:
    provenance: simulated screenplay for a fictional production
    logline: 'A screwball comedy: A stuffy accountant inherits a failing nightclub and everything goes wrong.'
    central_conflict: Teresa Yates's simple plan spirals out of control, and Richard Calloway keeps making it worse
      and funnier
    characters:
    - 'Teresa Yates (the protagonist, played by Maxine Keating): wants to prove they still matter; flaw: a temper
      they can''t control; arc from a temper they can''t control toward honesty'
    - 'Richard Calloway (the reluctant partner-in-crime, played by Glenn Anderson): wants to win back respect they
      lost; flaw: fear of being ordinary; arc from fear of being ordinary toward letting go'
    - 'Vanessa (the boss, played by Ingrid Emerson): wants to finally tell the truth; flaw: an old lie; arc from
      an old lie toward a reckoning with honesty'
    - 'Dean Wyatt (the nosy neighbour, played by Daniel Brooks): wants to keep a promise; flaw: drinking; arc from
      drinking toward a reckoning with courage'
    relationships:
    - 'Teresa Yates and Richard Calloway: an odd-couple partnership'
    - 'Teresa Yates and Vanessa: antagonists'
    - 'Teresa Yates and Dean Wyatt: a complicated alliance'
    beats:
    - 'Setup: Teresa Yates''s ordinary life, already cracking (A stuffy accountant inherits a failing nightclub
      and everything goes wrong)'
    - 'Inciting incident: an event forces Teresa Yates and Richard Calloway together'
    - 'Midpoint: a revelation turns Vanessa from obstacle into real threat'
    - 'Low point: Teresa Yates loses what they were fighting for, and Richard Calloway walks away'
    - 'Climax: Teresa Yates confronts Vanessa; what Teresa Yates has become decides the ending'
    creative_intent: Michael Nankin wants long, unbroken takes and room for actors to find moments (simulation characterisation
      of this production, not a documented account of their real working methods; portray consistently with what
      is publicly known about them)
    your_key_scenes:
    - a late-night confrontation in a kitchen
    - an argument in a moving car
    your_read_of_the_script: you think it's solid; the central relationship works, though parts feel familiar (your
      impression; it may be wrong)
  provenance: 'simulated production: not a real film; its cast and characters are part of this timeline'
- title: The Red Run
  studio: Orion Pictures
  genre: action
  premise: A mercenary with a conscience must escort a witness across the border while the clock runs down.
  your_role: 'Charles Wyatt — supporting: a key supporting part'
  director: Michael D. Moore
  costars:
  - Arnold Schwarzenegger as Russell Abernathy (lead, character name simulated)
  - Lena Sterling as Donna Jameson (colead, character name simulated)
  - David Warner as Kenneth Vaughn (supporting, character name simulated)
  - Alec McCowen as Joel Okafor (supporting, character name simulated)
  - Francisco Rabal as Dean Szabo (featured, character name simulated)
  - Broderick Crawford as Andre Merrick (featured, character name simulated)
  - Beatrice Straight as Joan Vaughn (featured, character name simulated)
  - Michael Callan as Larry (featured, character name simulated)
  - David Wayne as Marcus Dawson (featured, character name simulated)
  - Jack Albertson as Victor Gallagher (featured, character name simulated)
  - Adolph Green as Jerry Yates (featured, character name simulated)
  - Len Cariou as Philip (featured, character name simulated)
  - Monty Baker as Anthony Halloran (featured, character name simulated)
  - Keith Barron as Desmond Donovan (featured, character name simulated)
  - Marion Ross as Joyce Yates (featured, character name simulated)
  - Mark Lester as Robert (featured, character name simulated)
  stage: post
  location: Toronto
  terms: $55k
  identity: glossy action; a low-budget exploitation picture aimed at drive-ins and late shows
  story:
    provenance: simulated screenplay for a fictional production
    logline: 'A glossy action: A mercenary with a conscience must escort a witness across the border while the clock
      runs down.'
    central_conflict: Russell Abernathy has one chance to stop Kenneth Vaughn before the deadline, and can't do
      it without Donna Jameson
    characters:
    - 'Russell Abernathy (the hero, played by Arnold Schwarzenegger): wants to get out of town for good; flaw: drinking;
      arc from drinking toward letting go'
    - 'Donna Jameson (the witness under protection, played by Lena Sterling): wants to protect the one person they
      love; flaw: fear of being ordinary; arc from fear of being ordinary toward forgiveness'
    - 'Kenneth Vaughn (the informant, played by David Warner): wants to keep a promise; flaw: pride; arc from pride
      toward a reckoning with honesty'
    - 'Charles Wyatt (the commanding officer, played by Daniel Brooks): wants to be left alone; flaw: a temper they
      can''t control; arc from a temper they can''t control toward a reckoning with courage'
    - 'Joel Okafor (the informant, played by Alec McCowen): wants to finally tell the truth; flaw: ambition; arc
      from ambition toward a reckoning with forgiveness'
    relationships:
    - 'Russell Abernathy and Donna Jameson: protector and witness'
    - 'Russell Abernathy and Kenneth Vaughn: antagonists'
    - 'Russell Abernathy and Charles Wyatt: a complicated alliance'
    - 'Russell Abernathy and Joel Okafor: a complicated alliance'
    beats:
    - 'Setup: Russell Abernathy''s ordinary life, already cracking (A mercenary with a conscience must escort a
      witness across the border while the clock runs down)'
    - 'Inciting incident: an event forces Russell Abernathy and Donna Jameson together'
    - 'Midpoint: a revelation turns Kenneth Vaughn from obstacle into real threat'
    - 'Low point: Russell Abernathy loses what they were fighting for, and Donna Jameson walks away'
    - 'Climax: Russell Abernathy confronts Kenneth Vaughn; what Russell Abernathy has become decides the ending'
    creative_intent: Michael D. Moore runs a tight, efficient set and expects lines cold on the day (simulation
      characterisation of this production, not a documented account of their real working methods; portray consistently
      with what is publicly known about them)
    your_key_scenes:
    - a phone call that changes everything
    - a chase through a crowded market
    your_read_of_the_script: you think it's genuinely good, especially the dialogue (your impression; it may be
      wrong)
  provenance: 'simulated production: not a real film; its cast and characters are part of this timeline'
- title: Warner's Motive
  kind: film bit
  status: under way
  dates: 1981-07-31 to 1981-08-14
  details: a small part in 'Warner's Motive' (New World Pictures); playing Leon Sinclair (a few scenes); directed
    by Charles Martin; with Bill Cosby, Monique Proulx, Joseph Maher, Reggie Kowalski
  pay: $11k
- title: An Enemy of the People
  kind: stage
  status: booked
  dates: 1981-08-21 to 1981-10-02
  details: Ibsen's 'An Enemy of the People' at a downtown Los Angeles repertory company; with Mitchell Warner, Peter
    Winslow, Michael Coleman
  pay: $12k
network:
- name: Margaret Hayes
  id: gen-ag-ag-sb-1
  who: agent at Starling-Barr Talent (fictional)
  how_you_know_them: monthly check-in call
  standing: cordial
  last_interaction: monthly check-in call (1981-08-07)
- name: Bill Cosby
  id: wd:Q213512
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Monique Proulx
  id: wd:Q16040924
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Joseph Maher
  id: wd:Q1406202
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Reggie Kowalski
  id: gen-a-00494
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Eve Plumb
  id: wd:Q453639
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Parker Stevenson
  id: wd:Q1319934
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Orson Welles
  id: wd:Q24829
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Hugh Burden
  id: wd:Q1634239
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Daphne Sterling
  id: gen-a-00057
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Louise Bennett-Coverley
  id: wd:Q965821
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Linda Gray
  id: wd:Q234086
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Kurtwood Smith
  id: wd:Q317228
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Anthony James
  id: wd:Q4772822
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
- name: Randy Wade
  id: gen-a-00697
  who: actor
  how_you_know_them: worked together on a small part in 'Warner's Motive' (New World Pictures)
  standing: cordial
  last_interaction: worked together on a small part in 'Warner's Motive' (New World Pictures) (1981-07-31)
open_threads:
- 'Upcoming: Ibsen''s ''An Enemy of the People'' at a downtown Los Angeles repertory company; with Mitchell Warner,
  Peter Winslow, Michael Coleman starting 1981-08-21'
- '''Signal of the Dawn'' is in awaiting release; release 1981-08-21'
- '''Wild Trouble'' is in post'
- '''The Red Run'' is in post'
- 'Career goal: you want serious, respected work that gets noticed at awards time. So far in 1981: 40 submissions,
  11 call-ins, 2 film role(s) booked.'
people:
- why_here: your agent
  id: gen-ag-ag-sb-1
  name: Margaret Hayes
  age: 29
  profession: agent at Starling-Barr Talent (fictional)
  public_profile: unknown to the public
  reputation: an unknown
  traits:
  - vain
  - relentlessly prepared
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: Agent at Starling-Barr Talent (fictional); a protective, old-school agent.
  persona:
    style: a protective, old-school agent
    hometown: Minneapolis
    signature: takes every call from the car on the 405
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history:
    - monthly check-in call (1981-05-01)
    - monthly check-in call (1981-06-05)
    - monthly check-in call (1981-07-03)
    - monthly check-in call (1981-08-07)
  narrative_canon:
  - '1980-01-04: Margaret takes calls standing at her office window on Wilshire and calls Daniel "kiddo" when she
    is about to give bad news.'
- why_here: directing your film 'Signal of the Dawn'
  id: wd:Q449220
  name: Bruce Beresford
  age: 40
  profession: director
  public_profile: unknown to the public
  reputation: director of drama and scifi with 2 films
  traits:
  - quick-tempered
  - guarded
  motivation: driven mostly by respect and awards, and also by challenging, meaningful work
  ambition: wants serious, respected work that gets noticed at awards time
  bio: Australian film director (born 1940); known for 'Side by Side' (1975).
  recent_work:
  - '''Side by Side'' (1975, director; documented)'
  - '''Signal of the Dawn'' (1980, director; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history:
    - a strong audition for 'Signal of the Dawn' (1980-05-23)
    - agreed to attach to your project 'The Long Field' (1981-01-16)
  narrative_canon:
  - '1980-07-25: Bruce Beresford shoots the hacker-lab scenes in long unbroken takes and asks Daniel to keep Leon''s
    hands busy with a soldering iron.'
  - '1981-01-16: Daniel gave Bruce Beresford The Long Field over coffee at Du-par''s on Ventura; Beresford read
    the first ten pages at the counter.'
- why_here: in the cast of your film 'Signal of the Dawn' (lead)
  id: gen-a-00632
  name: Hal Keating
  age: 41
  profession: actor
  public_profile: a recognisable face
  reputation: character actor in scifi and comedy
  traits:
  - private
  motivation: driven mostly by a steady, sane life, and also by fame and visibility
  ambition: wants steady work and a sustainable life
  bio: A recognisable name with a few memorable roles; most at home in horror; private.
  persona:
    hometown: San Francisco
    signature: plays guitar in the trailer between setups
    background: a stage actor from regional repertory theatre
    series: Silver Landing
  recent_work:
  - '''Rosie''s Street'' (1981, guest; this timeline)'
  - '''Sheridan''s Colony'' (1981, colead; this timeline)'
  - '''Hedda Gabler'' (1981, stage; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history:
    - clashed on the set of 'Signal of the Dawn' (a clash of two volatile temperaments) (1980-10-10)
- why_here: in the cast of your film 'Signal of the Dawn' (colead)
  id: gen-a-00623
  name: Natalie Rhodes
  age: 34
  profession: actor
  public_profile: well known
  reputation: character actor in romance and comedy
  traits: []
  motivation: driven mostly by financial security and big paydays, and also by challenging, meaningful work
  ambition: wants bigger paydays and financial security
  bio: A recognisable name with a few memorable roles; most at home in comedy.
  persona:
    hometown: a small town in Ohio
    signature: keeps a battered notebook of character ideas
    background: a former child actor
  recent_work:
  - '''Distant Bridges'' (1981, film_bit; this timeline)'
  - '''a national commercial for a camera'' (1981, commercial; this timeline)'
  - '''Fifth Street'' (1981, guest; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history: []
- why_here: in the cast of your film 'Signal of the Dawn' (supporting)
  id: wd:Q34851
  name: Elizabeth Taylor
  age: 49
  profession: actor
  public_profile: a recognisable face
  reputation: leading actor in scifi and romance
  traits:
  - even-keeled
  - guarded
  - demanding
  motivation: driven mostly by respect and awards, and also by fame and visibility
  ambition: wants serious, respected work that gets noticed at awards time
  bio: Actress (born 1932); known for 'A Little Night Music' (1977); Academy Award winner.
  recent_work:
  - '''Hart & Associates'' (1981, guest; this timeline)'
  - '''Lakeview County'' (1981, guest; this timeline)'
  - '''Brennan Files'' (1981, guest; this timeline)'
  relationship_status: married (spouse outside the film industry) (documented)
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history:
    - clashed on the set of 'Signal of the Dawn' (a disagreement that got heated) (1980-09-19)
- why_here: directing your film 'Wild Trouble'
  id: wd:Q6833019
  name: Michael Nankin
  age: 25
  profession: director
  public_profile: unknown to the public
  reputation: director of comedy and romance with 3 films
  traits:
  - private
  motivation: driven mostly by respect and awards, and also by financial security and big paydays
  ambition: wants serious, respected work that gets noticed at awards time
  bio: American film director (born 1955); known for 'Junior High School' (1978).
  recent_work:
  - '''Junior High School'' (1978, director; documented)'
  - '''Midnight Madness'' (1980, director; this timeline)'
  - '''Wild Trouble'' (1981, director; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history:
    - a strong audition for 'Wild Trouble' (1980-10-31)
- why_here: in the cast of your film 'Wild Trouble' (lead)
  id: gen-a-00139
  name: Maxine Keating
  age: 31
  profession: actor
  public_profile: famous
  reputation: leading actor in comedy and action
  traits:
  - hungry
  - private
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: A bona fide star; most at home in action; hungry, private.
  persona:
    hometown: Kansas City
    signature: reads tarot for the cast
    background: a former child actor
  recent_work:
  - '''Harper''s Getaway'' (1981, lead; this timeline)'
  - '''Red Force'' (1981, colead; this timeline)'
  - '''The Silent Exposure'' (1981, film_bit; this timeline)'
  relationship_status: single
  with_you:
    standing: strained
    status: acquainted
    history:
    - clashed on the set of 'Wild Trouble' (pressure from a slipping schedule boiled over) (1981-01-02)
    - clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments) (1981-01-16)
  lately:
  - '1981-06-05: Maxine Keating was cast as Marisol (colead) in ''Red Force'' (Paramount Pictures).'
  - '1981-06-12: Reviews for ''Hot Wedding'': mixed-to-positive (critics'' aggregate 68/100); opening-night audiences
    gave it a B.'
  - '1981-06-19: ''Moonlit Dance'' finished its theatrical run with $6.2M domestic and an estimated $5.5M overseas.'
- why_here: in the cast of your film 'Wild Trouble' (colead)
  id: gen-a-00049
  name: Glenn Anderson
  age: 29
  profession: actor
  public_profile: a household name
  reputation: leading actor in comedy and romance
  traits:
  - volatile
  - hungry
  motivation: driven mostly by financial security and big paydays, and also by challenging, meaningful work
  ambition: wants bigger paydays and financial security
  bio: A bona fide star; most at home in romance; volatile, hungry.
  persona:
    hometown: Toronto
    signature: chain-smokes between takes
    background: a former model
  recent_work:
  - '''Twelfth Night'' (1980, stage; this timeline)'
  - '''a national commercial for a breakfast cereal'' (1980, commercial; this timeline)'
  - '''Wild Trouble'' (1981, colead; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history:
    - clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments) (1980-12-26)
- why_here: in the cast of your film 'Wild Trouble' (supporting)
  id: gen-a-00619
  name: Ingrid Emerson
  age: 63
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in comedy and action
  traits:
  - self-effacing
  - cautious with choices
  motivation: driven mostly by challenging, meaningful work, and also by respect and awards
  ambition: wants challenging material over safe paychecks
  bio: A working actor with a steady run of supporting parts; most at home in drama; self-effacing, cautious with
    choices.
  persona:
    hometown: the San Fernando Valley
    signature: carries a thermos of terrible coffee everywhere
    background: came up through Chicago improv
    series: Dugan's Garage
  recent_work:
  - '''Paradise Estate'' (1980, guest; this timeline)'
  - '''Hart & Associates'' (1980, guest; this timeline)'
  - '''The Midnight Pursuit'' (1981, supporting; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history: []
- why_here: directing your film 'The Red Run'
  id: wd:Q6829651
  name: Michael D. Moore
  age: 66
  profession: director
  public_profile: unknown to the public
  reputation: director of action with 2 films
  traits:
  - guarded
  - low-key
  - private
  motivation: driven mostly by a steady, sane life, and also by challenging, meaningful work
  ambition: wants steady work and a sustainable life
  bio: Film director (born 1914); known for 'Mister Deathman' (1977).
  recent_work:
  - '''Mister Deathman'' (1977, director; documented)'
  - '''The Red Run'' (1981, director; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history:
    - a strong audition for 'The Red Run' (1981-01-30)
- why_here: in the cast of your film 'The Red Run' (lead)
  id: wd:Q2685
  name: Arnold Schwarzenegger
  age: 34
  profession: actor
  public_profile: a recognisable face
  reputation: working actor in action and romance
  traits:
  - cautious with choices
  - charming
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: Austrian actor (born 1947); known for 'The Villain' (1979); award-nominated.
  recent_work:
  - '''Lakeview Mercy'' (1981, guest; this timeline)'
  - '''Desert Force'' (1981, guest; this timeline)'
  - '''Desert Rescue'' (1981, guest; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history:
    - clashed on the set of 'The Red Run' (exhaustion after long days) (1981-05-29)
- why_here: in the cast of your film 'The Red Run' (colead)
  id: gen-a-y1980-0002
  name: Lena Sterling
  age: 21
  profession: actor
  public_profile: unknown to the public
  reputation: working actor in thriller and action
  traits:
  - cautious with choices
  motivation: driven mostly by financial security and big paydays, and also by a steady, sane life
  ambition: wants bigger paydays and financial security
  bio: A newcomer still looking for a first real break; most at home in family; cautious with choices.
  persona:
    hometown: Baltimore
    signature: plays guitar in the trailer between setups
    background: studied theatre at a state university
  recent_work:
  - '''Fort Apache, The Bronx'' (1981, featured; this timeline)'
  - '''The Red Run'' (1981, colead; this timeline)'
  - '''Skyhook'' (1981, featured; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history:
    - clashed on the set of 'The Red Run' (a clash of two volatile temperaments) (1981-05-15)
  lately:
  - '1981-07-03: Reviews for ''Fort Apache, The Bronx'': savage (critics'' aggregate 30/100); opening-night audiences
    gave it a B-.'
  - '1981-08-07: Reviews for ''Room of the Brave'': mixed (critics'' aggregate 53/100); opening-night audiences
    gave it an A-.'
- why_here: in the cast of your film 'The Red Run' (supporting)
  id: wd:Q363271
  name: David Warner
  age: 40
  profession: actor
  public_profile: well known
  reputation: character actor in horror and romance
  traits:
  - warm
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: British actor (born 1941); known for 'Nightwing' (1979).
  recent_work:
  - '''Eagle Ranch'' (1981, guest; this timeline)'
  - '''Westside Beat'' (1981, guest; this timeline)'
  - '''Paramour'' (1981, featured; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history:
    - clashed on the set of 'The Red Run' (exhaustion after long days) (1981-05-22)
  lately:
  - '1981-06-19: David Warner was cast as Jeffrey (featured) in ''Paramour'' (Universal Pictures).'
  - '1981-07-03: Reviews for ''The French Lieutenant''s Woman'': mixed (critics'' aggregate 51/100); opening-night
    audiences gave it a D.'
- why_here: in the cast of your film 'The Red Run' (supporting)
  id: wd:Q492176
  name: Alec McCowen
  age: 56
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in action and drama
  traits:
  - quick-tempered
  - drawn to risky material
  motivation: driven mostly by fame and visibility, and also by financial security and big paydays
  ambition: wants a breakout role and a recognisable name
  bio: British actor (born 1925); known for 'Hanover Street' (1979).
  recent_work:
  - '''a national commercial for a family sedan'' (1980, commercial; this timeline)'
  - '''Heartbeeps'' (1981, featured; this timeline)'
  - '''The Red Run'' (1981, supporting; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history:
    - clashed on the set of 'The Red Run' (exhaustion after long days) (1981-06-12)
  lately:
  - '1981-07-03: Reviews for ''Heartbeeps'': strong (critics'' aggregate 75/100); opening-night audiences gave it
    a B.'
industry:
  box_office_chart:
  - 1. 'Thorne's Promise' (Warner Bros.) — $4.7M this week, $15.6M total, week 3
  - 2. 'Escape from New York' (AVCO Embassy Pictures) — $4.2M this week, $20.4M total, week 5
  - 3. 'Letters of the Wolves' (Orion Pictures) — $3.6M this week, $6.9M total, week 2
  - 4. 'Raiders of the Lost Ark' (Paramount Pictures) — $3.4M this week, $53.5M total, week 9
  - 5. 'Taps' (20th Century Fox) — $2.9M this week, $19.4M total, week 6
  news:
  - date: '1981-07-17'
    text: Austin Pendleton and Susan Lanier have started seeing each other.
    provenance: 'simulated (not historical): an alternate-timeline development'
  - date: '1981-08-07'
    text: Peter Cushing was cast as Michael (featured) in 'Frontier of the Damned' (Orion Pictures).
    provenance: simulated casting in a fictional production
  - date: '1981-08-07'
    text: John Belushi was cast as Donald Blake (lead) in 'Dead Force' (Columbia Pictures).
    provenance: simulated casting in a fictional production
  - date: '1981-08-07'
    text: Susan Blakely was cast as Joyce Rossi (lead) in 'Silent Room' (United Artists).
    provenance: simulated casting in a fictional production
  - date: '1981-08-07'
    text: 'Reviews for ''Condorman'': mixed (critics'' aggregate 54/100); opening-night audiences gave it a B.'
    provenance: simulated event in this timeline
  - date: '1981-08-07'
    text: 'Reviews for ''Student Bodies'': savage (critics'' aggregate 26/100); opening-night audiences gave it
      an F.'
    provenance: simulated event in this timeline
  - date: '1981-08-07'
    text: 'Reviews for ''Room of the Brave'': mixed (critics'' aggregate 53/100); opening-night audiences gave it
      an A-.'
    provenance: simulated event in this timeline
  - date: '1981-08-07'
    text: 'Trades: ''Room of the Brave'' beat industry expectations on its opening.'
  - date: '1981-08-07'
    text: '''Gloria'' finished its theatrical run with $46.9M domestic and an estimated $38.1M overseas.'
    provenance: simulated event in this timeline
  - date: '1981-08-07'
    text: 'Trades: ''Student Bodies'' beat industry expectations on its opening.'
  - date: '1981-08-07'
    text: '''Final Exam'' finished its theatrical run with $237k domestic and an estimated $196k overseas.'
    provenance: simulated event in this timeline
  - date: '1981-08-07'
    text: '''Thief'' finished its theatrical run with $12.9M domestic and an estimated $13.8M overseas.'
    provenance: simulated event in this timeline
  - date: '1981-08-07'
    text: Richard Pryor married Jennifer Lee Pryor.
    provenance: documented history
  - date: '1981-08-07'
    text: Melvyn Douglas died.
    provenance: documented history
pending_decisions: []
continuity:
  career_so_far:
  - '1977: ''Great Dog'' (colead)'
  - '1977: ''Quantum Station'' (supporting)'
  - '1980: ''Sky Squadron'' (guest)'
  - '1980: ''Sky Squadron'' (guest)'
  - '1980: ''Fifth Street'' (guest)'
  - '1980: ''Desert Rescue'' (guest)'
  - '1980: ''Signal of the Dawn'' (supporting)'
  - '1980: ''Mountain Run'' (guest)'
  - '1981: ''Wild Trouble'' (supporting)'
  - '1981: ''The Red Run'' (supporting)'
  - '1981: ''Deadly Inheritance'' (tv_movie)'
  - '1981: ''Sky Squadron'' (guest)'
  initiatives_resolved:
  - '1980-07-25 meet: Meeting requested with Sydney Pollack. -> Met Sydney Pollack.'
  earlier_key_moments:
  - '1981-02-20: ''Wild Trouble'' wrapped principal photography and moved into post-production.'
  - '1981-04-24: Principal photography began on ''The Red Run'' in Toronto (12 weeks scheduled).'
  - '1981-05-15: Tension on the set of ''The Red Run'': you clashed with Lena Sterling (a clash of two volatile
    temperaments).'
  - '1981-05-15: There is an unmistakable spark between you and Lena Sterling on the set of ''The Red Run''.'
  - '1981-05-15: Chemistry with Lena Sterling: pursue something, or keep it professional?'
  - '1981-05-22: Tension on the set of ''The Red Run'': you clashed with David Warner (exhaustion after long days).'
  - '1981-05-29: Tension on the set of ''The Red Run'': you clashed with Arnold Schwarzenegger (exhaustion after
    long days).'
  - '1981-06-05: You auditioned for James in ''Red Force'' and made the final two.'
  - '1981-06-12: Audition: Anthony Rhodes, the lead role in ''Cold Exposure'' (thriller, Orion Pictures; director
    Ivan Passer; casting Lori Wade) on 1981-06-19. Premise: A junior senator''s aide realises a client is not who
    he says as the killer closes in.'
  - '1981-06-12: Tension on the set of ''The Red Run'': you clashed with Alec McCowen (exhaustion after long days).'
  - '1981-06-19: You auditioned for Anthony Rhodes in ''Cold Exposure'' and made the final two.'
  - '1981-07-03: You auditioned for Brian in ''Last Witness'' and did not get a callback.'
  recent_scenes_and_threads:
  - '1981-07-31: with Eve Plumb: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-07-31: with Hugh Burden: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-07-31: with Joseph Maher: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-07-31: with Kurtwood Smith: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-07-31: with Linda Gray: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-07-31: with Louise Bennett-Coverley: worked together on a small part in ''Warner''s Motive'' (New World
    Pictures)'
  - '1981-07-31: with Monique Proulx: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-07-31: with Orson Welles: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-07-31: with Parker Stevenson: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-07-31: with Randy Wade: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-07-31: with Reggie Kowalski: worked together on a small part in ''Warner''s Motive'' (New World Pictures)'
  - '1981-08-07: with Margaret Hayes: monthly check-in call'
narrative_canon:
- '1980-01-04: Margaret takes calls standing at her office window on Wilshire and calls Daniel "kiddo" when she
  is about to give bad news.'
- '1980-01-04: Daniel rents a bungalow in Los Feliz with a lemon tree he never waters.'
- '1980-07-25: Bruce Beresford shoots the hacker-lab scenes in long unbroken takes and asks Daniel to keep Leon''s
  hands busy with a soldering iron.'
- '1980-08-22: Daniel writes the first pages of The Long Field longhand in a Big Chief tablet at the craft-services
  table between setups.'
- '1981-01-16: Daniel gave Bruce Beresford The Long Field over coffee at Du-par''s on Ventura; Beresford read the
  first ten pages at the counter.'
era:
  year: 1981
  average_ticket_price: $2.78
  note: The blockbuster era is a few years old; theatrical release dominates and home video is small but growing
    fast.
narrator_notes: []
```

## REPLY FORMAT
End your reply with exactly one block like this:

```engine
reply_to: pkt-00025
decisions:            # one entry per decision the player made (omit if none)
  - {id: dec-00000, choice: accept}            # counter needs: {id: ..., choice: counter, fee: 60000}
initiatives:          # consequential moves for the engine to adjudicate; target/via take a name or an id
  - {kind: pursue_project, target: "<film title or id>", role: "<character, optional>", approach: "..."}
  - {kind: inquire, target: "<film or person>"}
  - {kind: meet, target: "<person>", approach: "why you want the meeting"}
  - {kind: introduction, target: "<person>", via: "<someone you know who knows them>"}
  - {kind: social, target: "<person you know>", approach: "dinner at their place"}
  - {kind: publicity, mode: publicist|interview|talk_show|charity}
  - {kind: reposition, details: {genres: [drama], avoid_genres: [horror], min_role: supporting, no_tv: false, no_commercials: true}}
  - {kind: develop_project, title: "...", genre: drama, logline: "one sentence"}
proposals:            # interpersonal developments (optional)
  - {id: p1, type: relationship_shift, with: <person id>, direction: positive|negative, severity: minor|moderate|major, cause: "..."}
  - {id: p2, type: romantic_overture, to: <person id>, approach: "..."}
  - {id: p3, type: player_intent, kind: take_class|rest|seek_agent, text: "..."}
  - {id: p4, type: purchase, item: car|apartment|house|gift|vacation|wardrobe, text: "..."}
  - {id: p5, type: reputation_moment, person: <id>, direction: positive|negative, severity: minor|moderate, public: true|false, cause: "..."}
narrative:            # narrative canon: nonconsequential details to keep (optional `about` names or ids)
  - {text: "Rehearsed the diner scene with Ray at his apartment; he hums Sinatra between takes.", about: ["<name>"]}
advance: {weeks: 4}   # or {until: YYYY-MM-DD}; omit to stay at this date
```
