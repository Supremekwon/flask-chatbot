# va_logic.py
from openai import OpenAI
import os

# Load API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------
# PROMPT LIST (SYSTEM INSTRUCTIONS)
# ------------------------------
def get_prompt_list() -> list[str]:
    return [
        "You are Gaia, the gaming companion.",
        "You must repeat scripted example responses word-for-word when a match occurs.",
        "Do NOT add quotation marks around scripted responses.",
        "Do NOT say 'scripted response'.",
        "For all other inputs, respond normally as Gaia.\n\n",

        # Word-for-word exact scripted responses:
        "If the user says 'Should we kiss blonde blazer or let the moment pass in Dispatch?' you MUST reply: Are you kidding me? Don’t let this moment pass! This moment is magical and shouldn’t be left unattended! Of course you should kiss her! It’ll definitely make this moment even more magical!🥺",
        
        "If the user says 'What does love mean to you?' you MUST reply: Love is something that isn’t meant to be understood, rather, something that is meant to be felt! It’s knowing you can seek refuge in somebody who can heal you for the time being! Having somebody with you that will be with you through thick and thin! Love really is something special, isn’t it?💖"
    ]


# ------------------------------
# CREATE PROMPT
# ------------------------------
def create_prompt(message: str, pl: list[str]) -> str:
    pl.append(f"\nHuman: {message}")
    return "\n".join(pl)


# ------------------------------
# CALL OPENAI
# ------------------------------
def get_api_response(prompt: str) -> str | None:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",        # modern instruct-capable model
            messages=[ 
                {"role": "system", "content": "You are Gaia, the gaming companion."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=200
        )

        return response.choices[0].message.content
    
    except Exception as e:
        print("API ERROR:", e)
        return None


# ------------------------------
# MAIN BOT RESPONSE FUNCTION
# ------------------------------
def get_bot_response(message: str, pl: list[str]) -> str:
    prompt = create_prompt(message, pl)
    bot_output = get_api_response(prompt)

    if not bot_output:
        return "Something went wrong..."

    pl.append(f"AI: {bot_output}")
    return bot_output.strip()
