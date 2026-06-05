import requests

# Your API key from OpenWeatherMap
API_KEY = "69fbc8866168904d49f0ab87bb00b6a6"  # 👈 Replace this with your actual key

# South African cities we want weather data for
CITIES = ["Johannesburg", "Cape Town", "Durban", "Pretoria","Springs"]

# The base URL for the OpenWeatherMap API
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def extract_weather(city):
    """
    Pulls raw weather data for a single city from the API.
    Returns the raw JSON response as a Python dictionary.
    """
    params = {
        "q": city + ",ZA",   # ZA = South Africa country code
        "appid": API_KEY,
        "units": "metric"    # So temperatures come in Celsius
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        print(f"✅ Successfully extracted data for {city}")
        return response.json()
    else:
        print(f"❌ Failed to get data for {city}. Status code: {response.status_code}")
        return None


def extract_all_cities():
    """
    Loops through all cities and extracts weather data for each one.
    Returns a list of raw weather dictionaries.
    """
    raw_data = []

    for city in CITIES:
        data = extract_weather(city)
        if data is not None:
            raw_data.append(data)

    return raw_data


# lets you test this file on its own
if __name__ == "__main__":
    results = extract_all_cities()
    print(f"\n📦 Total cities extracted: {len(results)}")
    print("\nSample raw data for first city:")
    print(results[0])  