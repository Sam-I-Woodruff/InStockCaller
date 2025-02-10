import subprocess
import time
import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client

# Load environment variables
load_dotenv()

# Twilio Credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
STORE_PHONE_NUMBER = os.getenv("STORE_PHONE_NUMBER")

# Start Flask app
print("Starting Flask server...")
flask_process = subprocess.Popen(["python", "app.py"])

# Give Flask time to start
time.sleep(5)

# Start ngrok and get the public URL
print("Starting ngrok...")
ngrok_process = subprocess.Popen(["ngrok", "http", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait a few seconds for ngrok to start
time.sleep(5)

# Get ngrok public URL
try:
    response = requests.get("http://localhost:4040/api/tunnels")
    ngrok_url = response.json()["tunnels"][0]["public_url"]
    print(f"Ngrok URL: {ngrok_url}")
except Exception as e:
    print("Error getting ngrok URL:", e)
    flask_process.terminate()
    ngrok_process.terminate()
    exit(1)

# Update .env with the new ngrok URL
with open(".env", "r") as f:
    lines = f.readlines()

with open(".env", "w") as f:
    for line in lines:
        if line.startswith("AI_SERVER_URL="):
            f.write(f"AI_SERVER_URL={ngrok_url}\n")
        else:
            f.write(line)

print("Updated .env with new ngrok URL.")

# Give Flask some time to pick up new .env variables
time.sleep(5)

# Initiate Twilio Call
print("Making AI-powered call...")
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

call = client.calls.create(
    to=STORE_PHONE_NUMBER,
    from_=TWILIO_PHONE_NUMBER,
    url=ngrok_url  # Connects the call to the AI server
)

print(f"Call initiated: {call.sid}")

# Keep processes running
try:
    flask_process.wait()
    ngrok_process.wait()
except KeyboardInterrupt:
    print("Stopping servers...")
    flask_process.terminate()
    ngrok_process.terminate()
