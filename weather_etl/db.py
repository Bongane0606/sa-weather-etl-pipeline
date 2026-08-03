import psycopg2
import os
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger("db")

load_dotenv()


def get_connection():
    """
    Creates and returns a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        logger.info("Successfully connected to PostgreSQL database")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None


def create_table():
    """
    Creates the weather_data table if it doesn't already exist.
    """
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS weather_data (
            id                SERIAL PRIMARY KEY,
            city              VARCHAR(100) NOT NULL,
            country           VARCHAR(10) NOT NULL,
            temperature_c     NUMERIC(5,2),
            feels_like_c      NUMERIC(5,2),
            temp_min_c        NUMERIC(5,2),
            temp_max_c        NUMERIC(5,2),
            humidity_percent  INTEGER,
            wind_speed_mps    NUMERIC(5,2),
            condition         VARCHAR(200),
            extracted_at      TIMESTAMP
        );
    """

    conn = get_connection()
    if conn is None:
        logger.error("Cannot create table — no database connection")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        logger.info("Table 'weather_data' is ready")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Failed to create table: {e}")
        conn.rollback()
        conn.close()
        return False


def test_connection():
    """
    Quick test to verify database connection is working.
    """
    conn = get_connection()
    if conn:
        logger.info("Database connection test PASSED ✅")
        conn.close()
        return True
    else:
        logger.error("Database connection test FAILED ❌")
        return False


if __name__ == "__main__":
    test_connection()
    create_table()