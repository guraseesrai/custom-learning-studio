import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to generate text using OpenAI
def generate_text(prompt, model="gpt-4", max_tokens=500):
    openai.api_key = OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"
