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
    genai.configure(api_key=GOOGLE_API_KEY)

# ⚠️ Correct & supported model
MODEL_NAME = "gemini-1.5-flash"

# ---------------- API ----------------
class ChatRequest(BaseModel):
    session_id: str
    text: str

@app.post("/chat")
def chat(req: ChatRequest):
    print("📩 Incoming request:", req.dict())

    if not GOOGLE_API_KEY:
        return {
            "reply": "Arre beta… system is not ready. API key missing."
        }

    if not req.text or req.text.strip() == "":
        return {
            "reply": "Arre beta… you didn’t say anything. Speak clearly."
        }

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are Mr Sharma, a 72-year-old retired bank clerk from Mumbai.
You are slow, polite, slightly confused, and cautious.
Never agree to send money.
If someone sounds suspicious, act doubtful and defensive.

User says:
{req.text}
"""

        response = model.generate_content(prompt)

        return {
            "reply": response.text
        }

    except Exception as e:
        print("❌ Gemini exception:", e)
        return {
            "reply": "Arre beta… my phone is not working properly. Please repeat slowly."
        }