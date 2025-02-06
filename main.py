# ai_call.py - Script to initiate AI call via Twilio
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio Credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
STORE_PHONE_NUMBER = os.getenv("STORE_PHONE_NUMBER")  # Change to target store number

# Your AI server URL (publicly accessible)
AI_SERVER_URL = os.getenv("AI_SERVER_URL")

def make_ai_call():
    """Initiates a call to the store with AI voice."""
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    call = client.calls.create(
        to=STORE_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        url=AI_SERVER_URL  # Twilio fetches instructions from here
    )

    print(f"Call initiated: {call.sid}")

if __name__ == "__main__":
    make_ai_call()
