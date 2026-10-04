# Snake Game (Inside snake-game)

This directory contains a terminal-based Snake game implemented in pure Python.

Author: Arvind Gadde

How to run:
- From project root: python snake-game/main.py
- Or as you prefer using your 'uv' command: uv snake-game/main.py

Dependencies:
- Python 3.14 or newer (uses only standard library)
- Optional: openai library if you add AI features

Controls:
- Arrow keys or WASD to move
- P to pause
- Q to quit
- R to restart after game over

Files:
- main.py - main game implementation
- highscore.txt - created after first run to store high score

Notes:
This terminal game uses different input handling for Windows and Unix-like systems. It attempts to be simple and self-contained.
