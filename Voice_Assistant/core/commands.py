
from core.speech import speak, listen
from features import time_date, web_search, weather, email_sender, wiki_search, apps

def handle_command(command):
    if "time" in command:
        time_date.tell_time()

    elif "date" in command:
        time_date.tell_date()

    elif "search" in command:
        speak("What should I search for?")
        query = listen()
        if query:
            web_search.search_web(query)

    elif "weather" in command:
        speak("Which city?")
        city = listen()
        weather.get_weather(city)

    elif "email" in command:
        speak("Who is the recipient?")
        recipient = listen()
        if "friend" in recipient:
            to = "friend_email@example.com"
            speak("What is the subject?")
            subject = listen()
            speak("What should I say?")
            body = listen()
            email_sender.send_email(to, subject, body)

    elif "wikipedia" in command:
        speak("What should I search on Wikipedia?")
        query = listen()
        wiki_search.wiki_search(query)

    elif "open youtube" in command:
        apps.open_youtube()

    elif "open google" in command:
        apps.open_google()

    elif "stop" in command or "exit" in command:
        speak("Goodbye!")
        exit()

    elif command != "":
        speak("I didn't understand that, but I'm learning.")
