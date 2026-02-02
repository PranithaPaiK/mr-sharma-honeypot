import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from honeypot import HoneypotChat

# Load env variables
load_dotenv()

app = FastAPI()

# Initialize honeypot once
honeypot = HoneypotChat()

class Message(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
def chat(msg: Message):
    return honeypot.send_message(msg.text)