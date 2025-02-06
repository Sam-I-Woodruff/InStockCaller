import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file 
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("OPENAI_API_KEY1")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=API_KEY)

# Initialize a list to keep track of the conversation
conversation_history = []

def chat_with_gpt(prompt):
    # Add the user input to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Get a response from the GPT model with the entire conversation history
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        max_tokens=100
    )

    # Get the response from the model and add it to the conversation history
    model_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": model_response})

    return model_response

if __name__ == "__main__":
    print("Start chatting with GPT! Type 'exit' to end the conversation.")
    
    while True:
        user_prompt = input("You: ")
        
        if user_prompt.lower() == 'exit':
            print("Ending conversation.")
            break
        
        response = chat_with_gpt(user_prompt)
        print("\nChatGPT: ", response)
