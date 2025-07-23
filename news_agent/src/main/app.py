from fastapi import FastAPI, Request
from pydantic import BaseModel
from src.main import agent  # import your agent module

app = FastAPI()

# Define a request body model
class ChatRequest(BaseModel):
    app_name: str  #
    user_id: str
    session_id: str
    query: str

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

@app.post("/chat")
async def chat_with_agent(chat: ChatRequest):
    # get the runner and session
    runner = await agent.get_or_create_runner(chat.app_name, chat.user_id, chat.session_id)

    
    # call agent
    response = await agent.call_agent_async(chat.query, chat.user_id, chat.session_id, runner)
    
    return {"response": response}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
