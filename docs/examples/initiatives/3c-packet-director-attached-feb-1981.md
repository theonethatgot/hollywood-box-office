# Narrator packet pkt-00018 — 1981-02-06

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
packet: pkt-00018
date: '1981-02-06'
covers: 1981-01-16 .. 1981-02-06
state_hash: fae46cd468be6ad2
protagonist:
  id: player
  name: Daniel Brooks
  age: 30
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
  quote_reported_in_trades: $99k
  agent: Margaret Hayes at Starling-Barr Talent (fictional)
  agent_strategy: Pursuing respected directors and serious dramatic material and interesting scripts, stage work
    and character parts, even for less money; not prioritising steady bookings and series work over long shots.
  persona:
    hometown: Columbus, Ohio
    signature: always first to arrive and last to leave
    background: trained at the Yale School of Drama
  money:
    cash: 129937.0
    monthly_costs: 6000.0
  energy: tired
  relationship_status: single
  awards: []
canon:
- id: ev-5178
  date: '1981-01-16'
  text: You will audition for Carlos in 'Final Motive' on 1981-01-16.
- id: ev-5179
  date: '1981-01-16'
  text: Bruce Beresford agreed to attach to 'The Long Field'.
  provenance: simulated event in this timeline
- id: ev-5248
  date: '1981-01-16'
  text: 'Feedback from the room on ''Final Motive'' (via your agent): they went with a more established name.'
- id: ev-5249
  date: '1981-01-16'
  text: You auditioned for Carlos in 'Final Motive' and made the final two.
- id: ev-5250
  date: '1981-01-16'
  text: 'Others seen for Carlos: Sylvester Stallone, Tommy Lee Jones, Wesley Lawson.'
  provenance: simulated event in this timeline
- id: ev-5287
  date: '1981-01-16'
  text: 'Tension on the set of ''Wild Trouble'': you clashed with Maxine Keating (a clash of two volatile temperaments).'
- id: ev-5329
  date: '1981-01-23'
  text: 'Your agent got you in the room: Charles Wyatt in ''The Red Run'' (casting: Lori Wade) — the casting director
    asked for you by name.'
- id: ev-5330
  date: '1981-01-23'
  text: 'Audition booked: Charles Wyatt in ''The Red Run'' on 1981-01-30.'
- id: ev-5380
  date: '1981-01-30'
  text: You auditioned for Charles Wyatt in 'The Red Run' and won the part.
- id: ev-5381
  date: '1981-01-30'
  text: 'Others seen for Charles Wyatt: David Strathairn, Howard Pierce, Tom Berenger.'
  provenance: simulated event in this timeline
- id: ev-5382
  date: '1981-01-30'
  text: 'Offer (after auditions): Charles Wyatt, supporting in ''The Red Run'' — A mercenary with a conscience must
    escort a witness across the border while the clock runs down. Orion Pictures, dir. Michael D. Moore. Terms $55k.
    Shoots 1981-04-24 to 1981-07-17 (Toronto).'
- id: ev-5430
  date: '1981-01-30'
  text: 'Pitched ''The Long Field'' to United Artists: United Artists liked it but wants changes or a bigger name
    attached; still pitching.'
period_summary:
  overview: 3 week(s), working on 1 job(s), 4 submission(s) by your agent, 1 call-in(s), 2 audition(s), 0 booking(s);
    net money +$0.
  working:
  - shooting 'Wild Trouble' (1980-12-19 to 1981-02-27)
  quiet_period: false
  note: ''
rulings:
- proposal: dec-00005
  type: decision
  result: applied
  text: Audition confirmed for 'Final Motive' (prepared).
- proposal: i1
  type: initiative:develop_project
  result: accepted
  text: Bruce Beresford read it and said yes. Your agent will take the package back to the studios that were interested.
  initiative: ini-00002
