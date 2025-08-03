import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_weather_data(city_name, units="metric"):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("❌ Missing API key. Make sure WEATHER_API_KEY is set in your .env file.")
        return None

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": units
    }

    try:
        response = requests.get(base_url, params=params)
        print(f"🌐 Request URL: {response.url}")
        print(f"🔄 Status Code: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Weather fetch failed. Status Code: {response.status_code}")
            print(f"⚠️ Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Weather fetch exception: {e}")
        return None
