import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    if not API_KEY:
        print("❌ API key not found.")
        return {}
    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        return response.json()
    except Exception as e:
        print(f"❌ Weather fetch error: {e}")
        return {}
