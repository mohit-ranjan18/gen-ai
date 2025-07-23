from google.adk.agents import Agent
# from google.adk.tools import google_search
from news_agent.sub_agents.agent import news_agent

# def get_weather(city: str) -> dict:
#     """Retrieves the current weather report for a specified city.

#     Returns:
#         dict: A dictionary containing the weather information with a 'status' key ('success' or 'error') and a 'report' key with the weather details if successful, or an 'error_message' if an error occurred.
#     """
#     if city.lower() == "new york":
#         return {"status": "success",
#                 "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit)."}
#     else:
#         return {"status": "error",
#                 "error_message": f"Weather information for '{city}' is not available."}

# def get_current_time(city:str) -> dict:
#     """Returns the current time in a specified city.

#     Args:
#         dict: A dictionary containing the current time for a specified city information with a 'status' key ('success' or 'error') and a 'report' key with the current time details in a city if successful, or an 'error_message' if an error occurred.
#     """
#     import datetime
#     from zoneinfo import ZoneInfo

#     if city.lower() == "new york":
#         tz_identifier = "America/New_York"
#     else:
#         return {"status": "error",
#                 "error_message": f"Sorry, I don't have timezone information for {city}."}

#     tz = ZoneInfo(tz_identifier)
#     now = datetime.datetime.now(tz)
#     return {"status": "success",
#             "report": f"""The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}"""}

# sports_agent = Agent(
#     name="supervisor_agent",
#     model="gemini-2.0-flash",
#     description="sports agent",
#     instruction="Ask user preference on news type,sport he like ,his agent and gender. If required to fetch latest update use google search tool to answer or else based on his feature return answer",
#     # sub_agents=[sports_agent]
#     tools=[google_search]
# )

root_agent = Agent(
    name="supervisor_agent",
    model="gemini-2.0-flash",
    description="Supervisor agent",
    instruction="do initial greetings ,Identify user query and route to specific sub agent , if user ask news",
    sub_agents=[news_agent]
    # tools=[get_weather, get_current_time]
)