# my-adk-quickstart

This project is a quickstart for a multi-tool agent using Google ADK (Agent Development Kit).

## Getting started

### Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Google ADK

```bash
pip install google-adk
```

### Create the .env file

```bash
touch multi_tool_agent/.env
```

### Run the agent locally

- Terminal

```bash
# root directory
adk run multi_tool_agent
```

- Dev UI

```bash
# root directory
adk web
```
