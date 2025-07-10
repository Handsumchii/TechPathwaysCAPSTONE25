import requests
import os
from dotenv import load_dotenv

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
def get_weather_by_coordinates(lat, lon):
    try:
        response = requests.get(BASE_URL, params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_forecast_by_coordinates(lat, lon):
    try:
        response = requests.get(FORECAST_URL, params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_additional_data_by_coordinates(lat, lon):
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
def get_weather_by_zip(zip_code):
    try:
        response = requests.get(BASE_URL, params={"zip": zip_code, "appid": API_KEY, "units": "metric"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_forecast_by_zip(zip_code):
    try:
        response = requests.get(FORECAST_URL, params={"zip": zip_code, "appid": API_KEY, "units": "metric"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_additional_data_by_zip(zip_code):
    try:
        response = requests.get(ONECALL_URL, params={
            "zip": zip_code,
            "exclude": "minutely,daily,alerts",
            "appid": API_KEY,
            "units": "metric"
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_weather_by_city_id(city_id):
    try:
        response = requests.get(BASE_URL, params={"id": city_id, "appid": API_KEY, "units": "metric"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_forecast_by_city_id(city_id):
    try:
        response = requests.get(FORECAST_URL, params={"id": city_id, "appid": API_KEY, "units": "metric"})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_additional_data_by_city_id(city_id):
    try:
        response = requests.get(ONECALL_URL, params={
            "id": city_id,
            "exclude": "minutely,daily,alerts",
            "appid": API_KEY,
            "units": "metric"
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_weather_by_coordinates_and_city(lat, lon, city):
    try:
        response = requests.get(BASE_URL, params={
            "lat": lat,
            "lon": lon,
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_forecast_by_coordinates_and_city(lat, lon, city):
    try:
        response = requests.get(FORECAST_URL, params={
            "lat": lat,
            "lon": lon,
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_additional_data_by_coordinates_and_city(lat, lon, city):
    try:
        response = requests.get(ONECALL_URL, params={
            "lat": lat,
            "lon": lon,
            "q": city,
            "exclude": "minutely,daily,alerts",
            "appid": API_KEY,
            "units": "metric"
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_weather_by_coordinates_and_zip(lat, lon, zip_code):
    try:
        response = requests.get(BASE_URL, params={
            "lat": lat,
            "lon": lon,
            "zip": zip_code,
            "appid": API_KEY,
            "units": "metric"
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_forecast_by_coordinates_and_zip(lat, lon, zip_code):
    try:
        response = requests.get(FORECAST_URL, params={
            "lat": lat,
            "lon": lon,
            "zip": zip_code,
            "appid": API_KEY,
            "units": "metric"
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def get_additional_data_by_coordinates_and_zip(lat, lon, zip_code):
    try:
        response = requests.get(ONECALL_URL, params={
            "lat": lat,
            "lon": lon,
            "zip": zip_code,
            "exclude": "minutely,daily,alerts",
            "appid": API_KEY,
            "units": "metric"
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    
    
