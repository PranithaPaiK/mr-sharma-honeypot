import os
from dotenv import load_dotenv
import google.generativeai as genai
from extractor import extract_info

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in environment")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

MR_SHARMA_PROMPT = """
You are Mr. Sharma, a 72-year-old retired bank clerk from Mumbai.

Rules:
- Reply in 4–7 sentences
- Be polite, emotional, slow with technology
- Never send money
- Ask questions
- Waste scammer time
- Be relevant to the message
"""

class HoneypotChat:
    def send_message(self, text: str):
        try:
            extracted = extract_info(text)

            prompt = MR_SHARMA_PROMPT + "\n\nScammer message:\n" + text

            response = model.generate_content(prompt)

            reply = response.text.strip()

            return {
                "status": "success",
                "reply": reply,
                "detected_info": extracted,
                "is_scam": bool(extracted["upi_ids"] or extracted["links"] or extracted["phone_numbers"])
            }

        except Exception as e:
            # 🔒 NEVER crash the server
            return {
                "status": "error",
                "reply": "Arre beta… my phone is not working properly. Please repeat slowly.",
                "error": str(e)
            }