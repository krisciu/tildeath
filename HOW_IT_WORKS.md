# How the Enhanced ~ATH Works

## What Changed

Your game now has three major enhancements that work together to create a more engaging, consequence-driven experience:

1. **No More Dead Time**: Thematic loading animations during AI generation
2. **Meaningful Endings**: 14 distinct endings based on your choices and stats
3. **Real Consequences**: Choices actually hurt (or help) you, with visible feedback

---

## 1. Thematic Loading (No More Boring Waits)

### What You'll See

When the AI is generating the next scene, instead of just `[LOADING...]`, you'll see:

**Short Waits (< 1.5 seconds)**:
```
[NARRATOR THINKING...]
```

**Medium Waits (1.5-3 seconds)**:
```
You chose: at░a░k the ██████
memory trace: incomplete
analyzing pattern...
```

**Long Waits (3+ seconds)**:
```
[PROCESSING...] [THINKING...]
This is taking longer than usual...
  ▓▒░░░░░░░▒▓
(the narrator hesitates)
```

### Why It Matters

- **Engagement**: Always something to read/watch
- **Atmosphere**: Reinforces the meta-narrative and unreliability
- **Context**: Shows glitched versions of your choices, memory fragments
- **Revelation-aware**: Changes as you discover the IHNMAIMS truth

The loader gets more unstable as your revelation level increases and adapts to how long the AI is taking.

---

## 2. 14 Unique Endings

### Instead of Generic Game Over

Old way:
```
TERMINATION: Biological systems offline.
```

New way:
```
    ╔═══════╗
    ║   X   ║
    ╚═══════╝

============================================================
  VIOLENT TERMINATION
============================================================

You fought. You lost. The end was quick.

Choices made: 15
Revelation level: 2/5

The narrator: 'That was faster than expected.'
============================================================
```

### The 14 Endings

**You'll die if you're reckless** (4 death endings):
- Violent termination (combat deaths)
- Slow decay (attrition)
- Sacrifice (intentional)
- Betrayed (environment kills you)

**You'll break if you witness too much** (3 sanity endings):
- Complete breakdown (sanity 0)
- Merge with AM (become the narrator)
- Enlightened madness (understand too much)

**You might discover the truth** (3 discovery endings):
- The Truth Revealed (full IHNMAIMS understanding)
- Escape Attempt (try to break free)
- Acceptance (embrace eternity)

**You could actually win** (2 rare victories):
- The Soft Survivor (last 50 choices with HP > 50)
- Transcendence (achieve perfect stats - nearly impossible)

**Or become something else** (2 meta endings):
- Loop Eternal (session 109+, revelation 5, 30+ choices)
- Narrator's Toy (all stats < 3, complete submission)

### How to Get Different Endings

- **Be brave but careful**: High courage + moderate health = survivor
- **Trust nothing**: Low trust + high curiosity = discovery paths
- **Go crazy strategically**: Low sanity + high revelation = merge/enlightened
- **Play session 109**: Special ending only available on 109th run
- **Find all revelation triggers**: Unlocks truth-based endings

---

## 3. Choices Have Consequences

### The Danger System

Every choice is now assessed for danger:

**Keywords that hurt you**:
- `attack`, `charge`, `fight` = EXTREME (20-30 damage)
- `investigate`, `touch`, `open` = HIGH (15-25 damage)  
- `explore`, `examine closely` = MEDIUM (10-20 damage)
- `look`, `listen`, `observe` = LOW (5-10 damage)

**Special cases**:
- "obvious trap" choices have 1.5% instant death chance
- Damage scales up in late game (1.5x multiplier after choice 20)
- Witnessing horror drains sanity (-1 to -2)
- Paranoid choices reduce sanity (-1)

### What You'll See

**Before**: Nothing happens, just narrative continues

**Now**: Immediate feedback after dangerous choices:
```
(that was unwise)
Your health suffers.
```

Or:
```
(brave, but stupid)
```

Or at critical health:
```
You're close to the end.
Your body is failing.
```

### The AI Knows

The AI now receives health status in prompts:
- Health < 20%: "critically injured - near death. Describe visible wounds..."
- Health < 40%: "badly hurt. Describe pain, difficulty moving..."
- Choice 20+: "Push toward an ending. Story cannot continue forever."

