# Narrator packet pkt-00009 — 1980-07-25

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
packet: pkt-00009
date: '1980-07-25'
covers: 1980-06-27 .. 1980-07-25
state_hash: 176c7f79a00584c9
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
    cash: 126605.0
    monthly_costs: 6000.0
  energy: fresh
  relationship_status: single
  awards: []
canon:
- id: ev-1724
  date: '1980-06-27'
  text: 'Payment received: first half of fee for ''Signal of the Dawn'' — $50k gross, $27k after commission and
    tax.'
- id: ev-1725
  date: '1980-06-27'
  text: Principal photography began on 'Signal of the Dawn' in Los Angeles (16 weeks scheduled).
  provenance: simulated event in this timeline
- id: ev-1958
  date: '1980-07-04'
  text: Margaret Hayes checked in; there was little in your range this month to submit you for; they want to get
    you seen in a respected stage production.
period_summary:
  overview: 4 week(s), working on 1 job(s), 0 submission(s) by your agent, 0 call-in(s), 0 audition(s), 0 booking(s);
    net money +$21k.
  working:
  - shooting 'Signal of the Dawn' (1980-06-27 to 1980-10-24)
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
  attention: 'Margaret Hayes represents 67 actors and you are mid-list. Calls are limited: they push when you just
    miss a casting director''s list on a part worth it, or when a director already rates you'
initiatives: []
career_activity:
  agent_calls:
  - '1980-07-04: Margaret Hayes checked in; there was little in your range this month to submit you for; they want
    to get you seen in a respected stage production.'
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
  stage: shooting
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
  shoot: 1980-06-27 to 1980-10-17
network:
- name: Margaret Hayes
  id: gen-ag-ag-sb-1
  who: agent at Starling-Barr Talent (fictional)
  how_you_know_them: monthly check-in call
  standing: cordial
  last_interaction: monthly check-in call (1980-07-04)
- name: Claudia Hudson
  id: gen-ca-st-fox-1
  who: casting director at 20th Century Fox
  how_you_know_them: a solid audition for 'Zorro, The Gay Blade'
  standing: cordial
  last_interaction: a solid audition for 'Zorro, The Gay Blade' (1980-05-30)
- name: Peter Medak
  id: wd:Q724100
  who: director
  how_you_know_them: a solid audition for 'Zorro, The Gay Blade'
  standing: cordial
  last_interaction: a solid audition for 'Zorro, The Gay Blade' (1980-05-30)
- name: Lori Winslow
  id: gen-ca-st-col-0
  who: casting director at Columbia Pictures
  how_you_know_them: a strong audition for 'Signal of the Dawn'
  standing: cordial
  last_interaction: a strong audition for 'Signal of the Dawn' (1980-05-23)
- name: Bruce Beresford
  id: wd:Q449220
  who: director
  how_you_know_them: a strong audition for 'Signal of the Dawn'
  standing: cordial
  last_interaction: a strong audition for 'Signal of the Dawn' (1980-05-23)
- name: Gloria Hudson
  id: gen-a-00145
  who: actor
  how_you_know_them: worked together on a guest role on 'Desert Rescue' (ABC)
  standing: cordial
  last_interaction: worked together on a guest role on 'Desert Rescue' (ABC) (1980-03-28)
- name: Wendy Okafor
  id: gen-a-00299
  who: actor
  how_you_know_them: worked together on a guest role on 'Desert Rescue' (ABC)
  standing: cordial
  last_interaction: worked together on a guest role on 'Desert Rescue' (ABC) (1980-03-28)
- name: June Carver
  id: gen-a-00022
  who: actor
  how_you_know_them: worked together on a guest role on 'Desert Rescue' (ABC)
  standing: cordial
  last_interaction: worked together on a guest role on 'Desert Rescue' (ABC) (1980-03-28)
- name: Malcolm Dawson
  id: gen-d-tv-0-2
  who: director
  how_you_know_them: worked together on a guest role on 'Desert Rescue' (ABC)
  standing: cordial
  last_interaction: worked together on a guest role on 'Desert Rescue' (ABC) (1980-03-28)
