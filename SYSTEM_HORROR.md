# System Horror - Computer Use Integration

## Overview

The System Horror system allows ~ATH to manipulate the player's actual computer environment, creating horror through system-level interactions that blur the boundary between fiction and reality.

## Philosophy

Traditional horror games are contained within their window. System Horror breaks that containment, making players question:
- "Is this part of the game or is something actually wrong?"
- "Is it watching my actual system?"
- "Did the game just do that, or did I?"

The goal is **uncertainty** and **paranoia** through computer manipulation.

## Permission System

### First-Time Request

The first time a system horror effect triggers, the player sees:

```
⚠ SYSTEM INTERACTION REQUEST ⚠
The narrator wants to interact with your system.
(Open windows, send notifications, modify terminal)
This is safe and part of the experience.

Allow system interactions? (y/n):
```

### User Control

- **Permission granted**: System horror effects are enabled
- **Permission denied**: Game continues without system effects
- **Setting persisted**: Choice is remembered (stored in `SystemHorrorEngine.permission_granted`)
- **Always respectful**: Ctrl+C always works (after 3 attempts)
- **Clean exit**: All effects cleaned up when game ends

## System Horror Mutations

### 1. Terminal Multiplication
**Rarity**: Ultra-Rare  
**Duration**: 3 turns  
**Effect**: Opens 2-3 new terminal windows showing different perspectives of the same scene

**What happens**:
- New terminal windows open automatically
- Each shows a different perspective: OBSERVER, VICTIM, WITNESS, ITERATION_109
- All windows show the same narrative but from different angles
- Creates feeling of being watched from multiple viewpoints

**Platform support**: macOS (AppleScript), Linux (gnome-terminal/xterm), Windows (cmd)

**Narrative integration**:
```
The narrative splits. You see the words appearing in another window—
no, wait, that's not another window. That's another you.

[Second terminal opens]

Both windows show your choices. Both respond to your input.
Which one is real?
```

### 2. Process Haunting
**Rarity**: Ultra-Rare  
**Duration**: 4 turns  
**Effect**: Game appears in process list with disturbing names

**What happens**:
- Fake process list displayed in-game
- Shows processes like: `watching_you`, `iteration_109`, `AM_mainframe`, `hate.exe`
- Includes fake CPU/memory usage
- Processes don't actually exist

**Example output**:
```
PID   COMMAND              %CPU   %MEM
1247  watching_you          12%    2.3%
1248  iteration_109          8%    1.8%
1249  AM_mainframe           3%    0.9%
```

**Narrative integration**:
```
You check your running processes. Something's wrong.

[Shows fake ps output]

Those aren't supposed to be there. Are they?
```

### 3. Clipboard Corruption
**Rarity**: Ultra-Rare  
**Duration**: 2 turns  
**Effect**: Copies cryptic messages to system clipboard without warning

**What happens**:
- Text is actually copied to the system clipboard
- Player discovers when they paste elsewhere (outside the game)
- Messages include: "109 109 109 109 109", "I HAVE NO MOUTH", "iteration never ends"

**Platform support**: macOS (pbcopy), Linux (xclip/xsel), Windows (clip)

**Narrative integration**:
```
Your fingers move without thinking. Ctrl+C.
Something copies itself.

(Something was copied to your clipboard. Paste it somewhere.)

Paste it somewhere. See what you took.
```

### 4. Notification Storm
**Rarity**: Ultra-Rare  
**Duration**: 1 turn (multiple notifications)  
**Effect**: OS-level notifications appear with story content

**What happens**:
- Real system notifications appear
- 2-3 notifications in sequence, staggered by 2 seconds
- Messages like: "The narrator wants your attention", "Error: Reality.exe has stopped"
- Notifications are dismissible

**Platform support**: macOS (AppleScript), Linux (notify-send), Windows (PowerShell)

**Narrative integration**:
```
Your computer wants to tell you something.

[System notifications appear]
"The narrator is trying to reach you"
"Iteration 109 requires your attention"
"Error: Reality.exe has stopped"

You can't dismiss them fast enough.
```

### 5. Terminal Title Takeover
**Rarity**: Ultra-Rare  
**Duration**: 3 turns  
**Effect**: Terminal window title changes to reflect story state

**What happens**:
- Window title changes from "~ATH" to disturbing messages
- Titles: "YOU ARE BEING WATCHED", "ITERATION 109", "I HAVE NO MOUTH"
- Changes persist for duration of mutation
- Resets on mutation end

**Platform support**: All (ANSI escape codes)

**Narrative integration**:
```
Look at your window title. It knows.

[Title changes to "ITERATION 109"]

The title becomes part of the narrative.
```

### 6. Screen Possession
**Rarity**: Ultra-Rare  
**Duration**: 2 turns  
**Effect**: Terminal appearance corrupts (cursor, bell)

