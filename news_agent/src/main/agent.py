import os
import asyncio
from typing import Optional
from google.adk.agents import Agent
# from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService,Session
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.genai.types import Part, Content
from google.genai import types
from src.main.prompts import NEWS_RESULT_AGENT_PROMPT
from google.adk.tools.agent_tool import AgentTool
from src.main.sub_agents.agent import web_search_agent

# https://chatgpt.com/share/687bef11-b550-8003-8292-eb44ef000c9b

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

load_dotenv()

root_agent = Agent(
    name="news_agent",
    model="gemini-2.0-flash",
    description="Gives latest info or best news using websearch agent",
    instruction=NEWS_RESULT_AGENT_PROMPT,
    # sub_agents=[sports_agent]
    tools=[AgentTool(web_search_agent)]
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