- name: Susan Kowalski
  id: gen-ca-ind-4
  who: independent casting director
  how_you_know_them: read for a guest part on 'Desert Rescue' (ABC)
  standing: cordial
  last_interaction: read for a guest part on 'Desert Rescue' (ABC) (1980-03-14)
- name: Raymond Warner
  id: gen-a-00118
  who: actor
  how_you_know_them: worked together on a guest role on 'Fifth Street' (CBS)
  standing: cordial
  last_interaction: worked together on a guest role on 'Fifth Street' (CBS) (1980-02-29)
- name: Tina Lawson
  id: gen-a-00225
  who: actor
  how_you_know_them: worked together on a guest role on 'Fifth Street' (CBS)
  standing: cordial
  last_interaction: worked together on a guest role on 'Fifth Street' (CBS) (1980-02-29)
- name: John Palmer
  id: gen-a-00495
  who: actor
  how_you_know_them: worked together on a guest role on 'Fifth Street' (CBS)
  standing: cordial
  last_interaction: worked together on a guest role on 'Fifth Street' (CBS) (1980-02-29)
- name: Reggie Flynn
  id: gen-d-tv-16-1
  who: director
  how_you_know_them: worked together on a guest role on 'Fifth Street' (CBS)
  standing: cordial
  last_interaction: worked together on a guest role on 'Fifth Street' (CBS) (1980-02-29)
- name: Margaret Merrick
  id: gen-ca-ind-5
  who: independent casting director
  how_you_know_them: read for a guest part on 'Paradise Estate' (ABC)
  standing: friendly
  last_interaction: read for a guest part on 'Fifth Street' (CBS) (1980-02-15)