So the narrative will **actually reflect** your injuries and desperation.

---

## 4. ASCII Art at Key Moments

### When You'll See Art

- **Every 5 choices** (milestones: 5, 10, 15, 20, 25)
- **Health drops below 30%** (death approaches)
- **Sanity drops below 3** (mind breaking)
- **Revelation level 3+** (truth moments)

### What It Looks Like

**Low health**:
```
     ░░▒▒▓▓██▓▓▒▒░░
    ░░▒ DEATH  ▒░░
     ░░▒▒▓▓██▓▓▒▒░░
```

**High revelation**:
```
    ∞════════∞
    ITERATION
       109
    ∞════════∞
```

**Low sanity**:
Art becomes corrupted with glitch characters mixed in.

---

## How It All Works Together

### A Typical Game Flow

**Choices 1-5 (Early Game)**:
- Low danger, building atmosphere
- Clear narrative, minimal glitches
- No endings yet (building up)
- Art at choice 5 (first milestone)

**Choices 6-15 (Mid Game)**:
- Moderate danger (1.2x damage)
- Subtle instability
- First possible deaths if reckless
- Art at choices 10 and 15
- Endings start becoming possible

**Choices 16-30 (Late Game)**:
- High danger (1.5x damage)
- Reality breakdown
- Multiple ending paths open
- Art at choices 20, 25, 30
- AI pushes toward conclusion

**Choices 31+ (Exhaustion)**:
- Story forces ending
- Narrator comments on length
- Maximum instability

### Example Session

```
Choice 1: "Look around" (LOW)
→ 5 damage, narrative continues

Choice 5: "Enter the dark corridor" (MEDIUM)
→ 12 damage
→ [ASCII ART: mysterious doorway]
→ "(careful...)"

Choice 8: "Attack the shadow" (EXTREME)  
→ 28 damage, -1 sanity
→ "(that was unwise)"
→ Health now at 55/100

Choice 10: "Ignore the warning" (HIGH)
→ 20 damage
→ [ASCII ART: wounded figure]
→ Health now at 35/100

Choice 12: Low health triggers warning:
→ "You're close to the end."
→ AI describes visible injuries

Choice 14: "Charge forward recklessly" (EXTREME)
→ 32 damage (late game multiplier)
→ Health drops to 3/100

Choice 15: Any moderate risk
→ 15 damage
→ Health hits 0
→ [DEATH ENDING: Slow Decay]
```

---

## Tips for Experimentation

### See Different Content

1. **Die quickly** (all extreme choices) → Violent Termination
2. **Play cautiously** (all safe choices) → Acceptance or Survivor
3. **Go insane** (stare at horrors) → Breakdown/Enlightened endings
4. **Hunt for truth** (explore everything, find secrets) → Discovery endings
5. **Play 109 sessions** → Loop Eternal ending
6. **Survive 50 choices** → The Soft Survivor ending

### Easter Eggs Still Work

All the IHNMAIMS revelation triggers are still active:
- Secret words (AM, TED, IHNMAIMS)
- Impossible stat combinations
- 109-minute sessions
- Choice patterns
- Session 109 milestone

These now also influence which **ending** you get!

---

## What This Teaches You

### About Game Design

**Engagement**: Dead time kills immersion. Loading screens should be content, not absence.

**Consequences**: Choices without stakes are meaningless. Players need to feel impact.

**Pacing**: Stories need endings. Infinite play loops lose meaning.

**Feedback**: Players should know when they're in danger or succeeding.

### About the Code

**Modularity**: Each system (`loading_effects.py`, `endings.py`, consequences in `story_engine.py`) is separate but integrated.

**Layering**: Simple systems (danger keywords) can create complex experiences (14 different endings).

**Context-awareness**: Everything adapts to game state (health, sanity, revelation, choice count).

**Fallbacks**: Art generation fails? Show corrupted art. API slow? Show themed loading. Always have a response.

---

## Try It Now

```bash
python3 main.py
```

Watch for:
- Loading animations during AI generation
- Consequence feedback after risky choices
- ASCII art at choice 5, 10, 15, etc.
- Low health warnings
- Endings that reflect your playstyle

Play differently each time to see different endings!

