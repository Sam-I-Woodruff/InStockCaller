from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import openai
import speech_recognition as sr
from elevenlabs import Voice, play
from elevenlabs.client import ElevenLabs
import requests
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

# Initialize OpenAI client
API_KEY = os.getenv("OPENAI_API_KEY1")
client = openai.OpenAI(api_key=API_KEY)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")  # Eleven Labs API Key

app = Flask(__name__)
recognizer = sr.Recognizer()

# Initialize conversation history
conversation_history = []

@app.route("/voice", methods=["POST"])
def handle_call():
    """Handles Twilio call: transcribes speech, generates AI response, and speaks back."""
    audio_url = request.form.get("RecordingUrl")

    # Convert speech to text
    user_text = transcribe_audio(audio_url)
    if not user_text:
        return respond_with_audio("Sorry, I didn't hear that. Could you repeat?")

    # Generate AI response
    ai_response = generate_ai_response(user_text)

    # Convert AI response to speech
    speech_file = text_to_speech(ai_response)

    # Return response with speech playback
    return respond_with_audio(speech_file)

def transcribe_audio(audio_url):
    """Downloads and transcribes speech from the call."""
    audio_data = requests.get(audio_url).content
    with open("temp.wav", "wb") as f:
        f.write(audio_data)

    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)  # Convert speech to text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def generate_ai_response(prompt):
    """Maintains conversation and generates AI responses."""
    global conversation_history

    # Add user message
    conversation_history.append({"role": "user", "content": prompt})

    # Get AI response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        max_tokens=200
    )

    # Store response
    model_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": model_response})

    return model_response

def text_to_speech(text):
    """Converts AI-generated text to speech using Eleven Labs."""
    elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    # Generate audio file
    audio = elevenlabs_client.text_to_speech(
        text=text,
        voice=Voice(name="Josh")  # Choose a voice
    )

    # Save the audio to a file
    speech_file = "response.mp3"
    audio.save(speech_file)

    return speech_file  # Return the file path for Twilio to play

def respond_with_audio(file_path):
    """Generates Twilio response with AI-generated speech."""
    response = VoiceResponse()
    response.play(file_path)  # Twilio will play the audio file
    return str(response)

@app.route("/make-call", methods=["POST"])
def make_ai_call():
    """Initiates an AI-powered call using Twilio."""
    from twilio.rest import Client

    # Load Twilio credentials
    TWILIO_SID = os.getenv("TWILIO_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    STORE_PHONE_NUMBER = os.getenv("STORE_PHONE_NUMBER")

    # Local Flask server URL
    AI_SERVER_URL = "http://127.0.0.1:5000/voice"

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    call = client.calls.create(
        to=STORE_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        url=AI_SERVER_URL  # Connects call to the AI server
    )

    print(f"Call initiated: {call.sid}")

    return "Call initiated!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
