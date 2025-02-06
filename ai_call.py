from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

# Twilio Credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
STORE_PHONE_NUMBER = os.getenv("STORE_PHONE_NUMBER")

# Local Flask server URL
AI_SERVER_URL = "http://127.0.0.1:5000/voice"

def make_ai_call():
    """Initiates an AI-powered call using Twilio."""
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    call = client.calls.create(
        to=STORE_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        url=AI_SERVER_URL  # Connects call to the AI server
    )

    print(f"Call initiated: {call.sid}")

if __name__ == "__main__":
    make_ai_call()
