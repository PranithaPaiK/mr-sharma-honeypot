from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from honeypot import HoneypotChat

app = FastAPI()

honeypot = HoneypotChat()

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(msg: Message):
    try:
        return honeypot.send_message(msg.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Mr. Sharma Honeypot API is running 🚀"
    }