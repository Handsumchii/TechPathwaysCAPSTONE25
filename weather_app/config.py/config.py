from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ONECALL_URL = "https://api.openweathermap.org/data/2.5/onecall"
def get_weather_data(city):
    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_hourly_forecast(city):
    try:
        response = requests.get(FORECAST_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_additional_data(lat, lon):
    try:
        response = requests.get(ONECALL_URL, params={
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,daily,alerts",
            "appid": API_KEY,
            "units": "metric"
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
# Ensure the API_KEY is set in your .env file
if not API_KEY:
    raise ValueError("API_KEY not found in .env file. Please set it to use the weather API.")
# This module handles all interactions with the OpenWeatherMap API.
# It provides functions to get current weather data, hourly forecasts, and additional weather data based on latitude and longitude.
# Make sure to set your OpenWeatherMap API key in a .env file with the variable `OPENWEATHER_API_KEY`.
