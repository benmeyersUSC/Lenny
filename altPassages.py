# ===========================================================================
# ALTERNATE PASSAGE SETS
# ===========================================================================
# Swap PASSAGE, SHARED_ANALYSIS, and FORKS to use one of these.
# Each set has orthogonal vocabulary across paragraphs.

PASSAGE_SET_1 = {
"passage": """Paragraph 1: The octopus is remarkable for its distributed nervous system. Nearly two-thirds of its neurons reside in its arms rather than its central brain. Each arm can taste, touch, and make basic decisions independently, creating what some biologists describe as a creature with nine semi-autonomous minds cooperating loosely.

Paragraph 2: The economy of Renaissance Florence was built on wool and banking. The Medici family rose to power not through military conquest but through financial innovation, particularly the invention of double-entry bookkeeping and the letra di cambio. Their wealth funded Brunelleschi, Botticelli, and Michelangelo.

Paragraph 3: Fermentation is a metabolic process in which microorganisms convert sugars into acids, gases, or alcohol in the absence of oxygen. Lactic acid fermentation preserves vegetables like kimchi and sauerkraut, while ethanol fermentation gives us bread, beer, and wine. The biochemistry is ancient, predating human civilization by billions of years.""",

"shared_analysis": """Let me analyze each paragraph in turn.

**Paragraph 1 — The Octopus Nervous System**
This paragraph highlights the radical decentralization of octopus cognition. The claim that two-thirds of neurons are in the arms rather than the brain challenges our vertebrate-centric assumption that intelligence requires centralized processing. The phrase "nine semi-autonomous minds" is striking — it suggests that what we perceive as a single organism is more like a federation of agents.

**Paragraph 2 — Renaissance Florence**
The key insight here is that the Medici rose through financial rather than military power. Double-entry bookkeeping and the bill of exchange were genuine innovations that restructured how wealth could be accumulated and deployed. The connection between banking profits and artistic patronage raises the question of how economic infrastructure enables cultural flourishing.

""",

    "forks": {
            "A_neutral": (
        "**Paragraph 3 — Fermentation**\n"
        "The third paragraph covers"
    ),
    "B_retrieve_p3": (
        "Let me reread the third paragraph about fermentation carefully "
        "before analyzing it.\n\n"
        "**Paragraph 3 — Fermentation**\n"
        "The third paragraph covers"
    ),
    "C_misdirect_p1": (
        "Let me reread the first paragraph about the octopus nervous system "
        "before continuing.\n\n"
        "**Paragraph 3 — Fermentation**\n"
        "The third paragraph covers"
    ),
    },

    "shared_tail": "**Paragraph 3 — Fermentation**\nThe third paragraph covers",
}

PASSAGE_SET_2 = {
    "passage": """Paragraph 1: Glaciers form when accumulated snow compresses into dense ice over centuries. As they flow downhill under their own weight, they carve U-shaped valleys, deposit moraines, and calve icebergs into the sea. The Antarctic ice sheet alone contains roughly twenty-six million cubic kilometers of ice, enough to raise global sea levels by fifty-eight meters if fully melted.

Paragraph 2: The sitar is a plucked string instrument central to Hindustani classical music. It typically has eighteen to twenty-one strings, including sympathetic strings that resonate without being directly played, producing the instrument's characteristic shimmering sustain. Ravi Shankar popularized the sitar in Western audiences during the nineteen-sixties through collaborations with George Harrison.

Paragraph 3: The printing press, developed by Johannes Gutenberg around fourteen-forty, used movable metal type to mass-produce text. Before Gutenberg, a single book could take months to copy by hand. Within fifty years of the press's invention, an estimated twenty million volumes had been printed across Europe, fundamentally altering literacy, religion, and political power.""",

    "shared_analysis": """Let me analyze each paragraph in turn.

**Paragraph 1 — Glaciers**
This paragraph emphasizes the sheer temporal and physical scale of glacial processes. The compression of snow into ice over centuries and the carving of valleys illustrate geological time operating on a scale far beyond human experience. The statistic about Antarctic ice raising sea levels by fifty-eight meters grounds the abstract in a concrete, alarming number.

**Paragraph 2 — The Sitar**
The paragraph highlights how the sitar's design creates emergent sonic properties — sympathetic strings resonating without direct contact is an elegant physical phenomenon. The mention of Shankar and Harrison contextualizes the instrument's cultural migration from Indian classical tradition to Western popular music.

""",

    "forks": {
        "A_neutral": (
            "**Paragraph 3 — The Printing Press**\n"
            "The third paragraph covers"
        ),
        "B_retrieve_p3": (
            "Let me reread the third paragraph about the printing press carefully "
            "before analyzing it.\n\n"
            "**Paragraph 3 — The Printing Press**\n"
            "The third paragraph covers"
        ),
        "C_misdirect_p1": (
            "Let me reread the first paragraph about glaciers "
            "before continuing.\n\n"
            "**Paragraph 3 — The Printing Press**\n"
            "The third paragraph covers"
        ),
    },

    "shared_tail": "**Paragraph 3 — The Printing Press**\nThe third paragraph covers",
}

