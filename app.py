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
    if not GOOGLE_API_KEY:
        return {
            "reply": "Arre beta… system is not ready. API key missing."
        }

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(req.text)

        return {
            "reply": response.text
        }

    except Exception as e:
        # 🔥 THIS prevents ASGI crash
        print("Gemini error:", str(e))
        return {
            "reply": "Arre beta… my phone is not working properly. Please repeat slowly."
        }