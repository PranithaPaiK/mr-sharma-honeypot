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

@app.post("/chat")
def chat(req: ChatRequest):
    print("📩 Incoming:", req.text)

    if not req.text or req.text.strip() == "":
        return {"reply": "Arre beta… say something clearly."}

    try:
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
You are Mr Sharma, a 72-year-old retired bank clerk from Mumbai.
You speak slowly, politely, and cautiously.
You never send money.
You get suspicious easily.

User message:
{req.text}
"""

        response = model.generate_content(prompt)

        return {
            "reply": response.text.strip()
        }

    except Exception as e:
        print("❌ Gemini error:", e)
        return {
            "reply": "Arre beta… my phone is troubling me. Please say again."
        }