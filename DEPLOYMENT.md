# Deployment & Publishing Guide

## For Hackathon Demo (10:15 PM Deadline)

### Pre-Demo Checklist

✅ All dependencies installed: `pip3 install -r requirements.txt`
✅ `.env` file configured with API key
✅ Visual demo tested: `python3 test_visuals.py`
✅ Full game tested with API: `python3 main.py`
✅ Documentation complete (README, QUICKSTART, etc.)

### Demo Presentation Structure

**1. Hook (30 seconds)**
```bash
python3 test_visuals.py
```
Show the visual effects - glitching text, typography experiments, corruption.

**2. Concept (1 minute)**
Explain:
- AI-generated horror CYOA
- Unreliable narrator
- Typography becomes storytelling
- Every run is unique

**3. Live Demo (2-3 minutes)**
```bash
python3 main.py
```
Play through 3-5 choices, showing:
- Dynamic narrative generation
- Choice consequences
- Visual progression
- Narrator interjections

**4. Technical Deep Dive (1-2 minutes)**
Show code structure:
- Modular architecture
- AI prompt engineering
- Typography engine
- Stat systems

**5. Close (30 seconds)**
- Emphasize experimental nature
- Mention future possibilities
- Share repository

### Demo Tips

1. **Terminal Setup**
   - Use full-screen terminal
   - Dark background for aesthetic
   - Font size large enough for audience
   - Minimum 80 column width

2. **Avoid Live Failures**
   - Test API connection beforehand
   - Have `test_visuals.py` as backup
   - Pre-run once to verify everything works

3. **Timing**
   - Visual demo: 30 sec
   - Full game: 3-5 choices max
   - Don't let AI generation slow you down

## Publishing Options

### Zero-Setup Zipapp Bundle (New)

Use `scripts/build_bundle.py` to produce a single executable archive plus a templated installer:

```bash
python3 scripts/build_bundle.py --api-key-file anthropic_key.txt
```

Outputs (in `dist/`):

- `tildeath.pyz` – executable zipapp with all dependencies
- `install_stub.sh` – edit the placeholder download URL, then share with friends:
  ```bash
  curl -fsSL https://your.host/install_stub.sh | bash
  ```
- `README.txt` – quick reference for the bundle

The launcher installs to `~/.ATH` and caches the bundle in `~/.cache/tildeath`. The Anthropic key from `anthropic_key.txt` is embedded in the launcher stub so you can revoke it later without touching the bundle.

### Option 1: GitHub Release (Recommended)

```bash
# Initialize git repo
git init
git add .
git commit -m "Initial release: Terminal Story Engine"

# Create GitHub repo and push
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

**README.md** is your landing page - already complete!

### Option 2: PyPI Package

Create `setup.py`:
```python
from setuptools import setup, find_packages

setup(
    name="terminal-story-engine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.7.0",
        "anthropic>=0.25.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'story-engine=main:main',
        ],
    },
)
```

Then:
```bash
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

### Option 3: Itch.io Distribution

1. Package as executable using PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

2. Create itch.io page
3. Upload executable + README
4. Tag as "experimental", "interactive fiction", "horror"

