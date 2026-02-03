import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from honeypot import HoneypotChat

load_dotenv()

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder (NOT inside static)
templates = Jinja2Templates(directory="templates")

# Home page (FRONTEND)
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# Health check (API)
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Mr. Sharma Honeypot API is running 🚀"
    }

# Chat API
class Message(BaseModel):
    text: str

honeypot = HoneypotChat()

@app.post("/chat")
def chat(msg: Message):
    return honeypot.send_message(msg.text)