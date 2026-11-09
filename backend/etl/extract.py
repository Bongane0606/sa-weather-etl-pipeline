import os
import requests
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger("extract")

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# One representative city per South African province. "city" is the name
# passed to OpenWeatherMap's geocoding -- for provinces where the modern
# official city name isn't reliably recognised by the API, the more common
# historical name is used instead (noted below).
CITIES = [
    {"city": "Johannesburg", "province": "Gauteng"},
    {"city": "Cape Town", "province": "Western Cape"},
    {"city": "Durban", "province": "KwaZulu-Natal"},
    {"city": "Port Elizabeth", "province": "Eastern Cape"},   # now Gqeberha
    {"city": "Bloemfontein", "province": "Free State"},
    {"city": "Polokwane", "province": "Limpopo"},
    {"city": "Nelspruit", "province": "Mpumalanga"},          # now Mbombela
    {"city": "Mahikeng", "province": "North West"},
    {"city": "Kimberley", "province": "Northern Cape"},
]

if not API_KEY:
    logger.error("API_KEY is not set. Add it to your .env file.")


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
    The province is attached onto the raw response so it survives
    into transform.py without needing a second lookup there.
    """
    logger.info(f"Starting extraction for {len(CITIES)} cities")
    raw_data = []

    for entry in CITIES:
        data = extract_weather(entry["city"])
        if data is not None:
            data["province"] = entry["province"]
            raw_data.append(data)

    logger.info(f"Extraction complete — {len(raw_data)}/{len(CITIES)} cities successful")
    return raw_data


if __name__ == "__main__":
    results = extract_all_cities()