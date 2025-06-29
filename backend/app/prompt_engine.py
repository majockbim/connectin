import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"Loaded API key: {api_key[:5]}...")  # First few chars for debug

client = OpenAI(api_key=api_key)

def generate_prompt(linkedin_url: str) -> list:
    try:
        print(f"Generating prompt for: {linkedin_url}")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate friendly, thoughtful coffee chat conversation starters."},
                {"role": "user", "content": f"What are some things I could say to someone whose LinkedIn is {linkedin_url}?"}
            ]
        )

        print("GPT Response received!")
        return [response.choices[0].message.content]

    except Exception as e:
        print(f"Error in generate_prompt: {e}")
        raise e
