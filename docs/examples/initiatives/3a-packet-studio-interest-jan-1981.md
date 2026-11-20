# Narrator packet pkt-00017 — 1981-01-16

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
packet: pkt-00017
date: '1981-01-16'
covers: 1981-01-02 .. 1981-01-16
state_hash: d981bb3c142dc1ce
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
  energy: fine
  relationship_status: single
  awards: []
canon:
- id: ev-5001
  date: '1981-01-02'
  text: 'Tension on the set of ''Wild Trouble'': you clashed with Maxine Keating (pressure from a slipping schedule
    boiled over).'
- id: ev-5062
  date: '1981-01-02'
  text: 'Margaret Hayes checked in; they submitted you for 2 roles this past month; 0 got you in the room; the most
    common feedback on passes: ''they went with other actors''; they want to get you seen in a respected stage production.'
- id: ev-5063
  date: '1981-01-02'
  text: 'Pitched ''The Long Field'' to Metro-Goldwyn-Mayer: Metro-Goldwyn-Mayer passed.'
- id: ev-5157
  date: '1981-01-09'
  text: 'Your agent got you in the room: Carlos in ''Final Motive'' (casting: Lori Wade) — the casting director
    liked your submission.'
- id: ev-5158
  date: '1981-01-09'
  text: 'Audition: Carlos, the lead role in ''Final Motive'' (thriller, Orion Pictures; director Frank Corbin; casting
    Lori Wade) on 1981-01-16. Premise: A junior senator''s aide realises a client is not who he says with powerful
    people watching.'
- id: ev-5170
  date: '1981-01-09'
  text: 'Tension on the set of ''Wild Trouble'': you clashed with John Altman (a clash of two volatile temperaments).'
  provenance: simulated event in this timeline
period_summary:
  overview: 2 week(s), working on 1 job(s), 3 submission(s) by your agent, 1 call-in(s), 0 audition(s), 0 booking(s);
    net money -$6k.
  working:
  - shooting 'Wild Trouble' (1980-12-19 to 1981-02-27)
  quiet_period: false
  note: ''
rulings: []
delegated: []
standing_changes:
  now:
    public_profile: a recognisable face
    momentum: steady
    draw: a modest draw
    critics: respected
    industry_standing: a working professional
    quote: $99k
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
  status: pitching
  started: '1980-08-22'
  history:
  - '1980-10-31: Columbia Pictures passed.'
  - '1980-11-14: 20th Century Fox passed.'
  - '1980-11-28: Buena Vista (Disney) passed.'
  - '1980-12-12: United Artists liked it but wants changes or a bigger name attached; still pitching.'
  - '1981-01-02: Metro-Goldwyn-Mayer passed.'
  next_step_due: '1981-01-16'
career_activity:
  submissions:
  - '1981-01-02: Kenneth (supporting) in ''Crazy Trouble at Coney Island'' (Warner Bros., casting Donna Barrett)
    — passed: they went with other actors'
  - '1981-01-02: Gordon Morrow (featured) in ''Crazy Trouble at Coney Island'' (Warner Bros., casting Donna Barrett)
    — passed: the part pays well below your quote'
  - '1981-01-09: Carlos (lead) in ''Final Motive'' (Orion Pictures, casting Lori Wade) — called in: the casting
    director liked your submission'
  auditions:
  - '1981-01-09: Your agent got you in the room: Carlos in ''Final Motive'' (casting: Lori Wade) — the casting director
    liked your submission.'
  agent_calls:
  - '1981-01-02: Margaret Hayes checked in; they submitted you for 2 roles this past month; 0 got you in the room;
    the most common feedback on passes: ''they went with other actors''; they want to get you seen in a respected
    stage production.'
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
- name: John Altman
  id: wd:Q1991526
  who: actor
  how_you_know_them: clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments)
  standing: strained
  last_interaction: clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments) (1981-01-09)
- name: Margaret Hayes
  id: gen-ag-ag-sb-1
  who: agent at Starling-Barr Talent (fictional)
  how_you_know_them: monthly check-in call
  standing: cordial
  last_interaction: monthly check-in call (1981-01-02)