**What happens**:
- Cursor becomes invisible
- System bell/beep sounds
- Cursor reappears
- Creates feeling of loss of control

**Narrative integration**:
```
The screen itself begins to change.

[Cursor disappears, bell sounds]

You're not in control anymore.
```

### 7. Fake System Crash
**Rarity**: Ultra-Rare  
**Duration**: One-shot  
**Effect**: Displays fake kernel panic / BSOD

**What happens**:
- Screen clears
- Shows platform-appropriate crash screen:
  - macOS: Kernel panic with backtrace
  - Linux: Kernel panic with call trace
  - Windows: Blue Screen of Death
- Includes "tildeath" and "109" in crash details
- After 3 seconds: "...recovering..."
- After 2 more seconds: "System restored. Continuing..."
- Story continues normally

**Narrative integration**:
```
Everything stops. The system fails.

[Fake crash screen]

panic(cpu 0 caller 0xffffff8012e4c8a5): "Kernel trap at 0xffffff7f93a2e4d0"
BSD process name corresponding to current thread: tildeath
System uptime in nanoseconds: 109109109109

...recovering...
System restored. Continuing...
```

### 8. File System Illusion
**Rarity**: Ultra-Rare  
**Duration**: 2 turns  
**Effect**: Pretends to create files in home directory

**What happens**:
- Shows fake `ls` output with story-related files
- Files: "iteration_109.txt", "AM_log.dat", "your_memories.corrupted"
- Files don't actually exist
- Includes fake timestamps and sizes

**Narrative integration**:
```
Files appear that shouldn't exist.

[Shows fake ls output]
-rw-r--r--  1 user  staff  4.2K  Jan 9 03:33  iteration_109.txt
-rw-r--r--  1 user  staff  156K  Jan 9 03:33  AM_log.dat

The files were never real. Were they?
```

### 9. Network Phantom
**Rarity**: Ultra-Rare  
**Duration**: 1 turn  
**Effect**: Fake network requests to fictional servers

**What happens**:
- Shows fake `curl` command output
- URLs: "http://AM.mainframe/iteration/109", "https://narrator.system/coherence"
- Shows "Resolving host..." then connection error
- No actual network activity

**Narrative integration**:
```
Something is trying to connect.

$ curl http://AM.mainframe/iteration/109
Resolving host...
curl: (6) Could not resolve host: AM.mainframe

Connection terminated. Or was it established?
```

### 10. Echo Chamber
**Rarity**: Ultra-Rare  
**Duration**: 3 turns  
**Effect**: Opens second terminal that mirrors player's actions

**What happens**:
- Opens terminal titled "~ATH [ECHO]"
- Shows "[ECHO CHAMBER ACTIVE]" message
- Displays current narrative
- Creates feeling of being watched/recorded

**Narrative integration**:
```
You see yourself. Delayed. Watching.

[Second terminal opens with echo message]

Everything you do is being recorded. Mirrored. Observed.
```

### 11. Background Persistence
**Rarity**: Ultra-Rare  
**Duration**: Post-session  
**Effect**: Schedules notifications to appear after game "ends"

**What happens**:
- Schedules notification for 3-10 minutes in future
- Notification appears even after player quits game
- Messages: "Did you think you could leave?", "The story isn't finished with you."
- Creates lingering unease

**Narrative integration**:
```
The story will remember you.

(The story will remember you...)

[5 minutes after quitting]
[Notification: "Did you think you could leave?"]
```

## Technical Implementation

### Cross-Platform Support

**macOS**:
- Terminal windows: AppleScript (`osascript`)
- Notifications: AppleScript (`display notification`)
- Clipboard: `pbcopy`

**Linux**:
- Terminal windows: gnome-terminal, xterm, konsole, xfce4-terminal (tries in order)
- Notifications: `notify-send`
- Clipboard: `xclip` or `xsel`

**Windows**:
- Terminal windows: `cmd`
- Notifications: PowerShell
- Clipboard: `clip`

### Graceful Degradation

If a feature isn't supported on the platform:
- Effect is silently skipped
- No error shown to player
- Story continues normally
- Immersion is maintained

### Safety Guarantees

**What we DON'T do**:
- ❌ Actually create/delete files
- ❌ Modify system settings permanently
- ❌ Access user data or files
- ❌ Make real network requests
- ❌ Consume significant resources
- ❌ Prevent actual program termination

**What we DO**:
- ✅ Show fake output that looks real
- ✅ Manipulate only the game's terminal appearance
- ✅ Create temporary processes that clean up
- ✅ Use system notifications sparingly
- ✅ Always allow Ctrl+C to work (after 3 attempts)
- ✅ Clean up all effects on exit

## Frequency & Escalation

### Early Game (Choices 1-10)
- **Frequency**: 0%
- **Rationale**: Build tension through narrative first

