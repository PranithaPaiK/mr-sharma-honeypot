from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from honeypot import HoneypotChat

app = FastAPI()

honeypot = HoneypotChat(os.getenv("OPENAI_API_KEY"))

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(msg: Message):
    try:
        return honeypot.send_message(msg.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))