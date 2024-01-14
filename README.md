# GPTChatBot

I wanted to experiment with building a simple ChatGPT based chatbot as part of my [path](https://github.com/themotleycoder/learning-ml) to learning more about AI and machine learning.

The following project was deisgned to work on Mac OS, I would like to get it working on Raspberry PI too but hav enot had time to get some of the nuances worked out.

### Dependencies

- SpeechRecognition
- pyttsx3
- pyAudio

### Configuration
A file called 'config' is required with the following format:

```python
API_KEY = "<API key here>"
KEY_WORD = "<Trigger word here>"
VOICE_ID = "<Voice ID here>"
```

**API_KEY**: Is you OpenAI API key
**KEY_WORD**: The trigger word is the word you want to use to trigger the chatbot to perform a request. e.g. 'Jarvis' what is 3x3?
**VOICE_ID**: Is the ID of the voice to be used, these tend to be specific to the platform you run the project on
