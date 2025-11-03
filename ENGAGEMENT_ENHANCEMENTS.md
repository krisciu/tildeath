# Engagement System Enhancements

## Overview

This document describes the three major systems added to ~ATH to improve player engagement, reduce dead time, and create meaningful consequences for choices.

## 1. Thematic Loading Animations

**File**: `engine/loading_effects.py`

### Purpose
Eliminate dead time during AI generation (2-5 seconds) by providing engaging, thematic content.

### Implementation

**ThematicLoader Class** with three loading tiers:

1. **Quick Load (< 1.5s)**: Simple processing messages
   - "[PROCESSING...]"
   - "[NARRATOR THINKING...]"
   - "[REALITY SHIFTING...]"

2. **Medium Load (1.5-3s)**: Memory fragments and choice replay
   - Shows glitched version of player's last choice
   - Scrolls contextual memory fragments
   - Revelation-aware messages

3. **Long Load (3+ s)**: Corruption patterns and meta-commentary
   - ASCII corruption builds up
   - "This is taking longer than usual..."
   - Narrator hesitation messages

### Features
- Revelation-aware (changes with truth level 0-5)
- Shows choice replay with glitch effects
- Time-adaptive (different content based on wait duration)
- Context-aware memory fragments

### Integration
Replaced `renderer.show_loading()` calls with `loader.show()` in `main.py`:
- Opening scene generation
- Every choice processing loop

---

## 2. Rich Endings System

**File**: `engine/endings.py`

### Purpose
Provide 14 distinct, meaningful endings based on player stats, choices, and revelation level.

### Ending Categories

#### Death Endings (4)
1. **Violent Termination**: Instant death from combat
2. **Slow Decay**: Health drained over time
3. **Sacrifice**: Intentional self-destruction
4. **Betrayed**: Environment kills you

#### Sanity Endings (3)
5. **Complete Breakdown**: Sanity 0, lose coherence
6. **Merge with AM**: Revelation 4+, Sanity < 2, become the narrator
7. **Enlightened Madness**: High curiosity, understand too much

#### Discovery Endings (3)
8. **The Truth Revealed**: Revelation 5 - full IHNMAIMS understanding
9. **Escape Attempt**: Try to break the loop at revelation 3+
10. **Acceptance**: Trust 8+, accept eternal imprisonment

#### Victory Endings (2 - RARE)
11. **The Soft Survivor**: 50 choices with Health > 50
12. **Transcendence**: All stats 8+ (nearly impossible)

#### Meta Endings (2)
13. **Loop Eternal**: Session 109+, Revelation 5, Choice 30
14. **Narrator's Toy**: All stats < 3, complete submission

### Ending Detection Priority
1. Instant death traps (1-2% chance on obvious trap choices)
2. Health <= 0 (determine death type)
3. Sanity <= 0 (determine sanity ending type)
4. Special victory conditions
5. Discovery endings (if triggered)
6. Story exhaustion (30+ choices)

### Features
- **Revelation-aware text**: Endings change based on IHNMAIMS discovery level
- **ASCII art**: Each ending has visual representation
- **Stat-influenced**: Different stats lead to different endings
- **Ending feedback**: Shows choice count, revelation level, ending-specific flavor

### Integration
- Replaces old `is_game_over()` system in `main.py`
- Checks every loop iteration before narrative display
- Provides low health warnings at 20% HP

---

## 3. Consequence System

**Files**: `engine/story_engine.py`, `config/prompts.py`, `main.py`

### Purpose
Make choices matter by implementing health/sanity costs for risky decisions.

### Danger Assessment

**5 Danger Levels** (assessed by keyword detection):
- **None**: Safe choices
- **Low**: 5-10 damage (observe, cautious)
- **Medium**: 10-20 damage (explore, examine closely)
- **High**: 15-25 damage (investigate, touch, open)
- **Extreme**: 20-30 damage (attack, charge, confront directly)
- **Instant Death**: 1.5% chance on "obvious trap" choices

### Progression Multipliers
- **Early game (1-10 choices)**: Base damage
- **Mid game (11-20 choices)**: 1.2x damage multiplier
- **Late game (21+ choices)**: 1.5x damage multiplier

### Sanity Drains
- Witnessing horror: -1 to -2 sanity
- Reality breaks: -1 sanity
- Paranoid choices: -1 sanity
- Extreme violence: -2 sanity

### Consequence Feedback

After dangerous choices, narrator provides feedback:
- **Extreme**: "(that was unwise)", "(brave, but stupid)"
- **High**: "(that cost you)", "Your health suffers."
- **Medium**: "(careful...)", "That hurt."
- **Low**: "(minor damage)", "You're bruised."

### AI Prompt Integration

