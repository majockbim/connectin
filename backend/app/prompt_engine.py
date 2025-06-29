# Handles OpenAI interaction 

import openai
import os

open.api_key = os.getenv("OPENAI_API_KEY")

def generate_prompt(linkedin_url: str) -> list:

    prompt = f"What are some things I could say to someone over a coffee whose LinkedIn is: {linkedin_url}?"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", "content": "Generate friendly, insightful conversation"
            },
            {
                "role": "user", "content": prompt
            }
        ]
    )
    return [choice["message"]["content"] for choice in response.choices]