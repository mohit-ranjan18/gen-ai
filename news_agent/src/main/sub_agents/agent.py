from google.adk.agents import Agent
from google.adk.tools import google_search





web_search_agent = Agent(
    name="web_search_agent",
    model="gemini-2.0-flash",
    description="search internet for latest update",
    instruction="Fetch latest information based on user query",
    # sub_agents=[sports_agent]
    tools=[google_search]
)