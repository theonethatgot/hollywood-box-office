# Narrator packet pkt-00041 — 1982-08-13

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
packet: pkt-00041
date: '1982-08-13'
covers: 1982-07-16 .. 1982-08-13
state_hash: b7ce8d4552eebfee
protagonist:
  id: player
  name: Daniel Brooks
  age: 32
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
    cash: 221686.0
    monthly_costs: 6000.0
  energy: exhausted
  relationship_status: single
  awards: []
canon:
- id: ev-9703
  date: '1982-07-16'
  text: 'Your agent got you in the room: Hal Sullivan in ''Final Agenda'' (casting: Lori Winslow) — the casting
    director asked for you by name.'
- id: ev-9704
  date: '1982-07-16'
  text: 'Audition booked: Hal Sullivan in ''Final Agenda'' on 1982-07-23.'
- id: ev-9705
  date: '1982-07-16'
  text: Your agent got you a read for a rookie officer on 'Hart Investigations' (PBS), casting Greta Keating.
- id: ev-9706
  date: '1982-07-16'
  text: 'You read for a rookie officer on ''Hart Investigations'' (PBS) (an episode about a nightclub singer in
    danger) and were not picked; casting: Greta Keating.'
- id: ev-9707
  date: '1982-07-16'
  text: 'Feedback on ''Hart Investigations'' (PBS) (via your agent): they liked the read but wanted someone with
    more screen presence.'
- id: ev-9708
  date: '1982-07-16'
  text: Your agent got you a read for a society reporter on 'Desert Rescue West' (NBC), casting Margaret Merrick.
- id: ev-9709
  date: '1982-07-16'
  text: 'You read for a society reporter on ''Desert Rescue West'' (NBC) (an episode about a mountain avalanche)
    and were not picked; casting: Margaret Merrick.'
- id: ev-9710
  date: '1982-07-16'
  text: 'Feedback on ''Desert Rescue West'' (NBC) (via your agent): they liked the read but wanted someone with
    more screen presence.'
- id: ev-9711
  date: '1982-07-16'
  text: Your agent got you a read for an old friend of the lead on 'Highway Force West' (ABC), casting Randy Moreno.
- id: ev-9712
  date: '1982-07-16'
  text: 'You read for an old friend of the lead on ''Highway Force West'' (ABC) (an episode about a stranded school
    bus) and were not picked; casting: Randy Moreno.'
- id: ev-9713
  date: '1982-07-16'
  text: 'Feedback on ''Highway Force West'' (ABC) (via your agent): they liked the read but wanted someone with
    more screen presence.'
- id: ev-9736
  date: '1982-07-23'
  text: 'Feedback from the room on ''Final Agenda'' (via your agent): your read was solid, but they felt the actor
    they chose commanded the room more.'
- id: ev-9737
  date: '1982-07-23'
  text: You auditioned for Hal Sullivan in 'Final Agenda' and made the final two.
- id: ev-9738
  date: '1982-07-23'
  text: 'Others seen for Hal Sullivan: Robert Englund, Peter Criss, Jim Kelly.'
  provenance: simulated event in this timeline
- id: ev-9771
  date: '1982-07-23'
  text: Your agent got you a read for a union boss on 'Hart & Associates' (first-run syndication), casting Margaret
    Merrick.
- id: ev-9772
  date: '1982-07-23'
  text: 'You read for a union boss on ''Hart & Associates'' (first-run syndication) (an episode about a nightclub
    singer in danger) and booked it; casting: Margaret Merrick.'
- id: ev-9773
  date: '1982-07-23'
  text: Booked a guest role on 'Hart & Associates' (first-run syndication); playing Steven, a union boss; an episode
    about a nightclub singer in danger; directed by Joyce Malone; with Raymond Emerson, Connie Lindgren (1982-08-06
    to 1982-08-13, $8k).
- id: ev-9774
  date: '1982-07-23'
  text: 'Payment received: a guest role on ''Santos Files'' (CBS) — $9k gross, $5k after commission and tax.'
- id: ev-9775
  date: '1982-07-23'
  text: Wrapped a guest role on 'Santos Files' (CBS).
- id: ev-9842
  date: '1982-07-30'
  text: 'Your agent got you in the room: Calvin Marchetti in ''House of the Brave'' (casting: Sharon Kowalski) —
    the casting director asked for you by name.'
- id: ev-9843
  date: '1982-07-30'
  text: 'Audition booked: Calvin Marchetti in ''House of the Brave'' on 1982-08-06.'
- id: ev-9844
  date: '1982-07-30'
  text: 'Your agent got you in the room: Wayne in ''Outer Voyager'' (casting: Joan Barrett) — the casting director
    asked for you by name.'
- id: ev-9845
  date: '1982-07-30'
  text: 'Audition booked: Wayne in ''Outer Voyager'' on 1982-08-06.'
