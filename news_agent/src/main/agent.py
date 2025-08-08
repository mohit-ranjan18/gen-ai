from google.adk.agents import Agent
# from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService,Session
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai import types
from src.main.prompts import NEWS_RESULT_AGENT_PROMPT
from google.adk.tools.agent_tool import AgentTool
from src.main.sub_agents.agent import web_search_agent
# from tools import fetch_preferences

# https://chatgpt.com/share/687bef11-b550-8003-8292-eb44ef000c9b

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

load_dotenv()

import requests


from pydantic import BaseModel
from typing import List, Dict, Union
from datetime import datetime


class PreferenceNewsItem(BaseModel):
    name: str
    description: str
    datetime: float  # or use datetime if it's converted
    status: str
    news: List[str]


class NewsFetchedResponse(BaseModel):
    news_fetched: List[PreferenceNewsItem]


def fetch_preferences() -> dict:
    """
    Fetch user preferences from the news hub API.

    This method does not take any input.

    Returns:
        dict: Contains:
            - 'status': str
            - 'preferences': List[dict] with keys: 'name', 'description', 'datetime', 'status'

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: If the response status is not 'success' or JSON can't be parsed.
    """
    url = "https://news-hub-be-dev.up.railway.app/v1/preference"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        status = data.get("status", "unknown")
        if status != "success":
            error_msg = data.get("message", "Unknown error from API")
            raise ValueError(f"API Error: {error_msg}")

        preferences_data = data.get("data", {}).get("preferences", [])

        preferences = [
            {
                "name": pref.get("name"),
                "description": pref.get("description"),
                "datetime": pref.get("datetime"),
                "status": pref.get("status")
            }
            for pref in preferences_data[:2]
        ]

        return {
            "status": status,
            "preferences": preferences
        }

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise
    except (ValueError, KeyError, TypeError) as e:
        print(f"Error parsing response: {e}")
        raise

root_agent = Agent(
    name="news_agent",
    model="gemini-2.0-flash",
    # output_schema=NewsFetchedResponse,
    description="Gives latest info or best news using websearch agent",
    instruction=NEWS_RESULT_AGENT_PROMPT,
    # sub_agents=[sports_agent]
    tools=[fetch_preferences,AgentTool(web_search_agent)]
)

print(f"Agent '{root_agent.name}")



async def main():
    APP_NAME = "news_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001"
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    
    runner = Runner(
    agent=root_agent,
    app_name="news_app",
    session_service=session_service
    )
    print(f"Runner created for agent '{runner.agent.name}'.")
    return SESSION_ID,runner


async def call_agent_async(query: str, user_id, session_id,runner):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      print("News agent is fetching...")
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found
      print(f"<<< Agent Response: {final_response_text}")
  return final_response_text

  print(f"<<< Agent Response: {final_response_text}")

runner_store = {}

async def get_or_create_runner(app_name, user_id, session_id):
    global runner_store

    key = f"{app_name}:{user_id}:{session_id}"
    if key in runner_store:
        return runner_store[key]

    # Create new session and runner
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service
    )
    runner_store[key] = runner
    return runner



# if __name__ == "__main__":
#     # Define constants for identifying the interaction context
#     session_id ,runner =  asyncio.run(main())
#     asyncio.run(call_agent_async("get me news","user_1",session_id,runner))