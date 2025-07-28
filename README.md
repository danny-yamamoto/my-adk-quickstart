# my-adk-quickstart

このプロジェクトは Google ADK (Agent Development Kit) を使用したマルチツールエージェントのクイックスタートです。

## Getting started

### 1. 仮想環境の作成とアクティベート
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Google ADK のインストール
```bash
pip install google-adk
```

### 3. エージェントディレクトリとファイルの作成
```bash
mkdir multi_tool_agent/
echo "from . import agent" > multi_tool_agent/__init__.py
touch multi_tool_agent/agent.py
touch multi_tool_agent/.env
```

### 4. エージェントの実行
```bash
adk run multi_tool_agent
```
