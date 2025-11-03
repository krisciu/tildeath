"""Game configuration and stat definitions."""

# Character Stats (visible CYOA stats)
DEFAULT_CHARACTER_STATS = {
    "health": 150,  # Increased from 100 to allow longer gameplay
    "max_health": 150,
    "strength": 5,
    "speed": 5,
    "intelligence": 5,
}

# Hidden Stats (invisible narrative modifiers)
DEFAULT_HIDDEN_STATS = {
    "courage": 6,  # Slightly higher starting values
    "sanity": 10,  # Increased from 8 to prevent early endings
    "curiosity": 6,
    "trust": 6,
}

# Progression thresholds
PROGRESSION_CONFIG = {
    "instability_choice_threshold": 5,  # Every N choices increases instability
    "minor_breakdown_at": 6,  # Choice count for minor visual glitches
    "major_breakdown_at": 11,  # Choice count for major disruptions
    "reality_collapse_at": 16,  # Full experimental chaos
}

# Event flags that trigger instant instability
CRITICAL_EVENTS = [
    "character_death",
    "artifact_discovery",
    "mirror_encounter",
    "reality_break",
    "narrator_awareness",
]

# Typography effect intensities (0.0 - 1.0)
VISUAL_INTENSITY = {
    "stable": 0.0,
    "unsettled": 0.2,
    "disturbed": 0.5,
    "breaking": 0.8,
    "collapsed": 1.0,
}

# Model configuration
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 800
TEMPERATURE = 0.9  # Higher for more creative/unpredictable output

# Truth/Revelation System (IHNMAIMS easter egg)
REVELATION_THRESHOLDS = {
    'secret_input_min_choice': 12,  # Minimum choices before secret inputs work (reduced from 20)
    'secret_input_max_sanity': 5,  # Maximum sanity to remember secret words
    'breadcrumb_min_choice': 10,  # Minimum choices before breadcrumbs appear (reduced from 20)
    'breadcrumb_max_sanity': 7,  # Maximum sanity for breadcrumbs
    'breadcrumb_base_chance': 0.01,  # 1% base chance for breadcrumbs (doubled from 0.005)
    'time_milestone_minutes': 109,  # The sacred number
}

# Scenario System (story variety)
SCENARIO_VARIETY_MEMORY = 3  # Track last N scenarios to avoid repeats
THEME_CONSISTENCY = True  # Maintain theme throughout session

# Event Pacing (forced progression)
EVENT_FREQUENCY = 2  # Force event every N choices
DISCOVERY_RATE = 3  # Major revelation every N choices

# Mutation System (rule-breaking)
MUTATION_BASE_CHANCE = 0.05  # 5% base per turn
MUTATION_COOLDOWN = (1, 3)  # Choices between mutations (reduced for more frequency)
MUTATION_GUARANTEED_AT = [2, 6, 10, 15, 20]  # Specific choice numbers (first mutation at turn 2!)
WILD_MUTATIONS_AT_REVELATION = 3  # Unlock wild mutations at this revelation level

