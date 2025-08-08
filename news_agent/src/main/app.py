from fastapi import FastAPI, Request
from pydantic import BaseModel
from src.main import agent  # import your agent module
import json
import re
from .agent import NewsFetchedResponse 

app = FastAPI()

# Define a request body model
class ChatRequest(BaseModel):
    app_name: str  #
    user_id: str
    session_id: str
    query: str

 # your Pydantic model

def extract_and_validate_response(agent_output: str) -> NewsFetchedResponse:
    # Step 1: Remove triple backticks and optional 'json' tag
    if agent_output.strip().startswith("```json"):
        agent_output = agent_output.strip().lstrip("```json").rstrip("```").strip()
    elif agent_output.strip().startswith("```"):
        agent_output = agent_output.strip().lstrip("```").rstrip("```").strip()

    # Step 2: Load JSON string to Python dict
    try:
        response_dict = json.loads(agent_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}\n\nRaw output:\n{agent_output}")

    # Step 3: Validate against Pydantic schema
    try:
        validated = NewsFetchedResponse.model_validate(response_dict)
    except Exception as e:
        raise ValueError(f"Pydantic validation failed: {e}")

    return validated

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

@app.post("/chat")
async def chat_with_agent(chat: ChatRequest):
    # get the runner and session
    runner = await agent.get_or_create_runner(chat.app_name, chat.user_id, chat.session_id)

    
    # call agent
    response = await agent.call_agent_async(chat.query, chat.user_id, chat.session_id, runner)
    print(response,type(response))
    structured_response = extract_and_validate_response(response)
    print(structured_response)
    
    return {"response": structured_response}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)