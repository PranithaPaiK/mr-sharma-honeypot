from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from honeypot import HoneypotChat

app = FastAPI()

# CORS (frontend support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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