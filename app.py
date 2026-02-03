from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from honeypot import HoneypotChat

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve templates
templates = Jinja2Templates(directory="templates")

honeypot = HoneypotChat()

class Message(BaseModel):
    text: str

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(msg: Message):
    # 🔥 ONLY pass latest message
    return honeypot.send_message(msg.text)

@app.post("/reset")
def reset():
    honeypot.reset()
    return {"status": "reset"}

@app.get("/")
def root():
    return{"status":"ok"}