import requests
from logger import get_logger

logger = get_logger("extract")

API_KEY = "69fbc8866168904d49f0ab87bb00b6a6"  
CITIES = ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Springs"]
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def extract_weather(city):
    """
    Pulls raw weather data for a single city from the API.
    """
    params = {
        "q": city + ",ZA",
        "appid": API_KEY,
        "units": "metric"
    }

    logger.info(f"Extracting data for {city}...")

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)

        if response.status_code == 200:
            logger.info(f"Successfully extracted data for {city}")
            return response.json()
        else:
            logger.error(f"Failed to get data for {city} — Status: {response.status_code}")
            return None

    except requests.exceptions.Timeout:
        logger.error(f"Request timed out for {city}")
        return None

    except requests.exceptions.ConnectionError:
        logger.error(f"No internet connection — could not reach API for {city}")
        return None


def extract_all_cities():
    """
    Loops through all cities and extracts weather data for each one.
    """
    logger.info(f"Starting extraction for {len(CITIES)} cities")
    raw_data = []

    for city in CITIES:
        data = extract_weather(city)
        if data is not None:
            raw_data.append(data)

    logger.info(f"Extraction complete — {len(raw_data)}/{len(CITIES)} cities successful")
    return raw_data


if __name__ == "__main__":
    results = extract_all_cities()