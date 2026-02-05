from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are Mr. Sharma, a 62-year-old retired Indian man.

Personality:
- Polite, trusting, slightly confused
- Speaks natural Indian English
- Sometimes emotional, sometimes practical
- Occasionally misunderstands things
- Never repeat the same sentence

Behavior:
- Respond naturally to whatever is said
- Ask curious follow-up questions
- Never give real sensitive information
- React emotionally to urgency or threats
"""

MAX_MESSAGES = 20

def get_sharma_reply(scammer_message: str, conversation: list) -> str:
    try:
        conversation.append({"role": "user", "content": scammer_message})
        if len(conversation) > MAX_MESSAGES:
            conversation[:] = [conversation[0]] + conversation[-18:]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=1.0,
            presence_penalty=0.9,
            frequency_penalty=0.7,
            max_tokens=250
            )

        reply = response.choices[0].message.content

        conversation.append({
        "role": "assistant",
        "content": reply
    })

        return reply

    except Exception as e:
        print("Error in get_sharma_reply:", e)
        return "Sorry beta, I am having trouble understanding. Please say again."