import wikipedia
from core.speech import speak

def wiki_search(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("I couldn't find information on that.")
