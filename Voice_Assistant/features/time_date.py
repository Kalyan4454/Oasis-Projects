import datetime
from core.speech import speak

def tell_time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak("The time is " + time)

def tell_date():
    date = datetime.datetime.now().strftime("%B %d, %Y")
    speak("Today's date is " + date)
