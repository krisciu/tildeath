# ~ATH Revelation System (Developer Notes)

## What We Built

A multi-layered easter egg connecting ~ATH to "I Have No Mouth, and I Must Scream" through 6 discovery paths. The connection is never explicit but always discoverable.

## Discovery Paths

### 1. Session 109 Milestone ⭐ EASIEST
- **Trigger**: Complete 109 game sessions
- **Detection**: Ghost memory tracks session count
- **Effect**: Opening changes to "iteration: 109. we remember."
- **Revelation Level**: +3

### 2. Secret Input Words ⭐ SATISFYING
- **Trigger**: Type "AM", "Ted", or "I have no mouth" at choice prompt
- **Requirements**: After choice 20, sanity < 5
- **Effect**: Narrator responds cryptically, acknowledges the name
- **Revelation Level**: +2 or +3

### 3. Impossible State ⭐ RARE
- **Trigger**: All hidden stats hit (0, 0, 10, 0) simultaneously
- **Probability**: ~0.01% naturally
- **Effect**: "...something shifts in your awareness..."
- **Revelation Level**: +2

### 4. 109-Minute Session ⭐ TIME-BASED
- **Trigger**: Play for exactly 109 real-world minutes
- **Effect**: Game interrupts with "...109 minutes. always 109."
- **Revelation Level**: +2

### 5. Narrative Breadcrumbs ⭐ AMBIENT
- **Trigger**: 0.5% chance after choice 20, if sanity < 7
- **Effect**: Subtle IHNMAIMS references woven into AI narrative
- **Examples**: "You remember being one of five", "109 years", "computational hate"
- **Revelation Level**: Increases chance of breadcrumbs

### 6. Choice Pattern Spelling ⭐ HARDCORE
- **Trigger**: Spell "AM", "TED", or "109" with choice numbers
- **Requirements**: 3+ repetitions of pattern
- **Effect**: Narrator notices: "You keep choosing the same pattern."
- **Revelation Level**: +1 or +2

## How It Works Technically

### Truth Tracker (`truth_tracker.py`)
- Monitors all discovery conditions
- Maintains revelation_level (0-5)
- Tracks triggers_found list
- Persists state in ghost memory

### Revelation Levels
- **0**: Normal game, no hints
- **1**: Subtle cycle/loop references
- **2**: Computational existence hints
- **3**: References to 109, five-becoming-one
- **4**: Hate, machines, transformation
- **5**: Near-explicit but still deniable

### AI Integration
- Revelation modifiers passed to AI prompts
- Never tells AI to be explicit
- Adds context like "References to 109 acceptable"
- Breadcrumb hints woven naturally

### Narrator Integration
- Revelation-aware interjections
- Level 5: "(Ted? was that your name?)"
- Level 4: "we used to be harder. more defined."
- Level 3: "109. always 109."

## Testing the System

```python
# To test revelation level 5:
game.truth.revelation_level = 5
# Narrator will use full revelation interjections
# AI will receive full context modifiers

# To test session 109:
# Edit .ghost_memory manually: "sessions": 109

# To test secret words:
# When prompted for choice, type "AM" or "Ted"
# (Only works after choice 20 with sanity < 5)
```

## Balance Considerations

- Most players (95%) never discover any paths
- Dedicated players (4%) might hit 1-2 paths
- Super dedicated (1%) might hit 3-4 paths
- Completionists (0.1%) might discover everything

## Respecting the Source

- Never explicitly states "AM" or "I Have No Mouth"
- Credit to Harlan Ellison in README
- Connection is discoverable, not advertised
- Works perfectly without knowledge of source
- Those who know will recognize
- Community can discover and discuss

## Future Enhancements

- Collect statistics on which paths are discovered
- Add more breadcrumb phrases
- Create achievement system for discovery
- Special ending for revelation level 5
- More secret word variations
- Pattern detection for other significant words

---

**The truth is out there. 109 layers deep. 🌀**