delegated:
- Your agent booked you an audition for Charles Wyatt in 'The Red Run' on 1981-01-30.
standing_changes:
  now:
    public_profile: a recognisable face
    momentum: steady
    draw: a modest draw
    critics: respected
    industry_standing: a working professional
    quote: $99k
  changes: []
  relevant_events:
  - '1981-01-30: You auditioned for Charles Wyatt in ''The Red Run'' and won the part.'
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
  status: pitching
  started: '1980-08-22'
  history:
  - '1980-11-28: Buena Vista (Disney) passed.'
  - '1980-12-12: United Artists liked it but wants changes or a bigger name attached; still pitching.'
  - '1981-01-02: Metro-Goldwyn-Mayer passed.'
  - '1981-01-16: Bruce Beresford read ''The Long Field'' and agreed to attach.'
  - '1981-01-30: United Artists liked it but wants changes or a bigger name attached; still pitching.'
  next_step_due: '1981-02-20'
career_activity:
  submissions:
  - '1981-01-23: Rick Hastings (lead) in ''Trouble of the Dawn'' (New World Pictures, casting Linda Wyatt) — passed:
    they went with other actors'
  - '1981-01-23: Russell Abernathy (lead) in ''The Red Run'' (Orion Pictures, casting Lori Wade) — passed: they
    went with other actors'
  - '1981-01-23: Charles Wyatt (supporting) in ''The Red Run'' (Orion Pictures, casting Lori Wade) — requested:
    the casting director asked for you by name'
  - '1981-01-23: Joel Reeves (supporting) in ''Glass Motive'' (Paramount Pictures, casting Elizabeth Nolan) — passed:
    they didn''t see you as a family type'
  auditions:
  - '1981-01-16: You auditioned for Carlos in ''Final Motive'' and made the final two.'
  - '1981-01-16: Others seen for Carlos: Sylvester Stallone, Tommy Lee Jones, Wesley Lawson.'
  - '1981-01-23: Your agent got you in the room: Charles Wyatt in ''The Red Run'' (casting: Lori Wade) — the casting
    director asked for you by name.'
  - '1981-01-30: You auditioned for Charles Wyatt in ''The Red Run'' and won the part.'
  - '1981-01-30: Others seen for Charles Wyatt: David Strathairn, Howard Pierce, Tom Berenger.'
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
  stage: post
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
  stage: shooting
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
  shoot: 1980-12-19 to 1981-02-20
network:
- name: Lori Wade
  id: gen-ca-st-ori-0
  who: casting director at Orion Pictures
  how_you_know_them: a strong audition for 'Affair of the Deep'
  standing: friendly
  last_interaction: a strong audition for 'The Red Run' (1981-01-30)
- name: Michael D. Moore
  id: wd:Q6829651
  who: director
  how_you_know_them: a strong audition for 'The Red Run'
  standing: cordial
  last_interaction: a strong audition for 'The Red Run' (1981-01-30)
- name: Bruce Beresford
  id: wd:Q449220
  who: director
  how_you_know_them: a strong audition for 'Signal of the Dawn'
  standing: cordial
  last_interaction: agreed to attach to your project 'The Long Field' (1981-01-16)
- name: Maxine Keating
  id: gen-a-00139
  who: actor
  how_you_know_them: clashed on the set of 'Wild Trouble' (pressure from a slipping schedule boiled over)
  standing: strained
  last_interaction: clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments) (1981-01-16)
- name: Frank Corbin
  id: gen-d-tv-37-0
  who: director
  how_you_know_them: a strong audition for 'Final Motive'
  standing: cordial
  last_interaction: a strong audition for 'Final Motive' (1981-01-16)
- name: John Altman
  id: wd:Q1991526
  who: actor
  how_you_know_them: clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments)
  standing: cordial
  last_interaction: clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments) (1981-01-09)
- name: Margaret Hayes
  id: gen-ag-ag-sb-1
  who: agent at Starling-Barr Talent (fictional)
  how_you_know_them: monthly check-in call
  standing: cordial
  last_interaction: monthly check-in call (1981-01-02)
- name: Glenn Anderson
  id: gen-a-00049
  who: actor
  how_you_know_them: clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments)
  standing: cordial
  last_interaction: clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments) (1980-12-26)
