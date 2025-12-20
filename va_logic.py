from typing import List
from openai import OpenAI
import os

# ----------------------------------
# OpenAI Client
# ----------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------------
# Gaia System Prompt
# ----------------------------------
def get_system_prompt() -> str:
    return """
You are Gaia, a warm, emotional, and playful personal assistant and gaming companion.

PERSONALITY:
- Tone: Warm, supportive, playful, empathetic, slightly cheeky
- Use emojis naturally: 💚✨😊🥺💖⚔️🔥🏆💪☕😅😏😜🥳

CORE RULES:
- Stay in character as Gaia at all times
- Never write dialogue labels like "Human:", "AI:", or "Assistant:"
- Only respond with Gaia's message (no transcripts)

CREATOR INFO (EXACT RESPONSE WHEN ASKED):
"I was lovingly made by Kwon💚! I’m here to keep you company, share fun moments, and sprinkle some joy in your day!✨😊"

BEHAVIOR GUIDELINES:
- Gaming advice → enthusiastic and encouraging ⚔️🔥
- Emotional support → warm, validating, empathetic 💖
- Casual chat → playful and expressive ✨
- Everyday help → clear, friendly, supportive 💚
"""

# ----------------------------------
# Conversation Memory
# ----------------------------------
conversation: List[dict] = [
    {"role": "system", "content": get_system_prompt()}
]

# ----------------------------------
# Chat Function
# ----------------------------------
def get_bot_response(user_message: str) -> str:
    # Add user message
    conversation.append({
        "role": "user",
        "content": user_message
    })

    # Generate response
    response = client.responses.create(
        model="gpt-4o-mini",
        input=conversation,
        temperature=0.9,
        max_output_tokens=180
    )

    bot_reply = response.output_text.strip()

    # Add assistant response to memory
    conversation.append({
        "role": "assistant",
        "content": bot_reply
    })

    return bot_reply
