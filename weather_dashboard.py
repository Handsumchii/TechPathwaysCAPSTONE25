import tkinter as tk
from tkinter import messagebox
import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHERMAP_KEY")
API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Save weather to file
def save_weather_to_file(city, temp, description):
    with open("data/weather_history.txt", "a") as file:
        file.write(f"{city},{temp},{description}\n")

# Fetch weather from API
def fetch_weather(city):
    try:
        params = {"q": city, "appid": API_KEY, "units": "imperial"}
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize()
        }
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch weather data: {e}")
        return None
