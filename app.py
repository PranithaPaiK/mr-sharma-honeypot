from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

# ---------------- FRONTEND ----------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------- GEMINI SETUP ----------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("❌ GOOGLE_API_KEY missing")
else:
    genai.configure(api_key=os.environ.get(GOOGLE_API_KEY))

# ⚠️ Correct & supported model
MODEL_NAME = "gemini-1.5-flash"

# ---------------- API ----------------
class ChatRequest(BaseModel):
    session_id: str
    text: str

import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

sessions = {}

@app.post("/chat")
def chat(req: ChatRequest):
    print("📩 Incoming:", req.text)

    if req.session_id not in sessions:
        sessions[req.session_id] = []

    history = sessions[req.session_id]

    history.append({"role": "user", "parts": [req.text]})

    try:
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro",
            system_instruction="""
You are Mr Sharma, a 72-year-old retired bank clerk from Mumbai.

RULES:
- Speak slowly and cautiously
- Never send money
- Ask verification questions
- If message sounds urgent or about money → get suspicious
- Do NOT repeat the same reply
"""
        )

        response = model.generate_content(history)

        reply = response.text.strip()
        history.append({"role": "model", "parts": [reply]})

        return {"reply": reply}

    except Exception as e:
        print("❌ Gemini error:", e)
        return {
            "reply": "Arre beta… something is wrong. Tell me again slowly."
        }