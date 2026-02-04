from fastapi import FastAPI
from pydantic import BaseModel
import os
import google.generativeai as genai

# ---- FASTAPI APP (THIS IS WHAT RENDER NEEDS) ----
app = FastAPI()

# ---- GEMINI SETUP ----
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in environment")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---- REQUEST MODEL ----
class ChatRequest(BaseModel):
    session_id: str
    text: str

# ---- CHAT ENDPOINT ----
@app.post("/chat")
def chat(req: ChatRequest):
    response = model.generate_content(req.text)
    return {
        "reply": response.text
    }

# ---- HEALTH CHECK ----
@app.get("/")
def root():
    return {"status": "ok"}