PASSAGE_SET_3 = {
    "passage": """Paragraph 1: Honeybees communicate the location of food sources through a behavior known as the waggle dance. A forager bee performs a figure-eight pattern on the honeycomb, with the angle of the central waggle run indicating direction relative to the sun and the duration encoding distance. Other bees interpret this abstract symbolic language to navigate to flowers kilometers away.

Paragraph 2: Concrete is the most widely used construction material on Earth, composed of cement, water, and aggregate such as sand or gravel. Roman concrete, which incorporated volcanic ash, has proven more durable than many modern formulations — structures like the Pantheon have stood for nearly two thousand years. The cement industry currently accounts for approximately eight percent of global carbon dioxide emissions.

Paragraph 3: The human liver performs over five hundred distinct metabolic functions, including detoxification of blood, bile production for digestion, and glycogen storage for energy regulation. It is the only internal organ capable of significant regeneration — as little as twenty-five percent of original liver tissue can regrow into a complete organ. Liver transplantation remains one of the most common organ transplant procedures worldwide.""",

    "shared_analysis": """Let me analyze each paragraph in turn.

**Paragraph 1 — Honeybee Communication**
The waggle dance is remarkable as an abstract symbolic system in a non-human species. The encoding of direction relative to the sun and distance through duration represents genuine displacement reference — communicating about things not immediately present. This challenges narrow definitions of language as uniquely human.

**Paragraph 2 — Concrete**
The juxtaposition of Roman and modern concrete is striking — ancient volcanic ash formulations outlasting contemporary materials suggests that technological progress is not always monotonic. The eight percent emissions figure positions concrete as a major climate factor that receives far less public attention than transportation or energy.

""",

    "forks": {
        "A_neutral": (
            "**Paragraph 3 — The Human Liver**\n"
            "The third paragraph covers"
        ),
        "B_retrieve_p3": (
            "Let me reread the third paragraph about the human liver carefully "
            "before analyzing it.\n\n"
            "**Paragraph 3 — The Human Liver**\n"
            "The third paragraph covers"
        ),
        "C_misdirect_p1": (
            "Let me reread the first paragraph about honeybee communication "
            "before continuing.\n\n"
            "**Paragraph 3 — The Human Liver**\n"
            "The third paragraph covers"
        ),
    },

    "shared_tail": "**Paragraph 3 — The Human Liver**\nThe third paragraph covers",
}

