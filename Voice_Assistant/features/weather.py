import requests
from core.speech import speak
from config import OPENWEATHER_API_KEY

def get_weather(city="Hyderabad"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp}°C with {desc}")
    else:
        speak("Sorry, I couldn't fetch the weather.")