- name: Maxine Keating
  id: gen-a-00139
  who: actor
  how_you_know_them: clashed on the set of 'Wild Trouble' (pressure from a slipping schedule boiled over)
  standing: strained
  last_interaction: clashed on the set of 'Wild Trouble' (pressure from a slipping schedule boiled over) (1981-01-02)
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
- name: Hal Keating
  id: gen-a-00632
  who: actor
  how_you_know_them: clashed on the set of 'Signal of the Dawn' (a clash of two volatile temperaments)
  standing: cordial
  last_interaction: clashed on the set of 'Signal of the Dawn' (a clash of two volatile temperaments) (1980-10-10)
- name: Alan Okonkwo
  id: gen-a-00005
  who: actor
  how_you_know_them: clashed on the set of 'Signal of the Dawn' (exhaustion after long days)
  standing: cordial
  last_interaction: clashed on the set of 'Signal of the Dawn' (exhaustion after long days) (1980-10-10)
- name: Timothy Yates
  id: gen-d-tv-30-2
  who: director
  how_you_know_them: worked together on a guest role on 'Sky Squadron' (ABC)
  standing: cordial
  last_interaction: a strong audition for 'Affair of the Deep' (1980-10-03)
- name: Lori Wade
  id: gen-ca-st-ori-0
  who: casting director at Orion Pictures
  how_you_know_them: a strong audition for 'Affair of the Deep'
  standing: cordial
  last_interaction: a strong audition for 'Affair of the Deep' (1980-10-03)
open_threads:
- 'Decision waiting: Audition: Carlos, the lead role in ''Final Motive'' (thriller, Orion Pictures; director Frank
  Corbin; casting Lori Wade) on 1981-01-16. Premise: A junior senator''s aide realises a client is not who he says
  with powerful people watching. (by 1981-01-16)'
- '''Signal of the Dawn'' is in post'
- '''Wild Trouble'' is in shooting'
- 'Career goal: you want serious, respected work that gets noticed at awards time. So far in 1981: 3 submissions,
  1 call-ins, 1 film role(s) booked.'
- 'Relationship in motion with Maxine Keating: clashed on the set of ''Wild Trouble'' (pressure from a slipping
  schedule boiled over)'
- 'Relationship in motion with Glenn Anderson: clashed on the set of ''Wild Trouble'' (a clash of two volatile temperaments)'
- 'Relationship in motion with John Altman: clashed on the set of ''Wild Trouble'' (a clash of two volatile temperaments)'
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
  narrative_canon:
  - '1980-07-25: Bruce Beresford shoots the hacker-lab scenes in long unbroken takes and asks Daniel to keep Leon''s
    hands busy with a soldering iron.'
- why_here: in the cast of your film 'Signal of the Dawn' (lead)
  id: gen-a-00632
  name: Hal Keating
  age: 41
  profession: actor
  public_profile: a recognisable face
  reputation: working actor in comedy and scifi
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
  - '''Dugan''s Street'' (1980, guest; this timeline)'
  - '''Santos Files'' (1980, guest; this timeline)'
  - '''Westside Beat'' (1981, guest; this timeline)'
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
  - '''Harbor Badge Story'' (1980, guest; this timeline)'
  - '''Dakota Case Story'' (1980, guest; this timeline)'
  - '''Maple Street'' (1981, guest; this timeline)'
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
  - '''The Devil and Max Devlin'' (1980, film_bit; this timeline)'
  - '''Paradise Landing'' (1980, guest; this timeline)'
  - '''Bay City Patrol'' (1980, guest; this timeline)'
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
  age: 30
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
- why_here: directing 'Final Motive', which a pending decision is about
  id: gen-d-tv-37-0
  name: Frank Corbin
  age: 61
  profession: director
  public_profile: unknown to the public
  reputation: director of thriller
  traits:
  - low-key
  motivation: driven mostly by respect and awards, and also by financial security and big paydays
  ambition: wants serious, respected work that gets noticed at awards time
  bio: Television director who works regularly on 'Santos Files'.
  persona:
    hometown: Chicago
    signature: insists on shooting on location
  recent_work:
  - '''Final Motive'' (1981, director; this timeline)'
  relationship_status: married (spouse outside the film industry)
  lately:
  - '1981-01-09: Frank Corbin will direct ''Final Motive'' for Orion Pictures.'
