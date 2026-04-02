import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_current_weather(city: str):
    """
    Fetch current weather data from OpenWeather API.
    """
    if not API_KEY:
        raise ValueError("API key not found. Set OPENWEATHER_API_KEY in .env")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(CURRENT_URL, params=params, timeout=15)
    data = response.json()

    if response.status_code != 200:
        raise Exception(f"API Error: {data}")

    return data


def get_forecast(city: str):
    """
    Fetch 5-day / 3-hour forecast data from OpenWeather API.
    """
    if not API_KEY:
        raise ValueError("API key not found. Set OPENWEATHER_API_KEY in .env")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(FORECAST_URL, params=params, timeout=15)
    data = response.json()

    if response.status_code != 200:
        raise Exception(f"API Error: {data}")

    return data["list"]