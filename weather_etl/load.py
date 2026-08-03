import csv
import os
import psycopg2
from dotenv import load_dotenv
from logger import get_logger
from db import get_connection

logger = get_logger("load")

load_dotenv()

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
    """
    Saves transformed weather data to a CSV file.
    """
    create_output_folder()
    file_exists = os.path.exists(OUTPUT_FILE)

    with open(OUTPUT_FILE, mode="a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)

        if not file_exists:
            writer.writeheader()
            logger.info("Created new CSV file with headers")

        for city_data in transformed_data:
            writer.writerow(city_data)
            logger.info(f"Loaded {city_data['city']} into CSV")

    logger.info(f"Data saved to: {OUTPUT_FILE}")


def load_to_postgres(transformed_data):
    """
    Inserts transformed weather data into PostgreSQL database.
    """
    insert_sql = """
        INSERT INTO weather_data (
            city, country, temperature_c, feels_like_c,
            temp_min_c, temp_max_c, humidity_percent,
            wind_speed_mps, condition, extracted_at
        ) VALUES (
            %(city)s, %(country)s, %(temperature_c)s, %(feels_like_c)s,
            %(temp_min_c)s, %(temp_max_c)s, %(humidity_percent)s,
            %(wind_speed_mps)s, %(condition)s, %(extracted_at)s
        );
    """

    conn = get_connection()
    if conn is None:
        logger.error("Cannot load to PostgreSQL — no database connection")
        return False

    try:
        cursor = conn.cursor()

        for city_data in transformed_data:
            cursor.execute(insert_sql, city_data)
            logger.info(f"Inserted {city_data['city']} into PostgreSQL")

        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Successfully inserted {len(transformed_data)} records into PostgreSQL")
        return True

    except Exception as e:
        logger.error(f"Failed to insert data into PostgreSQL: {e}")
        conn.rollback()
        conn.close()
        return False


def preview_postgres():
    """
    Queries and prints the last 5 records from PostgreSQL.
    """
    logger.info("Generating database preview...")
    print("\n Preview of database records:")
    print("-" * 80)

    conn = get_connection()
    if conn is None:
        logger.error("Cannot preview — no database connection")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT city, country, temperature_c, feels_like_c,
                   temp_max_c, temp_min_c, humidity_percent,
                   wind_speed_mps, condition, extracted_at
            FROM weather_data
            ORDER BY extracted_at DESC
            LIMIT 5;
        """)

        rows = cursor.fetchall()

        for row in rows:
            print(f"  City:        {row[0]}, {row[1]}")
            print(f"  Temperature: {row[2]}°C  (Feels like {row[3]}°C)")
            print(f"  High/Low:    {row[4]}°C / {row[5]}°C")
            print(f"  Humidity:    {row[6]}%")
            print(f"  Wind Speed:  {row[7]} m/s")
            print(f"  Condition:   {row[8]}")
            print(f"  Extracted:   {row[9]}")
            print("-" * 80)

        # Get total record count
        cursor.execute("SELECT COUNT(*) FROM weather_data;")
        total = cursor.fetchone()[0]
        print(f" Total records in database: {total}")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Failed to preview database: {e}")


def preview_csv():
    logger.info("Generating CSV preview...")
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

    print(f"Total records in file: {len(rows)}")