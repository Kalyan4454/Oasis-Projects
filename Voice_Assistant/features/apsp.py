import webbrowser
from core.speech import speak

def open_youtube():
    webbrowser.open("https://youtube.com")
    speak("Opening YouTube")

def open_google():
    webbrowser.open("https://google.com")
    speak("Opening Google")
