"""Name and text generators for fictional professionals and projects.

Generated names are era-flavoured but fictional. Collisions with real people
are possible and harmless (generated people are tagged tier G).
"""
from __future__ import annotations

FIRST_M = """James John Robert Michael William David Richard Thomas Charles Daniel Mark
Paul Steven Kevin Brian Gary Jeffrey Scott Timothy Larry Dennis Douglas Gregory Kenneth
Ronald Anthony Donald Peter Frank Raymond Jerry Bruce Wayne Randy Roger Terry Craig Keith
Alan Barry Glenn Dale Russell Vincent Philip Curtis Leon Victor Marcus Elliot Nathan Dean
Malcolm Wesley Calvin Howard Neil Rick Stuart Trevor Clark Gordon Mitchell Lionel Desmond
Reggie Joel Max Toby Hal Rex Monty Walt Ellis Jasper Felix Gil Luis Carlos Ramon Andre""".split()

FIRST_F = """Mary Linda Patricia Susan Deborah Barbara Karen Nancy Donna Cynthia Sandra Pamela
Sharon Kathleen Carol Diane Brenda Laura Janet Elizabeth Julie Lisa Kim Cheryl Teresa Denise
Joyce Gail Rebecca Wendy Connie Paula Dana Robin Jill Lori Tina Leslie Valerie Joan Gloria
Rachel Sarah Margaret Diana Ellen Holly Meredith Joanna Natalie Vanessa Claudia Rita Stella
Anita Monica Celia Ingrid Lena Nora Vera June Faye Daphne Greta Ivy Maxine Rosalind Lorraine
Theresa Yvonne Jeanette Marisol Elena Carmen Lucia Simone Bianca""".split()

LAST = """Anderson Baker Barrett Bishop Blake Boyd Brennan Brooks Burke Calloway Cameron Carver
Chandler Clayton Coleman Conway Corbin Crane Dalton Dawson Delaney Donovan Drake Duncan Ellison
Emerson Farrell Fielding Fletcher Flynn Foster Gallagher Garrison Gilmore Granger Hale Halloran
Hammond Harlow Harper Hastings Hayes Holloway Hudson Irving Jameson Keating Kendall Kessler Lambert
Langley Lawson Lennox Lowell Maddox Malone Mercer Merrick Monroe Morrow Nash Nolan Oakley Palmer
Pierce Porter Quinlan Radford Ramsey Reardon Reeves Rhodes Riordan Rowan Sawyer Sheridan Shaw
Sinclair Slater Stanton Sterling Sullivan Talbot Thorne Tierney Underwood Vance Vaughn Wade
Walsh Warner Whitaker Winslow Wolcott Wyatt Yates Kowalski Moreno Castillo Delgado Okafor
Nakamura Petrakis Rossi Abernathy Lindqvist Marchetti Szabo Lindgren Okonkwo Brandt Hollis""".split()

TRAITS = {
    "temperament": (["even-keeled", "unflappable"], ["volatile", "quick-tempered"]),
    "warmth": (["guarded", "aloof"], ["warm", "generous with colleagues"]),
    "ego": (["self-effacing", "low-key"], ["vain", "demanding"]),
    "discipline": (["undisciplined", "chronically late"], ["meticulous", "relentlessly prepared"]),
    "ambition": (["unhurried about fame"], ["fiercely ambitious", "hungry"]),
    "risk": (["cautious with choices"], ["drawn to risky material"]),
    "openness": (["private", "hard to read"], ["charming", "outgoing"]),
}

TITLE_WORDS = {
    "drama": (["Quiet", "Distant", "Last", "Broken", "Long", "Winter", "Silent", "Second"],
              ["Harbor", "Season", "Promise", "Country", "Witness", "Inheritance", "Bridges", "Letters"]),
    "comedy": (["Big", "Crazy", "Wild", "Lucky", "Double", "Weekend", "Hot", "Rented"],
               ["Trouble", "Getaway", "Business", "Neighbors", "Wedding", "Shift", "Vacation", "Scheme"]),
    "action": (["Steel", "Dead", "Iron", "Midnight", "Red", "Fast", "Hard", "Thunder"],
               ["Justice", "Run", "Target", "Force", "Crossing", "Line", "Strike", "Pursuit"]),
    "romance": (["Summer", "Endless", "Paris", "First", "Golden", "Tender", "Lonely", "Moonlit"],
                ["Affair", "Hearts", "Kiss", "Dance", "Promise", "Embrace", "Hours", "Season"]),
    "thriller": (["Cold", "Hidden", "Black", "Night", "Silent", "Final", "Blind", "Glass"],
                 ["Witness", "Agenda", "Signal", "Contact", "Exposure", "Circle", "Motive", "Room"]),
    "horror": (["Dark", "Blood", "Hollow", "Grave", "Shadow", "Hungry", "Pale", "Crawling"],
               ["House", "Harvest", "Woods", "Night", "Cellar", "Lake", "Ritual", "Visitors"]),
    "family": (["Magic", "Little", "Great", "Secret", "Runaway", "Brave", "Lost", "Flying"],
               ["Pony", "Treasure", "Adventure", "Summer", "Island", "Friends", "Dog", "Kingdom"]),
    "scifi": (["Star", "Outer", "Dark", "Final", "Quantum", "Solar", "Lost", "Alien"],
              ["Frontier", "Colony", "Signal", "Horizon", "Voyager", "Machine", "Orbit", "Station"]),
}

