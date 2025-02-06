import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("OPENAI_API_KEY1")

client = openai.OpenAI(api_key=API_KEY)

# Initialize an empty list to store conversation history
conversation_history = []

def chat_with_gpt(prompt):
    # Append the new user message to conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Get the assistant's response, using the full conversation history
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4" if you have access
        messages=conversation_history,
        max_tokens=20  # Adjust the max_tokens as needed
    )

    # Extract assistant's reply and append to conversation history
    assistant_reply = response['choices'][0]['message']['content']  # Corrected line
    conversation_history.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply

if __name__ == "__main__":
    print("Conversation started! (Type 'end' to end)\n")
    while True:
        user_prompt = input("You: ")

        # end condition
        if user_prompt.lower() == "end":
            print("Ending conversation.")
            break

        # Get response from ChatGPT and print it
        response = chat_with_gpt(user_prompt)
        print(f"ChatGPT: {response}\n")
