# Agent Harness

This project is a small Python playground for experimenting with AI-powered coding assistants and local terminal tools. It combines a few lightweight prototypes built around the OpenAI API, plus a terminal-based Snake game as a fun companion project.

## What I built

### 1. Simple OpenAI chat app with memory
File: `agent_with_memory.py`

This script creates a basic chat loop where the assistant remembers the previous conversation and responds to follow-up questions. It:
- loads environment variables from `.env`
- creates an OpenAI client
- stores past messages in a list
- keeps the conversation going until the user types `quit`

### 2. Coding assistant harness with built-in tools
File: `coding-assistant-harness.py`

This is the more advanced prototype. It gives the model access to tools that can:
- list files in a directory
- read a file
- write a file
- run shell commands after user approval

The assistant can operate as a lightweight terminal-based coding agent by using tool calls to inspect and modify the workspace.

### 3. Standalone agent prototype
File: `standalone_agent.py`

This script demonstrates a minimal autonomous agent pattern using a system prompt and tool definitions. It is a simpler version of the same idea: ask the model to act like a terminal coding agent and use functions to perform work.

### 4. Snake game
Folder: `snake-game/`

This project also includes a terminal Snake game in pure Python. It is a self-contained game that runs in the terminal and supports:
- keyboard controls
- score tracking
- pause and restart
- high score persistence

## Tech stack
- Python 3.14+
- OpenAI Python SDK
- python-dotenv
- uv for dependency management

## Project structure

```text
agent-harness/
├── .env
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── agent_with_memory.py
├── coding-assistant-harness.py
├── standalone_agent.py
├── snake-game/
│   ├── README.md
│   ├── main.py
│   └── highscore.txt
└── uv.lock
```

## Setup

1. Create a virtual environment or use the included `.venv`.
2. Add your OpenAI API key to `.env`:

```env
OPENAI_API_KEY=your_key_here
```

3. Install dependencies:

```bash
uv sync
```

Or with pip:

```bash
pip install openai python-dotenv
```

## Run the projects

### Chat app with memory
```bash
python agent_with_memory.py
```

### Coding assistant harness
```bash
python coding-assistant-harness.py
```

### Standalone agent prototype
```bash
python standalone_agent.py
```

### Snake game
```bash
python snake-game/main.py
```

## Notes

This repo is meant as a learning and experimentation space for building AI assistant behaviors in a local environment. The focus is to explore:
- how to wire an LLM to tools
- how to maintain conversational memory
- how to let an agent inspect and edit files
- how to prototype useful terminal experiences

## Author
Arvind Gadde
