# app.py - Flask server handling AI responses
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import openai
import speech_recognition as sr
from elevenlabs import generate, save
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

app = Flask(__name__)
recognizer = sr.Recognizer()

@app.route("/voice", methods=["POST"])
def handle_call():
    """Processes Twilio call, transcribes speech, generates AI response, and plays audio back."""
    audio_url = request.form["RecordingUrl"]

    # Convert speech to text
    user_text = transcribe_audio(audio_url)
    if not user_text:
        return respond_with_audio("Sorry, I didn't catch that. Can you repeat?")

    # Generate AI response
    ai_response = generate_ai_response(user_text)

    # Convert AI response to speech
    speech_file = text_to_speech(ai_response)

    # Respond with AI-generated voice
    return respond_with_audio(speech_file)

def transcribe_audio(audio_url):
    """Download and transcribe Twilio's recorded audio."""
    audio_data = requests.get(audio_url).content
    with open("temp.wav", "wb") as f:
        f.write(audio_data)
    
    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
    
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def generate_ai_response(text):
    """Generates a conversational AI response using GPT-4."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a polite AI assistant."},
                  {"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]

def text_to_speech(text):
    """Converts text to speech using ElevenLabs and saves as an MP3."""
    audio = generate(api_key=ELEVENLABS_API_KEY, text=text, voice="Josh", model="eleven_monolingual-v1")
    speech_file = "response.mp3"
    save(audio, speech_file)
    return speech_file

def respond_with_audio(file_path):
    """Generates TwiML response with the AI-generated speech."""
    response = VoiceResponse()
    response.play(file_path)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
