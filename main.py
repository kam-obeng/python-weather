import requests
import tkinter as tk
from tkinter import messagebox, ttk

# OpenWeatherMap API Key (Replace with your own API key)
API_KEY = "d5d299edb4e73976bc6fa4a9c7761f0e"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def convert_wind_direction(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return
    
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Fetching weather data...\n")
    result_text.config(state=tk.DISABLED)
    root.update()
    
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        wind_degrees = data["wind"].get("deg", 0)
        wind_direction = convert_wind_direction(wind_degrees)
        
        weather_info = (
            f"City: {city}\n"
            f"Weather: {weather}\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Wind Direction: {wind_direction} ({wind_degrees}°)"
        )
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, weather_info)
        result_text.config(state=tk.DISABLED)
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network error. Please try again.")
    except KeyError:
        messagebox.showerror("Error", f"City '{city}' not found.")

# Creating the GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("450x400")
root.configure(bg="#dbeafe")  # Light blue background for a calming look
root.resizable(True, True)  # Allow window resizing

# Title Label
title_label = tk.Label(root, text="Weather App", font=("Arial", 18, "bold"), bg="#dbeafe", fg="#1e3a8a")
title_label.pack(pady=10)

# Entry Field
city_entry = ttk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10, padx=20, fill=tk.X)

# Search Button
search_button = ttk.Button(root, text="Get Weather", command=get_weather)
search_button.pack(pady=10)

# Frame for Text Widget and Scrollbar
text_frame = tk.Frame(root)
text_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Result Text Widget (With Scrollbar)
result_text = tk.Text(text_frame, font=("Arial", 12), bg="#dbeafe", fg="#1e3a8a", height=6, width=40, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=scrollbar.set)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=result_text.yview)

root.mainloop()
