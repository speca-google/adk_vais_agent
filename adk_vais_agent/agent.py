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
from google.adk.agents import Agent
from dotenv import load_dotenv

# Import the list of dynamically loaded tools and the prompt
from . import tools
from .prompt import VAIS_AGENT_PROMPT

# Load environment variables from the .env file
load_dotenv()

# --- Agent Definition ---

# The name of the model to be used by the root agent.
ROOT_AGENT_MODEL = os.environ.get("ROOT_AGENT_MODEL", "gemini-2.5-flash")

# Get the list of tools loaded from tools_config.json
available_tools = tools.vais_tools

if not available_tools:
    print("WARNING: No tools were loaded. Please check 'tools_config.json' and your .env file.")
else:
    print(f"Agent initialized with {len(available_tools)} Vertex AI Search tool(s).")

# This is the main agent. It now has access to multiple tools.
# The model will decide which tool to call based on the user's question
# and the 'description' provided in the tools_config.json for each tool.
root_agent = Agent(
    name="multi_source_search_agent",
    model=ROOT_AGENT_MODEL,
    description="An agent that routes user questions to the appropriate Vertex AI Search datastore based on the topic.",
    instruction=VAIS_AGENT_PROMPT,
    tools=available_tools
)