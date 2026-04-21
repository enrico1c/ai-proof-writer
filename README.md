# ai-proof-writer

A two-phase pipeline that rewrites text into undetectable Italian prose and then types it into a word processor with forensic-level human keystroke simulation.

---

## What it does

| Phase | Skill | What it produces |
|-------|-------|-----------------|
| 1 | `italian-rewriting` | Rewrites any source text into academic Italian prose that passes GPTZero, Originality, and ZeroGPT |
| 2 | `robotic-process-automation` | Generates a Python script that physically types the rewritten text with human-like keystroke timing and typo patterns |
| Full pipeline | `ai-proof-writer` | Runs both phases end-to-end automatically |

---

## Requirements

### 1. Claude Code (mandatory)

The skills are slash commands for **Claude Code** — Anthropic's official CLI.

- Download: https://claude.ai/download (Desktop app) or install via npm:
  ```bash
  npm install -g @anthropic-ai/claude-code
  ```
- Requires an Anthropic account with an active Claude subscription (Pro or above recommended for long documents).
- Claude Code must be version that supports custom slash commands (`~/.claude/commands/`).

### 2. Python 3.10 or higher (for Phase 2)

The typing script generated in Phase 2 requires Python 3.10+.

Check your version:
```bash
python --version
```

Download: https://www.python.org/downloads/

### 3. pynput (Python library)

The typing script uses `pynput` to control the keyboard. Install it once:
```bash
pip install pynput
```

Or run the included setup script (recommended — it also checks permissions):
```bash
python setup.py
```

---

## Platform permissions

### Windows
No special permissions required. `pynput` works out of the box.

### macOS
`pynput` requires **Accessibility permission** to control the keyboard.

Steps:
1. Open **System Settings → Privacy & Security → Accessibility**
2. Click **+** and add your Terminal app (or iTerm / VS Code if running from there)
3. Re-run `python setup.py` after granting permission

Without this, the typing script will fail silently.

### Linux
For X11 (most common setups): no extra steps needed if running as the display owner.

For Wayland or headless environments:
```bash
sudo usermod -aG input $USER
# Log out and back in for the change to take effect
```

---

## Installation

### Step 1 — Install Claude Code

See requirements above.

### Step 2 — Copy skill files to Claude Code commands directory

```bash
# macOS / Linux
cp italian-rewriting.md ~/.claude/commands/
cp robotic-process-automation.md ~/.claude/commands/
cp ai-proof-writer.md ~/.claude/commands/

# Windows (PowerShell)
Copy-Item italian-rewriting.md "$env:USERPROFILE\.claude\commands\"
Copy-Item robotic-process-automation.md "$env:USERPROFILE\.claude\commands\"
Copy-Item ai-proof-writer.md "$env:USERPROFILE\.claude\commands\"
```

### Step 3 — Run setup (installs pynput + checks permissions)

```bash
python setup.py
```

---

## Usage

### Full pipeline (rewrite + typing script)

Open Claude Code and run:
```
/ai-proof-writer

[paste your source text here]
```

Claude will:
1. Split the text into chunks and rewrite each one interactively (type `Next` between chunks, `Assemble` after the last one)
2. Deliver the final assembled Italian text
3. Generate a ready-to-run Python typing script

Save the script as `typing_sim.py`, open a blank Word document or Google Docs, then:
```bash
python typing_sim.py
```
Click inside the document during the 10-second countdown. The script types the text automatically.

**Emergency stop:** `Ctrl+C` in the terminal, or move the mouse to any corner of the screen.

---

### Rewriting only

```
/italian-rewriting

[paste source text]
```

### Typing script only (for already-rewritten text)

```
/robotic-process-automation

[paste finalized text]
```

---

## Skill details

### `italian-rewriting`

Rewrites source material (PDF extract, raw text, docx content) into natural Italian prose designed to pass AI detectors.

**What it targets:**
- GPTZero, Originality.ai, ZeroGPT, and trained human editors
- 4 layers of anti-detection rules covering lexical, syntactic, linguist-level, and micro-syntactic fingerprints
- Systemic fixes for perplexity, logical non-linearity, and burstiness
- 30 quality gates applied per chunk

**How it works:**
- Splits long texts into 400–600 word chunks automatically
- Maintains a Continuity Ledger across chunks (noun variants, structural elements, seam continuity)
- Interactive loop: pauses after each chunk and waits for `Next` or `Assemble`
- Verifies every factual claim against the source — nothing is invented

**Authorizations needed:** Claude Code subscription only. No external APIs.

---

### `robotic-process-automation`

Takes finalized text and generates a Python script that physically types it into any word processor, simulating human keystroke patterns at the forensic level.

**7 simulation levels:**
| Level | What it does |
|-------|-------------|
| 1 | `pynput` keyboard controller — Unicode-safe, preserves Italian accents (è, à, ò) |
| 2 | Per-character micro-rhythm: 0.04–0.12s standard, 0.10–0.20s for capitals/special chars |
| 3 | Syntactic pauses: comma 0.3–0.8s · period/!/? 1.5–3.5s · newline 5–15s |
| 4 | 1.5% typo injection with backspace + human reaction time (0.3–0.6s) |
| 5 | Cognitive pause every 400–600 characters for 10–25s (simulates re-reading) |
| 6 | 10-second countdown + kill-switch instructions before typing starts |
| 7 | `TARGET_TEXT` hardcoded in script; optional `target_text.txt` file fallback |

**Authorizations needed:**
- Claude Code subscription (to generate the script)
- `pynput` installed (`pip install pynput`)
- Platform keyboard access permissions (see Platform permissions above)

---

### `ai-proof-writer`

Orchestrates both skills end-to-end. Invoke this when you want the full pipeline: rewritten Italian text + ready-to-run typing script in one session.

**Authorizations needed:**
- Claude Code subscription
- `pynput` installed
- Platform keyboard access permissions

---

## File structure

```
ai-proof-writer/
├── README.md                       — this file
├── setup.py                        — installs pynput, checks platform permissions
├── ai-proof-writer.md              — orchestrating skill (install to ~/.claude/commands/)
├── italian-rewriting.md            — rewriting skill (install to ~/.claude/commands/)
└── robotic-process-automation.md   — typing simulator skill (install to ~/.claude/commands/)
```

---

## Optional: register shortcut

Add to your shell profile for quick access:

```bash
# .bashrc / .zshrc
alias apw='claude /ai-proof-writer'
```
