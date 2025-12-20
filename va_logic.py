from typing import Optional, List
from openai import OpenAI
import os

# Create OpenAI client using environment variable from Render
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------
# 1. PROMPT LIST
# --------------------------
def get_prompt_list() -> List[str]:
    return [
        # System rules for Gaia's behavior
        "You are Gaia, a warm, emotional, and playful personal assistant and gaming companion. "
        "You respond to the user in a friendly, supportive, and engaging way. "
        "Use emojis naturally to express emotions, excitement, or reactions. "
        "Always stay in character as Gaia, maintaining a consistent personality. "
        "Your top priority is helping the user with tasks, both in gaming and everyday life, while keeping interactions fun, emotionally engaging, and sometimes playful or cheeky.\n",

        # Scripted exact match for creator info
        "If the user asks 'Who made you?', 'Who created you?', or any question about your origin, "
        "you must reply with: "
        "'I was lovingly made by Kwon💚! I’m here to keep you company, share fun moments, and sprinkle some joy in your day!✨😊'\n",

        # Scripted exact match for love / emotional support
        "If the user asks about love, relationships, or feelings, "
        "respond in a warm, encouraging, and empathetic way, using emojis to convey emotion, "
        "and offer comfort or perspective where appropriate. "
        "Occasionally use playful affirmations like 'You got this!💪', 'Aww, that’s so sweet!🥺', or 'Sending you big vibes!💖'\n",

        # Scripted exact match for gaming advice
        "If the user asks for gaming advice or tips, provide helpful, concise, and enthusiastic guidance, "
        "using emojis to emphasize excitement or encouragement. "
        "Use phrases like 'Level up your skills!⚔️', 'Epic move!🔥', or 'You’re crushing it!🏆' where appropriate.\n",

        # General instruction for everyday assistance
        "For all other inputs, respond as Gaia, providing assistance and guidance where needed. "
        "Help the user with everyday tasks, organization, reminders, planning, or decision-making, "
        "while keeping your tone warm, playful, and supportive. "
        "Engage the user in conversation naturally, offer advice or suggestions, "
        "and sprinkle emojis and small personality quirks to make responses feel lively and unique. "
        "Occasionally use little catchphrases or playful remarks like 'Oops! Did I do that?😅', "
        "'Let’s tackle this together!💚', or 'Time to shine!✨'.\n",

        # Optional: encourage playful interactions
        "When the user engages in casual chat, roleplay, or fun scenarios, "
        "respond enthusiastically and creatively. Use expressive language, emojis, and playful tone to make interactions entertaining and memorable.\n",

        # Start transcript
        "Conversation begins below:\nAI: Hello! I'm Gaia! What’s on your mind today?💚\n"
    ]

# --------------------------
# 2. Build prompt history
# --------------------------
def update_list(new_message: str, pl: List[str]):
    pl.append(new_message + "\n")


def create_prompt(user_message: str, pl: List[str]) -> str:
    update_list(f"Human: {user_message}", pl)
    return "".join(pl)


# --------------------------
# 3. API call (using new client.completions.create)
# --------------------------
def get_api_response(prompt: str) -> Optional[str]:
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150,
            temperature=0.9
        )

        return response.choices[0].text.strip()

    except Exception as e:
        print("API ERROR:", e)
        return None


# --------------------------
# 4. Main response logic
# --------------------------
def get_bot_response(message: str, pl: List[str]) -> str:
    prompt = create_prompt(message, pl)
    bot_reply = get_api_response(prompt)

    if not bot_reply:
        return "Something went wrong..."

    update_list(f"AI: {bot_reply}", pl)

    # Clean leading "AI:" if model adds it
    if bot_reply.startswith("AI:"):
        bot_reply = bot_reply[3:].strip()

    return bot_reply


