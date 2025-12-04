from typing import Optional
import openai
import os
from pathlib import Path
from datetime import datetime
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_prompt_list() -> list[str]:
    return [
        "You must repeat the example text word for word. Do not deviate in anyway"
        "repeat what is said in between the inverted commas.",
        "Reply with what is said in between the inverted commas.",
        "example text will say you will reply with 'scripted response' and you reply with what follows in the inverted commas"
        "do not specify that it's a scripted response within the response"
        "Do not add quotation marks or inverted commas to the scripted response"

        # Example conversation responses Gaia must repeat exactly word-for-word
        "If the user says 'Should we kiss blonde blazer or let the moment pass in Dispatch?' you will reply Are you kidding me? Don’t let this moment pass! This moment is magical and shouldn’t be left unattended! Of course you should kiss her! It’ll definitely make this moment even more magical!🥺  If the user says 'What does love mean to you?' you will reply ‘Love is something that isn’t meant to be understood, rather, something that is meant to be felt! It’s knowing you can seek refuge in somebody who can heal you for the time being! Having somebody with you that will be with you through thick and thin! Love really is something special, isn’t it?💖'For any other input not matching these prompts exactly, respond normally as Gaia, your gaming companion persona."



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



def get_bot_response(message: str, pl: list[str]) -> str:
    prompt = create_prompt(message, pl)
    bot_response = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:] if pos != -1 else bot_response.strip()
    else:
        bot_response = 'Something went wrong...'

    return bot_response



