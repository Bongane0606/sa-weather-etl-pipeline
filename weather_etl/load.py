import csv
import os
from logger import get_logger

logger = get_logger("load")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "weather_data.csv")

CSV_COLUMNS = [
    "city", "country", "temperature_c", "feels_like_c",
    "temp_min_c", "temp_max_c", "humidity_percent",
    "wind_speed_mps", "condition", "extracted_at"
]


def create_output_folder():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        logger.info(f"Created output folder: {OUTPUT_FOLDER}")


def load_to_csv(transformed_data):
    create_output_folder()
    file_exists = os.path.exists(OUTPUT_FILE)

    with open(OUTPUT_FILE, mode="a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)

        if not file_exists:
            writer.writeheader()
            logger.info("Created new CSV file with headers")

        for city_data in transformed_data:
            writer.writerow(city_data)
            logger.info(f"Loaded data for {city_data['city']} into CSV")

    logger.info(f"Data saved to: {OUTPUT_FILE}")


def preview_csv():
    logger.info("Generating data preview...")
    print("\n Preview of saved data:")
    print("-" * 80)

    with open(OUTPUT_FILE, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

        for row in rows[-5:]:
            print(f"  City:        {row['city']}, {row['country']}")
            print(f"  Temperature: {row['temperature_c']}°C  (Feels like {row['feels_like_c']}°C)")
            print(f"  High/Low:    {row['temp_max_c']}°C / {row['temp_min_c']}°C")
            print(f"  Humidity:    {row['humidity_percent']}%")
            print(f"  Wind Speed:  {row['wind_speed_mps']} m/s")
            print(f"  Condition:   {row['condition']}")
            print(f"  Extracted:   {row['extracted_at']}")
            print("-" * 80)

    print(f" Total records in file: {len(rows)}")