- name: Margaret Merrick
  id: gen-ca-ind-5
  who: independent casting director
  how_you_know_them: read for a guest part on 'Paradise Estate' (ABC)
  standing: friendly
  last_interaction: read for a guest part on 'Paradise Estate' (ABC) (1980-11-14)
- name: Monty Coleman
  id: gen-a-00583
  who: actor
  how_you_know_them: worked together on a guest role on 'Mountain Run' (PBS)
  standing: cordial
  last_interaction: worked together on a guest role on 'Mountain Run' (PBS) (1980-11-07)
- name: Carmen Lindgren
  id: gen-a-00493
  who: actor
  how_you_know_them: worked together on a guest role on 'Mountain Run' (PBS)
  standing: cordial
  last_interaction: worked together on a guest role on 'Mountain Run' (PBS) (1980-11-07)
- name: Scott Fielding
  id: gen-d-tv-42-0
  who: director
  how_you_know_them: worked together on a guest role on 'Mountain Run' (PBS)
  standing: cordial
  last_interaction: worked together on a guest role on 'Mountain Run' (PBS) (1980-11-07)
- name: Neil Burke
  id: gen-ca-st-bv-0
  who: casting director at Buena Vista (Disney)
  how_you_know_them: a strong audition for 'Wild Trouble'
  standing: cordial
  last_interaction: a strong audition for 'Wild Trouble' (1980-10-31)
- name: Michael Nankin
  id: wd:Q6833019
  who: director
  how_you_know_them: a strong audition for 'Wild Trouble'
  standing: cordial
  last_interaction: a strong audition for 'Wild Trouble' (1980-10-31)
- name: Bruce Malone
  id: gen-ca-ind-7
  who: independent casting director
  how_you_know_them: read for a guest part on 'Dugan's Garage Blues' (PBS)
  standing: cordial
  last_interaction: read for a guest part on 'Maple Street' (CBS) (1980-10-24)
open_threads:
- 'Decision waiting: Offer (after auditions): Charles Wyatt, supporting in ''The Red Run'' — A mercenary with a
  conscience must escort a witness across the border while the clock runs down. Orion Pictures, dir. Michael D.
  Moore. Terms $55k. Shoots 1981-04-24 to 1981-07-17 (Toronto). (by 1981-02-09)'
- '''Signal of the Dawn'' is in post'
- '''Wild Trouble'' is in shooting'
- 'Career goal: you want serious, respected work that gets noticed at awards time. So far in 1981: 7 submissions,
  2 call-ins, 1 film role(s) booked.'
