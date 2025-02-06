import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("OPENAI_API_KEY1")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=API_KEY)

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    user_prompt = input("Enter your message: ")
    response = chat_with_gpt(user_prompt)
    print("\nChatGPT Response:\n", response)
