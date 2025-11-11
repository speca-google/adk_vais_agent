# Vertex AI Search ADK Agent

This project implements an intelligent agent using the Google Agent Development Kit (ADK). The agent is capable of understanding questions in natural language and routing them to the appropriate Vertex AI Search (VAIS) Datastore based on the topic (e.g., Engineering docs, HR policies, etc.).

The key feature of this agent is its ability to support **multiple knowledge bases**. By configuring a simple JSON file, the agent dynamically creates search tools and uses its reasoning capabilities to decide which source to query to answer the user's request.

## Project Structure
```
/adk_vais_agent/                      # Root project folder
|
├── .venv/                            # Virtual environment directory
|
├── adk_vais_agent/                   # Python package containing the agent's source code
│   ├── __init__.py                   # Makes the directory a Python package
│   ├── .env                          # File to store credentials (not versioned)
│   ├── agent.py                      # Defines the main agent and routing logic
│   ├── config.yaml                   # Agent deployment settings
│   ├── tools_config.json             # JSON configuration for multiple Datastores
│   ├── prompt.py                     # Stores the agent's instructions and guidelines
│   └── tools.py                      # Logic to dynamically load Search tools
|
├── deploy_agent_engine.ipynb         # Python notebook to step-by-step deploy on Vertex Agent Engine
├── requirements.txt                  # File listing Python dependencies
└── README.md                         # This file
```

## Prerequisites

* Python 3.12 or higher
* Access to a Google Cloud Project with **Vertex AI Search and Conversation** API enabled.
* Existing Data Stores created in Vertex AI Search (e.g., Website search, Unstructured data).
* Appropriate IAM permissions to access the Data Stores (e.g., `Discovery Engine Viewer` or `Discovery Engine Editor`).

## Installation and Execution Guide

Follow the steps below to set up and run the project.

### 1. Clone the Repository (Optional)

If you are starting on a new machine, clone the repository.

```bash
git clone git@github.com:your-org/adk_vais_agent.git
cd adk_vais_agent
```

### 2. Create and Activate the Virtual Environment (venv)

It is a good practice to isolate the project's dependencies in a virtual environment.

Create the virtual environment:
```bash
python -m venv .venv
```

Activate the virtual environment:
```bash
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` inside the `adk_vais_agent/` directory.

**`adk_vais_agent/.env` Example:**

```env
# --- Vertex AI Settings ---
GOOGLE_GENAI_USE_VERTEXAI="True"
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"   # Project ID from GCP
GOOGLE_CLOUD_LOCATION="us-central1"          # Location where the agent will be deployed
GOOGLE_CLOUD_BUCKET="gs://your-agent-bucket" # Bucket for deployment

# --- Agent Models ---
ROOT_AGENT_MODEL="gemini-2.5-flash"

# --- Vertex AI Search Defaults ---
# Fallback values if not specified in tools_config.json
VAIS_PROJECT_ID="your-gcp-project-id"
VAIS_LOCATION_ID="global"                    # Often 'global' or 'us-central1'
```

### 5. Configure Search Tools

Open the `adk_vais_agent/tools_config.json` file. This is where you define which Data Stores your agent can access.

**Format:**
* **name**: A unique name for the tool (used by the LLM).
* **description**: A clear description of what this datastore contains. **Crucial**: The agent uses this text to decide when to call this tool.
* **datastore_id**: The ID of your Vertex AI Search Datastore.

**Example `tools_config.json`:**
```json
[
  {
    "name": "engineering_docs",
    "description": "Search for technical architecture, API references, and system design documents.",
    "datastore_id": "engineering-ds-id-123",
    "location_id": "global",
    "project_id": "" 
  },
  {
    "name": "hr_policies",
    "description": "Search for employee benefits, leave policies, and code of conduct.",
    "datastore_id": "hr-ds-id-456",
    "location_id": "us-central1",
    "project_id": "optional-different-project-id"
  }
]
```

### 6. Run the Agent Locally for Testing

Now that everything is configured, you can start the agent using the ADK web interface.

Make sure you are in the root directory:
```bash
adk web
```
The `adk web` command will open a web UI to test your agent. 

**Authentication Note:**
If you encounter permission errors, ensure you are authenticated with Google Cloud credentials that have access to the defined Datastores:
```bash
gcloud auth application-default login
```

### 7. Deploy this agent on Agent Engine

To deploy this agent to Vertex AI Agent Engine, use the Python Notebook `deploy_agent_engine.ipynb`. This file contains a step-by-step guide for deployment.