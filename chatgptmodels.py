import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY1")

client = openai.OpenAI(api_key=API_KEY)

models = client.models.list()

for model in models.data:
    print(model.id)
