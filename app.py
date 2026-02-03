import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from honeypot import HoneypotChat

app = FastAPI()

# CORS (safe for your use-case)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates (HTML)
templates = Jinja2Templates(directory="static/templates")

honeypot = HoneypotChat()

class Message(BaseModel):
    text: str

# 🔹 FRONTEND ROUTE (THIS WAS MISSING)
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# 🔹 CHAT API
@app.post("/chat")
def chat(msg: Message):
    try:
        return honeypot.send_message(msg.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 HEALTH CHECK
@app.get("/health")
def health():
    return {"status": "ok"}