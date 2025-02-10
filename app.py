# app.py - AI Agent for Twilio Calls
from flask import Flask, request, make_response
from twilio.twiml.voice_response import VoiceResponse
import openai
import speech_recognition as sr
# from elevenlabs import generate, save
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

conversation_history = []

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")  # Eleven Labs API Key

app = Flask(__name__)
recognizer = sr.Recognizer()

@app.route('/')
def hello():
    return "Hello from Flask!"


@app.route("/voice", methods=["POST"])
def handle_call():
    print("Received a POST request on /voice")
    """Handles Twilio call: transcribes speech, generates AI response, and speaks back."""
    audio_url = request.form.get("RecordingUrl")


    if not audio_url:
        return "No audio URL provided", 400  # Error response if no URL found


    # Convert speech to text
    user_text = transcribe_audio(audio_url)
    if not user_text:
        return respond_with_audio("Sorry, I didn't hear that. Could you repeat?")

    # Generate AI response
    ai_response = generate_ai_response(user_text)

    # Convert AI response to speech
    speech_file = text_to_speech(ai_response)

    # Play AI response
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
        model="gpt-4o-mini",
        messages=conversation_history,
        max_tokens=200
    )

    # Store response
    model_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": model_response})

    return model_response

# def text_to_speech(text):
#     """Converts AI text to speech using Eleven Labs."""
#     audio = generate(api_key=ELEVENLABS_API_KEY, text=text, voice="Josh", model="eleven_monolingual-v1")
#     speech_file = "response.mp3"
#     save(audio, speech_file)
#     return speech_file

def text_to_speech(text):
    """Converts AI-generated text to speech using Eleven Labs."""
    elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    # Generate audio
    audio = elevenlabs_client.text_to_speech(
        text=text,
        voice=Voice(name="Josh")  # Choose a voice
    )

    # Play the audio
    play(audio)

    return "response.mp3"  # Placeholder for Twilio playback


def respond_with_audio(file_path):
    """Generates Twilio response with AI-generated speech."""
    response = VoiceResponse()
    response.play(file_path)
    print(str(response))
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0', port=5000)
