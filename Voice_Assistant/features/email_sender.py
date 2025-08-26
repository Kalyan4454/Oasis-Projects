import smtplib
from core.speech import speak
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(to, subject, body):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL_ADDRESS, to, message)
        server.quit()
        speak("Email sent successfully.")
    except:
        speak("Sorry, I could not send the email.")
