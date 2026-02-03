import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from honeypot import HoneypotChat

load_dotenv()

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/health")
def health():
    return {"status": "ok"}

class Message(BaseModel):
    text: str

conversation_history= []

honeypot = HoneypotChat()

@app.post("/chat")
def chat(msg: Message):
    # Add user message
    conversation_history.append({
        "role": "user",
        "content": msg.text
    })

    # Get response from honeypot
    reply = honeypot.send_message(conversation_history)

    # Add assistant reply
    conversation_history.append({
        "role": "assistant",
        "content": reply["message"]
    })

    return reply
    @app.post("/reset")
    async def reset():
        conversation_history.clear()
        return {"status": "conversation reset"}