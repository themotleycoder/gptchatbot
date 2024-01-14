# GPTChatBot

I wanted to experiment with building a simple ChatGPT based chatbot as part of my [path](https://github.com/themotleycoder/learning-ml) to learning more about AI and machine learning.

The following project was designed to work on Mac OS, I would like to get it working on Raspberry PI too but have not had time to get some of the nuances worked out.

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

`API_KEY`: Is you [OpenAI API key](https://platform.openai.com/api-keys)

`KEY_WORD`: The trigger word is the word you want to use to trigger the chatbot to perform a request. e.g. 'Jarvis' what is 3x3?

`VOICE_ID`: Is the ID of the voice to be used, these tend to be specific to the platform you run the project on

### LLM Options
In the latest version you can also replace the call to ChatGPT API with a call to a local [Ollama](https://ollama.ai/) model instead. You will need to install ollama and then install the model you would like to use. Instructions on how to do this can be found on their [website](https://ollama.ai/).

Once completed you will need to comment/replace the line to call the ChatGPT API `call_chatgpt_api(text)` and then uncomment the relevant model line (or provide a new one) to access the Ollama model service call `call_ollama(model, text)`
