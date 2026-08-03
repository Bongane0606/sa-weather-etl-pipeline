from weather_etl.logger import get_logger

logger = get_logger("validate")

RULES = {
    "temperature_c":    (-20, 60),
    "feels_like_c":     (-20, 60),
    "temp_min_c":       (-20, 60),
    "temp_max_c":       (-20, 60),
    "humidity_percent": (0, 100),
    "wind_speed_mps":   (0, 113),  
}


def validate_city(city_data):
    """
    Runs quality checks on a single city's transformed data.
    Returns True if data passes all checks, False if it fails.
    """
    city = city_data.get("city", "Unknown")
    passed = True

    required_fields = [
        "city", "country", "temperature_c", "feels_like_c",
        "temp_min_c", "temp_max_c", "humidity_percent",
        "wind_speed_mps", "condition", "extracted_at"
    ]

    for field in required_fields:
        if field not in city_data or city_data[field] is None or city_data[field] == "":
            logger.warning(f"[{city}] FAILED — Missing or empty field: '{field}'")
            passed = False

    for field, (min_val, max_val) in RULES.items():
        if field in city_data:
            try:
                value = float(city_data[field])
                if not (min_val <= value <= max_val):
                    logger.warning(
                        f"[{city}] FAILED — '{field}' value {value} "
                        f"is outside expected range ({min_val} to {max_val})"
                    )
                    passed = False
            except (ValueError, TypeError):
                logger.warning(f"[{city}] FAILED — '{field}' is not a valid number")
                passed = False

    try:
        temp_min = float(city_data.get("temp_min_c", 0))
        temp_max = float(city_data.get("temp_max_c", 0))
        if temp_min > temp_max:
            logger.warning(
                f"[{city}] FAILED — temp_min ({temp_min}) "
                f"is greater than temp_max ({temp_max})"
            )
            passed = False
    except (ValueError, TypeError):
        pass

    if passed:
        logger.info(f"[{city}] PASSED all quality checks ")

    return passed


def validate_all(transformed_data):
    """
    Validates all cities and returns only the ones that pass.
    Logs a summary at the end.
    """
    logger.info(f"Starting data quality validation for {len(transformed_data)} cities")

    passed_data = []
    failed_count = 0

    for city_data in transformed_data:
        if validate_city(city_data):
            passed_data.append(city_data)
        else:
            failed_count += 1

    logger.info(f"Validation complete — {len(passed_data)} passed, {failed_count} failed")

    if failed_count > 0:
        logger.warning(f"{failed_count} cities failed validation and were NOT loaded")

    return passed_data