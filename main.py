import requests
import tkinter as tk
from tkinter import messagebox

# OpenWeatherMap API Key (Replace with your own API key)
API_KEY = "d5d299edb4e73976bc6fa4a9c7761f0e"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return
    
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if response.status_code == 200:
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
    else:
        messagebox.showerror("Error", f"City '{city}' not found.")

# Creating the GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("350x300")

city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)

search_button = tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 12))
search_button.pack()

result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=20)

root.mainloop()
