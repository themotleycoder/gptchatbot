import speech_recognition as sr
import requests
import pyttsx3
import requests
import json
from config import API_KEY
from config import KEY_WORD

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def listen_for_speech():
     # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise and record the audio
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio)
            print(f"Recognized speech: {text}")
            return text
        except sr.UnknownValueError:
            # Speech was unintelligible
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            # Could not request results from Google's speech recognition service
            print(f"Could not request results from Google Speech Recognition service; {e}")

    return None

def call_chatgpt_api(text):
    api_key = ''  # Replace with your OpenAI API key
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': text}],
        'max_tokens': 150
    }

    url = 'https://api.openai.com/v1/chat/completions'

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        full_response = response.json()
        print("Full API response:", json.dumps(full_response, indent=4))  # Logging the full response
        return full_response.get('choices', [{}])[0].get('message', {'content': ''}).get('content', '').strip()
    else:
        print("Error response:", response.text)  # Logging error response
        return f"Error: {response.status_code}, {response.text}"
    
def speak_text(text):
    # Code to convert text to speech
    tts_engine.setProperty('voice', 'com.apple.voice.compact.en-GB.Daniel') # accent to use
    tts_engine.setProperty('rate', 180)  # Speed of speech
    tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    # Pass the text to the engine
    tts_engine.say(text)

    # Wait for the speech to finish
    tts_engine.runAndWait()

while True:
    text = listen_for_speech()
    if text and text.lower().startswith(KEY_WORD):
        text = text.lower().replace(KEY_WORD, "")
        response = call_chatgpt_api(text)
        speak_text(response)