- id: ev-9861
  date: '1982-07-30'
  text: '''Wild Trouble'' finished its theatrical run with $15.8M domestic and an estimated $16.5M overseas.'
  provenance: simulated event in this timeline
- id: ev-9873
  date: '1982-08-06'
  text: You auditioned for Calvin Marchetti in 'House of the Brave' and won the part.
- id: ev-9874
  date: '1982-08-06'
  text: 'Others seen for Calvin Marchetti: Richard Masur, Rob Reiner, Ron Howard.'
  provenance: simulated event in this timeline
- id: ev-9875
  date: '1982-08-06'
  text: 'Offer (after auditions): Calvin Marchetti, supporting in ''House of the Brave'' — A group of camp counsellors
    is trapped in a snowed-in lodge far from any help. Columbia Pictures, dir. Oliver Stone. Terms $95k. Shoots
    1982-09-17 to 1982-10-22 (Chicago).'
- id: ev-9887
  date: '1982-08-06'
  text: You auditioned for Wayne in 'Outer Voyager' and won the part.
- id: ev-9888
  date: '1982-08-06'
  text: 'Others seen for Wayne: Alan Malone, John Heard, Gil Gerard.'
  provenance: simulated event in this timeline
- id: ev-9889
  date: '1982-08-06'
  text: 'Offer (after auditions): Wayne, supporting in ''Outer Voyager'' — A teenage hacker wakes up decades after
    the launch as the station fails. Paramount Pictures, dir. Arthur Rankin Jr.. Terms $95k. Shoots 1982-10-29 to
    1983-02-18 (Vancouver).'
- id: ev-9911
  date: '1982-08-06'
  text: 'Your agent got you in the room: Dennis in ''Night Signal'' (casting: Lisa Jameson) — the casting director
    asked for you by name.'
- id: ev-9912
  date: '1982-08-06'
  text: 'Audition booked: Dennis in ''Night Signal'' on 1982-08-13.'
- id: ev-9913
  date: '1982-08-06'
  text: Your agent got you a read for a young doctor on 'Santos Investigations' (PBS), casting Greta Keating.
- id: ev-9914
  date: '1982-08-06'
  text: 'You read for a young doctor on ''Santos Investigations'' (PBS) (an episode about a blackmailed movie producer)
    and booked it; casting: Greta Keating.'
- id: ev-9915
  date: '1982-08-06'
  text: Booked a guest role on 'Santos Investigations' (PBS); playing Carlos Merrick, a young doctor; an episode
    about a blackmailed movie producer; directed by Neil Granger; with Glenn Ramsey, Barbara Clayton, Terry Delaney
    (1982-08-20 to 1982-08-27, $7k).
- id: ev-9935
  date: '1982-08-06'
  text: 'Margaret Hayes checked in; they submitted you for 29 roles this past month; 11 got you in the room; the
    most common feedback on passes: ''they went with other actors''; 3 smaller bookings came through; they''re steering
    you toward thriller parts, where you''ve been landing near the top of the room; they want to get you seen in
    a respected stage production.'
period_summary:
  overview: 4 week(s), working on 2 job(s), 19 submission(s) by your agent, 9 call-in(s), 8 audition(s), 2 booking(s);
    net money -$643.
  working:
  - 'tv guest: Hart & Associates (1982-08-06 to 1982-08-13)'
  - 'tv guest: Santos Files (1982-07-16 to 1982-07-23)'
  quiet_period: false
  note: ''
rulings: []
delegated:
- Your agent booked you an audition for Hal Sullivan in 'Final Agenda' on 1982-07-23.
- 'Margaret Hayes booked you: a guest role on ''Hart & Associates'' (first-run syndication); playing Steven, a union
  boss; an episode about a nightclub singer in danger; directed by Joyce Malone; with Raymond Emerson, Connie Lindgren
  — 1982-08-06 to 1982-08-13, paying $8k.'
- Your agent booked you an audition for Calvin Marchetti in 'House of the Brave' on 1982-08-06.
- Your agent booked you an audition for Wayne in 'Outer Voyager' on 1982-08-06.
- Your agent booked you an audition for Dennis in 'Night Signal' on 1982-08-13.
- 'Margaret Hayes booked you: a guest role on ''Santos Investigations'' (PBS); playing Carlos Merrick, a young doctor;
  an episode about a blackmailed movie producer; directed by Neil Granger; with Glenn Ramsey, Barbara Clayton, Terry
  Delaney — 1982-08-20 to 1982-08-27, paying $7k.'
standing_changes:
  now:
    public_profile: a recognisable face
    momentum: steady
    draw: a modest draw
    critics: respected
    industry_standing: a working professional
    quote: $94k
  changes: []
  relevant_events:
  - '1982-07-23: Wrapped a guest role on ''Santos Files'' (CBS).'
  - '1982-07-30: ''Wild Trouble'' finished its theatrical run with $15.8M domestic and an estimated $16.5M overseas.'
  - '1982-08-06: You auditioned for Calvin Marchetti in ''House of the Brave'' and won the part.'
  - '1982-08-06: You auditioned for Wayne in ''Outer Voyager'' and won the part.'
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
initiatives: []
career_activity:
  submissions:
  - '1982-07-23: a union boss (guest) in ''Brennan Files'' (ABC, casting Susan Kowalski) — passed: they had plenty
    of strong submissions'
  - '1982-07-23: the new neighbour (guest) in ''Highway Force West'' (ABC, casting Randy Moreno) — passed: they
    had plenty of strong submissions'
  - '1982-07-23: a rookie officer (guest) in ''Dakota Case Story'' (first-run syndication, casting Lena Brooks)
    — passed: they had plenty of strong submissions'
  - '1982-07-23: a union boss (guest) in ''Hart & Associates'' (first-run syndication, casting Margaret Merrick)
    — called in: the show''s casting director wanted to see you'
  - '1982-07-30: Calvin Marchetti (supporting) in ''House of the Brave'' (Columbia Pictures, casting Sharon Kowalski)
    — requested: the casting director asked for you by name'
  - '1982-07-30: Keith Fielding (lead) in ''Outer Voyager'' (Paramount Pictures, casting Joan Barrett) — passed:
    they want a bigger name for this part'
  - '1982-07-30: Wayne (supporting) in ''Outer Voyager'' (Paramount Pictures, casting Joan Barrett) — requested:
    the casting director asked for you by name'
  - '1982-08-06: Dennis (supporting) in ''Night Signal'' (Metro-Goldwyn-Mayer, casting Lisa Jameson) — requested:
    the casting director asked for you by name'
  - '1982-08-06: Craig (featured) in ''Night Signal'' (Metro-Goldwyn-Mayer, casting Lisa Jameson) — passed: they
    went with other actors'
  - '1982-08-06: a young doctor (guest) in ''Santos Investigations'' (PBS, casting Greta Keating) — called in: the
    show''s casting director wanted to see you'
  auditions:
  - '1982-07-30: Your agent got you in the room: Wayne in ''Outer Voyager'' (casting: Joan Barrett) — the casting
    director asked for you by name.'
  - '1982-08-06: You auditioned for Calvin Marchetti in ''House of the Brave'' and won the part.'
  - '1982-08-06: Others seen for Calvin Marchetti: Richard Masur, Rob Reiner, Ron Howard.'
  - '1982-08-06: You auditioned for Wayne in ''Outer Voyager'' and won the part.'
  - '1982-08-06: Others seen for Wayne: Alan Malone, John Heard, Gil Gerard.'
  - '1982-08-06: Your agent got you in the room: Dennis in ''Night Signal'' (casting: Lisa Jameson) — the casting
    director asked for you by name.'
  - '1982-08-06: Your agent got you a read for a young doctor on ''Santos Investigations'' (PBS), casting Greta
    Keating.'
  - '1982-08-06: You read for a young doctor on ''Santos Investigations'' (PBS) (an episode about a blackmailed
    movie producer) and booked it; casting: Greta Keating.'
  bookings:
  - '1982-08-06 to 1982-08-13: a guest role on ''Hart & Associates'' (first-run syndication); playing Steven, a
    union boss; an episode about a nightclub singer in danger; directed by Joyce Malone; with Raymond Emerson, Connie
    Lindgren ($8k)'
  - '1982-08-20 to 1982-08-27: a guest role on ''Santos Investigations'' (PBS); playing Carlos Merrick, a young
    doctor; an episode about a blackmailed movie producer; directed by Neil Granger; with Glenn Ramsey, Barbara
    Clayton, Terry Delaney ($7k)'
  agent_calls:
  - '1982-08-06: Margaret Hayes checked in; they submitted you for 29 roles this past month; 11 got you in the room;
    the most common feedback on passes: ''they went with other actors''; 3 smaller bookings came through; they''re
    steering you toward thriller parts, where you''ve been landing near the top of the room; they want to get you
    seen in a respected stage production.'
your_work:
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
  stage: released
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
  release_date: '1982-01-01'
  box_office:
    opening: $1.8M
    domestic_to_date: $15.8M
    weeks: 31
    critics: 42/100
    audience_grade: a B-
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
  stage: released
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
  release_date: '1982-01-29'
  box_office:
    opening: $486k
    domestic_to_date: $8.1M
    weeks: 28
    critics: 45/100
    audience_grade: an A+
- title: The Long Field
  studio: Orion Pictures
  genre: drama
  premise: A minor-league catcher comes home to Ohio to care for his father and has to decide whether one more season
    is worth the farm.
  your_role: 'Stuart — lead: the protagonist; carries the film'
  director: Bruce Beresford
  costars:
  - Jacqueline Bisset as Gail (colead, character name simulated)
  - Stephen Macht as Gordon Kendall (supporting, character name simulated)
  - Carol Kane as Julie Irving (supporting, character name simulated)
  - Lisa Lu as Nora Warner (featured, character name simulated)
  - Gil Kendall as Curtis (featured, character name simulated)
  - Jeanette Marchetti as Lisa Delaney (featured, character name simulated)
  - Rhodes Reason as Terry (featured, character name simulated)
  - Ronee Blakley as Elizabeth (featured, character name simulated)
  - Bill Murray as Nathan (featured, character name simulated)
  - Richard Jaeckel as Neil Nolan (featured, character name simulated)
  - Betsy Palmer as Leslie Hudson (featured, character name simulated)
  - Patricia Quinn as Lisa Kessler (featured, character name simulated)
  - William Keating as Brian (featured, character name simulated)
  - David Hasselhoff as Calvin Radford (featured, character name simulated)
  - Wayne Gallagher as Hal Foster (featured, character name simulated)
  stage: post
  location: Mexico
  terms: $94k + 2 net points
  identity: drive-in drama; an original project developed by its star
  story:
    provenance: simulated screenplay for a fictional production
    logline: 'A drive-in drama: A minor-league catcher comes home to Ohio to care for his father and has to decide
      whether one more season is worth the farm.'
    central_conflict: Stuart must face what tore the family apart, and Gail is the one person who remembers it differently
    characters:
    - 'Stuart (the protagonist, played by Daniel Brooks): wants to get out of town for good; flaw: blind loyalty;
      arc from blind loyalty toward forgiveness'
    - 'Gail (the spouse, played by Jacqueline Bisset): wants to belong somewhere; flaw: a temper they can''t control;
      arc from a temper they can''t control toward forgiveness'
    - 'Gordon Kendall (the neighbour, played by Stephen Macht): wants to protect the one person they love; flaw:
      a habit of running from trouble; arc from a habit of running from trouble toward a reckoning with forgiveness'
    - 'Julie Irving (the lawyer, played by Carol Kane): wants to keep a promise; flaw: trusting the wrong people;
      arc from trusting the wrong people toward a reckoning with letting go'
    relationships:
    - 'Stuart and Gail: a marriage under strain'
    - 'Stuart and Gordon Kendall: antagonists'
    - 'Stuart and Julie Irving: a complicated alliance'
    beats:
    - 'Setup: Stuart''s ordinary life, already cracking (A minor-league catcher comes home to Ohio to care for his
      father and has to decide whether one more season is worth the farm)'
    - 'Inciting incident: an event forces Stuart and Gail together'
    - 'Midpoint: a revelation turns Gordon Kendall from obstacle into real threat'
    - 'Low point: Stuart loses what they were fighting for, and Gail walks away'
    - 'Climax: Stuart confronts Gordon Kendall; what Stuart has become decides the ending'
    creative_intent: Bruce Beresford wants long, unbroken takes and room for actors to find moments (simulation
      characterisation of this production, not a documented account of their real working methods; portray consistently
      with what is publicly known about them)
    your_key_scenes:
    - a crowded party where everything comes out
    - a long single take at a hospital bedside
    your_read_of_the_script: you think it's genuinely good, especially the humour (your impression; it may be wrong)
  provenance: 'simulated production: not a real film; its cast and characters are part of this timeline'
- title: Runaway Adventure
  studio: Universal Pictures
  genre: family
  premise: A stubborn grandfather sets out to find a lost treasure over one magical summer.
  your_role: 'Charles Reeves — colead: the second lead; a major arc opposite the protagonist'
  director: Daniel Petrie
  costars:
  - Mary Reardon as Marisol Shaw (lead, character name simulated)
  - Anita Corbin as Connie Hastings (supporting, character name simulated)
  - Leslie Crane as Jill Pierce (supporting, character name simulated)
  - Richard Masur as Terry Gallagher (supporting, character name simulated)
  - Eve Arden as Jill (featured, character name simulated)
  - Nipsey Russell as Scott Garrison (featured, character name simulated)
  - Max Wright as Paul Delaney (featured, character name simulated)
  - David Bradley as Elliot Irving (featured, character name simulated)
  - Sandra Bernhard as Rosalind Palmer (featured, character name simulated)
  - Eileen Heckart as Gloria Boyd (featured, character name simulated)
  - Bert Freed as Gil (featured, character name simulated)
  - David Proval as Timothy (featured, character name simulated)
  - Ray Danton as Frank (featured, character name simulated)
  - Ivy Bishop as Nancy (featured, character name simulated)
  stage: post
  location: New York
  terms: $94k
  identity: sentimental family; a modestly budgeted picture that needs to find its audience
  story:
    provenance: simulated screenplay for a fictional production
    logline: 'A sentimental family: A stubborn grandfather sets out to find a lost treasure over one magical summer.'
    central_conflict: Marisol Shaw sets out on an adventure no adult will approve of, with Charles Reeves as the
      most unlikely companion
    characters:
    - 'Marisol Shaw (the young hero, played by Mary Reardon): wants to finally tell the truth; flaw: a habit of
      running from trouble; arc from a habit of running from trouble toward honesty'
    - 'Charles Reeves (the unlikely friend, played by Daniel Brooks): wants to be left alone; flaw: pride; arc from
      pride toward self-respect'
    - 'Connie Hastings (the grumpy guardian, played by Anita Corbin): wants to get out of town for good; flaw: trusting
      the wrong people; arc from trusting the wrong people toward a reckoning with forgiveness'
    - 'Jill Pierce (the villain, played by Leslie Crane): wants to keep a promise; flaw: fear of being ordinary;
      arc from fear of being ordinary toward a reckoning with honesty'
    - 'Terry Gallagher (the wise elder, played by Richard Masur): wants to prove they still matter; flaw: drinking;
      arc from drinking toward a reckoning with letting go'
    relationships:
    - 'Marisol Shaw and Charles Reeves: an unlikely friendship'
    - 'Marisol Shaw and Connie Hastings: a complicated alliance'
    - 'Marisol Shaw and Jill Pierce: antagonists'
    - 'Marisol Shaw and Terry Gallagher: mentor and protégé'
    beats:
    - 'Setup: Marisol Shaw''s ordinary life, already cracking (A stubborn grandfather sets out to find a lost treasure
      over one magical summer)'
    - 'Inciting incident: an event forces Marisol Shaw and Charles Reeves together'
    - 'Midpoint: a revelation turns Jill Pierce from obstacle into real threat'
    - 'Low point: Marisol Shaw loses what they were fighting for, and Charles Reeves walks away'
    - 'Climax: Marisol Shaw confronts Jill Pierce; what Marisol Shaw has become decides the ending'
    creative_intent: Daniel Petrie is focused on pace and big moments that will play in a trailer (simulation characterisation
      of this production, not a documented account of their real working methods; portray consistently with what
      is publicly known about them)
    your_key_scenes:
    - a phone call that changes everything
    - a late-night confrontation in a kitchen
    your_read_of_the_script: you think it's solid; the dialogue works, though parts feel familiar (your impression;
      it may be wrong)
  provenance: 'simulated production: not a real film; its cast and characters are part of this timeline'
- title: Hart & Associates
  kind: tv guest
  status: under way
  dates: 1982-08-06 to 1982-08-13
  details: a guest role on 'Hart & Associates' (first-run syndication); playing Steven, a union boss; an episode
    about a nightclub singer in danger; directed by Joyce Malone; with Raymond Emerson, Connie Lindgren
  pay: $8k
  format: hour-long private-eye series
- title: Santos Investigations
  kind: tv guest
  status: booked
  dates: 1982-08-20 to 1982-08-27
  details: a guest role on 'Santos Investigations' (PBS); playing Carlos Merrick, a young doctor; an episode about
    a blackmailed movie producer; directed by Neil Granger; with Glenn Ramsey, Barbara Clayton, Terry Delaney
  pay: $7k
  format: hour-long private-eye series
network:
- name: Greta Keating
  id: gen-ca-ind-1
  who: independent casting director
  how_you_know_them: read for a guest part on 'Santos Investigations' (PBS)
  standing: cordial
  last_interaction: read for a guest part on 'Santos Investigations' (PBS) (1982-08-06)
- name: Margaret Hayes
  id: gen-ag-ag-sb-1
  who: agent at Starling-Barr Talent (fictional)
  how_you_know_them: monthly check-in call
  standing: cordial
  last_interaction: monthly check-in call (1982-08-06)
- name: Sharon Kowalski
  id: gen-ca-st-col-1
  who: casting director at Columbia Pictures
  how_you_know_them: a strong audition for 'House of the Brave'
  standing: cordial
  last_interaction: a strong audition for 'House of the Brave' (1982-08-06)
- name: Oliver Stone
  id: wd:Q179497
  who: director
  how_you_know_them: a strong audition for 'House of the Brave'
  standing: cordial
  last_interaction: a strong audition for 'House of the Brave' (1982-08-06)
- name: Joan Barrett
  id: gen-ca-st-par-1
  who: casting director at Paramount Pictures
  how_you_know_them: a strong audition for 'Outer Voyager'
  standing: cordial
  last_interaction: a strong audition for 'Outer Voyager' (1982-08-06)
- name: Arthur Rankin Jr.
  id: wd:Q1983712
  who: director
  how_you_know_them: a strong audition for 'Outer Voyager'
  standing: cordial
  last_interaction: a strong audition for 'Outer Voyager' (1982-08-06)
- name: Raymond Emerson
  id: gen-a-00399
  who: actor
  how_you_know_them: worked together on a guest role on 'Hart & Associates' (first-run syndication)
  standing: cordial
  last_interaction: worked together on a guest role on 'Hart & Associates' (first-run syndication) (1982-08-06)
- name: Connie Lindgren
  id: gen-a-00244
  who: actor
  how_you_know_them: worked together on a guest role on 'Hart & Associates' (first-run syndication)
  standing: cordial
  last_interaction: worked together on a guest role on 'Hart & Associates' (first-run syndication) (1982-08-06)
- name: Joyce Malone
  id: gen-d-tv-43-2
  who: director
  how_you_know_them: worked together on a guest role on 'Hart & Associates' (first-run syndication)
  standing: cordial
  last_interaction: worked together on a guest role on 'Hart & Associates' (first-run syndication) (1982-08-06)
- name: Margaret Merrick
  id: gen-ca-ind-5
  who: independent casting director
  how_you_know_them: read for a guest part on 'Paradise Estate' (ABC)
  standing: close
  last_interaction: read for a guest part on 'Hart & Associates' (first-run syndication) (1982-07-23)
- name: Lori Winslow
  id: gen-ca-st-col-0
  who: casting director at Columbia Pictures
  how_you_know_them: a strong audition for 'Signal of the Dawn'
  standing: cordial
  last_interaction: a solid audition for 'Final Agenda' (1982-07-23)
- name: Ivan Nagy
  id: wd:Q3156157
  who: director
  how_you_know_them: a solid audition for 'Final Agenda'
  standing: cordial
  last_interaction: a solid audition for 'Final Agenda' (1982-07-23)
- name: Randy Moreno
  id: gen-ca-ind-6
  who: independent casting director
  how_you_know_them: read for a guest part on 'Lakeview County' (first-run syndication)
  standing: cordial
  last_interaction: read for a guest part on 'Highway Force West' (ABC) (1982-07-16)
- name: Greta Ramsey
  id: gen-a-00445
  who: actor
  how_you_know_them: worked together on a guest role on 'Santos Files' (CBS)
  standing: cordial
  last_interaction: worked together on a guest role on 'Santos Files' (CBS) (1982-07-16)
- name: Terry Underwood
  id: gen-d-tv-37-1
  who: director
  how_you_know_them: worked together on a guest role on 'Santos Files' (CBS)
  standing: cordial
  last_interaction: worked together on a guest role on 'Santos Files' (CBS) (1982-07-16)
open_threads:
- 'Decision waiting: Offer (after auditions): Calvin Marchetti, supporting in ''House of the Brave'' — A group of
  camp counsellors is trapped in a snowed-in lodge far from any help. Columbia Pictures, dir. Oliver Stone. Terms
  $95k. Shoots 1982-09-17 to 1982-10-22 (Chicago). (by 1982-08-16)'
- 'Decision waiting: Offer (after auditions): Wayne, supporting in ''Outer Voyager'' — A teenage hacker wakes up
  decades after the launch as the station fails. Paramount Pictures, dir. Arthur Rankin Jr.. Terms $95k. Shoots
  1982-10-29 to 1983-02-18 (Vancouver). (by 1982-08-16)'
- 'Upcoming: a guest role on ''Santos Investigations'' (PBS); playing Carlos Merrick, a young doctor; an episode
  about a blackmailed movie producer; directed by Neil Granger; with Glenn Ramsey, Barbara Clayton, Terry Delaney
  starting 1982-08-20'
- '''The Long Field'' is in post'
- '''Runaway Adventure'' is in post'
- 'Career goal: you want serious, respected work that gets noticed at awards time. So far in 1982: 64 submissions,
  20 call-ins, 2 film role(s) booked.'
- 'Relationship in motion with Sharon Kowalski: a strong audition for ''House of the Brave'''
- 'Relationship in motion with Oliver Stone: a strong audition for ''House of the Brave'''
- 'Relationship in motion with Joan Barrett: a strong audition for ''Outer Voyager'''
people:
- why_here: your agent
  id: gen-ag-ag-sb-1
  name: Margaret Hayes
  age: 30
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
    - monthly check-in call (1982-05-07)
    - monthly check-in call (1982-06-04)
    - monthly check-in call (1982-07-02)
    - monthly check-in call (1982-08-06)
  narrative_canon:
  - '1980-01-04: Margaret takes calls standing at her office window on Wilshire and calls Daniel "kiddo" when she
    is about to give bad news.'
