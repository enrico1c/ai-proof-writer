---
name: robotic-process-automation
description: "Takes finalized text and generates a standalone Python script that physically types it into a word processor (Word, Google Docs) simulating 100% human behavior across 7 levels: Unicode typing, micro-rhythm, syntactic pauses, typo injection, cognitive fatigue, safety countdown, and code structure."
level: 3
---

# Robotic Process Automation — Human Typing Simulator

Takes a finalized input text and outputs a complete, ready-to-execute Python script that physically types the text into an open word processor, simulating human keystroke patterns at the forensic level. Evades authorship metadata analysis and keystroke tracking systems (academic and corporate).

**Input:** finalized text (paste directly or reference `target_text.txt`)
**Output:** one complete Python script — no filler, no explanation

---

## When to Use

Use this skill when:
- the user provides finalized text and asks for a typing script
- the goal is to produce a document with authentic human keystroke metadata
- the user says "genera lo script", "crea lo script di digitazione", "RPA", or similar
- the output must simulate real human typing for forensic or metadata purposes

Do **not** use when:
- the user wants a translation or rewrite (use `/italian-rewriting`)
- the target application is not a writable text field

---

## Seven Levels of Human Simulation

### Level 1 — Libraries and Unicode Compatibility
- **Never** use `pyautogui.write()` — it destroys Italian accented characters (è, à, ò, ì, ù) on non-US layouts
- Use `pynput` (`from pynput.keyboard import Controller, Key`) — handles Unicode natively
- Required imports: `pynput`, `time`, `random`

### Level 2 — Typing Cadence (Micro-Rhythm)
- Standard characters: random delay 0.04–0.12 seconds per character
- Special characters and capitals (Shift required): longer delay 0.10–0.20 seconds
- No two consecutive characters have the same interval

### Level 3 — Syntactic Pauses (Macro-Rhythm)
| Character typed | Pause range |
|---|---|
| `,` | 0.3–0.8 s |
| `.` `?` `!` | 1.5–3.5 s |
| `\n` (newline) | 5.0–15.0 s |

### Level 4 — Error Simulation (Typo Injection)
- Error rate: 1.5% (`probability = 0.015`) for alphanumeric characters only
- On trigger: type a random wrong letter → pause 0.3–0.6 s (reaction time) → `Key.backspace` → pause 0.1–0.3 s → type correct character
- A file with zero Backspace events is mathematically artificial and flags automated authorship

### Level 5 — Cognitive Pauses (Fatigue Simulation)
- Character counter initialized at script start
- Every 400–600 characters (threshold randomized per cycle): pause 10–25 seconds
- Simulates user looking away, checking notes, or re-reading

### Level 6 — Safety and Initialization
- 10-second countdown printed to terminal before any typing begins
- Console message: instructions for emergency kill (Ctrl+C or physical mouse movement to corner)
- Script never starts instantly

### Level 7 — Code Structure
- `TARGET_TEXT` variable: text hardcoded as triple-quoted string (default)
- Optional: reads from `target_text.txt` if file exists (fallback)
- Heavily commented throughout

---

## Workflow

**Local (Claude Code):** generates a Python script (`typing_sim.py`) run with `python typing_sim.py`.

**Web (claude.ai):** generates a JavaScript browser console script run directly in Chrome DevTools on Google Docs — no Python, no installation.

Detect which mode to use from context:
- If the user has mentioned `--web`, is on claude.ai, or has said they have no local Python → generate the JS console script
- Otherwise → generate the Python script (default)

1. User invokes `/robotic-process-automation` and pastes the finalized text
2. Generate the appropriate script (Python or JS) with `TARGET_TEXT` set to that text
3. Output **only** the script — no preamble, no explanation after

---

## Python Script Template

When the user provides text, populate `TARGET_TEXT` and output this script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA Human Typing Simulator — 7-Level Forensic Human Behavior Engine
Requires: pip install pynput
Usage:    python typing_sim.py
          (click inside the target document during the 10s countdown)
