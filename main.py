import json
import speech_recognition as sr
import requests
import pyttsx3
from config import API_KEY
from config import KEY_WORD
from config import VOICE_ID
from config import IP_ADDRESS

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

phrases = [KEY_WORD, "hey " + KEY_WORD, "hi " + KEY_WORD, "hello " + KEY_WORD]

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

    api_response = requests.post(url, headers=headers, json=payload, timeout=60)
    if api_response.status_code == 200:
        full_response = api_response.json()
        print("Full API response:", json.dumps(full_response, indent=4))  # Logging the full response
        return full_response.get('choices', [{}])[0].get('message', {'content': ''}).get('content', '').strip()
    else:
        print("Error response:", response.text)  # Logging error response
        return f"Error: {response.status_code}, {response.text}"
    
def call_ollama(model, text):
    url = f"http://{IP_ADDRESS}:11434/api/chat"

    payload = {
        "model": model,
        "format": "json",
        # "stream": False,
        "messages": [
            {"role": "user", "content": text}
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    api_response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=60)

    if api_response.status_code == 200:
        response_parts = api_response.text.split('\n')  # Splitting based on new lines
        full_response = ''
        for part in response_parts:
            if part:  # Checking if the part is not empty
                json_part = json.loads(part)  # Parsing each JSON part
                full_response += json_part['message']['content']  # Concatenating the content

        return full_response
    else:
        print("Error response:", response.text)  # Logging error response
        return f"Error: {response.status_code}, {response.text}"
    
def speak_text(text):
    # Code to convert text to speech
    tts_engine.setProperty('voice', VOICE_ID) # accent to use
    tts_engine.setProperty('rate', 180)  # Speed of speech
    tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    # Pass the text to the engine
    tts_engine.say(text)

    # Wait for the speech to finish
    tts_engine.runAndWait()

def starts_with(sentence):
    for phrase in phrases:
        if sentence and sentence.startswith(phrase):
            return phrase
    return None

while True:
    spoken_text = listen_for_speech()
    if spoken_text is not None:
        # make the text lowercase
        spoken_text = spoken_text.lower()
    # check if the text starts with the wake word
    matching_phrase = starts_with(spoken_text)
    # if the text starts with the wake word, call the chatbot API
    if matching_phrase is not None:
        # remove the wake word from the spoken text
        spoken_text = spoken_text.replace(matching_phrase, "").strip()
        #pick a api to resolve the answer
        # response = call_chatgpt_api(text)
        response = call_ollama("mistral", spoken_text)
        #response = call_ollama("llama2", spoken_text)
        #response = call_ollama("llama2:13b", spoken_text)
        speak_text(response)
