import requests
import tkinter as tk
from tkinter import messagebox, ttk

# OpenWeatherMap API Key (Replace with your own API key)
API_KEY = "d5d299edb4e73976bc6fa4a9c7761f0e"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return
    
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        weather_info = (
            f"City: {city}\n"
            f"Weather: {weather}\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
        result_label.config(text=weather_info)
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network error. Please try again.")
    except KeyError:
        messagebox.showerror("Error", f"City '{city}' not found.")

# Creating the GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("400x350")
root.configure(bg="#dbeafe")  # Light blue background for a calming look

# Title Label
title_label = tk.Label(root, text="Weather App", font=("Arial", 18, "bold"), bg="#dbeafe", fg="#1e3a8a")
title_label.pack(pady=10)

# Entry Field
city_entry = ttk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10, padx=20, fill=tk.X)

# Search Button
search_button = ttk.Button(root, text="Get Weather", command=get_weather)
search_button.pack(pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12), bg="#dbeafe", fg="#1e3a8a", justify="left")
result_label.pack(pady=20, padx=20)

root.mainloop()
