---
name: ai-proof-writer
description: "Full pipeline: rewrites any input text into undetectable Italian prose (italian-rewriting skill, all 4 layers + 30 quality gates, chunked loop) then generates a forensic-level human typing script (robotic-process-automation skill, 7 levels of pynput simulation) ready to bypass both AI detectors and authorship metadata analysis."
level: 3
---

# AI-Proof Writer — Full Pipeline Skill

Two-phase orchestration of `italian-rewriting` and `robotic-process-automation`.

**Input:** any raw text (Italian or source language)
**Output Phase 1:** rewritten Italian prose — undetectable by GPTZero, Originality, ZeroGPT, human editors
**Output Phase 2:** a ready-to-run Python script that types the rewritten text with forensic-level human keystroke metadata

---

## When to Use

Invoke `/ai-proof-writer` when:
- the user provides source text and wants it both rewritten AND typed with human metadata
- the goal is to pass AI detectors AND authorship forensic analysis simultaneously
- the user says "scrivi come un umano", "fai passare tutto", "full pipeline", or similar

Do **not** use when:
- only rewriting is needed (use `/italian-rewriting`)
- only the typing script is needed (use `/robotic-process-automation`)
- the output language is not Italian

---

## Setup (first run only)

Before first use, the user must run:

```bash
python setup.py
```

This script (included in the `ai-proof-writer` GitHub repo) will:
1. Verify Python ≥ 3.10
2. Install `pynput` automatically
3. Guide through platform-specific keyboard access permissions:
   - **macOS:** Accessibility permission in System Settings
   - **Linux:** `/dev/input` group or X11 access
   - **Windows:** no special permissions required
4. Run a functional smoke-test of the keyboard controller
5. Print step-by-step usage instructions

---

## Phase 1 — Italian Rewriting (full `italian-rewriting` skill)

Apply the complete `italian-rewriting` skill workflow. All rules are active:
- Layer 1: Absolute Lexical Blacklist · Organic Burstiness · Pro-Drop · Dislocation · Active Voice · Anti-Sandwich · Typography
- Layer 2: Asyndeton · -mente Blacklist · Weak Support Verb Ban · Internal Meta-Discourse Ban · Ciò Cap · Containment Rule · List Asymmetry
- Layer 3: Lexical Entrainment · Explanatory Colon · Nominalization · Litotes · Collocations
- Layer 4: Semicolons · Inciso · Epistemic Conditional · Organic Quote Weaving · Correlatives
- Systemic Fixes: Perplexity Injection · Logical Non-Linearity · Functional Burstiness Audit
- All 30 quality gates applied per-chunk

### Chunking Loop (interactive — mandatory)

**Step 1 — Chunk Analysis**
Count words. Split at natural boundaries into 400–600 word chunks. Tell the user: `"N chunks identified. Starting chunk 1/N."`

**Step 2 — Initialize Continuity Ledger**
```
CONTINUITY LEDGER
─────────────────────────────────────────────
Document scope:     [1-2 sentences on what this text is about]
Register:           accademico (default) / saggistico / conversazionale
─────────────────────────────────────────────
Core noun variants used:   [noun → variants deployed]
Structural elements:
  Acknowledged tangent:  [ ] not yet  /  [✓] chunk X
  Open minor thread:     [ ] not yet  /  [✓] chunk X
  Conclusion-first:      count = 0
Perplexity injections:   [domain-crossing word → chunk X]
Last sentence of prev chunk: —
─────────────────────────────────────────────
```

**Step 3 — Per-Chunk Loop**
For each chunk [i/N]:
1. **Context Refresh:** re-read all 4 Layers + Systemic Fixes rule groups
2. **Consult Ledger:** check noun variants, pending structural elements, last sentence for seam
3. **Rewrite:** apply all rules, verify all facts against source
4. **6-item fast check:** em-dashes=0 · blacklist=0 · burstiness functional · ≥1 dislocation · ≥1 asyndeton · seam clean
5. **Update Ledger + STOP:** print updated Ledger, then output exactly:
   `"Chunk [i/N] complete. Type 'Next' to continue, or 'Assemble' if this was the last chunk."`
   **Do NOT generate anything else until the user responds.**

**Step 4 — On 'Assemble'**
Run the full 30-gate quality pass across all chunks, then output the final assembled Italian text.

---

## Phase 2 — Generate Typing Script (full `robotic-process-automation` skill)

Immediately after delivering the assembled text, generate the complete Python typing script with `TARGET_TEXT` set to the assembled output. Output **only** the script — no preamble.

The script implements all 7 levels:

