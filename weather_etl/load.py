import csv
import os
from datetime import datetime


# Where we want to save our data
OUTPUT_FOLDER = "output"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "weather_data.csv")

# The column names for our CSV file
CSV_COLUMNS = [
    "city",
    "country",
    "temperature_c",
    "feels_like_c",
    "temp_min_c",
    "temp_max_c",
    "humidity_percent",
    "wind_speed_mps",
    "condition",
    "extracted_at"
]


def create_output_folder():
    """
    Creates the output folder if it doesn't exist yet.
    """
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"📁 Created output folder: {OUTPUT_FOLDER}")


def load_to_csv(transformed_data):
    """
    Saves the transformed weather data to a CSV file.
    If the file already exists, it APPENDS new data to it.
    If it doesn't exist, it creates it with headers first.
    """
    create_output_folder()

    # Check if file already exists (so we know whether to write headers)
    file_exists = os.path.exists(OUTPUT_FILE)

    with open(OUTPUT_FILE, mode="a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)

        # Only write the header row if the file is new
        if not file_exists:
            writer.writeheader()
            print("📝 Created new CSV file with headers")

        # Write each city as a row
        for city_data in transformed_data:
            writer.writerow(city_data)
            print(f"✅ Loaded data for {city_data['city']} into CSV")

    print(f"\n💾 Data saved to: {OUTPUT_FILE}")


def preview_csv():
    """
    Reads and prints the CSV file in a clean, readable table format.
    """
    print("\n📊 Preview of saved data:")
    print("-" * 80)

    with open(OUTPUT_FILE, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

        # Print each city as a clean readable block
        for row in rows[-5:]:  # Only show the last 5 rows (most recent run)
            print(f"🏙️  City:        {row['city']}, {row['country']}")
            print(f"🌡️  Temperature: {row['temperature_c']}°C  (Feels like {row['feels_like_c']}°C)")
            print(f"🔼  High/Low:    {row['temp_max_c']}°C / {row['temp_min_c']}°C")
            print(f"💧  Humidity:    {row['humidity_percent']}%")
            print(f"💨  Wind Speed:  {row['wind_speed_mps']} m/s")
            print(f"⛅  Condition:   {row['condition']}")
            print(f"🕐  Extracted:   {row['extracted_at']}")
            print("-" * 80)

    print(f"📁 Total records in file: {len(rows)}")

# Test this file on its own using fake transformed data
if __name__ == "__main__":
    # Fake transformed data (output from transform.py)
    fake_transformed_data = [
        {
            "city": "Johannesburg",
            "country": "ZA",
            "temperature_c": 18.5,
            "feels_like_c": 17.2,
            "temp_min_c": 15.0,
            "temp_max_c": 21.0,
            "humidity_percent": 65,
            "wind_speed_mps": 3.5,
            "condition": "clear sky",
            "extracted_at": "2026-06-05 08:30:00"
        },
        {
            "city": "Cape Town",
            "country": "ZA",
            "temperature_c": 14.0,
            "feels_like_c": 13.0,
            "temp_min_c": 11.0,
            "temp_max_c": 16.0,
            "humidity_percent": 80,
            "wind_speed_mps": 5.2,
            "condition": "light rain",
            "extracted_at": "2026-06-05 08:30:00"
        }
    ]

    load_to_csv(fake_transformed_data)
    preview_csv()