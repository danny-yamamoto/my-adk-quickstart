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

### Deploy the agent

```bash
python3 ./deploy.py 
```

<details>

<summary>Example log</summary>

```bash
(.venv) vscode ➜ /workspaces/my-adk-quickstart (main) $ python3 ./deploy.py 
Identified the following requirements: {'pydantic': '2.11.7', 'google-cloud-aiplatform': '1.105.0', 'cloudpickle': '3.1.1'}
The following requirements are missing: {'pydantic', 'cloudpickle'}
The following requirements are appended: {'pydantic==2.11.7', 'cloudpickle==3.1.1'}
The final list of requirements: ['google-adk>=0.1.0', 'google-cloud-aiplatform[adk,agent-engines]>=1.88.0', 'google-cloud-bigquery>=3.31.0', 'pydantic==2.11.7', 'cloudpickle==3.1.1']
/workspaces/my-adk-quickstart/.venv/lib/python3.12/site-packages/google/auth/_default.py:76: UserWarning: Your application has authenticated using end user credentials from Google Cloud SDK without a quota project. You might receive a "quota exceeded" or "API not enabled" error. See the following page for troubleshooting: https://cloud.google.com/docs/authentication/adc-troubleshooting/user-creds. 
  warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
/workspaces/my-adk-quickstart/.venv/lib/python3.12/site-packages/google/auth/_default.py:76: UserWarning: Your application has authenticated using end user credentials from Google Cloud SDK without a quota project. You might receive a "quota exceeded" or "API not enabled" error. See the following page for troubleshooting: https://cloud.google.com/docs/authentication/adc-troubleshooting/user-creds. 
  warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
Using bucket [BUCKET_NAME]
Wrote to gs://[BUCKET_NAME]/agent_engine/agent_engine.pkl
Writing to gs://[BUCKET_NAME]/agent_engine/requirements.txt
Creating in-memory tarfile of extra_packages
Writing to gs://[BUCKET_NAME]/agent_engine/dependencies.tar.gz
Creating AgentEngine
Create AgentEngine backing LRO: projects/[PROJECT_NUMBER]/locations/us-central1/reasoningEngines/[RESOURCE_ID]/operations/[OPERATION_ID]
View progress and logs at https://console.cloud.google.com/logs/query?project=[PROJECT_ID]
AgentEngine created. Resource name: projects/[PROJECT_NUMBER]/locations/us-central1/reasoningEngines/[RESOURCE_ID]
To use this AgentEngine in another session:
agent_engine = vertexai.agent_engines.get('projects/[PROJECT_NUMBER]/locations/us-central1/reasoningEngines/[RESOURCE_ID]')
(.venv) vscode ➜ /workspaces/my-adk-quickstart (main) $ 
```

</details>

### Query the agent

```bash
python3 ./query.py 
```

<details>

<summary>Example log</summary>

```bash
(.venv) vscode ➜ /workspaces/my-adk-quickstart (main) $ python3 ./query.py 
/workspaces/my-adk-quickstart/.venv/lib/python3.12/site-packages/google/auth/_default.py:76: UserWarning: Your application has authenticated using end user credentials from Google Cloud SDK without a quota project. You might receive a "quota exceeded" or "API not enabled" error. See the following page for troubleshooting: https://cloud.google.com/docs/authentication/adc-troubleshooting/user-creds. 
  warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
Found existing session, reusing it.
{'content': {'parts': [{'function_call': {'id': 'adk-[FUNCTION_ID]', 'args': {'city': 'new york'}, 'name': 'get_weather'}}], 'role': 'model'}, 'usage_metadata': {'candidates_token_count': 6, 'candidates_tokens_details': [{'modality': 'TEXT', 'token_count': 6}], 'prompt_token_count': 432, 'prompt_tokens_details': [{'modality': 'TEXT', 'token_count': 432}], 'total_token_count': 438, 'traffic_type': 'ON_DEMAND'}, 'invocation_id': '[INVOCATION_ID]', 'author': '[AGENT_NAME]', 'actions': {'state_delta': {}, 'artifact_delta': {}, 'requested_auth_configs': {}}, 'long_running_tool_ids': [], 'id': '[MESSAGE_ID]', 'timestamp': [TIMESTAMP]}
{'content': {'parts': [{'function_response': {'id': 'adk-[FUNCTION_ID]', 'name': 'get_weather', 'response': {'status': 'success', 'report': 'The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit).'}}}], 'role': 'user'}, 'invocation_id': '[INVOCATION_ID]', 'author': '[AGENT_NAME]', 'actions': {'state_delta': {}, 'artifact_delta': {}, 'requested_auth_configs': {}}, 'id': '[MESSAGE_ID]', 'timestamp': [TIMESTAMP]}
{'content': {'parts': [{'text': 'The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit).'}], 'role': 'model'}, 'usage_metadata': {'candidates_token_count': 22, 'candidates_tokens_details': [{'modality': 'TEXT', 'token_count': 22}], 'prompt_token_count': 466, 'prompt_tokens_details': [{'modality': 'TEXT', 'token_count': 466}], 'total_token_count': 488, 'traffic_type': 'ON_DEMAND'}, 'invocation_id': '[INVOCATION_ID]', 'author': '[AGENT_NAME]', 'actions': {'state_delta': {}, 'artifact_delta': {}, 'requested_auth_configs': {}}, 'id': '[MESSAGE_ID]', 'timestamp': [TIMESTAMP]}
(.venv) vscode ➜ /workspaces/my-adk-quickstart (main) $ 
```

</details>
