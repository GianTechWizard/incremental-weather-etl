from etl.logger import setup_logger


def validate_weather_data(data: dict) -> tuple[bool, list]:
    logger = setup_logger()
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

    if not is_valid:
        logger.error(f"Validation failed with errors: {errors}")
    else:
        logger.info("Validation passed successfully")

    return is_valid, errors


def data_quality_report(data: dict) -> dict:
    logger = setup_logger()
    report = {
        "total_records": 1,
        "null_fields": [k for k, v in data.items() if v is None],
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
        "wind_speed": data.get("wind_speed"),
    }

    logger.info(f"Data Quality Report generated: {report}")
    return report


if __name__ == "__main__":
    from etl.extract import extract_weather_data
    from etl.transform import transform_weather_data

    raw = extract_weather_data("Jakarta")
    transformed = transform_weather_data(raw)

    is_valid, errors = validate_weather_data(transformed)
    report = data_quality_report(transformed)

    print("VALID:", is_valid)
    print("DATA QUALITY REPORT:", report)

    if errors:
        print("ERRORS:", errors)
