from datetime import datetime, timezone
from etl.logger import setup_logger


def transform_weather_data(raw_data: dict) -> dict:
    """
    Transform raw OpenWeather API response into a clean, flat structure
    """
    logger = setup_logger()
    logger.info("Transforming raw weather data")

    transformed = {
        "city": raw_data.get("name"),
        "country": raw_data.get("sys", {}).get("country"),
        "temperature": raw_data.get("main", {}).get("temp"),
        "humidity": raw_data.get("main", {}).get("humidity"),
        "weather_description": raw_data.get("weather", [{}])[0].get("description"),
        "wind_speed": raw_data.get("wind", {}).get("speed"),
        "weather_timestamp": datetime.fromtimestamp(
            raw_data.get("dt"), tz=timezone.utc
        ).isoformat(),
        "extracted_at": raw_data.get("extracted_at"),
    }

    logger.info("Weather data transformed successfully")
    return transformed


if __name__ == "__main__":
    from etl.extract import extract_weather_data

    raw = extract_weather_data("Jakarta")
    transformed = transform_weather_data(raw)

    print(transformed)
