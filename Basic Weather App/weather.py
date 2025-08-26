import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        condition = data["weather"][0]["description"].title()
        icon_code = data["weather"][0]["icon"]

        # Update labels
        result_label.config(
            text=f"{city_name}, {country}\n"
                 f"Temperature: {temp}°C (Feels like {feels_like}°C)\n"
                 f"Condition: {condition}\n"
                 f"Humidity: {humidity}%\n"
                 f"Wind Speed: {wind} m/s"
        )

        # Fetch and show weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        img_data = icon_response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((80, 80), Image.Resampling.LANCZOS)
        icon_img = ImageTk.PhotoImage(img)
        icon_label.config(image=icon_img)
        icon_label.image = icon_img

    except requests.exceptions.HTTPError:
        messagebox.showerror("Error", "City not found. Try again.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.config(bg="#2C3E50")  # dark blue background

# Entry
city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)

# Button
get_btn = tk.Button(root, text="Get Weather", command=get_weather,
                    font=("Arial", 12), bg="#1ABC9C", fg="white")
get_btn.pack(pady=5)

# Weather info
icon_label = tk.Label(root, bg="#2C3E50")
icon_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 12), fg="white", bg="#2C3E50", justify="center")
result_label.pack(pady=10)

root.mainloop()