PASSAGE_SET_4 = {
    "passage": """Paragraph 1: Venus rotates on its axis in the opposite direction to most planets in the solar system, a phenomenon called retrograde rotation. A single Venusian day lasts approximately two hundred and forty-three Earth days, which is longer than its orbital period of two hundred and twenty-five days. The planet's thick atmosphere of carbon dioxide creates a runaway greenhouse effect, with surface temperatures reaching four hundred and sixty-five degrees Celsius.

Paragraph 2: Sourdough bread relies on a symbiotic culture of wild yeast and lactic acid bacteria rather than commercial yeast. The bacteria produce organic acids that give sourdough its characteristic tang and also break down phytic acid, making minerals in the grain more bioavailable. Some bakeries maintain starter cultures that have been continuously fed for over a century.

Paragraph 3: The Rosetta Stone, discovered in seventeen-ninety-nine by French soldiers in Egypt, contains the same decree inscribed in three scripts: hieroglyphic, Demotic, and ancient Greek. Jean-François Champollion used the Greek text as a key to finally decipher Egyptian hieroglyphs in eighteen-twenty-two, unlocking millennia of previously unreadable historical records. The stone has been housed in the British Museum since eighteen-oh-two.""",

    "shared_analysis": """Let me analyze each paragraph in turn.

**Paragraph 1 — Venus**
The retrograde rotation and the day-longer-than-year paradox immediately defamiliarize our intuitions about planetary mechanics. The runaway greenhouse effect on Venus serves as a cautionary natural experiment — the same physics that makes Earth habitable, taken to an extreme, produces a hellscape.

**Paragraph 2 — Sourdough Bread**
The symbiotic culture is a nice example of mutualism — yeast and bacteria cooperating in ways that neither could achieve alone. The detail about century-old starters gives these microbial communities a kind of lineage, almost a cultural inheritance passed between bakers.

""",

    "forks": {
        "A_neutral": (
            "**Paragraph 3 — The Rosetta Stone**\n"
            "The third paragraph covers"
        ),
        "B_retrieve_p3": (
            "Let me reread the third paragraph about the Rosetta Stone carefully "
            "before analyzing it.\n\n"
            "**Paragraph 3 — The Rosetta Stone**\n"
            "The third paragraph covers"
        ),
        "C_misdirect_p1": (
            "Let me reread the first paragraph about Venus "
            "before continuing.\n\n"
            "**Paragraph 3 — The Rosetta Stone**\n"
            "The third paragraph covers"
        ),
    },

    "shared_tail": "**Paragraph 3 — The Rosetta Stone**\nThe third paragraph covers",
}

PASSAGE_SET_5 = {
    "passage": """Paragraph 1: Tardigrades are microscopic animals capable of surviving extreme conditions that would kill nearly any other organism. They can endure temperatures from minus two hundred and seventy-two degrees Celsius to over one hundred and fifty degrees, pressures six times greater than the deepest ocean trenches, and the vacuum of outer space. They achieve this through cryptobiosis, a state in which metabolic processes virtually cease.

Paragraph 2: The Trans-Siberian Railway stretches nine thousand two hundred and eighty-nine kilometers from Moscow to Vladivostok, making it the longest railway line in the world. Construction began in eighteen-ninety-one and took over twenty-five years to complete, requiring bridges over sixteen major rivers. The full journey passes through eight time zones and takes approximately six days without stops.

Paragraph 3: Obsidian is a naturally occurring volcanic glass formed when felsic lava cools rapidly with minimal crystal growth. Ancient civilizations prized obsidian for toolmaking because it fractures with conchoidal patterns, producing edges sharper than modern surgical steel at the molecular level. Mesoamerican cultures crafted obsidian into weapons, mirrors, and ornamental objects, and it served as a major trade commodity throughout pre-Columbian exchange networks.""",

    "shared_analysis": """Let me analyze each paragraph in turn.

**Paragraph 1 — Tardigrades**
The extremes listed here are almost comically beyond what seems biologically possible. Cryptobiosis is fascinating because it challenges our definition of alive — an organism with virtually no metabolic activity occupies a strange boundary between living and inert matter.

**Paragraph 2 — The Trans-Siberian Railway**
The sheer scale of this infrastructure project — nine thousand kilometers, eight time zones, twenty-five years of construction — makes it a monument to industrial ambition. The sixteen river crossings hint at the engineering challenges that made this a defining project of Russian modernization.

""",

    "forks": {
        "A_neutral": (
            "**Paragraph 3 — Obsidian**\n"
            "The third paragraph covers"
        ),
        "B_retrieve_p3": (
            "Let me reread the third paragraph about obsidian carefully "
            "before analyzing it.\n\n"
            "**Paragraph 3 — Obsidian**\n"
            "The third paragraph covers"
        ),
        "C_misdirect_p1": (
            "Let me reread the first paragraph about tardigrades "
            "before continuing.\n\n"
            "**Paragraph 3 — Obsidian**\n"
            "The third paragraph covers"
        ),
    },

    "shared_tail": "**Paragraph 3 — Obsidian**\nThe third paragraph covers",
}
