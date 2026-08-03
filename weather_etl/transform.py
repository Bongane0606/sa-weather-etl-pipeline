from datetime import datetime
from weather_etl.logger import get_logger


def transform_city_weather(raw_data):
    """
    Takes raw messy API data for one city and extracts
    only the fields we care about, in a clean structure.
    """
    transformed = {
        "city":             raw_data["name"],
        "country":          raw_data["sys"]["country"],
        "temperature_c":    raw_data["main"]["temp"],
        "feels_like_c":     raw_data["main"]["feels_like"],
        "temp_min_c":       raw_data["main"]["temp_min"],
        "temp_max_c":       raw_data["main"]["temp_max"],
        "humidity_percent": raw_data["main"]["humidity"],
        "wind_speed_mps":   raw_data["wind"]["speed"],
        "condition":        raw_data["weather"][0]["description"],
        "extracted_at":     datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return transformed


def transform_all(raw_data_list):
    """
    Takes a list of raw city data and transforms each one.
    Returns a clean list of dictionaries.
    """
    transformed_list = []

    for raw_city in raw_data_list:
        clean_city = transform_city_weather(raw_city)
        transformed_list.append(clean_city)
        print(f" Transformed data for {clean_city['city']}")

    return transformed_list


if __name__ == "__main__":
    fake_raw_data = [
        {
            "name": "Johannesburg",
            "sys": {"country": "ZA"},
            "main": {
                "temp": 18.5,
                "feels_like": 17.2,
                "temp_min": 15.0,
                "temp_max": 21.0,
                "humidity": 65
            },
            "wind": {"speed": 3.5},
            "weather": [{"description": "clear sky"}]
        },
        {
            "name": "Cape Town",
            "sys": {"country": "ZA"},
            "main": {
                "temp": 14.0,
                "feels_like": 13.0,
                "temp_min": 11.0,
                "temp_max": 16.0,
                "humidity": 80
            },
            "wind": {"speed": 5.2},
            "weather": [{"description": "light rain"}]
        }
    ]

    results = transform_all(fake_raw_data)

    print("\nTransformed Data:")
    for city in results:
        print(city)

logger = get_logger("transform")


def transform_city_weather(raw_data):
    """
    Takes raw API data for one city and extracts clean fields.
    """
    transformed = {
        "city":             raw_data["name"],
        "country":          raw_data["sys"]["country"],
        "temperature_c":    raw_data["main"]["temp"],
        "feels_like_c":     raw_data["main"]["feels_like"],
        "temp_min_c":       raw_data["main"]["temp_min"],
        "temp_max_c":       raw_data["main"]["temp_max"],
        "humidity_percent": raw_data["main"]["humidity"],
        "wind_speed_mps":   raw_data["wind"]["speed"],
        "condition":        raw_data["weather"][0]["description"],
        "extracted_at":     datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    logger.info(f"Transformed data for {transformed['city']}")
    return transformed


def transform_all(raw_data_list):
    """
    Transforms a list of raw city data.
    """
    logger.info(f"Starting transformation for {len(raw_data_list)} cities")
    transformed_list = []

    for raw_city in raw_data_list:
        clean_city = transform_city_weather(raw_city)
        transformed_list.append(clean_city)

    logger.info(f"Transformation complete — {len(transformed_list)} cities transformed")
    return transformed_list