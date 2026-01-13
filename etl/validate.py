def validate_weather_data(data: dict) -> tuple[bool, list]:
    """
    Validate transformed weather data.

    Returns:
        is_valid (bool): validation status
        errors (list): list of validation error messages
    """
    errors = []

    # =========================
    # NOT NULL CHECKS
    # =========================
    required_fields = [
        "city",
        "country",
        "temperature",
        "humidity",
        "weather_timestamp",
    ]

    for field in required_fields:
        if data.get(field) is None:
            errors.append(f"{field} is NULL")

    # =========================
    # RANGE CHECKS
    # =========================
    temp = data.get("temperature")
    humidity = data.get("humidity")
    wind_speed = data.get("wind_speed")

    if temp is not None and not (-50 <= temp <= 60):
        errors.append(f"temperature out of range: {temp}")

    if humidity is not None and not (0 <= humidity <= 100):
        errors.append(f"humidity out of range: {humidity}")

    if wind_speed is not None and wind_speed < 0:
        errors.append(f"wind_speed out of range: {wind_speed}")

    is_valid = len(errors) == 0
    return is_valid, errors

if __name__ == "__main__":
    from extract import extract_weather_data
    from transform import transform_weather_data

    raw = extract_weather_data("Jakarta")
    transformed = transform_weather_data(raw)

    is_valid, errors = validate_weather_data(transformed)

    print("VALID:", is_valid)
    if errors:
        print("ERRORS:", errors)
