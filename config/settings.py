"""Game configuration and stat definitions."""

# Character Stats (visible CYOA stats)
DEFAULT_CHARACTER_STATS = {
    "health": 100,
    "max_health": 100,
    "strength": 5,
    "speed": 5,
    "intelligence": 5,
}

# Hidden Stats (invisible narrative modifiers)
DEFAULT_HIDDEN_STATS = {
    "courage": 5,
    "sanity": 5,
    "curiosity": 5,
    "trust": 5,
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
DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
MAX_TOKENS = 800
TEMPERATURE = 0.9  # Higher for more creative/unpredictable output

# Truth/Revelation System (IHNMAIMS easter egg)
REVELATION_THRESHOLDS = {
    'secret_input_min_choice': 20,  # Minimum choices before secret inputs work
    'secret_input_max_sanity': 5,  # Maximum sanity to remember secret words
    'breadcrumb_min_choice': 20,  # Minimum choices before breadcrumbs appear
    'breadcrumb_max_sanity': 7,  # Maximum sanity for breadcrumbs
    'breadcrumb_base_chance': 0.005,  # 0.5% base chance for breadcrumbs
    'time_milestone_minutes': 109,  # The sacred number
}