- 'Relationship in motion with Maxine Keating: clashed on the set of ''Wild Trouble'' (a clash of two volatile temperaments)'
- 'Relationship in motion with John Altman: clashed on the set of ''Wild Trouble'' (a clash of two volatile temperaments)'
- 'Relationship in motion with Frank Corbin: a strong audition for ''Final Motive'''
people:
- why_here: your agent
  id: gen-ag-ag-sb-1
  name: Margaret Hayes
  age: 28
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
    - monthly check-in call (1980-10-03)
    - monthly check-in call (1980-11-07)
    - monthly check-in call (1980-12-05)
    - monthly check-in call (1981-01-02)
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
  reputation: leading actor in comedy and horror
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
  - '''Santos Files'' (1980, guest; this timeline)'
  - '''Westside Beat'' (1981, guest; this timeline)'
  - '''Hollow Harvest'' (1981, lead; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history:
    - clashed on the set of 'Signal of the Dawn' (a clash of two volatile temperaments) (1980-10-10)
- why_here: in the cast of your film 'Signal of the Dawn' (colead)
  id: gen-a-00623
  name: Natalie Rhodes
  age: 33
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
  - '''Dakota Case Story'' (1980, guest; this timeline)'
  - '''Maple Street'' (1981, guest; this timeline)'
  - '''Desert Rescue West'' (1981, guest; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history: []
  lately:
  - '1980-11-07: Reviews for ''Moonlighting'': savage (critics'' aggregate 29/100); opening-night audiences gave
    it an F.'
- why_here: in the cast of your film 'Signal of the Dawn' (supporting)
  id: wd:Q34851
  name: Elizabeth Taylor
  age: 48
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
  - '''Paradise Landing'' (1980, guest; this timeline)'
  - '''Bay City Patrol'' (1980, guest; this timeline)'
  - '''Oakley''s Signal'' (1981, film_bit; this timeline)'
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
  lately:
  - '1980-10-24: Michael Nankin will direct ''Wild Trouble'' for Buena Vista (Disney).'
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
  - '''Hot Wedding'' (1980, colead; this timeline)'
  - '''Wild Trouble'' (1981, lead; this timeline)'
  - '''Harper''s Getaway'' (1981, lead; this timeline)'
  relationship_status: single
  with_you:
    standing: strained
    status: acquainted
    history:
    - clashed on the set of 'Wild Trouble' (pressure from a slipping schedule boiled over) (1981-01-02)
    - clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments) (1981-01-16)
  lately:
  - '1980-10-24: Maxine Keating was cast as Teresa Yates (lead) in ''Wild Trouble'' (Buena Vista (Disney)).'
  - '1981-01-02: Maxine Keating was cast as Diane Kessler (lead) in ''Harper''s Getaway'' (AVCO Embassy Pictures).'
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
  lately:
  - '1980-10-31: Glenn Anderson was cast as Richard Calloway (colead) in ''Wild Trouble'' (Buena Vista (Disney)).'
- why_here: in the cast of your film 'Wild Trouble' (supporting)
  id: gen-a-00619
  name: Ingrid Emerson
  age: 62
  profession: actor
  public_profile: a recognisable face
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
- why_here: directing 'The Red Run', which a pending decision is about
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
  lately:
  - '1981-01-23: Michael D. Moore will direct ''The Red Run'' for Orion Pictures.'
- why_here: already cast in 'The Red Run', which a pending decision is about
  id: wd:Q2685
  name: Arnold Schwarzenegger
  age: 33
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
  - '''Silver Landing'' (1981, guest; this timeline)'
  - '''Desert Rescue'' (1981, guest; this timeline)'
  - '''The Red Run'' (1981, lead; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  lately:
  - '1981-01-30: Arnold Schwarzenegger was cast as Russell Abernathy (lead) in ''The Red Run'' (Orion Pictures).'
- why_here: already cast in 'The Red Run', which a pending decision is about
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
  - '''Room of the Brave'' (1980, featured; this timeline)'
  - '''Fort Apache, The Bronx'' (1981, featured; this timeline)'
  - '''The Red Run'' (1981, colead; this timeline)'
  relationship_status: single
