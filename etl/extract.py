import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def extract_weather_data(city: str) -> dict:
    """
    Extract current weather data from OpenWeather API
    """
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.text}")

    data = response.json()

    data["extracted_at"] = datetime.utcnow().isoformat()

    return data

if __name__ == "__main__":
    city = "Jakarta"
    weather_data = extract_weather_data(city)
    print(weather_data)
