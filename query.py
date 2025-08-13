import os
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
RESOURCE_ID = os.getenv("RESOURCE_ID")

if not PROJECT_ID or not LOCATION or not RESOURCE_ID:
    print("Error: PROJECT_ID, LOCATION, and RESOURCE_ID environment variables must be set")
    exit(1)

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
)

remote_agent = agent_engines.get(RESOURCE_ID)

user_id = "kuribo-"

# 既存のセッションがないか確認するためにセッションを一覧表示
session_list = remote_agent.list_sessions(user_id=user_id).get("sessions", [])

if session_list:
    print("Found existing session, reusing it.")
    session = session_list[0]
else:
    print("No existing session found, creating a new one.")
    session = remote_agent.create_session(user_id=user_id)

for event in remote_agent.stream_query(
    user_id=user_id,
    session_id=session["id"],
    message="whats the weather in new york",
):
    print(event)
