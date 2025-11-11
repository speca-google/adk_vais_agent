# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
from dotenv import load_dotenv
from google.adk.tools import VertexAiSearchTool

# Load environment variables from the .env file
load_dotenv()

# Configuration file name
CONFIG_FILE = "tools_config.json"

# Default Fallback Credentials (from .env)
DEFAULT_PROJECT_ID = os.environ.get("VAIS_PROJECT_ID")
DEFAULT_LOCATION_ID = os.environ.get("VAIS_LOCATION_ID", "global")


def _load_tool_config() -> list:
    """
    Internal helper to load the tool configuration from the JSON file.
    Returns a list of tool dictionaries.
    """
    try:
        base_path = os.path.dirname(__file__)
        config_path = os.path.join(base_path, CONFIG_FILE)
        
        if not os.path.exists(config_path):
            print(f"WARNING: Config file {CONFIG_FILE} not found. No tools loaded.")
            return []

        with open(config_path, 'r') as f:
            return json.load(f)
            
    except Exception as e:
        print(f"ERROR: Failed to load tool config: {e}")
        return []


def get_tools_summary_for_prompt() -> str:
    """
    Generates a formatted string summarizing the available tools and their descriptions.
    This is used to inject context into the Agent's system prompt so it knows
    what data sources it has access to.

    Returns:
        str: A bulleted list of tool names and descriptions.
    """
    tools_config = _load_tool_config()
    
    if not tools_config:
        return "No specific data stores are currently configured."

    summary_lines = []
    for tool_conf in tools_config:
        name = tool_conf.get("name", "Unnamed Tool")
        description = tool_conf.get("description", "No description provided.")
        summary_lines.append(f"- **{name}**: {description}")
    
    return "\n".join(summary_lines)


def load_vais_tools_from_config() -> list:
    """
    Reads the 'tools_config.json' file and instantiates a VertexAiSearchTool
    for each entry found.

    Returns:
        list: A list of configured VertexAiSearchTool instances.
    """
    vais_tools_list = []
    tools_config = _load_tool_config()

    print(f"--- Loading Vertex AI Search Tools from {CONFIG_FILE} ---")

    for tool_conf in tools_config:
        try:
            # Extract configuration
            name = tool_conf.get("name")
            description = tool_conf.get("description")
            datastore_id = tool_conf.get("datastore_id")
            
            # Optional overrides with fallbacks to .env defaults
            project_id = tool_conf.get("project_id") or DEFAULT_PROJECT_ID
            location_id = tool_conf.get("location_id") or DEFAULT_LOCATION_ID

            if not datastore_id or not project_id:
                print(f"Skipping tool '{name}': Missing datastore_id or project_id.")
                continue

            # Construct the full resource path required by the tool
            # Format: projects/{project}/locations/{location}/collections/default_collection/dataStores/{datastore_id}
            datastore_path = (
                f"projects/{project_id}/locations/{location_id}/"
                f"collections/default_collection/dataStores/{datastore_id}"
            )

            # Instantiate the Built-in VertexAiSearchTool
            tool_instance = VertexAiSearchTool(data_store_id=datastore_path)
            
            # IMPORTANT: Override the tool's name and description so the LLM knows 
            # specifically what this instance is for (e.g., "engineering_docs" vs "hr_policies").
            # The ADK/LangChain integration uses these fields for tool selection.
            tool_instance.name = name
            tool_instance.description = description

            vais_tools_list.append(tool_instance)
            print(f"Successfully loaded tool: {name}")

        except Exception as e:
            print(f"Error loading tool '{tool_conf.get('name')}': {e}")

    print(f"--- Loaded {len(vais_tools_list)} tools ---")
    return vais_tools_list

# --- Module Level Execution ---
# Initialize the tools list so it can be imported by agent.py as `tools.vais_tools`
vais_tools = load_vais_tools_from_config()