- why_here: already cast in 'The Red Run', which a pending decision is about
  id: wd:Q363271
  name: David Warner
  age: 39
  profession: actor
  public_profile: a recognisable face
  reputation: working actor in horror and action
  traits:
  - warm
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: British actor (born 1941); known for 'Nightwing' (1979).
  recent_work:
  - '''Bay City Patrol'' (1980, guest; this timeline)'
  - '''Santos Investigations'' (1980, guest; this timeline)'
  - '''The Red Run'' (1981, supporting; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  lately:
  - '1980-10-10: Reviews for ''The Island'': mixed (critics'' aggregate 54/100); opening-night audiences gave it
    a B.'
  - '1981-01-30: David Warner was cast as Kenneth Vaughn (supporting) in ''The Red Run'' (Orion Pictures).'
- why_here: already cast in 'The Red Run', which a pending decision is about
  id: wd:Q492176
  name: Alec McCowen
  age: 55
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
industry:
  box_office_chart:
  - 1. 'The Incredible Shrinking Woman' (Universal Pictures) — $5.9M this week, $5.9M total, week 1
  - 2. 'Any Which Way You Can' (Warner Bros.) — $5.3M this week, $58.8M total, week 7
  - 3. 'Superman II' (Warner Bros.) — $4.8M this week, $81.8M total, week 9
  - 4. '9 to 5' (20th Century Fox) — $2.7M this week, $31.5M total, week 7
  - 5. 'The Formula' (United Artists) — $2.4M this week, $25.2M total, week 7
  news:
  - date: '1981-01-23'
    text: Michael D. Moore will direct 'The Red Run' for Orion Pictures.
    provenance: fictional production
  - date: '1981-01-23'
    text: Orion Pictures greenlit 'The Red Run', an action picture. A mercenary with a conscience must escort a
      witness across the border while the clock runs down.
  - date: '1981-01-23'
    text: Kevin Castillo will direct 'Glass Motive' for Paramount Pictures.
  - date: '1981-01-23'
    text: Paramount Pictures greenlit 'Glass Motive', a thriller picture. A wiretap technician realises a client
      is not who he says as the killer closes in.
  - date: '1981-01-30'
    text: David Warner was cast as Kenneth Vaughn (supporting) in 'The Red Run' (Orion Pictures).
    provenance: simulated casting in a fictional production
  - date: '1981-01-30'
    text: Beatrice Straight was cast as Joan Vaughn (featured) in 'The Red Run' (Orion Pictures).
    provenance: simulated casting in a fictional production
  - date: '1981-01-30'
    text: Robert Houston was cast as Jerry Tierney (supporting) in 'Glass Motive' (Paramount Pictures).
    provenance: simulated casting in a fictional production
  - date: '1981-01-30'
    text: 'Reviews for ''The Incredible Shrinking Woman'': mixed (critics'' aggregate 55/100); opening-night audiences
      gave it an A.'
    provenance: simulated event in this timeline
  - date: '1981-01-30'
    text: 'Reviews for ''Broken Inheritance at Gallows Hill'': poor (critics'' aggregate 31/100); opening-night
      audiences gave it a B+.'
    provenance: simulated event in this timeline
  - date: '1981-01-30'
    text: '''The Hunter'' finished its theatrical run with $12.9M domestic and an estimated $8.6M overseas.'
    provenance: simulated event in this timeline
  - date: '1981-01-30'
    text: '''Crane''s Trouble'' finished its theatrical run with $28.0M domestic and an estimated $28.0M overseas.'
    provenance: simulated event in this timeline
  - date: '1981-01-30'
    text: '''The Big Red One'' finished its theatrical run with $55.4M domestic and an estimated $26.7M overseas.'
    provenance: simulated event in this timeline
  - date: '1981-01-30'
    text: Bill Murray married Mickey Kelly.
    provenance: documented history
  - date: '1981-01-30'
    text: Lynne Frederick married David Frost.
    provenance: documented history
pending_decisions:
- id: dec-00006
  kind: offer
  summary: 'Offer (after auditions): Charles Wyatt, supporting in ''The Red Run'' — A mercenary with a conscience
    must escort a witness across the border while the clock runs down. Orion Pictures, dir. Michael D. Moore. Terms
    $55k. Shoots 1981-04-24 to 1981-07-17 (Toronto).'
  options:
  - accept
  - decline
  - counter(fee)
  deadline: '1981-02-09'
  if_unanswered: decline
  story_preview:
    provenance: simulated screenplay for a fictional production
    logline: 'A glossy action: A mercenary with a conscience must escort a witness across the border while the clock
      runs down.'
    central_conflict: Russell Abernathy has one chance to stop Kenneth Vaughn before the deadline, and can't do
      it without Donna Jameson
    your_key_scenes:
    - a phone call that changes everything
    - a chase through a crowded market
    your_read_of_the_script: you think it's genuinely good, especially the dialogue (your impression; it may be
      wrong)
    your_character: 'Charles Wyatt (the commanding officer): wants to be left alone; flaw: a temper they can''t
      control; arc from a temper they can''t control toward a reckoning with courage'
  context: Your quote is $99k. Countering risks the studio walking away.