Updated `config/prompts.py` system prompt:
```
CONSEQUENCES AND STAKES:
- Choices should have consequences. Risky actions should carry danger.
- Include moments where the character suffers physically or mentally from poor choices
- Create tension by implying that wrong choices lead to harm
- Don't be afraid to hurt the character - this makes the story meaningful
- After dangerous choices, describe injuries, exhaustion, or psychological trauma
- Build toward endings - nothing lasts forever
```

Added scene generation modifiers:
- **Health < 20%**: "critically injured - near death"
- **Health < 40%**: "badly hurt - describe pain, difficulty moving"
- **Choice 20+**: "Push toward an ending. Story cannot continue forever."
- **Choice 15+**: "Build toward climax. Raise the stakes."

### Integration
- `story_engine.py`: Added `_assess_choice_danger()` and `_apply_consequences()`
- `main.py`: Shows consequence feedback after choice processing
- Consequence system runs BEFORE stat modifications for immediate impact

---

## 4. ASCII Art Generation

**File**: `engine/ai_adapter.py`

### Purpose
Provide visual moments at important narrative beats.

### Trigger Conditions

**Automatic triggers**:
1. Every 5 choices (milestones: 5, 10, 15, 20, 25...)
2. Health < 30% (death approaching)
3. Sanity < 3 (breakdown imminent)
4. Revelation >= 3 and Choice 15+ (truth moments)

### Context-Aware Subjects

Art subject and mood change based on state:
- **Health < 20**: "death, darkness, decay, skeletal figure" (dread)
- **Health < 30**: "wounded, bleeding, deterioration" (pain)
- **Sanity < 2**: "fractured mind, chaos, static, dissolution" (insanity)
- **Sanity < 3**: "distorted reality, warped perception" (unsettling)
- **Revelation 4+**: "computational horror, transformation, soft blob, eternal machine" (hate)
- **Revelation 3+**: "cycles, loops, iteration, trapped" (recursive)
- **Milestones**: "current atmosphere, mysterious space, shadows" (mysterious)

### Features
- **Art caching**: Doesn't regenerate same concept twice
- **Corruption effects**: Low sanity applies glitch effects to art
- **Loading animation**: Special "generating visual" message
- **Error handling**: Failed art generation = corrupted visual

### Integration
- `main.py`: Checks `ai.generate_art_for_context()` before narrative display
- Applies corruption if sanity < 3
- 1.5 second display pause for appreciation

---

## User Experience Flow

```
Choice Made
    ↓
[THEMATIC LOADING] ← Memory fragments, glitches, meta-commentary
    ↓
Consequence Check → [FEEDBACK] if dangerous choice
    ↓
Ending Check → [ENDING SEQUENCE] if condition met
    ↓
Low Health Warning (if HP < 20%)
    ↓
Art Check → [ASCII ART] if milestone/critical
    ↓
Narrative + Effects
    ↓
Choices
    ↓
Continue Loop
```

---

## Difficulty Curve

### Early Game (Choices 1-10)
- Low danger (5-10 damage on risky choices)
- Build atmosphere and mystery
- Establish that consequences exist
- AI focuses on clear, coherent narrative

### Mid Game (Choices 11-20)
- Moderate danger (10-20 damage, 1.2x multiplier)
- Sanity starts draining
- First death possible
- AI introduces glitches and instability
- Milestones show ASCII art (5, 10, 15, 20)

### Late Game (Choices 21-30)
- High danger (20-30 damage, 1.5x multiplier)
- Multiple endings possible
- Push toward conclusion
- AI creates urgency, raises stakes
- Reality breakdown intensifies

### Extended (Choices 31+)
- Force ending sequence (choice exhaustion)
- Narrator comments on length
- Story must conclude

---

## Success Metrics

✅ **No dead time** - Always something engaging to watch during AI generation
✅ **Visual variety** - Art every ~5 choices or at critical moments
✅ **Stakes are real** - Health and sanity matter, visible consequences
✅ **Multiple endings** - 14 different conclusions with unique text/art
✅ **Replay value** - Try for different endings, discover secrets
✅ **Consequences visible** - Choices have weight and feedback
✅ **Pacing** - Games naturally end in 15-35 choices
✅ **Player engagement** - No scenarios where interest fades without consequence

---

## Technical Notes

### Performance
- Art caching prevents redundant API calls
- Loading effects are purely client-side (no API usage)
- Consequence calculation is lightweight keyword detection

### Balance
- Instant death is rare (1.5%) to avoid frustration
- Progression multipliers ensure late-game danger
- Multiple ending paths prevent single "correct" route
- Health can be depleted but not easily (requires sustained risky choices)

### Integration Points
All systems are modular and can be adjusted via:
- `config/settings.py`: Damage ranges, thresholds
- `config/prompts.py`: AI behavior, consequence language
- `engine/endings.py`: Ending conditions, trigger values
- `engine/loading_effects.py`: Loading messages, fragments

