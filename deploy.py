import os
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines
from multi_tool_agent.agent import root_agent

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
STAGING_BUCKET = os.getenv("STAGING_BUCKET")
DISPLAY_NAME = os.getenv("DISPLAY_NAME")
DESCRIPTION = os.getenv("DESCRIPTION")

if not PROJECT_ID or not LOCATION or not STAGING_BUCKET or not DISPLAY_NAME or not DESCRIPTION:
    print("Error: PROJECT_ID, LOCATION, STAGING_BUCKET, DISPLAY_NAME, and DESCRIPTION environment variables must be set")
    exit(1)

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)


def main():

    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    remote_app = agent_engines.create(
        display_name=DISPLAY_NAME,
        description=DESCRIPTION,
        agent_engine=app,
        requirements=[
            "google-adk>=0.1.0",
            "google-cloud-aiplatform[adk,agent-engines]>=1.88.0",
            "google-cloud-bigquery>=3.31.0",
        ],
        extra_packages=['multi_tool_agent']
    )


if __name__ == "__main__":
    main()