Emergency stop: Ctrl+C in terminal, or move mouse to any screen corner
"""

import time
import random
from pynput.keyboard import Controller, Key

# ─────────────────────────────────────────────────────────────────
# LEVEL 7 — TARGET TEXT
# Replace this string with the text to type, or place the text in
# a file named 'target_text.txt' in the same directory.
# ─────────────────────────────────────────────────────────────────
TARGET_TEXT = """[PASTE TEXT HERE]"""

# Attempt to load from file if it exists (overrides the variable above)
try:
    with open("target_text.txt", "r", encoding="utf-8") as f:
        TARGET_TEXT = f.read()
    print("[INFO] Loaded text from target_text.txt")
except FileNotFoundError:
    pass  # Use the hardcoded TARGET_TEXT above

# ─────────────────────────────────────────────────────────────────
# LEVEL 1 — KEYBOARD CONTROLLER (pynput, Unicode-safe)
# ─────────────────────────────────────────────────────────────────
keyboard = Controller()

# ─────────────────────────────────────────────────────────────────
# LEVEL 2 — MICRO-RHYTHM: per-character delay calculation
# ─────────────────────────────────────────────────────────────────
def get_char_delay(char: str) -> float:
    """Returns a randomized typing delay for a single character."""
    # Capitals and most punctuation require Shift — slightly slower
    if char.isupper() or char in '!"£$%^&*()_+{}|:<>?~@#':
        return random.uniform(0.10, 0.20)
    return random.uniform(0.04, 0.12)

# ─────────────────────────────────────────────────────────────────
# LEVEL 3 — MACRO-RHYTHM: syntactic pause after punctuation
# ─────────────────────────────────────────────────────────────────
def get_syntactic_pause(char: str) -> float:
    """Returns an additional pause after punctuation or newline."""
    if char == ',':
        return random.uniform(0.3, 0.8)
    if char in '.?!':
        return random.uniform(1.5, 3.5)
    if char == '\n':
        return random.uniform(5.0, 15.0)
    return 0.0

# ─────────────────────────────────────────────────────────────────
# LEVEL 4 — TYPO INJECTION: 1.5% error rate on alphanumeric chars
# ─────────────────────────────────────────────────────────────────
COMMON_MISTYPE = list('asdfjklqwertyuiopzxcvbnm')
ERROR_RATE = 0.015

def maybe_inject_typo(correct_char: str) -> None:
    """
    With ERROR_RATE probability, types a wrong character,
    pauses (human reaction), presses Backspace, then types the correct one.
    Only fires for alphanumeric characters.
    """
    if correct_char.isalnum() and random.random() < ERROR_RATE:
        wrong = random.choice(COMMON_MISTYPE)
        keyboard.type(wrong)
        time.sleep(random.uniform(0.3, 0.6))   # reaction time
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
        time.sleep(random.uniform(0.1, 0.3))   # brief pause after correction

# ─────────────────────────────────────────────────────────────────
# LEVEL 5 — COGNITIVE PAUSE: fatigue simulation every 400-600 chars
# ─────────────────────────────────────────────────────────────────
def cognitive_pause(char_count: int, next_threshold: int) -> tuple[int, int]:
    """
    If char_count has reached next_threshold, execute a cognitive pause
    and reset the counter + randomize the next threshold.
    Returns (new_char_count, new_threshold).
    """
    if char_count >= next_threshold:
        pause_duration = random.uniform(10.0, 25.0)
        print(f"\n[COGNITIVE PAUSE] {pause_duration:.1f}s — simulating user re-reading...",
              flush=True)
        time.sleep(pause_duration)
        return 0, random.randint(400, 600)
    return char_count, next_threshold

# ─────────────────────────────────────────────────────────────────
# LEVEL 6 — SAFETY: 10-second countdown + kill-switch instructions
# ─────────────────────────────────────────────────────────────────
def safety_countdown() -> None:
    """Prints a 10-second countdown and kill-switch instructions."""
    print("=" * 60)
    print("  RPA Human Typing Simulator")
    print("=" * 60)
    print(f"  Characters to type: {len(TARGET_TEXT)}")
    print()
    print("  EMERGENCY STOP: press Ctrl+C in this terminal,")
    print("  or move the mouse to any corner of the screen.")
    print()
    print("  Click inside the target document NOW.")
    print("=" * 60)
    for i in range(10, 0, -1):
        print(f"  Starting in {i}...", flush=True)
        time.sleep(1)
    print("  TYPING STARTED\n")

# ─────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────
def main() -> None:
    safety_countdown()

    char_count = 0
    next_threshold = random.randint(400, 600)

    for char in TARGET_TEXT:
        # Level 5: check for cognitive pause before typing each character
        char_count, next_threshold = cognitive_pause(char_count, next_threshold)

        # Level 4: possibly inject a typo (only for alphanumeric chars)
        maybe_inject_typo(char)

        # Level 2: calculate per-character delay
        delay = get_char_delay(char)

        # Level 1: type the character via pynput (Unicode-safe)
        if char == '\n':
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        else:
            keyboard.type(char)

        char_count += 1

        # Level 2: apply micro-rhythm delay
        time.sleep(delay)

        # Level 3: apply syntactic macro-pause after punctuation
        syntactic = get_syntactic_pause(char)
        if syntactic > 0:
            time.sleep(syntactic)

    print("\n[DONE] All text has been typed.")

if __name__ == "__main__":
    main()
```

---

## Web Mode — Browser Console Script (no Python required)

When the user specifies `--web` or has no local Python, generate this JavaScript template instead of the Python one. All 7 simulation levels are preserved.

**How it runs:** user opens Google Docs, presses `F12` → Console tab, pastes the script, clicks inside the document, waits 10 seconds.

**Emergency stop:** close the DevTools panel or navigate away.

```javascript
// ai-proof-writer — Phase 2 (Web Mode)
// Paste in Chrome DevTools Console while Google Docs is open and the document is focused.
// Emergency stop: close DevTools or navigate away from the page.

const TARGET_TEXT = `[ASSEMBLED REWRITTEN TEXT GOES HERE]`;

// ── Level 4 ───────────────────────────────────────────────────────────────────
const ERROR_RATE = 0.015;
const COMMON_MISTYPE = 'asdfjklqwertyuiopzxcvbnm'.split('');

// ── Helpers ───────────────────────────────────────────────────────────────────
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ── Level 2 — Micro-rhythm ────────────────────────────────────────────────────
function getCharDelay(char) {
  if (char === char.toUpperCase() && char !== char.toLowerCase())
    return 100 + Math.random() * 100;   // 0.10–0.20 s for capitals
  return 40 + Math.random() * 80;        // 0.04–0.12 s standard
}

// ── Level 3 — Syntactic pauses ────────────────────────────────────────────────
function getSyntacticPause(char) {
  if (char === ',')          return 300  + Math.random() * 500;
  if ('.?!'.includes(char))  return 1500 + Math.random() * 2000;
  if (char === '\n')         return 5000 + Math.random() * 10000;
  return 0;
}

// ── Level 1 — Find Google Docs editor and insert character ────────────────────
// Google Docs renders its editor inside a hidden iframe. execCommand must be
// called on that iframe's document, not on the outer page document.
function getEditorDoc() {
  const iframe = document.querySelector('.docs-texteventtarget-iframe');
  if (iframe && iframe.contentDocument) return iframe.contentDocument;
  return document; // fallback for other contenteditable targets
}

function insertChar(char) {
  const doc = getEditorDoc();
  if (char === '\n') {
    doc.execCommand('insertParagraph');
  } else {
    doc.execCommand('insertText', false, char);
  }
}

function deleteChar() {
  getEditorDoc().execCommand('delete');
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const iframe = document.querySelector('.docs-texteventtarget-iframe');
  if (!iframe) {
    console.warn('[WARNING] Google Docs iframe not found. Make sure this page is an open Google Docs document.');
  }

  console.log('════════════════════════════════════════════════════');
  console.log('  ai-proof-writer — Web Typing Simulator');
  console.log('════════════════════════════════════════════════════');
  console.log(`  Characters to type: ${TARGET_TEXT.length}`);
  console.log('  Click inside the Google Docs document NOW.');
  console.log('  Emergency stop: close DevTools or navigate away.');
  console.log('════════════════════════════════════════════════════');

  for (let i = 10; i > 0; i--) {
    console.log(`  Starting in ${i}...`);
    await sleep(1000);
  }
  console.log('  TYPING STARTED\n');

  let charCount = 0;
  let nextThreshold = 400 + Math.floor(Math.random() * 200);  // Level 5

  for (const char of TARGET_TEXT) {

    // Level 5 — Cognitive pause
    if (charCount >= nextThreshold) {
      const pause = 10000 + Math.random() * 15000;
      console.log(`[COGNITIVE PAUSE] ${(pause / 1000).toFixed(1)}s`);
      await sleep(pause);
      charCount = 0;
      nextThreshold = 400 + Math.floor(Math.random() * 200);
    }

    // Level 4 — Typo injection
    if (/[a-zA-Z0-9]/.test(char) && Math.random() < ERROR_RATE) {
      const wrong = COMMON_MISTYPE[Math.floor(Math.random() * COMMON_MISTYPE.length)];
      insertChar(wrong);
      await sleep(300 + Math.random() * 300);   // reaction time
      deleteChar();
      await sleep(100 + Math.random() * 200);   // correction pause
    }

    // Level 1 — Type the character
    insertChar(char);
    charCount++;

    // Level 2 — Micro-rhythm delay
    await sleep(getCharDelay(char));

    // Level 3 — Syntactic pause
    const syntactic = getSyntacticPause(char);
    if (syntactic > 0) await sleep(syntactic);
  }

  console.log('\n[DONE] All text has been typed.');
}

main();
```

---

## Usage

### Local (Claude Code)

```
/robotic-process-automation

[paste finalized text here]
```

Generates `typing_sim.py`. Run with:
```bash
pip install pynput
python typing_sim.py
```

Optional flags:
- `--file` — read text from `target_text.txt` instead of hardcoding
- `--lang it` (default)

### Web (claude.ai or no local Python)

```
/robotic-process-automation --web

[paste finalized text here]
```

Generates a JavaScript console script. To run it:
1. Open **Google Docs** and place the cursor where typing should begin
2. Press `F12` → go to the **Console** tab
3. Paste the script and press `Enter`
4. Click inside the document during the 10-second countdown

No installation required beyond a Chrome or Firefox browser.
