from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from honeypot import HoneypotChat

app = FastAPI()
sessions = {
    "session-1": HoneypotChat(),
    "session-2": HoneypotChat()
}

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve templates
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    session_id: str
    text: str

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(req: ChatRequest):

    # Create session if not exists
    if req.session_id not in sessions:
        sessions[req.session_id] = HoneypotChat()

    honeypot = sessions[req.session_id]
    return honeypot.send_message(request.message)

@app.post("/reset")
def reset():
    honeypot.reset()
    return {"status": "reset"}

@app.get("/")
def root():
    return{"status":"ok"}