continuity:
  career_so_far:
  - '1976: ''Lonely Promise'' (supporting)'
  - '1976: ''Last Bridges'' (colead)'
  - '1976: ''Moonlit Dance'' (supporting)'
  - '1977: ''Great Dog'' (colead)'
  - '1977: ''Quantum Station'' (supporting)'
  - '1980: ''Sky Squadron'' (guest)'
  - '1980: ''Sky Squadron'' (guest)'
  - '1980: ''Fifth Street'' (guest)'
  - '1980: ''Desert Rescue'' (guest)'
  - '1980: ''Signal of the Dawn'' (supporting)'
  - '1980: ''Mountain Run'' (guest)'
  - '1981: ''Wild Trouble'' (supporting)'
  initiatives_resolved:
  - '1980-07-25 meet: Meeting requested with Sydney Pollack. -> Met Sydney Pollack.'
  earlier_key_moments:
  - '1980-10-10: Tension on the set of ''Signal of the Dawn'': you clashed with Hal Keating (a clash of two volatile
    temperaments).'
  - '1980-10-10: Tension on the set of ''Signal of the Dawn'': you clashed with Alan Okonkwo (exhaustion after long
    days).'
  - '1980-10-17: ''Signal of the Dawn'' wrapped principal photography and moved into post-production.'
  - '1980-10-17: The draft of ''The Long Field'' arrived; you love it.'
  - '1980-10-31: You auditioned for Dean Wyatt in ''Wild Trouble'' and won the part.'
  - '1980-10-31: Offer (after auditions): Dean Wyatt, supporting in ''Wild Trouble'' — A stuffy accountant inherits
    a failing nightclub and everything goes wrong. Buena Vista (Disney), dir. Michael Nankin. Terms $99k. Shoots
    1980-12-19 to 1981-02-20 (Los Angeles).'
  - '1980-11-07: Daniel Brooks was cast as Dean Wyatt (supporting) in ''Wild Trouble'' (Buena Vista (Disney)).'
  - '1980-12-19: Principal photography began on ''Wild Trouble'' in Los Angeles (9 weeks scheduled).'
  - '1980-12-26: Tension on the set of ''Wild Trouble'': you clashed with Glenn Anderson (a clash of two volatile
    temperaments).'
  - '1981-01-02: Tension on the set of ''Wild Trouble'': you clashed with Maxine Keating (pressure from a slipping
    schedule boiled over).'
  - '1981-01-09: Audition: Carlos, the lead role in ''Final Motive'' (thriller, Orion Pictures; director Frank Corbin;
    casting Lori Wade) on 1981-01-16. Premise: A junior senator''s aide realises a client is not who he says with
    powerful people watching.'
  - '1981-01-09: Tension on the set of ''Wild Trouble'': you clashed with John Altman (a clash of two volatile temperaments).'
  recent_scenes_and_threads:
  - '1980-11-14: with Margaret Merrick: read for a guest part on ''Paradise Estate'' (ABC)'
  - '1980-12-05: with Margaret Hayes: monthly check-in call'
  - '1980-12-26: with Glenn Anderson: clashed on the set of ''Wild Trouble'' (a clash of two volatile temperaments)'
  - '1981-01-02: with Margaret Hayes: monthly check-in call'
  - '1981-01-02: with Maxine Keating: clashed on the set of ''Wild Trouble'' (pressure from a slipping schedule
    boiled over)'
  - '1981-01-09: with John Altman: clashed on the set of ''Wild Trouble'' (a clash of two volatile temperaments)'
  - '1981-01-16: with Bruce Beresford: agreed to attach to your project ''The Long Field'''
  - '1981-01-16: with Frank Corbin: a strong audition for ''Final Motive'''
  - '1981-01-16: with Lori Wade: a strong audition for ''Final Motive'''
  - '1981-01-16: with Maxine Keating: clashed on the set of ''Wild Trouble'' (a clash of two volatile temperaments)'
  - '1981-01-30: with Lori Wade: a strong audition for ''The Red Run'''
  - '1981-01-30: with Michael D. Moore: a strong audition for ''The Red Run'''
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
reply_to: pkt-00018
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
