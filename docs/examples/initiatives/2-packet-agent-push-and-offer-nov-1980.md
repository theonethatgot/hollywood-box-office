# Narrator packet pkt-00014 — 1980-11-07

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
packet: pkt-00014
date: '1980-11-07'
covers: 1980-10-10 .. 1980-11-07
state_hash: 230f772c0f9cb1fd
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
    cash: 118039.0
    monthly_costs: 6000.0
  energy: fine
  relationship_status: single
  awards: []
canon:
- id: ev-3836
  date: '1980-10-10'
  text: 'Tension on the set of ''Signal of the Dawn'': you clashed with Hal Keating (a clash of two volatile temperaments).'
- id: ev-3837
  date: '1980-10-10'
  text: 'Tension on the set of ''Signal of the Dawn'': you clashed with Alan Okonkwo (exhaustion after long days).'
- id: ev-3938
  date: '1980-10-17'
  text: 'Margaret Hayes pushed for you on Luis (colead) in ''Endless Promise'' (Metro-Goldwyn-Mayer, director Jack
    Smight) because you were just outside the casting director''s list; casting declined: they want a bigger name
    for this part.'
- id: ev-3939
  date: '1980-10-17'
  text: Your agent got you a read for a grieving widower on 'Fifth Street' (CBS), casting Margaret Merrick.
- id: ev-3940
  date: '1980-10-17'
  text: 'You read for a grieving widower on ''Fifth Street'' (CBS) (an episode about a talent show gone wrong) and
    were not picked; casting: Margaret Merrick.'
- id: ev-3941
  date: '1980-10-17'
  text: 'Feedback on ''Fifth Street'' (CBS) (via your agent): they liked the read but wanted someone with more screen
    presence.'
- id: ev-3955
  date: '1980-10-17'
  text: 'Payment received: second half of fee for ''Signal of the Dawn'' — $50k gross, $27k after commission and
    tax.'
