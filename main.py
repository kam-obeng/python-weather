import asyncio
import aiohttp
import tkinter as tk
from tkinter import messagebox, ttk
from geopy.geocoders import Nominatim
import json
import os

API_KEY = "d5d299edb4e73976bc6fa4a9c7761f0e"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
CACHE_FILE = "weather_cache.json"

# Load cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as file:
        CACHE = json.load(file)
else:
    CACHE = {}

def convert_wind_direction(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]

async def fetch_weather(city):
    print(f"Fetching weather for city: {city}")
    if city in CACHE:
        print("Returning cached data")
        return CACHE[city]  # Return cached data
    
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BASE_URL, params=params) as response:
                if response.status == 401:
                    messagebox.showerror("Error", "Invalid API Key")
                    return None
                elif response.status == 404:
                    messagebox.showerror("Error", f"City '{city}' not found.")
                    return None
                elif response.status != 200:
                    messagebox.showerror("Error", "Failed to fetch weather data. Try again later.")
                    return None
                
                data = await response.json()
                CACHE[city] = data  # Cache the response
                with open(CACHE_FILE, "w") as file:
                    json.dump(CACHE, file)
                print("Weather data fetched successfully")
                return data
        except aiohttp.ClientError as e:
            print(f"Network error: {e}")
            messagebox.showerror("Error", "Network error. Check your internet connection.")
            return None

async def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return
    
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Fetching weather data...\n")
    result_text.config(state=tk.DISABLED)
    root.update()
    
    data = await fetch_weather(city)
    if not data:
        return
    
    try:
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
    except KeyError as e:
        print(f"KeyError: {e}")
        messagebox.showerror("Error", f"City '{city}' not found.")

async def get_location():
    try:
        # Step 1: Get user's location from their IP address
        async with aiohttp.ClientSession() as session:
            async with session.get("http://ip-api.com/json/") as response:
                if response.status != 200:
                    messagebox.showerror("Error", "Failed to fetch location data")
                    return
                
                data = await response.json()
                if data["status"] != "success":
                    messagebox.showerror("Error", "Could not determine location.")
                    return
                
                latitude = data["lat"]
                longitude = data["lon"]

                # Step 2: Convert latitude & longitude into a city name
                geolocator = Nominatim(user_agent="geoapiExercises")
                location = geolocator.reverse((latitude, longitude), timeout=10)
                
                if location:
                    city_name = location.raw.get("address", {}).get("city", "Unknown")
                    if city_name == "Unknown":
                        messagebox.showerror("Error", "Could not determine city.")
                        return
                    city_entry.delete(0, tk.END)
                    city_entry.insert(0, city_name)
                    await get_weather()
                else:
                    messagebox.showerror("Error", "Failed to determine location.")
    except Exception as e:
        print(f"Geolocation error: {e}")
        messagebox.showerror("Error", "Location service failed.")

def run_async(func):
    asyncio.run(func())

# Creating the GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("450x400")
root.configure(bg="#f0f4f8")
root.resizable(True, True)
style = ttk.Style()
style.theme_use("clam")  # Modern ttk theme

# Title Label
title_label = ttk.Label(root, text="Weather App", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Entry Field
city_entry = ttk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10, padx=20, fill=tk.X)

# Buttons
search_button = ttk.Button(root, text="Get Weather", command=lambda: run_async(get_weather))
search_button.pack(pady=10)
location_button = ttk.Button(root, text="Use My Location", command=lambda: run_async(get_location))
location_button.pack(pady=10)

# Frame for Text Widget and Scrollbar
text_frame = ttk.Frame(root)
text_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Result Text Widget (With Scrollbar)
result_text = tk.Text(text_frame, font=("Arial", 12), height=6, width=40, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=scrollbar.set)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=result_text.yview)

root.mainloop()