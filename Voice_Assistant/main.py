import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import sys

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Female voice (change index if needed)
engine.setProperty("rate", 170)  # Speaking speed

def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            print(f"✅ You said: {command}")
            return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        talk("Sorry, I am having trouble connecting to the speech service.")
        return ""
    except:
        return ""

def run_assistant():
    command = take_command()

    if "hello" in command:
        talk("Hello! How can I help you?")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        talk(f"The time is {time}")

    elif "date" in command:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        talk(f"Today's date is {date}")

    elif "search" in command:
        talk("What should I search for?")
        query = take_command()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            talk(f"Here are the search results for {query}")

    elif "weather" in command:
        talk("Please say your city name")
        city = take_command()
        if city:
            api_key = "your_api_key_here"  # replace with your OpenWeather API key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            try:
                res = requests.get(url).json()
                if res["cod"] == 200:
                    weather = res["weather"][0]["description"]
                    temp = res["main"]["temp"]
                    talk(f"The weather in {city} is {weather} with a temperature of {temp}°C")
                else:
                    talk("Sorry, I could not fetch the weather.")
            except:
                talk("Error connecting to weather service.")

    elif "open google" in command:
        talk("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        talk("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open gmail" in command:
        talk("Opening Gmail")
        webbrowser.open("https://mail.google.com")

    elif "open linkedin" in command:
        talk("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")

    elif "who invented you" in command or "who created you" in command or "who made you" in command:
        talk("I was created by Kalyan.")

    elif "close" in command or "exit" in command or "stop" in command or "quit" in command:
        talk("Goodbye! Shutting down now.")
        sys.exit(0)

    else:
        if command != "":
            talk("Sorry, I didn't understand that.")

# Keep listening until closed
while True:
    run_assistant()