- id: ev-3956
  date: '1980-10-17'
  text: '''Signal of the Dawn'' wrapped principal photography and moved into post-production.'
  provenance: simulated event in this timeline
- id: ev-3968
  date: '1980-10-17'
  text: The draft of 'The Long Field' arrived; you love it.
- id: ev-4039
  date: '1980-10-24'
  text: 'Your agent got you in the room: Dean Wyatt in ''Wild Trouble'' (casting: Neil Burke) — the casting director
    liked your submission.'
- id: ev-4040
  date: '1980-10-24'
  text: 'Audition booked: Dean Wyatt in ''Wild Trouble'' on 1980-10-31.'
- id: ev-4042
  date: '1980-10-24'
  text: Your agent got you a read for a nervous bank teller on 'Maple Street' (CBS), casting Bruce Malone.
- id: ev-4043
  date: '1980-10-24'
  text: 'You read for a nervous bank teller on ''Maple Street'' (CBS) (an episode about a lottery ticket that might
    be a winner) and were not picked; casting: Bruce Malone.'
- id: ev-4044
  date: '1980-10-24'
  text: 'Feedback on ''Maple Street'' (CBS) (via your agent): they liked the read but wanted someone with more screen
    presence.'
- id: ev-4045
  date: '1980-10-24'
  text: Your agent got you a read for a hotshot lawyer on 'Mountain Run' (PBS), casting Margaret Merrick.
- id: ev-4046
  date: '1980-10-24'
  text: 'You read for a hotshot lawyer on ''Mountain Run'' (PBS) (an episode about a mountain avalanche) and were
    not picked; casting: Margaret Merrick.'
- id: ev-4047
  date: '1980-10-24'
  text: 'Feedback on ''Mountain Run'' (PBS) (via your agent): they liked the read but wanted someone with more screen
    presence.'
- id: ev-4048
  date: '1980-10-24'
  text: Your agent got you a read for a young doctor on 'Mountain Run' (PBS), casting Margaret Merrick.
- id: ev-4049
  date: '1980-10-24'
  text: 'You read for a young doctor on ''Mountain Run'' (PBS) (an episode about a sabotaged oil rig) and booked
    it; casting: Margaret Merrick.'
- id: ev-4050
  date: '1980-10-24'
  text: Booked a guest role on 'Mountain Run' (PBS); playing Keith Underwood, a young doctor; an episode about a
    sabotaged oil rig; directed by Scott Fielding; with Monty Coleman, Carmen Lindgren (1980-11-07 to 1980-11-14,
    $6k).
- id: ev-4104
  date: '1980-10-31'
  text: You auditioned for Dean Wyatt in 'Wild Trouble' and won the part.
- id: ev-4105
  date: '1980-10-31'
  text: 'Others seen for Dean Wyatt: Curtis Nash, Don Johnson, James Hudson.'
  provenance: simulated event in this timeline
- id: ev-4106
  date: '1980-10-31'
  text: 'Offer (after auditions): Dean Wyatt, supporting in ''Wild Trouble'' — A stuffy accountant inherits a failing
    nightclub and everything goes wrong. Buena Vista (Disney), dir. Michael Nankin. Terms $99k. Shoots 1980-12-19
    to 1981-02-20 (Los Angeles).'
- id: ev-4161
  date: '1980-10-31'
  text: 'Pitched ''The Long Field'' to Columbia Pictures: Columbia Pictures passed.'
period_summary:
  overview: 4 week(s), working on 1 job(s), 18 submission(s) by your agent, 5 call-in(s), 5 audition(s), 1 booking(s);
    net money +$27k.
  working:
  - 'tv guest: Mountain Run (1980-11-07 to 1980-11-14)'
  quiet_period: false
  note: ''
rulings:
- proposal: dec-00003
  type: decision
  result: applied
  text: You kept things professional with Gail Tierney.
delegated:
- Your agent booked you an audition for Dean Wyatt in 'Wild Trouble' on 1980-10-31.
- 'Margaret Hayes booked you: a guest role on ''Mountain Run'' (PBS); playing Keith Underwood, a young doctor; an
  episode about a sabotaged oil rig; directed by Scott Fielding; with Monty Coleman, Carmen Lindgren — 1980-11-07
  to 1980-11-14, paying $6k.'
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
  - '1980-10-31: You auditioned for Dean Wyatt in ''Wild Trouble'' and won the part.'
agent:
  agent: Margaret Hayes (agent at Starling-Barr Talent (fictional))
  strategy: Pursuing respected directors and serious dramatic material and interesting scripts, stage work and character
    parts, even for less money; not prioritising steady bookings and series work over long shots.
  attention: 'Margaret Hayes represents 67 actors and you are mid-list. Calls are limited: they push when you just
    miss a casting director''s list on a part worth it, or when a director already rates you'
  your_directives:
    avoid_genres:
    - horror
    no_commercials: true
  pushes_this_period:
  - '1980-10-17: pushed for Luis (colead) in ''Endless Promise'' — declined: they want a bigger name for this part'
initiatives:
- id: ini-00002
  kind: develop_project
  status: pitching
  started: '1980-08-22'
  history:
  - '1980-08-22: Hired screenwriter Ellen Lindqvist ($17k); first draft due about 1980-10-17.'
  - '1980-10-17: Ellen Lindqvist delivered the draft of ''The Long Field''; you love it.'
  - '1980-10-31: Columbia Pictures passed.'
  next_step_due: '1980-11-14'
career_activity:
  submissions:
  - '1980-10-24: Richard Calloway (colead) in ''Wild Trouble'' (Buena Vista (Disney), casting Neil Burke) — passed:
    they want a bigger name for this part'
  - '1980-10-24: Dean Wyatt (supporting) in ''Wild Trouble'' (Buena Vista (Disney), casting Neil Burke) — called
    in: the casting director liked your submission'
  - '1980-10-24: an old friend of the lead (guest) in ''Highway Force West'' (ABC, casting Randy Moreno) — passed:
    they had plenty of strong submissions'
  - '1980-10-24: a nervous bank teller (guest) in ''Maple Street'' (CBS, casting Bruce Malone) — requested: the
    show''s casting director wanted to see you'
  - '1980-10-24: a hotshot lawyer (guest) in ''Mountain Run'' (PBS, casting Margaret Merrick) — called in: the show''s
    casting director wanted to see you'
  - '1980-10-24: a young doctor (guest) in ''Mountain Run'' (PBS, casting Margaret Merrick) — called in: the show''s
    casting director wanted to see you'
  - '1980-10-31: Victor Malone (supporting) in ''Witness of the Heart'' (Orion Pictures, casting Lori Wade) — passed:
    they didn''t see you as a drama type'
  - '1980-10-31: Trevor Walsh (featured) in ''Witness of the Heart'' (Orion Pictures, casting Lori Wade) — passed:
    the part pays well below your quote'
  - '1980-10-31: Max (featured) in ''Witness of the Heart'' (Orion Pictures, casting Lori Wade) — passed: the part
    pays well below your quote'
  - '1980-10-31: Brian Petrakis (lead) in ''Cold Agenda'' (Universal Pictures, casting Gloria Maddox) — passed:
    they went with other actors'
  auditions:
  - '1980-10-24: Your agent got you a read for a nervous bank teller on ''Maple Street'' (CBS), casting Bruce Malone.'
  - '1980-10-24: You read for a nervous bank teller on ''Maple Street'' (CBS) (an episode about a lottery ticket
    that might be a winner) and were not picked; casting: Bruce Malone.'
  - '1980-10-24: Your agent got you a read for a hotshot lawyer on ''Mountain Run'' (PBS), casting Margaret Merrick.'
  - '1980-10-24: You read for a hotshot lawyer on ''Mountain Run'' (PBS) (an episode about a mountain avalanche)
    and were not picked; casting: Margaret Merrick.'
  - '1980-10-24: Your agent got you a read for a young doctor on ''Mountain Run'' (PBS), casting Margaret Merrick.'
  - '1980-10-24: You read for a young doctor on ''Mountain Run'' (PBS) (an episode about a sabotaged oil rig) and
    booked it; casting: Margaret Merrick.'
  - '1980-10-31: You auditioned for Dean Wyatt in ''Wild Trouble'' and won the part.'
  - '1980-10-31: Others seen for Dean Wyatt: Curtis Nash, Don Johnson, James Hudson.'
  bookings:
  - '1980-11-07 to 1980-11-14: a guest role on ''Mountain Run'' (PBS); playing Keith Underwood, a young doctor;
    an episode about a sabotaged oil rig; directed by Scott Fielding; with Monty Coleman, Carmen Lindgren ($6k)'
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
- title: Mountain Run
  kind: tv guest
  status: under way
  dates: 1980-11-07 to 1980-11-14
  details: a guest role on 'Mountain Run' (PBS); playing Keith Underwood, a young doctor; an episode about a sabotaged
    oil rig; directed by Scott Fielding; with Monty Coleman, Carmen Lindgren
  pay: $6k
  format: hour-long action-adventure
network:
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
- name: Margaret Merrick
  id: gen-ca-ind-5
  who: independent casting director
  how_you_know_them: read for a guest part on 'Paradise Estate' (ABC)
  standing: friendly
  last_interaction: read for a guest part on 'Mountain Run' (PBS) (1980-10-24)
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
- name: Margaret Hayes
  id: gen-ag-ag-sb-1
  who: agent at Starling-Barr Talent (fictional)
  how_you_know_them: monthly check-in call
  standing: cordial
  last_interaction: monthly check-in call (1980-10-03)
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
- name: Donna Barrett
  id: gen-ca-st-wb-1
  who: casting director at Warner Bros.
  how_you_know_them: a solid audition for 'Great Adventure'
  standing: cordial
  last_interaction: a solid audition for 'Great Adventure' (1980-09-26)
- name: Calvin Boyd
  id: gen-d-00012
  who: director
  how_you_know_them: a solid audition for 'Great Adventure'
  standing: cordial
  last_interaction: a solid audition for 'Great Adventure' (1980-09-26)
- name: Elizabeth Taylor
  id: wd:Q34851
  who: actor
  how_you_know_them: clashed on the set of 'Signal of the Dawn' (a disagreement that got heated)
  standing: cordial
  last_interaction: clashed on the set of 'Signal of the Dawn' (a disagreement that got heated) (1980-09-19)
- name: Lori Winslow
  id: gen-ca-st-col-0
  who: casting director at Columbia Pictures
  how_you_know_them: a strong audition for 'Signal of the Dawn'
  standing: cordial
  last_interaction: a solid audition for 'The Endless Kiss' (1980-09-05)
- name: Elliot Stanton
  id: gen-d-tv-28-0
  who: director
  how_you_know_them: a solid audition for 'The Endless Kiss'
  standing: cordial
  last_interaction: a solid audition for 'The Endless Kiss' (1980-09-05)
- name: Lisa Jameson
  id: gen-ca-st-mgm-1
  who: casting director at Metro-Goldwyn-Mayer
  how_you_know_them: a strong audition for 'Oakley's Signal'
  standing: cordial
  last_interaction: a strong audition for 'Oakley's Signal' (1980-09-05)
open_threads:
- 'Decision waiting: Offer (after auditions): Dean Wyatt, supporting in ''Wild Trouble'' — A stuffy accountant inherits
  a failing nightclub and everything goes wrong. Buena Vista (Disney), dir. Michael Nankin. Terms $99k. Shoots 1980-12-19
  to 1981-02-20 (Los Angeles). (by 1980-11-10)'
- '''Signal of the Dawn'' is in post'
- 'Career goal: you want serious, respected work that gets noticed at awards time. So far in 1980: 71 submissions,
  18 call-ins, 1 film role(s) booked.'
