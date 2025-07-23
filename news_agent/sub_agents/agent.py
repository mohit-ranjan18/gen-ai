from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from news_agent.sub_agents.prompts import NEWS_RESULT_AGENT_PROMPT



web_search_agent = Agent(
    name="web_search_agent",
    model="gemini-2.0-flash",
    description="search internet for latest update",
    instruction="Fetch latest information based on user query",
    # sub_agents=[sports_agent]
    tools=[google_search]
)

news_agent = Agent(
    name="news_agent",
    model="gemini-2.0-flash",
    description="Gives latest info or best news using websearch agent",
    instruction=NEWS_RESULT_AGENT_PROMPT,
    # sub_agents=[sports_agent]
    tools=[AgentTool(web_search_agent)]
)