| Level | Implementation |
|---|---|
| 1 | `pynput` Controller (Unicode-safe, Italian accents preserved) |
| 2 | Per-character micro-rhythm: 0.04–0.12s standard, 0.10–0.20s for Shift chars |
| 3 | Syntactic pauses: comma 0.3–0.8s · period/!/? 1.5–3.5s · newline 5–15s |
| 4 | 1.5% typo injection with backspace + reaction time (0.3–0.6s) |
| 5 | Cognitive pause every 400–600 chars for 10–25s |
| 6 | 10s countdown + kill-switch instructions to terminal |
| 7 | `TARGET_TEXT` hardcoded; `target_text.txt` fallback |

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai-proof-writer — Phase 2 Output
Generated typing script. Requires: pip install pynput
Usage: python typing_sim.py  (click inside target document during countdown)
Emergency stop: Ctrl+C in terminal, or move mouse to any screen corner.
"""

import time
import random
from pynput.keyboard import Controller, Key

TARGET_TEXT = """[ASSEMBLED REWRITTEN TEXT GOES HERE]"""

try:
    with open("target_text.txt", "r", encoding="utf-8") as f:
        TARGET_TEXT = f.read()
    print("[INFO] Loaded text from target_text.txt")
except FileNotFoundError:
    pass

keyboard = Controller()

def get_char_delay(char: str) -> float:
    if char.isupper() or char in '!"£$%^&*()_+{}|:<>?~@#':
        return random.uniform(0.10, 0.20)
    return random.uniform(0.04, 0.12)

def get_syntactic_pause(char: str) -> float:
    if char == ',': return random.uniform(0.3, 0.8)
    if char in '.?!': return random.uniform(1.5, 3.5)
    if char == '\n': return random.uniform(5.0, 15.0)
    return 0.0

COMMON_MISTYPE = list('asdfjklqwertyuiopzxcvbnm')
ERROR_RATE = 0.015

def maybe_inject_typo(correct_char: str) -> None:
    if correct_char.isalnum() and random.random() < ERROR_RATE:
        keyboard.type(random.choice(COMMON_MISTYPE))
        time.sleep(random.uniform(0.3, 0.6))
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
        time.sleep(random.uniform(0.1, 0.3))

def cognitive_pause(char_count: int, next_threshold: int) -> tuple[int, int]:
    if char_count >= next_threshold:
        pause_duration = random.uniform(10.0, 25.0)
        print(f"\n[COGNITIVE PAUSE] {pause_duration:.1f}s", flush=True)
        time.sleep(pause_duration)
        return 0, random.randint(400, 600)
    return char_count, next_threshold

def safety_countdown() -> None:
    print("=" * 60)
    print("  ai-proof-writer — Typing Simulator")
    print("=" * 60)
    print(f"  Characters to type: {len(TARGET_TEXT)}")
    print()
    print("  EMERGENCY STOP: Ctrl+C in terminal,")
    print("  or move mouse to any corner of the screen.")
    print()
    print("  Click inside the target document NOW.")
    print("=" * 60)
    for i in range(10, 0, -1):
        print(f"  Starting in {i}...", flush=True)
        time.sleep(1)
    print("  TYPING STARTED\n")

def main() -> None:
    safety_countdown()
    char_count = 0
    next_threshold = random.randint(400, 600)
    for char in TARGET_TEXT:
        char_count, next_threshold = cognitive_pause(char_count, next_threshold)
        maybe_inject_typo(char)
        delay = get_char_delay(char)
        if char == '\n':
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        else:
            keyboard.type(char)
        char_count += 1
        time.sleep(delay)
        syntactic = get_syntactic_pause(char)
        if syntactic > 0:
            time.sleep(syntactic)
    print("\n[DONE] All text has been typed.")

if __name__ == "__main__":
    main()
```

---

## Full Pipeline Summary

```
User provides text
       ↓
Phase 1: /italian-rewriting rules
  → Chunk 1 → 'Next' → Chunk 2 → 'Next' → ... → 'Assemble'
  → Final Italian text (all 30 gates passed)
       ↓
Phase 2: /robotic-process-automation rules
  → typing_sim.py generated with TARGET_TEXT = assembled text
       ↓
User runs: python typing_sim.py
  → Opens Word / Google Docs
  → 10s countdown
  → Text typed with human keystroke forensics
```

---

## Usage

```
/ai-proof-writer

[paste source text here]
```

Optionally specify:
- `--registro saggistico` or `--registro conversazionale` (default: accademico)
- `--file` to generate a script that reads from `target_text.txt`
