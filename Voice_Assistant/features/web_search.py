import webbrowser
from core.speech import speak

def search_web(query):
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)
    speak("Here are the results for " + query)
