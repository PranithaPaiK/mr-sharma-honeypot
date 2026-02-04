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

class ChatRequest(BaseModel):
    session_id: str
    text: str

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(req: ChatRequest):
    try:

        # Create session if not exists
        if req.session_id not in sessions:
            sessions[req.session_id] = HoneypotChat()

        honeypot = sessions[req.session_id]
        response = honeypot.send_message(req.text)
        return honeypot.send_message(req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
def reset(req: ChatRequest):
    if req.session_id in sessions:
        sessions[req.session_id].reset()
    return {"status": "reset"}