- why_here: directing your film 'The Long Field'
  id: wd:Q449220
  name: Bruce Beresford
  age: 41
  profession: director
  public_profile: unknown to the public
  reputation: director of drama and action with 4 films
  traits:
  - quick-tempered
  - guarded
  motivation: driven mostly by respect and awards, and also by challenging, meaningful work
  ambition: wants serious, respected work that gets noticed at awards time
  bio: Australian film director (born 1940); known for 'Side by Side' (1975).
  recent_work:
  - '''Signal of the Dawn'' (1980, director; this timeline)'
  - '''The Long Field'' (1982, director; this timeline)'
  - '''Fast Crossing'' (1982, director; this timeline)'
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
  lately:
  - '1982-07-02: Bruce Beresford will direct ''Fast Crossing'' for 20th Century Fox.'
  narrative_canon:
  - '1980-07-25: Bruce Beresford shoots the hacker-lab scenes in long unbroken takes and asks Daniel to keep Leon''s
    hands busy with a soldering iron.'
  - '1981-01-16: Daniel gave Bruce Beresford The Long Field over coffee at Du-par''s on Ventura; Beresford read
    the first ten pages at the counter.'
- why_here: in the cast of your film 'The Long Field' (colead)
  id: wd:Q232477
  name: Jacqueline Bisset
  age: 37
  profession: actor
  public_profile: well known
  reputation: character actor in action and drama
  traits:
  - unhurried about fame
  - private
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: English actress (born 1944); known for 'The Deep' (1977).
  recent_work:
  - '''Iron Force'' (1982, supporting; this timeline)'
  - '''a national commercial for an airline'' (1982, commercial; this timeline)'
  - '''Westside Badge'' (1982, guest; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history: []
  lately:
  - '1982-06-11: Jacqueline Bisset was cast as Sharon (supporting) in ''Iron Force'' (Buena Vista (Disney)).'
- why_here: in the cast of your film 'The Long Field' (supporting)
  id: wd:Q504164
  name: Stephen Macht
  age: 40
  profession: actor
  public_profile: known mostly inside the industry
  reputation: character actor in thriller and action
  traits:
  - vain
  - chronically late
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: American actor (born 1942); known for 'Nightwing' (1979).
  recent_work:
  - '''a national commercial for a light beer'' (1981, commercial; this timeline)'
  - '''a national commercial for a camera'' (1981, commercial; this timeline)'
  - '''The Long Field'' (1982, supporting; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history: []
- why_here: in the cast of your film 'The Long Field' (supporting)
  id: wd:Q235302
  name: Carol Kane
  age: 30
  profession: actor
  public_profile: famous
  reputation: character actor in horror and action
  traits:
  - meticulous
  - unhurried about fame
  motivation: driven mostly by respect and awards, and also by financial security and big paydays
  ambition: wants serious, respected work that gets noticed at awards time
  bio: American actress (born 1952); known for 'When a Stranger Calls' (1979); Academy Award nominee.
  recent_work:
  - '''Summer Promise'' (1982, colead; this timeline)'
  - '''a national commercial for a light beer'' (1982, commercial; this timeline)'
  - '''Desert Rescue West'' (1982, guest; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history:
    - clashed on the set of 'The Long Field' (exhaustion after long days) (1982-01-08)
  lately:
  - '1982-04-16: Reviews for ''Blood Ritual'': mixed-to-positive (critics'' aggregate 61/100); opening-night audiences
    gave it an A.'
  - '1982-06-04: Carol Kane was cast as Tina Hudson (colead) in ''Summer Promise'' (Buena Vista (Disney)).'
  - '1982-08-06: ''Vendetta'' finished its theatrical run with $51.6M domestic and an estimated $54.8M overseas.'
- why_here: directing your film 'Runaway Adventure'
  id: wd:Q705572
  name: Daniel Petrie
  age: 61
  profession: director
  public_profile: unknown to the public
  reputation: director of drama and scifi with 8 films
  traits:
  - undisciplined
  - hungry
  - drawn to risky material
  motivation: driven mostly by financial security and big paydays, and also by respect and awards
  ambition: wants bigger paydays and financial security
  bio: Canadian film director (born 1920); known for 'The Betsy' (1978); award-nominated.
  recent_work:
  - '''Alien Colony at Big Sur'' (1981, director; this timeline)'
  - '''Runaway Adventure'' (1982, director; this timeline)'
  - '''Silent Agenda'' (1982, director; this timeline)'
  relationship_status: dating Donna Reed (simulated, not historical)
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: friendly
    status: acquainted
    history:
    - a strong audition for 'Runaway Adventure' (1982-01-08)
    - a strong audition for 'Silent Agenda' (1982-07-09)
  lately:
  - '1982-07-02: Daniel Petrie will direct ''Silent Agenda'' for Universal Pictures.'
- why_here: in the cast of your film 'Runaway Adventure' (lead)
  id: gen-a-00458
  name: Mary Reardon
  age: 27
  profession: actor
  public_profile: famous
  reputation: leading actor in comedy and family
  traits:
  - volatile
  - aloof
  - fiercely ambitious
  - hard to read
  motivation: driven mostly by respect and awards, and also by fame and visibility
  ambition: wants serious, respected work that gets noticed at awards time
  bio: A bona fide star; most at home in scifi; volatile, aloof.
  persona:
    hometown: Toronto
    signature: quotes Brando at every opportunity
    background: a stuntman turned actor
  recent_work:
  - '''Runaway Adventure'' (1982, lead; this timeline)'
  - '''Summer Affair'' (1982, lead; this timeline)'
  - '''The Hot Scheme'' (1982, lead; this timeline)'
  relationship_status: married (spouse outside the film industry)
  with_you:
    standing: strained
    status: acquainted
    history:
    - clashed on the set of 'Runaway Adventure' (exhaustion after long days) (1982-04-16)
    - clashed on the set of 'Runaway Adventure' (exhaustion after long days) (1982-04-30)
  lately:
  - '1982-05-14: Mary Reardon was cast as Marisol (lead) in ''Summer Affair'' (Warner Bros.).'
  - '1982-06-25: Reviews for ''Last Season at Crystal Lake'': strong (critics'' aggregate 83/100); opening-night
    audiences gave it an A+.'
  - '1982-07-30: Mary Reardon was cast as Tina (lead) in ''The Hot Scheme'' (Warner Bros.).'
- why_here: in the cast of your film 'Runaway Adventure' (supporting)
  id: gen-a-00091
  name: Anita Corbin
  age: 68
  profession: actor
  public_profile: known mostly inside the industry
  reputation: character actor in comedy and thriller
  traits:
  - cautious with choices
  - outgoing
  motivation: driven mostly by respect and awards, and also by fame and visibility
  ambition: wants serious, respected work that gets noticed at awards time
  bio: A working actor with a steady run of supporting parts; most at home in scifi; cautious with choices, outgoing.
  persona:
    hometown: Brooklyn
    signature: obsessive about getting the period details right
    background: a former dancer
  recent_work:
  - '''Runaway Adventure'' (1982, supporting; this timeline)'
  - '''A Town Called Hope'' (1982, tv_movie; this timeline)'
  - '''Summer of the City'' (1982, featured; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history: []
- why_here: in the cast of your film 'Runaway Adventure' (supporting)
  id: gen-a-00645
  name: Leslie Crane
  age: 27
  profession: actor
  public_profile: known mostly inside the industry
  reputation: character actor in family and action
  traits:
  - hungry
  motivation: driven mostly by a steady, sane life, and also by challenging, meaningful work
  ambition: wants steady work and a sustainable life
  bio: A working actor with a steady run of supporting parts; most at home in family; hungry.
  persona:
    hometown: a small town in Ohio
    signature: keeps a battered notebook of character ideas
    background: a former dancer
    series: Westside Badge
  recent_work:
  - '''Lakeview County'' (1981, guest; this timeline)'
  - '''Runaway Adventure'' (1982, supporting; this timeline)'
  - '''Brandt''s Voyager'' (1982, film_bit; this timeline)'
  relationship_status: married (spouse outside the film industry)
  with_you:
    standing: cordial
    status: acquainted
    history:
    - worked together on a guest role on 'Westside Badge' (ABC) (1982-03-19)
  lately:
  - '1982-07-02: ''The Long Witness'' finished its theatrical run with $20.2M domestic and an estimated $12.7M overseas.'
  - '1982-07-09: Reviews for ''Star Station'': mixed (critics'' aggregate 55/100); opening-night audiences gave
    it a B-.'
- why_here: in the cast of your film 'Runaway Adventure' (supporting)
  id: wd:Q979778
  name: Richard Masur
  age: 33
  profession: actor
  public_profile: a recognisable face
  reputation: character actor in action and family
  traits:
  - low-key
  - cautious with choices
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: American actor (born 1948); known for 'Hanover Street' (1979).
  recent_work:
  - '''a national commercial for a fast-food chain'' (1981, commercial; this timeline)'
  - '''Runaway Adventure'' (1982, supporting; this timeline)'
  - '''Nolan''s Kingdom'' (1982, film_bit; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history: []
  lately:
  - '1982-05-21: ''Ritual of the Wolves'' finished its theatrical run with $8.6M domestic and an estimated $8.3M
    overseas.'
- why_here: directing 'House of the Brave', which a pending decision is about
  id: wd:Q179497
  name: Oliver Stone
  age: 35
  profession: director
  public_profile: unknown to the public
  reputation: director of horror with 4 films
  traits:
  - vain
  - fiercely ambitious
  motivation: driven mostly by respect and awards, and also by challenging, meaningful work
  ambition: wants serious, respected work that gets noticed at awards time
  bio: American film director (born 1946); Academy Award winner.
  recent_work:
  - '''Hollow Lake'' (1981, director; this timeline)'
  - '''The Crawling Lake'' (1982, director; this timeline)'
  - '''House of the Brave'' (1982, director; this timeline)'
  relationship_status: married (spouse outside the film industry)
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history:
    - a strong audition for 'House of the Brave' (1982-08-06)
  lately:
  - '1982-07-30: Oliver Stone will direct ''House of the Brave'' for Columbia Pictures.'
- why_here: already cast in 'House of the Brave', which a pending decision is about
  id: wd:Q232837
  name: Katharine Ross
  age: 42
  profession: actor
  public_profile: well known
  reputation: leading actor in horror and drama
  traits:
  - low-key
  motivation: driven mostly by fame and visibility, and also by financial security and big paydays
  ambition: wants a breakout role and a recognisable name
  bio: American actress (born 1940); known for 'The Legacy' (1978); Academy Award nominee.
  recent_work:
  - '''Oakwood Memorial'' (1982, guest; this timeline)'
  - '''a national commercial for a breakfast cereal'' (1982, commercial; this timeline)'
  - '''House of the Brave'' (1982, lead; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  lately:
  - '1982-07-30: ''Distant Witness'' finished its theatrical run with $5.6M domestic and an estimated $4.3M overseas.'
  - '1982-08-06: Katharine Ross was cast as Susan Merrick (lead) in ''House of the Brave'' (Columbia Pictures).'
  - '1982-08-06: ''The Endless Kiss'' finished its theatrical run with $25.9M domestic and an estimated $21.7M overseas.'
- why_here: already cast in 'House of the Brave', which a pending decision is about
  id: wd:Q65932
  name: Anthony Hopkins
  age: 44
  profession: actor
  public_profile: well known
  reputation: leading actor in horror and drama
  traits:
  - aloof
  motivation: driven mostly by respect and awards, and also by fame and visibility
  ambition: wants serious, respected work that gets noticed at awards time
  bio: Welsh actor (born 1937); known for 'Magic' (1978).
  recent_work:
  - '''Sky Squadron'' (1982, guest; this timeline)'
  - '''House of the Brave'' (1982, colead; this timeline)'
  - '''Riverside Memorial'' (1982, guest; this timeline)'
  relationship_status: married (spouse outside the film industry) (documented)
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  lately:
  - '1982-07-02: Reviews for ''Summer Dance'': strong (critics'' aggregate 81/100); opening-night audiences gave
    it an A-.'
  - '1982-08-06: Anthony Hopkins was cast as Keith (colead) in ''House of the Brave'' (Columbia Pictures).'
- why_here: already cast in 'House of the Brave', which a pending decision is about
  id: wd:Q333475
  name: Mel Ferrer
  age: 64
  profession: actor
  public_profile: a recognisable face
  reputation: leading actor in horror and action
  traits:
  - meticulous
  - unhurried about fame
  - drawn to risky material
  - charming
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: American actor (born 1917); known for 'The Visitor' (1979).
  recent_work:
  - '''A Doll''s House'' (1982, stage; this timeline)'
  - '''a national commercial for a fast-food chain'' (1982, commercial; this timeline)'
  - '''House of the Brave'' (1982, supporting; this timeline)'
  relationship_status: married (spouse outside the film industry) (documented)
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  lately:
  - '1982-08-06: Mel Ferrer was cast as Nathan (supporting) in ''House of the Brave'' (Columbia Pictures).'
industry:
  box_office_chart:
  - 1. 'Rossi's Promise' (Warner Bros.) — $11.8M this week, $99.6M total, week 8
  - 2. 'Jackpot' (Metro-Goldwyn-Mayer) — $5.2M this week, $5.2M total, week 1
  - 3. 'Dead Line at Crystal Lake' (Universal Pictures) — $5.1M this week, $62.4M total, week 9
  - 4. 'The Dark Ritual' (Paramount Pictures) — $4.5M this week, $4.5M total, week 1
  - 5. 'Moonstruck Summer' (Universal Pictures) — $4.2M this week, $9.0M total, week 2
  news:
  - date: '1982-07-30'
    text: Harold Sakata died.
    provenance: documented history
  - date: '1982-07-30'
    text: Roberta Pedon died.
    provenance: documented history
  - date: '1982-08-06'
    text: Ivan Passer will direct 'Night Signal' for Metro-Goldwyn-Mayer.
    provenance: fictional production
  - date: '1982-08-06'
    text: Metro-Goldwyn-Mayer greenlit 'Night Signal', a thriller picture. An insurance investigator realises a
      client is not who he says as the killer closes in.
  - date: '1982-08-06'
    text: John Hurt was cast as Keith Cameron (featured) in 'Outer Voyager' (Paramount Pictures).
    provenance: simulated casting in a fictional production
  - date: '1982-08-06'
    text: Peter Cushing was cast as Frank (featured) in 'The Hot Scheme' (Warner Bros.).
    provenance: simulated casting in a fictional production
  - date: '1982-08-06'
    text: Dale Drake was cast as Ramon Rossi (lead) in 'Night Signal' (Metro-Goldwyn-Mayer).
  - date: '1982-08-06'
    text: 'Reviews for ''Jackpot'': savage (critics'' aggregate 17/100); opening-night audiences gave it a C-.'
    provenance: simulated event in this timeline
  - date: '1982-08-06'
    text: 'Reviews for ''Dead Force'': poor (critics'' aggregate 44/100); opening-night audiences gave it an F.'
    provenance: simulated event in this timeline
  - date: '1982-08-06'
    text: 'Reviews for ''The Dark Ritual'': mixed-to-positive (critics'' aggregate 60/100); opening-night audiences
      gave it a B.'
    provenance: simulated event in this timeline
  - date: '1982-08-06'
    text: '''Oakley''s Signal'' finished its theatrical run with $6.8M domestic and an estimated $3.8M overseas.'
    provenance: simulated event in this timeline
  - date: '1982-08-06'
    text: '''Hard Force'' finished its theatrical run with $14.1M domestic and an estimated $5.7M overseas.'
    provenance: simulated event in this timeline
  - date: '1982-08-06'
    text: '''Sharky''s Machine'' finished its theatrical run with $26.1M domestic and an estimated $7.1M overseas.'
    provenance: simulated event in this timeline
  - date: '1982-08-06'
    text: Ivy Sheridan and Desmond Okonkwo have started seeing each other.
pending_decisions:
- id: dec-00012
  kind: offer
  summary: 'Offer (after auditions): Calvin Marchetti, supporting in ''House of the Brave'' — A group of camp counsellors
    is trapped in a snowed-in lodge far from any help. Columbia Pictures, dir. Oliver Stone. Terms $95k. Shoots
    1982-09-17 to 1982-10-22 (Chicago).'
  options:
  - accept
  - decline
  - counter(fee)
  deadline: '1982-08-16'
  if_unanswered: decline
  story_preview:
    provenance: simulated screenplay for a fictional production
    logline: 'A atmospheric horror: A group of camp counsellors is trapped in a snowed-in lodge far from any help.'
    central_conflict: something is hunting Susan Merrick's group, and Keith refuses to believe it until it's too
      late
    your_key_scenes:
    - a phone call that changes everything
    - an argument in a moving car
    your_read_of_the_script: you think it's solid; the set pieces work, though parts feel familiar (your impression;
      it may be wrong)
    your_character: 'Calvin Marchetti (the first victim): wants to make things right; flaw: drinking; arc from drinking
      toward a reckoning with letting go'
  context: Your quote is $94k. Countering risks the studio walking away.
- id: dec-00013
  kind: offer
  summary: 'Offer (after auditions): Wayne, supporting in ''Outer Voyager'' — A teenage hacker wakes up decades
    after the launch as the station fails. Paramount Pictures, dir. Arthur Rankin Jr.. Terms $95k. Shoots 1982-10-29
    to 1983-02-18 (Vancouver).'
  options:
  - accept
  - decline
  - counter(fee)
  deadline: '1982-08-16'
  if_unanswered: decline
  story_preview:
    provenance: simulated screenplay for a fictional production
    logline: 'A effects-driven scifi: A teenage hacker wakes up decades after the launch as the station fails.'
    central_conflict: far from help, Keith Fielding must hold the crew together while Wayne hides the truth about
      the mission
    your_key_scenes:
    - a showdown in the rain
    - a phone call that changes everything
    your_read_of_the_script: privately, you think the script is weak and hope the director can save it (your impression;
      it may be wrong)
    your_character: 'Wayne (the corporate liaison): wants to make things right; flaw: fear of being ordinary; arc
      from fear of being ordinary toward a reckoning with responsibility'
  context: Your quote is $94k. Countering risks the studio walking away.
continuity:
  career_so_far:
  - '1981: ''Deadly Inheritance'' (tv_movie)'
  - '1981: ''Sky Squadron'' (guest)'
  - '1981: ''Warner''s Motive'' (film_bit)'
  - '1981: ''An Enemy of the People'' (stage)'
  - '1981: ''A Town Called Hope'' (tv_movie)'
  - '1981: ''Riverside Memorial'' (guest)'
  - '1981: ''Oakwood Memorial'' (guest)'
  - '1982: ''The Long Field'' (lead)'
  - '1982: ''Runaway Adventure'' (colead)'
  - '1982: ''Mountain Run'' (guest)'
  - '1982: ''Westside Badge'' (guest)'
  - '1982: ''Santos Files'' (guest)'
  initiatives_resolved:
  - '1980-07-25 meet: Meeting requested with Sydney Pollack. -> Met Sydney Pollack.'
  - '1980-08-22 develop project: Hired screenwriter Ellen Lindqvist ($17k); first draft due about 1980-10-17. ->
    Orion Pictures said yes: ''The Long Field'' is greenlit with you attached.'
  earlier_key_moments:
  - '1982-01-29: Reviews for ''The Red Run'': mixed (critics'' aggregate 45/100); opening-night audiences gave it
    an A+.'
  - '1982-01-29: ''The Red Run'' opened with $486k over its opening weekend (rank #31, 266 screens; $783k to date).'
  - '1982-01-29: ''Signal of the Dawn'' finished its theatrical run with $7.5M domestic and an estimated $4.3M overseas.'
  - '1982-02-05: ''The Long Field'' wrapped principal photography and moved into post-production.'
  - '1982-04-02: Principal photography began on ''Runaway Adventure'' in New York (11 weeks scheduled).'
  - '1982-04-16: Tension on the set of ''Runaway Adventure'': you clashed with Mary Reardon (exhaustion after long
    days).'
  - '1982-04-30: Tension on the set of ''Runaway Adventure'': you clashed with Mary Reardon (exhaustion after long
    days).'
  - '1982-06-11: Audition: Daniel Wade, the lead role in ''The Red Strike'' (action, Metro-Goldwyn-Mayer; director
    Jack Smight; casting Lisa Jameson) on 1982-06-18. Premise: A federal marshal takes on a corrupt sheriff while
    the clock runs down.'
  - '1982-06-18: You auditioned for Daniel Wade in ''The Red Strike'' and did not get a callback.'
  - '1982-06-18: ''Runaway Adventure'' wrapped principal photography and moved into post-production.'
  - '1982-06-25: You auditioned for Neil Halloran in ''Winslow''s Letters'' and made the final two.'
  - '1982-07-09: You auditioned for Ramon Fletcher in ''Silent Agenda'' and made the final two.'
  recent_scenes_and_threads:
  - '1982-07-23: with Ivan Nagy: a solid audition for ''Final Agenda'''
  - '1982-07-23: with Lori Winslow: a solid audition for ''Final Agenda'''
  - '1982-07-23: with Margaret Merrick: read for a guest part on ''Hart & Associates'' (first-run syndication)'
  - '1982-08-06: with Arthur Rankin Jr.: a strong audition for ''Outer Voyager'''
  - '1982-08-06: with Connie Lindgren: worked together on a guest role on ''Hart & Associates'' (first-run syndication)'
  - '1982-08-06: with Greta Keating: read for a guest part on ''Santos Investigations'' (PBS)'
  - '1982-08-06: with Joan Barrett: a strong audition for ''Outer Voyager'''
  - '1982-08-06: with Joyce Malone: worked together on a guest role on ''Hart & Associates'' (first-run syndication)'
  - '1982-08-06: with Margaret Hayes: monthly check-in call'
  - '1982-08-06: with Oliver Stone: a strong audition for ''House of the Brave'''
  - '1982-08-06: with Raymond Emerson: worked together on a guest role on ''Hart & Associates'' (first-run syndication)'
  - '1982-08-06: with Sharon Kowalski: a strong audition for ''House of the Brave'''
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
- '1981-08-14: Ellen Lindqvist works on the rewrite at a corner booth in Canter''s and reads Daniel new scenes over
  the phone at midnight.'
era:
  year: 1982
  average_ticket_price: $2.94
  note: The blockbuster era is a few years old; theatrical release dominates and home video is small but growing
    fast.
narrator_notes: []
```

## REPLY FORMAT
End your reply with exactly one block like this:

```engine
reply_to: pkt-00041
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
