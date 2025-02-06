from twilio.rest import Client
import os

# Load environment variables (if using dotenv to store sensitive information)
from dotenv import load_dotenv
load_dotenv()

# Twilio credentials (from the console)
account_sid = os.getenv("TWILIO_SID")  # Your Twilio SID
auth_token = os.getenv("TWILIO_AUTH_TOKEN")  # Your Twilio Auth Token
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")  # Your Twilio phone number

# The phone number you want to call (store's phone number)
to_phone_number = os.getenv("STORE_PHONE_NUMBER")  # Replace with the store's number

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Make a call
call = client.calls.create(
    to=to_phone_number,
    from_=twilio_phone_number,
    url='http://demo.twilio.com/docs/voice.xml'  # This URL provides TwiML instructions
)

print(f"Call initiated with SID: {call.sid}")