- 'Relationship in motion with Timothy Yates: a strong audition for ''Affair of the Deep'''
- 'Relationship in motion with Hal Keating: clashed on the set of ''Signal of the Dawn'' (a clash of two volatile
  temperaments)'
- 'Relationship in motion with Alan Okonkwo: clashed on the set of ''Signal of the Dawn'' (exhaustion after long
  days)'
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
    - monthly check-in call (1980-07-04)
    - monthly check-in call (1980-08-01)
    - monthly check-in call (1980-09-05)
    - monthly check-in call (1980-10-03)
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
  - '''Highway Force'' (1980, guest; this timeline)'
  - '''Metro Precinct'' (1980, guest; this timeline)'
  - '''Signal of the Dawn'' (1980, lead; this timeline)'
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
  - '''a national commercial for a shampoo'' (1980, commercial; this timeline)'
  - '''Downtown Beat'' (1980, guest; this timeline)'
  - '''Signal of the Dawn'' (1980, colead; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history: []
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
  - '''Santos Investigations'' (1980, guest; this timeline)'
  - '''Signal of the Dawn'' (1980, supporting; this timeline)'
  - '''The Devil and Max Devlin'' (1980, film_bit; this timeline)'
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
- why_here: directing 'Wild Trouble', which a pending decision is about
  id: wd:Q6833019
  name: Michael Nankin
  age: 24
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
- why_here: already cast in 'Wild Trouble', which a pending decision is about
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
  - '''a national commercial for an airline'' (1980, commercial; this timeline)'
  - '''Hot Wedding'' (1980, colead; this timeline)'
  - '''Wild Trouble'' (1981, lead; this timeline)'
  relationship_status: single
  lately:
  - '1980-08-08: Maxine Keating was cast as Bianca (colead) in ''Hot Wedding'' (Columbia Pictures).'
  - '1980-10-24: Maxine Keating was cast as Teresa Yates (lead) in ''Wild Trouble'' (Buena Vista (Disney)).'
- why_here: already cast in 'Wild Trouble', which a pending decision is about
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
  lately:
  - '1980-10-31: Glenn Anderson was cast as Richard Calloway (colead) in ''Wild Trouble'' (Buena Vista (Disney)).'
- why_here: already cast in 'Wild Trouble', which a pending decision is about
  id: gen-a-00619
  name: Ingrid Emerson
  age: 62
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in comedy and family
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
  - '''Silver Landing'' (1980, guest; this timeline)'
  - '''Much Ado About Nothing'' (1980, stage; this timeline)'
  - '''Wild Trouble'' (1981, supporting; this timeline)'
  relationship_status: single
- why_here: already cast in 'Wild Trouble', which a pending decision is about
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
  - '''Uncle Vanya'' (1980, stage; this timeline)'
  - '''The Cherry Orchard'' (1980, stage; this timeline)'
  - '''Wild Trouble'' (1981, featured; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
- why_here: already cast in 'Wild Trouble', which a pending decision is about
  id: wd:Q6795996
  name: Maxine Stuart
  age: 62
  profession: actor
  public_profile: unknown to the public
  reputation: working actor in comedy and drama
  traits:
  - unhurried about fame
  - charming
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: American actress (born 1918); known for 'The Prisoner of Second Avenue' (1975).
  recent_work:
  - '''Tomorrow''s Child'' (1981, featured; this timeline)'
  - '''Shock Treatment'' (1981, featured; this timeline)'
  - '''Wild Trouble'' (1981, featured; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
- why_here: already cast in 'Wild Trouble', which a pending decision is about
  id: wd:Q259446
  name: Katy Jurado
  age: 56
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in comedy and drama
  traits:
  - generous with colleagues
  motivation: driven mostly by challenging, meaningful work, and also by respect and awards
  ambition: wants challenging material over safe paychecks
  bio: Mexican actress (born 1924); known for 'The Children of Sanchez' (1978); Academy Award nominee.
  recent_work:
  - '''Maniac'' (1980, film_bit; this timeline)'
  - '''Arms and the Man'' (1980, stage; this timeline)'
  - '''Wild Trouble'' (1981, featured; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
- why_here: already cast in 'Wild Trouble', which a pending decision is about
  id: wd:Q320036
  name: Richard Widmark
  age: 65
  profession: actor
  public_profile: a recognisable face
  reputation: character actor in action and comedy
  traits:
  - drawn to risky material
  motivation: driven mostly by fame and visibility, and also by respect and awards
  ambition: wants a breakout role and a recognisable name
  bio: American actor (born 1914); known for 'Coma' (1978); Academy Award nominee.
  recent_work:
  - '''The Seagull'' (1980, stage; this timeline)'
  - '''a national commercial for a long-distance phone company'' (1980, commercial; this timeline)'
  - '''Wild Trouble'' (1981, featured; this timeline)'
  relationship_status: married (spouse outside the film industry) (documented)
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
  lately:
  - '1980-10-31: Richard Widmark was cast as Jeffrey Emerson (featured) in ''Wild Trouble'' (Buena Vista (Disney)).'
- why_here: already cast in 'Wild Trouble', which a pending decision is about
  id: wd:Q632263
  name: David Opatoshu
  age: 62
  profession: actor
  public_profile: unknown to the public
  reputation: working actor in horror and comedy
  traits:
  - generous with colleagues
  - demanding
  - relentlessly prepared
  - hungry
  motivation: driven mostly by respect and awards, and also by challenging, meaningful work
  ambition: wants serious, respected work that gets noticed at awards time
  bio: 'American actor (born 1918); known for ''Ziegfeld: The Man and His Women'' (1978).'
  recent_work:
  - '''Beyond Evil'' (1980, featured; this timeline)'
  - '''Eyes of a Stranger'' (1981, featured; this timeline)'
  - '''Wild Trouble'' (1981, featured; this timeline)'
  relationship_status: single
  real_person: true
  note: Real person. Their career up to the start date is documented; their ambition is inferred from it; personality
    traits are simulation characterisation, not biography. Everything they do with you, and anything marked 'simulated',
    is this alternate timeline, not history.
industry:
  box_office_chart:
  - 1. 'Rough Cut' (Paramount Pictures) — $4.8M this week, $4.8M total, week 1
  - 2. 'Sunday Lovers' (United Artists) — $4.6M this week, $4.6M total, week 1
  - 3. 'Gloria' (Columbia Pictures) — $2.1M this week, $20.3M total, week 7
  - 4. 'When Time Ran Out' (Warner Bros.) — $2.1M this week, $20.3M total, week 8
  - 5. 'Private Benjamin' (Warner Bros.) — $2.0M this week, $11.4M total, week 4
  news:
  - date: '1980-10-31'
    text: Taylor Hackford will direct 'Quiet Letters' for Paramount Pictures.
    provenance: fictional production
  - date: '1980-10-31'
    text: Paramount Pictures greenlit 'Quiet Letters', a drama picture. An estranged daughter tries to rebuild a
      life after prison while the town turns against them.
  - date: '1980-10-31'
    text: Ivan Nagy will direct 'Cold Agenda' for Universal Pictures.
    provenance: fictional production
  - date: '1980-10-31'
    text: Universal Pictures greenlit 'Cold Agenda', a thriller picture. An insurance investigator uncovers a conspiracy
      inside a defence contractor before the story goes to print.
  - date: '1980-10-31'
    text: William Peter Blatty will direct 'Evilspeak' for Independent distributors.
    provenance: documented production
  - date: '1980-10-31'
    text: Andre Farrell turned down Ramon in 'The Long Witness'.
  - date: '1980-10-31'
    text: Rebecca Jameson was cast as Patricia Marchetti (supporting) in 'The Long Witness' (Paramount Pictures).
  - date: '1980-10-31'
    text: Meredith Lambert was cast as Joyce Moreno (lead) in 'Runaway Treasure' (Metro-Goldwyn-Mayer).
  - date: '1980-10-31'
    text: Jan-Michael Vincent was cast as Peter Drake (lead) in 'Witness of the Heart' (Orion Pictures).
    provenance: simulated casting in a fictional production
  - date: '1980-10-31'
    text: 'Reviews for ''Sunday Lovers'': rapturous (critics'' aggregate 89/100); opening-night audiences gave it
      a B.'
    provenance: simulated event in this timeline
  - date: '1980-10-31'
    text: 'Reviews for ''Rough Cut'': mixed (critics'' aggregate 54/100); opening-night audiences gave it an A-.'
    provenance: simulated event in this timeline
  - date: '1980-10-31'
    text: '''Ruckus'' finished its theatrical run with $1.0M domestic and an estimated $628k overseas.'
    provenance: simulated event in this timeline
  - date: '1980-10-31'
    text: '''Doctor Franken'' finished its theatrical run with $2.0M domestic and an estimated $1.3M overseas.'
    provenance: simulated event in this timeline
  - date: '1980-10-31'
    text: '''The Happy Hooker Goes Hollywood'' finished its theatrical run with $2.3M domestic and an estimated
      $1.5M overseas.'
    provenance: simulated event in this timeline
pending_decisions:
- id: dec-00004
  kind: offer
  summary: 'Offer (after auditions): Dean Wyatt, supporting in ''Wild Trouble'' — A stuffy accountant inherits a
    failing nightclub and everything goes wrong. Buena Vista (Disney), dir. Michael Nankin. Terms $99k. Shoots 1980-12-19
    to 1981-02-20 (Los Angeles).'
  options:
  - accept
  - decline
  - counter(fee)
  deadline: '1980-11-10'
  if_unanswered: decline
  story_preview:
    provenance: simulated screenplay for a fictional production
    logline: 'A screwball comedy: A stuffy accountant inherits a failing nightclub and everything goes wrong.'
    central_conflict: Teresa Yates's simple plan spirals out of control, and Richard Calloway keeps making it worse
      and funnier
    your_key_scenes:
    - a late-night confrontation in a kitchen
    - an argument in a moving car
    your_read_of_the_script: you think it's solid; the central relationship works, though parts feel familiar (your
      impression; it may be wrong)
    your_character: 'Dean Wyatt (the nosy neighbour): wants to keep a promise; flaw: drinking; arc from drinking
      toward a reckoning with courage'
  context: Your quote is $99k. Countering risks the studio walking away.
continuity:
  career_so_far:
  - '1973: ''Crazy Vacation'' (supporting)'
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
  initiatives_resolved:
  - '1980-07-25 meet: Meeting requested with Sydney Pollack. -> Met Sydney Pollack.'
  earlier_key_moments:
  - '1980-05-30: You auditioned for Barry Farrell in ''Zorro, The Gay Blade'' and made the final two.'
  - '1980-06-27: Principal photography began on ''Signal of the Dawn'' in Los Angeles (16 weeks scheduled).'
  - '1980-08-01: You met with Sydney Pollack (general meeting: Daniel wants to be on his radar for serious dramatic
    work).'
  - '1980-08-22: You hired Ellen Lindqvist to write ''The Long Field'' ($17k).'
  - '1980-08-29: Audition: Daniel Delgado, the lead role in ''Oakley''s Signal'' (scifi, Metro-Goldwyn-Mayer; director
    Gilbert Moses; casting Lisa Jameson) on 1980-09-05. Premise: A disillusioned astronaut discovers the company
    has lied about the mission as the station fails.'
  - '1980-09-05: You auditioned for Dennis Duncan in ''The Endless Kiss'' and did not get a callback.'
  - '1980-09-05: You auditioned for Daniel Delgado in ''Oakley''s Signal'' and did not get a callback.'
  - '1980-09-19: Tension on the set of ''Signal of the Dawn'': you clashed with Elizabeth Taylor (a disagreement
    that got heated).'
  - '1980-09-26: You auditioned for Wesley Conway in ''Great Adventure'' and did not get a callback.'
  - '1980-10-03: You auditioned for John Irving in ''Affair of the Deep'' and did not get a callback.'
  - '1980-10-03: There is an unmistakable spark between you and Gail Tierney on the set of ''Signal of the Dawn''.'
  - '1980-10-03: Chemistry with Gail Tierney: pursue something, or keep it professional?'
  recent_scenes_and_threads:
  - '1980-09-26: with Donna Barrett: a solid audition for ''Great Adventure'''
  - '1980-10-03: with Lori Wade: a strong audition for ''Affair of the Deep'''
  - '1980-10-03: with Margaret Hayes: monthly check-in call'
  - '1980-10-03: with Timothy Yates: a strong audition for ''Affair of the Deep'''
  - '1980-10-10: with Alan Okonkwo: clashed on the set of ''Signal of the Dawn'' (exhaustion after long days)'
  - '1980-10-10: with Hal Keating: clashed on the set of ''Signal of the Dawn'' (a clash of two volatile temperaments)'
  - '1980-10-17: with Margaret Merrick: read for a guest part on ''Fifth Street'' (CBS)'
  - '1980-10-24: with Bruce Malone: read for a guest part on ''Maple Street'' (CBS)'
  - '1980-10-24: with Margaret Merrick: read for a guest part on ''Mountain Run'' (PBS)'
  - '1980-10-24: with Margaret Merrick: read for a guest part on ''Mountain Run'' (PBS)'
  - '1980-10-31: with Michael Nankin: a strong audition for ''Wild Trouble'''
  - '1980-10-31: with Neil Burke: a strong audition for ''Wild Trouble'''
narrative_canon:
- '1980-01-04: Margaret takes calls standing at her office window on Wilshire and calls Daniel "kiddo" when she
  is about to give bad news.'
- '1980-01-04: Daniel rents a bungalow in Los Feliz with a lemon tree he never waters.'
- '1980-07-25: Bruce Beresford shoots the hacker-lab scenes in long unbroken takes and asks Daniel to keep Leon''s
  hands busy with a soldering iron.'
- '1980-08-22: Daniel writes the first pages of The Long Field longhand in a Big Chief tablet at the craft-services
  table between setups.'
era:
  year: 1980
  average_ticket_price: $2.69
  note: The blockbuster era is a few years old; theatrical release dominates and home video is small but growing
    fast.
narrator_notes: []
```

## REPLY FORMAT
End your reply with exactly one block like this:

```engine
reply_to: pkt-00014
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