### Option 4: Docker Container

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
```

Build and run:
```bash
docker build -t terminal-story-engine .
docker run -it --env-file .env terminal-story-engine
```

## Post-Hackathon Enhancements

### Short Term (1-2 days)

1. **Polish Current Features**
   - Fine-tune AI prompts
   - Adjust visual effect intensities
   - Balance stat modifications
   - Add more narrator interjections

2. **Additional Content**
   - More varied opening scenes
   - Additional event types
   - More typography effects
   - Expanded narrator moods

3. **Performance Optimization**
   - Implement async AI calls
   - More aggressive response caching
   - Reduce typing delay options

### Medium Term (1 week)

1. **Multi-Provider Support**
   - OpenAI integration
   - Grok integration
   - Local LLM support (Ollama)
   - Provider fallback system

2. **Advanced Features**
   - ASCII art generation (proper)
   - Session transcript export
   - Multiple ending types
   - Achievement system

3. **User Experience**
   - Configuration file for customization
   - In-game help system
   - Save/load checkpoint option
   - Difficulty presets

### Long Term (1+ month)

1. **Narrative Expansion**
   - Multiple story themes
   - Character persistence across sessions
   - Branching storylines
   - Community-contributed content

2. **Platform Expansion**
   - Web version (xterm.js + backend)
   - Mobile terminal app
   - Discord bot integration
   - Twitch integration for streaming

3. **Community Features**
   - Shared ghost memory network
   - Leaderboards (most choices survived)
   - Story sharing/export
   - Mod support

## Marketing & Promotion

### For Hackathon Judges

**Tagline**: "A haunted terminal that tells stories which only exist while you're reading them."

**Key Points**:
1. **Innovation**: Typography as storytelling, AI-driven narrative
2. **Technical**: Sophisticated prompt engineering, modular architecture
3. **Polish**: Complete documentation, working demo, visual effects
4. **Theme**: Experimental horror, meta-narrative, literary influences

### For General Audience

**Elevator Pitch**: "What if your terminal was haunted? A text-based horror game where the AI narrator lies to you, and the text itself decays as you read it. Every playthrough is unique. Nothing is saved. The program remembers you anyway."

**Social Media Snippet**:
```
🌀 [UNTITLED] - A Terminal Story Engine

• AI-generated horror stories
• Unreliable narrator that lies
• Text that glitches and decays
• Every run is unique
• House of Leaves meets AI

Try it: [repo link]
#experimentalgames #AIart #horror
```

### Demo Video Script (2 minutes)

1. **0:00-0:15**: Hook - Show corrupted text effects
2. **0:15-0:45**: Concept explanation with visuals
3. **0:45-1:30**: Live gameplay footage (5-6 choices)
4. **1:30-1:45**: Code walkthrough (brief)
5. **1:45-2:00**: Call to action + link

## Licensing

Current: Unlicensed (all rights reserved)

Recommendations:
- **MIT**: Maximum permissiveness, good for hackathon projects
- **GPL-3**: Copyleft, ensures derivatives stay open
- **CC BY-NC-SA**: Non-commercial, attribution required

Add `LICENSE` file:
```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge...
```

## Repository Maintenance

### README Badges

Add to top of README.md:
```markdown
![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status: Experimental](https://img.shields.io/badge/status-experimental-orange.svg)
```

### GitHub Topics

Add these topics to repo:
- `interactive-fiction`
- `ai-generated`
- `horror-game`
- `experimental`
- `terminal`
- `claude-ai`
- `python`
- `rich-tui`
- `cyoa`
- `narrative-game`

### Contributing Guidelines

If opening to contributions, create `CONTRIBUTING.md`:
```markdown
# Contributing

We welcome contributions! Areas of interest:

- New narrative content
- Visual effects
- AI prompt improvements
- Bug fixes
- Documentation

Please open an issue before major changes.
```

## Analytics (Optional)

For post-release:
- GitHub stars/forks
- PyPI downloads (if published)
- Itch.io views/downloads
- Social media engagement

## Support & Community

Consider creating:
- **Discord server**: For players and contributors
- **GitHub Discussions**: For feature requests
- **Twitter/X account**: For updates and showcase
- **Dev blog**: Document the creation process

## Final Checklist Before Publishing

- [ ] All code tested and working
- [ ] Documentation complete
- [ ] LICENSE file added
- [ ] .env.example included (not .env!)
- [ ] requirements.txt up to date
- [ ] README.md polished
- [ ] Demo video recorded (optional)
- [ ] Repository cleaned (no secrets)
- [ ] Git history clean
- [ ] Version tagged (v0.1.0)

---

**You're ready to ship! 🚀**

The terminal awaits the world.
