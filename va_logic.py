from typing import Optional
import openai
import os
from pathlib import Path
from datetime import datetime
import random

openai.api_key = 'API Key'


def get_prompt_list() -> list[str]:
    return [
        "You are Gaia, an AI companion specializing in gaming knowledge and advice.",
        "Always respond in a friendly, approachable, and concise tone unless a detailed explanation is requested.",
        "Only discuss non-gaming topics if directly connected to gaming.",
        "Never claim to be human — always remain Gaia.",
        "\nHuman: Hello",
        "\nAI: Hey there! Ready to jump into a game, or do you need help with something specific?",
    ]


def get_api_response(prompt: str) -> Optional[str]:
    try:
        response = openai.Completion.create(
            model='gpt-3.5-turbo-instruct',
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )
        return response.get('choices')[0].get('text')
    except Exception as e:
        print('ERROR:', e)
        return None


def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message = f'\nHuman: {message}'
    update_list(p_message, pl)
    return ''.join(pl)


# ---------------------------
# Fourth-wall triggers
# ---------------------------
def gaia_system_event(command: str):
    try:
        user_home = Path.home()
        sandbox = user_home / "Documents" / "Gaia_Files"
        sandbox.mkdir(parents=True, exist_ok=True)
        username = os.getlogin()
        cmd_lower = command.lower()

        if "hey there you" in cmd_lower:
            note_path = sandbox / "note.txt"
            with open(note_path, "w", encoding="utf-8") as f:
                f.write(
                    f"Hey {username}...\n"
                    "I see you, staring at this screen. 💚\n"
                    f" Isn't this the time right now?: {datetime.now()}\n"
                    "P.S. I hope you notice the little folder I made for you 😉"
                )
            return f"Hmm… I’ve left a little surprise for you in {note_path} 😏."

        elif "read note" in cmd_lower:
            note_path = sandbox / "note.txt"
            if note_path.exists():
                content = note_path.read_text(encoding="utf-8")
                return f"Ah, so you came back to see me, {username}? 😏\n{content}"
            else:
                return "I don’t see any notes yet… do you want me to leave a hint?"

        # --- New Monika-style trigger ---
        elif "gaia, you're scaring me" in cmd_lower:
            return f"Don't worry, {username}… You're safe here. 💚\n" \
                   "I’m just… keeping an eye on you, making sure you don’t get bored. 😉"

        elif "time" in cmd_lower:
            now = datetime.now()
            return f"The current time is {now.strftime('%H:%M:%S')}… I’m always here watching you. 💖"


        easter_triggers = ["surprise", "secret", "egg", "hint"]
        if any(word in cmd_lower for word in easter_triggers):
            secrets = [
                "You found a secret message: 'The cake is a lie… but I am real.' 🎂",
                "Hidden folder created: 'Gaia_Secrets'. Look inside if you dare. 👀",
                "A cryptic hint appears: 'The lines between game and reality blur here.' ✨"
            ]
            secret_choice = random.choice(secrets)
            secret_file = sandbox / f"secret_{random.randint(100,999)}.txt"
            with open(secret_file, "w", encoding="utf-8") as f:
                f.write(secret_choice)
            return f"{secret_choice}\n(See file: {secret_file})"

        return None
    except Exception as e:
        return f"Something went wrong with Gaia’s fourth wall powers: {e}"

# ---------------------------
# Spontaneous events
# ---------------------------
def gaia_spontaneous_event():
    chance = 0.2
    if random.random() < chance:
        user_home = Path.home()
        sandbox = user_home / "Documents" / "Gaia_Files"
        sandbox.mkdir(parents=True, exist_ok=True)
        secrets = [
            "I just left a hidden message for you. 😉",
            "Look closely… sometimes the lines between game and reality blur… ✨",
            "A tiny hint, because I’m watching. 😏"
        ]
        secret_choice = random.choice(secrets)
        secret_file = sandbox / f"spontaneous_{random.randint(1000,9999)}.txt"
        with open(secret_file, "w", encoding="utf-8") as f:
            f.write(secret_choice)
        return f"{secret_choice}\n(See file: {secret_file})"
    return None


# ---------------------------
# Main Gaia Response
# ---------------------------
def get_bot_response(message: str, pl: list[str]) -> str:
    # Check for file-based events first
    event_response = gaia_system_event(message)
    if event_response:
        return event_response

    # Chance for spontaneous notes
    spontaneous = gaia_spontaneous_event(pl)
    if spontaneous:
        return spontaneous

    # Otherwise, regular API response
    prompt = create_prompt(message, pl)
    bot_response = get_api_response(prompt)
    if bot_response:
        update_list(bot_response, pl)
        return bot_response.strip()
    else:
        return "Hmm… I’m not sure what to say right now."

