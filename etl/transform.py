from datetime import datetime, timezone

def transform_weather_data(raw_data: dict) -> dict:
    """
    Transform raw OpenWeather API response into a clean, flat structure
    """

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

    return transformed

if __name__ == "__main__":
    from extract import extract_weather_data

    raw = extract_weather_data("Jakarta")
    transformed = transform_weather_data(raw)

    print(transformed)