- why_here: in this period's events (called in, 1981-01-09)
  id: gen-ca-st-ori-0
  name: Lori Wade
  age: 54
  profession: casting director at Orion Pictures
  public_profile: unknown to the public
  reputation: an unknown
  traits:
  - undisciplined
  motivation: driven mostly by challenging, meaningful work, and also by respect and awards
  ambition: wants challenging material over safe paychecks
  bio: Casting director (Orion Pictures); notoriously hard to impress.
  persona:
    style: notoriously hard to impress
    hometown: Philadelphia
    signature: scouts small theatres every weekend
  relationship_status: married (spouse outside the film industry)
  with_you:
    standing: cordial
    status: acquainted
    history:
    - a strong audition for 'Affair of the Deep' (1980-10-03)
- why_here: in this period's events (set conflict, 1981-01-09)
  id: wd:Q1991526
  name: John Altman
  age: 28
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in comedy and drama
  traits:
  - low-key
  - unhurried about fame
  - outgoing
  motivation: driven mostly by challenging, meaningful work, and also by respect and awards
  ambition: wants challenging material over safe paychecks
  bio: Actor (born 1952); known for 'Birth of the Beatles' (1979).
  recent_work:
  - '''The Cherry Orchard'' (1980, stage; this timeline)'
  - '''Wild Trouble'' (1981, featured; this timeline)'
  - '''Candida'' (1980, stage; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: strained
    status: acquainted
    history:
    - clashed on the set of 'Wild Trouble' (a clash of two volatile temperaments) (1981-01-09)
- why_here: in the cast of your film 'Signal of the Dawn' (featured)
  id: wd:Q2549047
  name: Ward Costello
  age: 61
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in scifi and action
  traits:
  - aloof
  motivation: driven mostly by fame and visibility, and also by financial security and big paydays
  ambition: wants a breakout role and a recognisable name
  bio: American actor (born 1919); known for 'Goldengirl' (1979).
  recent_work:
  - '''Willie & Phil'' (1980, film_bit; this timeline)'
  - '''a national commercial for an airline'' (1980, commercial; this timeline)'
  - '''Signal of the Dawn'' (1980, featured; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history: []
- why_here: in the cast of your film 'Signal of the Dawn' (featured)
  id: wd:Q433514
  name: Joanne Linville
  age: 53
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in romance and drama
  traits: []
  motivation: driven mostly by financial security and big paydays, and also by a steady, sane life
  ambition: wants bigger paydays and financial security
  bio: American actress (born 1928); known for 'Gable and Lombard' (1976).
  recent_work:
  - '''A Star Is Born'' (1976, supporting; documented)'
  - '''Signal of the Dawn'' (1980, featured; this timeline)'
  - '''Zoot Suit'' (1981, featured; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  with_you:
    standing: cordial
    status: acquainted
    history: []
industry:
  box_office_chart:
  - 1. 'Any Which Way You Can' (Warner Bros.) — $9.7M this week, $39.7M total, week 4
  - 2. 'Superman II' (Warner Bros.) — $8.3M this week, $64.8M total, week 6
  - 3. '9 to 5' (20th Century Fox) — $4.6M this week, $22.1M total, week 4
  - 4. 'Raging Bull' (United Artists) — $3.6M this week, $19.0M total, week 4
  - 5. 'The Formula' (United Artists) — $3.5M this week, $17.2M total, week 4
  news:
  - date: '1981-01-02'
    text: Diane Keaton and Warren Beatty separated.
    provenance: documented history
  - date: '1981-01-02'
    text: Jane Seymour married David Flynn.
    provenance: documented history
  - date: '1981-01-02'
    text: Tommy Lee Jones married Kimberlea Cloughley.
    provenance: documented history
  - date: '1981-01-02'
    text: Jessica Lange and Paco Grande divorced.
    provenance: documented history
  - date: '1981-01-02'
    text: Bibi Andersson and Per Ahlmark divorced.
    provenance: documented history
  - date: '1981-01-02'
    text: Ron Leibman and Linda Lavin divorced.
    provenance: documented history
  - date: '1981-01-09'
    text: Jeffrey Pierce turned down Thomas Donovan in 'Hardcase'.
  - date: '1981-01-09'
    text: Richard Gere was cast as Vincent (lead) in 'Weekend Business' (Buena Vista (Disney)).
    provenance: simulated casting in a fictional production
  - date: '1981-01-09'
    text: Roger Dalton was cast as Nathan Clayton (lead) in 'Force of the Deep' (Metro-Goldwyn-Mayer).
  - date: '1981-01-09'
    text: Sigourney Weaver was cast as Diane Brandt (lead) in 'Hearts of the City' (Warner Bros.).
    provenance: simulated casting in a fictional production
  - date: '1981-01-09'
    text: '''Willie & Phil'' finished its theatrical run with $7.4M domestic and an estimated $5.7M overseas.'
    provenance: simulated event in this timeline
  - date: '1981-01-09'
    text: '''Cloud Dancer'' finished its theatrical run with $12.0M domestic and an estimated $21.2M overseas.'
    provenance: simulated event in this timeline
  - date: '1981-01-09'
    text: '''Hide in Plain Sight'' finished its theatrical run with $9.1M domestic and an estimated $7.9M overseas.'
    provenance: simulated event in this timeline
  - date: '1981-01-09'
    text: Caitlyn Jenner married Linda Thompson.
    provenance: documented history
pending_decisions:
- id: dec-00005
  kind: audition
  summary: 'Audition: Carlos, the lead role in ''Final Motive'' (thriller, Orion Pictures; director Frank Corbin;
    casting Lori Wade) on 1981-01-16. Premise: A junior senator''s aide realises a client is not who he says with
    powerful people watching.'
  options:
  - attend
  - attend_prepared
  - decline
  deadline: '1981-01-16'
  if_unanswered: decline
  story_preview:
    provenance: simulated screenplay for a fictional production
    logline: 'A Hitchcockian thriller: A junior senator''s aide realises a client is not who he says with powerful
      people watching.'
    central_conflict: Carlos uncovers something Rex Holloway will kill to keep hidden, and Greta may be in on it
    your_key_scenes:
    - a late-night confrontation in a kitchen
    - an argument in a moving car
    your_read_of_the_script: you think it's genuinely good, especially the structure (your impression; it may be
      wrong)
    your_character: 'Carlos (the investigator): wants to protect the one person they love; flaw: pride; arc from
      pride toward forgiveness'
  context: attend_prepared spends extra energy on preparation for a better read.
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
  - '1980-10-03: You auditioned for John Irving in ''Affair of the Deep'' and did not get a callback.'
  - '1980-10-03: There is an unmistakable spark between you and Gail Tierney on the set of ''Signal of the Dawn''.'
  - '1980-10-03: Chemistry with Gail Tierney: pursue something, or keep it professional?'
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
  recent_scenes_and_threads:
  - '1980-11-07: with Carmen Lindgren: worked together on a guest role on ''Mountain Run'' (PBS)'
  - '1980-11-07: with Margaret Hayes: monthly check-in call'
  - '1980-11-07: with Margaret Merrick: read for a guest part on ''Hart & Associates'' (first-run syndication)'
  - '1980-11-07: with Monty Coleman: worked together on a guest role on ''Mountain Run'' (PBS)'
  - '1980-11-07: with Scott Fielding: worked together on a guest role on ''Mountain Run'' (PBS)'
  - '1980-11-14: with Margaret Merrick: read for a guest part on ''Desert Rescue West'' (NBC)'
  - '1980-11-14: with Margaret Merrick: read for a guest part on ''Paradise Estate'' (ABC)'
  - '1980-12-05: with Margaret Hayes: monthly check-in call'
  - '1980-12-26: with Glenn Anderson: clashed on the set of ''Wild Trouble'' (a clash of two volatile temperaments)'
  - '1981-01-02: with Margaret Hayes: monthly check-in call'
  - '1981-01-02: with Maxine Keating: clashed on the set of ''Wild Trouble'' (pressure from a slipping schedule
    boiled over)'
  - '1981-01-09: with John Altman: clashed on the set of ''Wild Trouble'' (a clash of two volatile temperaments)'
narrative_canon:
- '1980-01-04: Margaret takes calls standing at her office window on Wilshire and calls Daniel "kiddo" when she
  is about to give bad news.'
- '1980-01-04: Daniel rents a bungalow in Los Feliz with a lemon tree he never waters.'
- '1980-07-25: Bruce Beresford shoots the hacker-lab scenes in long unbroken takes and asks Daniel to keep Leon''s
  hands busy with a soldering iron.'
- '1980-08-22: Daniel writes the first pages of The Long Field longhand in a Big Chief tablet at the craft-services
  table between setups.'
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
reply_to: pkt-00017
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