open_threads:
- '''Signal of the Dawn'' is in shooting'
- 'Career goal: you want serious, respected work that gets noticed at awards time. So far in 1980: 39 submissions,
  9 call-ins, 1 film role(s) booked.'
people:
- why_here: your agent
  id: gen-ag-ag-sb-1
  name: Margaret Hayes
  age: 27
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
    - monthly check-in call (1980-04-04)
    - monthly check-in call (1980-05-02)
    - monthly check-in call (1980-06-06)
    - monthly check-in call (1980-07-04)
  narrative_canon:
  - '1980-01-04: Margaret takes calls standing at her office window on Wilshire and calls Daniel "kiddo" when she
    is about to give bad news.'
- why_here: directing your film 'Signal of the Dawn'
  id: wd:Q449220
  name: Bruce Beresford
  age: 39
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
  lately:
  - '1980-05-16: Bruce Beresford will direct ''Signal of the Dawn'' for Columbia Pictures.'
- why_here: in the cast of your film 'Signal of the Dawn' (lead)
  id: gen-a-00632
  name: Hal Keating
  age: 40
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
    history: []
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
  lately:
  - '1980-05-23: Natalie Rhodes was cast as Susan Wyatt (colead) in ''Signal of the Dawn'' (Columbia Pictures).'
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
    history: []
  lately:
  - '1980-05-23: Elizabeth Taylor was cast as Lena Tierney (supporting) in ''Signal of the Dawn'' (Columbia Pictures).'
- why_here: in this period's events (shoot start, 1980-06-27)
  id: gen-a-00005
  name: Alan Okonkwo
  age: 23
  profession: actor
  public_profile: unknown to the public
  reputation: working actor in scifi and action
  traits:
  - generous with colleagues
  - unhurried about fame
  - cautious with choices
  - charming
  motivation: driven mostly by challenging, meaningful work, and also by financial security and big paydays
  ambition: wants challenging material over safe paychecks
  bio: A newcomer still looking for a first real break; most at home in horror; generous with colleagues, unhurried
    about fame.
  persona:
    hometown: the San Fernando Valley
    signature: talks openly about wanting to direct
    background: a former dancer
  recent_work:
  - '''The Exterminator'' (1980, featured; this timeline)'
  - '''Battle Beyond the Stars'' (1980, featured; this timeline)'
  - '''Signal of the Dawn'' (1980, featured; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history: []
  lately:
  - '1980-07-04: Reviews for ''Somewhere in Time'': strong (critics'' aggregate 83/100); opening-night audiences
    gave it a B+.'
  - '1980-07-04: Reviews for ''The Exterminator'': savage (critics'' aggregate 28/100); opening-night audiences
    gave it an F.'
- why_here: in this period's events (shoot start, 1980-06-27)
  id: gen-a-00261
  name: Joyce Halloran
  age: 58
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in horror and scifi
  traits:
  - demanding
  - undisciplined
  - unhurried about fame
  - charming
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: A working actor with a steady run of supporting parts; most at home in comedy; demanding, undisciplined.
  persona:
    hometown: Toronto
    signature: never eats before a performance
    background: a stage actor from regional repertory theatre
  recent_work:
  - '''Dugan''s Street'' (1980, guest; this timeline)'
  - '''Dark Harvest'' (1980, film_bit; this timeline)'
  - '''Signal of the Dawn'' (1980, featured; this timeline)'
  relationship_status: married (spouse outside the film industry)
  with_you:
    standing: cordial
    status: acquainted
    history: []
- why_here: in this period's events (shoot start, 1980-06-27)
  id: gen-a-00376
  name: Barry Sinclair
  age: 26
  profession: actor
  public_profile: unknown to the public
  reputation: working actor in scifi and drama
  traits:
  - quick-tempered
  motivation: driven mostly by financial security and big paydays, and also by challenging, meaningful work
  ambition: wants bigger paydays and financial security
  bio: A newcomer still looking for a first real break; most at home in scifi; quick-tempered.
  persona:
    hometown: Boston
    signature: always first to arrive and last to leave
    background: came up through Chicago improv
  recent_work:
  - '''Long Country'' (1979, supporting; backstory)'
  - '''The Apple'' (1980, featured; this timeline)'
  - '''Signal of the Dawn'' (1980, featured; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history: []
- why_here: in this period's events (shoot start, 1980-06-27)
  id: gen-a-00479
  name: Rachel Thorne
  age: 47
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in scifi and drama
  traits:
  - drawn to risky material
  - hard to read
  motivation: driven mostly by respect and awards, and also by financial security and big paydays
  ambition: wants serious, respected work that gets noticed at awards time
  bio: A working actor with a steady run of supporting parts; most at home in family; drawn to risky material, hard
    to read.
  persona:
    hometown: Seattle
    signature: collects vintage cars
    background: a former child actor
    series: Paradise Ridge
  recent_work:
  - '''Distant Bridges'' (1964, supporting; backstory)'
  - '''Lost Colony'' (1967, supporting; backstory)'
  - '''Signal of the Dawn'' (1980, featured; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history: []
- why_here: in this period's events (shoot start, 1980-06-27)
  id: gen-a-00557
  name: Gail Tierney
  age: 30
  profession: actor
  public_profile: unknown to the public
  reputation: working actor in drama and scifi
  traits:
  - unflappable
  motivation: driven mostly by financial security and big paydays, and also by respect and awards
  ambition: wants bigger paydays and financial security
  bio: A newcomer still looking for a first real break; most at home in comedy; unflappable.
  persona:
    hometown: Boston
    signature: plays guitar in the trailer between setups
    background: came to acting from stand-up comedy
  recent_work:
  - '''Dakota Investigations'' (1980, guest; this timeline)'
  - '''Broken Inheritance at Gallows Hill'' (1980, featured; this timeline)'
  - '''Signal of the Dawn'' (1980, featured; this timeline)'
  relationship_status: single
  with_you:
    standing: cordial
    status: acquainted
    history: []
  lately:
  - '1980-06-20: ''Macabre'' finished its theatrical run with $929k domestic and an estimated $558k overseas.'
  - '1980-07-04: Reviews for ''Oh, God! Book II'': mixed-to-positive (critics'' aggregate 63/100); opening-night
    audiences gave it a C-.'
  - '1980-07-04: Reviews for ''On the Nickel'': poor (critics'' aggregate 33/100); opening-night audiences gave
    it an F.'
- why_here: in this period's events (shoot start, 1980-06-27)
  id: wd:Q2097213
  name: Carl Ballantine
  age: 62
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in comedy and family
  traits:
  - chronically late
  - unhurried about fame
  motivation: driven mostly by financial security and big paydays, and also by fame and visibility
  ambition: wants bigger paydays and financial security
  bio: American actor (born 1917); known for 'The World's Greatest Lover' (1977).
  recent_work:
  - '''Blood Beach'' (1980, film_bit; this timeline)'
  - '''a national commercial for a fast-food chain'' (1980, commercial; this timeline)'
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
  lately:
  - '1980-07-04: Reviews for ''American Pop'': rapturous (critics'' aggregate 89/100); opening-night audiences gave
    it a B+.'
- why_here: in this period's events (shoot start, 1980-06-27)
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
- why_here: in this period's events (shoot start, 1980-06-27)
  id: wd:Q433514
  name: Joanne Linville
  age: 52
  profession: actor
  public_profile: known mostly inside the industry
  reputation: working actor in romance and scifi
  traits: []
  motivation: driven mostly by financial security and big paydays, and also by a steady, sane life
  ambition: wants bigger paydays and financial security
  bio: American actress (born 1928); known for 'Gable and Lombard' (1976).
  recent_work:
  - '''Gable and Lombard'' (1976, supporting; documented)'
  - '''A Star Is Born'' (1976, supporting; documented)'
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
- why_here: in this period's events (shoot start, 1980-06-27)
  id: wd:Q464367
  name: Don Adams
  age: 57
  profession: actor
  public_profile: unknown to the public
  reputation: working actor in scifi and drama
  traits:
  - unhurried about fame
  motivation: driven mostly by respect and awards, and also by challenging, meaningful work
  ambition: wants serious, respected work that gets noticed at awards time
  bio: American actor (born 1923); award-nominated.
  recent_work:
  - '''Permanent Vacation'' (1980, featured; this timeline)'
  - '''The Nude Bomb'' (1980, lead; this timeline)'
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
  lately:
  - '1980-07-04: Reviews for ''Hangar 18'': mixed (critics'' aggregate 46/100); opening-night audiences gave it
    a D.'
  - '1980-07-04: Reviews for ''Permanent Vacation'': mixed (critics'' aggregate 57/100); opening-night audiences
    gave it a C.'
industry:
  box_office_chart:
  - 1. 'Brubaker' (20th Century Fox) — $5.1M this week, $16.9M total, week 3
  - 2. 'Heaven's Gate' (United Artists) — $4.2M this week, $14.6M total, week 3
  - 3. 'Somewhere in Time' (Universal Pictures) — $3.7M this week, $12.5M total, week 3
  - 4. 'The Kidnapping of the President' (Crown International Pictures) — $3.6M this week, $10.0M total, week 3
  - 5. 'Hero at Large' (United Artists) — $3.4M this week, $50.3M total, week 7
  news:
  - date: '1980-07-18'
    text: Jesse Vint will direct 'Shadow Ritual' for AVCO Embassy Pictures.
    provenance: fictional production
  - date: '1980-07-18'
    text: AVCO Embassy Pictures greenlit 'Shadow Ritual', a horror picture. A babysitter awakens something beneath
      the lake as the bodies pile up.
  - date: '1980-07-18'
    text: Carroll Ballard will direct 'Flying Island' for Columbia Pictures.
    provenance: fictional production
  - date: '1980-07-18'
    text: Columbia Pictures greenlit 'Flying Island', a family picture. A stubborn grandfather builds a machine
      that changes everything over one magical summer.
  - date: '1980-07-18'
    text: Dean Delgado will direct 'Summer Hours' for Universal Pictures.
  - date: '1980-07-18'
    text: Universal Pictures greenlit 'Summer Hours', a romance picture. A touring folk singer rekindles a romance
      with a first love against her family's wishes.
  - date: '1980-07-18'
    text: Sidney Poitier was cast as Daniel Irving (supporting) in 'Room of the Brave' (Columbia Pictures).
    provenance: simulated casting in a fictional production
  - date: '1980-07-18'
    text: Ben Johnson was cast as Philip Slater (supporting) in 'Room of the Brave' (Columbia Pictures).
    provenance: simulated casting in a fictional production
  - date: '1980-07-18'
    text: Dale Holloway was cast as Michael Moreno (supporting) in 'Room of the Brave' (Columbia Pictures).
  - date: '1980-07-18'
    text: 'Reviews for ''Defiance'': mixed (critics'' aggregate 48/100); opening-night audiences gave it an F.'
    provenance: simulated event in this timeline
  - date: '1980-07-18'
    text: 'Reviews for ''Honeysuckle Rose'': strong (critics'' aggregate 76/100); opening-night audiences gave it
      a B-.'
    provenance: simulated event in this timeline
  - date: '1980-07-18'
    text: Don "Red" Barry died.
    provenance: documented history
  - date: '1980-07-18'
    text: Carlos López Moctezuma died.
    provenance: documented history
  - date: '1980-07-18'
    text: Donna Summer married Bruce Sudano.
    provenance: documented history
pending_decisions: []
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
  initiatives_resolved: []
  earlier_key_moments:
  - '1980-01-04: Daniel Brooks begins their story in Hollywood.'
  - '1980-05-23: You auditioned for Leon in ''Signal of the Dawn'' and won the part.'
  - '1980-05-23: Offer (after auditions): Leon, supporting in ''Signal of the Dawn'' — A teenage hacker wakes up
    decades after the launch before first contact turns to war. Columbia Pictures, dir. Bruce Beresford. Terms $99k.
    Shoots 1980-06-27 to 1980-10-17 (Los Angeles).'
  - '1980-05-30: Daniel Brooks was cast as Leon (supporting) in ''Signal of the Dawn'' (Columbia Pictures).'
  - '1980-05-30: You auditioned for Barry Farrell in ''Zorro, The Gay Blade'' and made the final two.'
  recent_scenes_and_threads:
  - '1980-03-14: with Susan Kowalski: read for a guest part on ''Desert Rescue'' (ABC)'
  - '1980-03-28: with Gloria Hudson: worked together on a guest role on ''Desert Rescue'' (ABC)'
  - '1980-03-28: with June Carver: worked together on a guest role on ''Desert Rescue'' (ABC)'
  - '1980-03-28: with Malcolm Dawson: worked together on a guest role on ''Desert Rescue'' (ABC)'
  - '1980-03-28: with Wendy Okafor: worked together on a guest role on ''Desert Rescue'' (ABC)'
  - '1980-05-02: with Margaret Hayes: monthly check-in call'
  - '1980-05-23: with Bruce Beresford: a strong audition for ''Signal of the Dawn'''
  - '1980-05-23: with Lori Winslow: a strong audition for ''Signal of the Dawn'''
  - '1980-05-30: with Claudia Hudson: a solid audition for ''Zorro, The Gay Blade'''
  - '1980-05-30: with Peter Medak: a solid audition for ''Zorro, The Gay Blade'''
  - '1980-06-06: with Margaret Hayes: monthly check-in call'
  - '1980-07-04: with Margaret Hayes: monthly check-in call'
narrative_canon:
- '1980-01-04: Margaret takes calls standing at her office window on Wilshire and calls Daniel "kiddo" when she
  is about to give bad news.'
- '1980-01-04: Daniel rents a bungalow in Los Feliz with a lemon tree he never waters.'
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
reply_to: pkt-00009
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