TITLE_NOUNS = ["Night", "Wolves", "Damned", "Deep", "Storm", "Lost", "Heart", "Dawn", "Gods", "Brave", "Fallen", "City"]
PLACES = ["Midnight", "Dawn", "Sundown", "Crystal Lake", "Eagle Pass", "Gallows Hill", "Coney Island", "Big Sur"]
SINGLE_TITLES = {
    "drama": ["Homecoming", "Inheritance", "Testament", "Reckoning", "Tidewater", "Hometown", "Wildflower"],
    "comedy": ["Hijinks", "Moonlighting", "Showoffs", "Bachelors", "Slapshot Sally", "Loose Change", "Jackpot"],
    "action": ["Outlaw", "Firestorm", "Vendetta", "Hardcase", "Overdrive", "Payback", "Crossfire"],
    "romance": ["Rendezvous", "Moonstruck Summer", "Serenade", "Sweethearts", "Daydream", "Paramour"],
    "thriller": ["Blackout", "Surveillance", "Undertow", "Cold Trail", "Fever Pitch", "Static", "Witness Box"],
    "horror": ["Nightcrawler", "Bloodline", "Hellbound", "The Hollow", "Scarecrow", "Eclipse", "The Pact"],
    "family": ["Bandit", "Skyhook", "Pip and the Pirates", "The Wishing Well", "Buckaroo", "Moonbeam"],
    "scifi": ["Starfall", "Outland Station", "Cryo", "Terminus", "Nova", "Exodus 9", "Zero Gravity"],
}

PREMISE = {
    "drama": (["a widowed steelworker", "an estranged daughter", "a small-town lawyer", "a fading jazz pianist",
               "two brothers", "a Vietnam veteran", "a single mother", "an ageing boxer"],
              ["returns home to settle a family debt", "takes on a case no one else will touch",
               "tries to rebuild a life after prison", "fights to keep the family farm",
               "confronts the secret that split the family"],
              ["as an old rivalry reopens", "while the town turns against them", "before time runs out",
               "with nothing left to lose"]),
    "comedy": (["a hapless car salesman", "two mismatched roommates", "a stuffy accountant",
                "a summer-camp counsellor", "a down-on-his-luck comic", "three college friends"],
               ["poses as a millionaire for a weekend", "has to host the boss for dinner",
                "accidentally wins a radio contest", "inherits a failing nightclub",
                "gets mistaken for a famous spy"],
               ["and everything goes wrong", "with the whole neighbourhood watching",
                "the week before the wedding", "in the middle of a heatwave"]),
    "action": (["a burned-out cop", "an ex-Marine", "a getaway driver", "a federal marshal",
                "a mercenary with a conscience"],
               ["hunts the gang that killed his partner", "must escort a witness across the border",
                "is framed for a heist he tried to stop", "takes on a corrupt sheriff"],
               ["in a city on the edge", "with forty-eight hours to clear his name",
                "while the clock runs down", "against impossible odds"]),
    "romance": (["a struggling painter", "a by-the-book architect", "a touring folk singer",
                 "a young widow", "a hotel concierge"],
                ["falls for a stranger she meets on a train", "rekindles a romance with a first love",
                 "is torn between two very different men", "must choose between love and a career"],
                ["one summer on the coast", "in late-seventies New York", "against her family's wishes",
                 "as the season ends"]),
    "thriller": (["an investigative reporter", "a night-shift nurse", "a wiretap technician",
                  "a junior senator's aide", "an insurance investigator"],
                 ["uncovers a conspiracy inside a defence contractor", "becomes the only witness to a murder",
                  "realises a client is not who he says", "starts receiving calls from a dead man"],
                 ["and no one believes her", "as the killer closes in", "with powerful people watching",
                  "before the story goes to print"]),
    "horror": (["a group of camp counsellors", "a young family", "five college friends",
                "a small-town sheriff", "a babysitter"],
               ["move into a house with a dark history", "are stalked by a masked killer",
                "awaken something beneath the lake", "are trapped in a snowed-in lodge"],
               ["on the anniversary of the murders", "one long night", "as the bodies pile up",
                "far from any help"]),
    "family": (["a lonely boy", "a stubborn grandfather", "two runaway sisters", "a clumsy inventor"],
               ["befriends a creature no one else can see", "sets out to find a lost treasure",
                "rescues a racehorse from the glue factory", "builds a machine that changes everything"],
               ["over one magical summer", "before the bank takes the farm", "with the help of unlikely friends"]),
    "scifi": (["the crew of a mining ship", "a disillusioned astronaut", "a teenage hacker", "a colony doctor"],
              ["intercepts a signal from deep space", "discovers the company has lied about the mission",
               "wakes up decades after the launch", "must stop a rogue computer"],
              ["light years from home", "as the station fails", "before first contact turns to war"]),
}

ROLE_DESC = {
    "lead": "the protagonist; carries the film",
    "colead": "the second lead; a major arc opposite the protagonist",
    "supporting": "a key supporting part",
    "featured": "a smaller speaking part with a few scenes",
}