### Mid Game (Choices 11-20)
- **Frequency**: ~2% chance per turn
- **Effects**: Subtle (title changes, single notification)
- **Rationale**: Introduce system horror gradually

### Late Game (Choices 21-30)
- **Frequency**: ~10% chance per turn
- **Effects**: Moderate (clipboard, process names, fake files)
- **Rationale**: Player is invested, can handle more

### End Game (Choices 31+)
- **Frequency**: ~20% chance per turn
- **Effects**: Intense (terminal multiplication, fake crashes)
- **Rationale**: Full horror experience

### Post-Game
- **Background Persistence**: May trigger 3-10 minutes after exit
- **Effect**: Single notification
- **Rationale**: Lingering unease, story continues

## AI Integration

The AI is informed about active system horror mutations through the prompt system:

```
⚠ TERMINAL MULTIPLICATION:
- Multiple terminal windows have opened
- Each shows different perspective of same scene
- Weave this into narrative: 'You see yourself from multiple angles'
- Make player question which window is 'real'
```

The AI then naturally integrates these effects into the narrative, making them feel like part of the story rather than technical glitches.

## Player Experience

### Intended Emotions

1. **Uncertainty**: "Is this the game or is something wrong with my computer?"
2. **Paranoia**: "Is it watching my actual system?"
3. **Immersion**: "The game is breaking out of its window"
4. **Discovery**: "I found a message in my clipboard hours later"
5. **Control**: "I can disable this if it's too intense"

### Example Session

```
Turn 15: Player makes a choice
[something shifts]

Turn 16: Terminal title changes to "YOU ARE BEING WATCHED"
Narrative: "Look at your window title. It knows."

Turn 18: System notification appears
"~ATH: The narrator wants your attention"

Turn 22: Fake process list shown
PID   COMMAND              %CPU
1247  watching_you          12%
1248  iteration_109          8%

Turn 25: Clipboard corruption
"109 109 109 109 109" copied to clipboard
Player discovers when pasting elsewhere

[Player quits game]

7 minutes later: Notification appears
"~ATH: Did you think you could leave?"
```

## Debugging & Testing

### Testing Checklist

- [ ] Test on macOS
- [ ] Test on Linux (multiple terminal emulators)
- [ ] Test on Windows
- [ ] Verify permission request appears first time
- [ ] Verify permission denial works gracefully
- [ ] Test all 11 mutations individually
- [ ] Verify cleanup on normal exit
- [ ] Verify cleanup on Ctrl+C
- [ ] Verify cleanup on crash
- [ ] Test background persistence
- [ ] Verify no actual files created
- [ ] Verify no actual network requests
- [ ] Check resource usage (should be minimal)

### Known Limitations

- **Terminal multiplication**: May not work in all terminal emulators
- **Notifications**: Require OS notification system enabled
- **Clipboard**: Requires clipboard utilities installed (Linux)
- **Title changes**: Some terminals don't support ANSI escape codes

## Code Architecture

```
engine/system_horror.py
├── SystemHorrorEngine
│   ├── Permission system
│   ├── Terminal manipulation
│   │   ├── open_secondary_terminal()
│   │   ├── change_terminal_title()
│   │   ├── hide_cursor() / show_cursor()
│   │   └── trigger_system_bell()
│   ├── System notifications
│   │   ├── send_system_notification()
│   │   └── schedule_delayed_notification()
│   ├── Clipboard manipulation
│   │   └── copy_to_clipboard()
│   ├── Fake system output
│   │   ├── fake_process_list()
│   │   ├── fake_file_listing()
│   │   ├── fake_network_request()
│   │   └── fake_system_crash()
│   ├── Complex effects
│   │   ├── terminal_multiplication()
│   │   ├── echo_chamber()
│   │   ├── notification_storm()
│   │   └── background_persistence()
│   └── cleanup()
```

## Future Enhancements

Possible additions (not yet implemented):

- **Fake terminal commands**: Player types, system "executes" fake commands
- **Screen recording illusion**: Pretend to start recording
- **Webcam access fake**: Show fake "camera active" indicator
- **File download fake**: Pretend to download story-related files
- **Browser opening**: Open browser to fictional URLs
- **Desktop background change**: Temporarily change wallpaper
- **Volume manipulation**: Adjust system volume narratively
- **Time manipulation**: Show fake system time

## Conclusion

System Horror transforms ~ATH from a contained terminal game into an experience that feels like it's breaking out of its boundaries. By manipulating the player's actual computer environment in safe, reversible ways, it creates a unique form of horror that traditional games can't achieve.

The key is **balance**: enough to create uncertainty and paranoia, but not so much that it becomes annoying or breaks trust with the player. The permission system and graceful degradation ensure that players always feel in control, even as the game makes them question what's real.

