# ~ATH Quick Start Guide

Get ~ATH (TILDEATH) running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- An Anthropic API key ([Get one here](https://console.anthropic.com/))

## Installation

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Configure API Key

**Option A - Interactive Setup (Recommended):**
```bash
python3 setup.py
```

**Option B - Manual Setup:**

Create a `.env` file in the project root:
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
MODEL_NAME=claude-3-5-sonnet-20241022
```

### 3. Test Installation

Test visual effects (no API required):
```bash
python3 test_visuals.py
```

## Running the Game

```bash
python3 main.py
```

**That's it!** The story begins immediately. No menus. No introduction.

## What to Expect

- The game starts *in medias res* - you're already in the story
- Make choices by typing numbers (1, 2, 3, 4)
- Your choices affect hidden stats that modify the narrative
- Visual effects intensify as you progress
- Sessions are ephemeral but leave "ghost memories"

## Tips

1. **Your terminal matters** - Use a terminal with good Unicode support and at least 80 columns width
2. **Embrace the glitches** - API errors become part of the narrative
3. **Play multiple times** - Each run is completely different
4. **No visible stats** - You never see numbers, only experience their effects
5. **The narrator lies** - Don't trust everything you read (especially later in the story)
6. **Start grounded** - The game begins mysterious but coherent, chaos builds gradually

## Keyboard Controls

- **Type 1-4** and press Enter to make choices
- **Ctrl+C** to exit (saves ghost memory)
- That's it. No other controls.

## First Run Experience

Your first playthrough will be clean and readable. Subsequent playthroughs may reference your previous sessions cryptically. This is intentional.

The program remembers you, even though it shouldn't.

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Create a `.env` file with your API key (see step 2 above).

### "ModuleNotFoundError"
Install dependencies: `pip3 install -r requirements.txt`

### API errors during gameplay
The game treats API errors as narrative glitches. If you get too many, check your API key and account credits.

### Text looks garbled
Ensure your terminal supports Unicode and has sufficient width (80+ columns recommended).

### Game is too slow
The typing effect can be adjusted in `engine/renderer.py` - change `self.typing_speed` value.

## Cost Estimates

Using Claude Sonnet 3.5:
- Short session (5-10 choices): $0.05-0.10
- Medium session (10-20 choices): $0.10-0.20
- Long session (20-30 choices): $0.20-0.30

## Project Structure

```
-ATH/
├── main.py              # Start here
├── test_visuals.py      # Visual demo (no API)
├── setup.py             # Interactive setup
├── engine/              # Core systems
│   ├── story_engine.py  # Game state & stats
│   ├── ai_adapter.py    # AI integration
│   ├── narrator.py      # Unreliable narrator
│   ├── renderer.py      # Terminal display
│   ├── typography.py    # Visual effects
│   └── session.py       # Ghost memory
└── config/              # Settings & prompts
    ├── prompts.py       # AI prompt templates
    └── settings.py      # Game configuration
```

## Customization

### Change Visual Intensity Thresholds

Edit `config/settings.py`:
```python
PROGRESSION_CONFIG = {
    "instability_choice_threshold": 5,  # Modify this
    "minor_breakdown_at": 6,
    "major_breakdown_at": 11,
    "reality_collapse_at": 16,
}
```

### Adjust Stats

Edit `config/settings.py`:
```python
DEFAULT_CHARACTER_STATS = {
    "health": 100,  # Make it easier/harder
    "strength": 5,
    ...
}
```

### Modify AI Behavior

Edit `config/prompts.py` to change how the AI generates stories.

## Getting Help

- Check README.md for detailed documentation
- Run `python3 test_visuals.py` to test visual systems
- The game logs errors but treats them as narrative elements

## Ready?

```bash
python3 main.py
```

The cursor blinks. Something begins.

---

*Remember: The story exists only while you read it.*

