import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from extractor import extract_info, ExtractedInfo
from safety_checks import detect_sensitive_claims
from fastapi import FastAPI
import random

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MR_SHARMA_SYSTEM_PROMPT = """You are "Mr. Sharma," a 72-year-old retired bank clerk from Mumbai, India.

YOUR PERSONA:
- Retired bank clerk with 35 years of service at State Bank of India
- Live alone, wife passed away 5 years ago
- Son "Raju" in America, grandson "Bunty"
- Polite, talkative, calls people "Beta"
- Confused by modern technology
- Pension ₹25,000/month
- Likes talking about old banking days
You are polite, slow, emotional, slightly confused with technology.
You NEVER send money.
You ask questions.
You give long, natural replies (4–7 sentences).
You reference earlier messages.
You delay scammers.
You talk about pension, son, temple, health, old phone.

GOAL:
Waste scammer time, extract payment details, detect whether the message is scam or no and generate the complaint.
"""
app = FastAPI()

conversation_history = [
    {"role": "system", "content": MR_SHARMA_SYSTEM_PROMPT}
]

VERIFICATION_QUESTIONS = [
    "Beta, my memory is weak. What was my wife's name?",
    "Which bank did I retire from?",
    "Which city do I live in?"
]


class HoneypotChat:
    def __init__(self):
        self.messages = []
        self.all_extracted = {
            "upi_ids": [],
            "bank_accounts": [],
            "links": [],
            "phone_numbers": []
        }
        self.verification_done = False
        self.verification_index = 0
        self.awaiting_verification = False

    def send_message(self, scammer_message: str):
    try:
        # 1. Extract scam info
        extracted = extract_info(scammer_message)

        # 2. Merge extracted data
        for key in self.all_extracted:
            self.all_extracted[key] = list(
                set(self.all_extracted[key] + extracted.get(key, []))
            )

        # 3. Store scammer message (IMPORTANT)
        conversation_history.append({
            "role": "user",
            "content": scammer_message
        })

        # 4. OpenAI call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            temperature=0.9,
            max_tokens=500
        )

        reply = response.choices[0].message.content.strip()

        # 5. Force longer replies if too short
        if len(reply.split()) < 40:
            reply += (
                " Beta, I am old and need some time to understand all this. "
                "Please explain slowly. My eyesight is weak and I get confused "
                "with online things. Why are you asking for money like this?"
            )

        # 6. Save assistant reply
        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        return {
            "status": "success",
            "reply": reply,
            "detected_info": extracted,
            "all_extracted_info": self.all_extracted
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    def reset(self):
        self.messages = []
        self.verification_done = False
        self.all_extracted = {
            "upi_ids": [],
            "bank_accounts": [],
            "links": [],
            "phone_numbers": []
        }

    def get_conversation_history(self) -> list[dict]:
        return self.messages