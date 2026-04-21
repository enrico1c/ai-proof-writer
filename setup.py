#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai-proof-writer — Setup & Permission Checker
Run once after cloning: python setup.py
"""

import sys
import subprocess
import platform
import time

REQUIRED = ["pynput"]

def banner(msg: str) -> None:
    print("\n" + "=" * 60)
    print(f"  {msg}")
    print("=" * 60)

def check_python() -> None:
    banner("Checking Python version")
    v = sys.version_info
    if v < (3, 10):
        print(f"  [ERROR] Python 3.10+ required. Found {v.major}.{v.minor}")
        sys.exit(1)
    print(f"  [OK] Python {v.major}.{v.minor}.{v.micro}")

def install_dependencies() -> None:
    banner("Installing dependencies")
    for pkg in REQUIRED:
        print(f"  Installing {pkg}...", end=" ", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", pkg],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("OK")
        else:
            print(f"FAILED\n{result.stderr}")
            sys.exit(1)

def check_pynput_permissions() -> None:
    banner("Verifying pynput keyboard access")
    os_name = platform.system()

    if os_name == "Darwin":   # macOS
        print("""
  [macOS] pynput requires Accessibility permission.

  Steps to grant it:
    1. Open: System Settings > Privacy & Security > Accessibility
    2. Click the '+' button
    3. Add your Terminal app (or iTerm / VS Code if running from there)
    4. Re-run this script after granting permission.

  Without this, the typing script will fail silently.
""")
        input("  Press ENTER once you have granted Accessibility access...")

    elif os_name == "Linux":
        print("""
  [Linux] pynput requires access to /dev/input or X11/Wayland.

  For X11 (most common):
    - No extra steps needed if running as the display owner.

  For Wayland or headless environments:
    - You may need to run as root, or add your user to the 'input' group:
      sudo usermod -aG input $USER
    - Log out and back in for the change to take effect.
""")

    elif os_name == "Windows":
        print("  [Windows] No special permissions required for pynput.")

    # Functional smoke-test: create the controller without actually pressing keys
    try:
        from pynput.keyboard import Controller, Key
        kb = Controller()
        print(f"  [OK] pynput Controller initialised on {os_name}.")
    except Exception as e:
        print(f"  [ERROR] pynput failed to initialise: {e}")
        sys.exit(1)

def print_next_steps() -> None:
    banner("Setup complete")
    print("""
  How to use ai-proof-writer:

    1. Start a new Claude Code session.
    2. Invoke: /ai-proof-writer
    3. Paste the source text you want rewritten.
    4. Claude will:
         Phase 1 — rewrite the text chunk-by-chunk using the
                   italian-rewriting skill (type 'Next' between chunks).
         Phase 2 — after you type 'Assemble', generate the
                   robotic-process-automation Python script.
    5. Save the generated script as typing_sim.py.
    6. Open a blank Word document (or Google Docs).
    7. Run:  python typing_sim.py
    8. Click inside the document during the 10-second countdown.

  Emergency stop during typing: Ctrl+C in the terminal,
  or move the mouse to any corner of the screen.
""")

if __name__ == "__main__":
    check_python()
    install_dependencies()
    check_pynput_permissions()
    print_next_steps()
