import os
from fastapi import FastAPI, Request
from fastapi.templating import jinja2Templates
from fastapi.static files import staticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from honeypot import HoneypotChat

# Load env variables
load_dotenv()

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve templates (HTML)
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# Initialize honeypot once
honeypot = HoneypotChat()

class Message(BaseModel):
    text: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
def chat(msg: Message):
    return honeypot.send_message(msg.text)