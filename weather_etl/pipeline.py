from extract import extract_all_cities
from transform import transform_all
from load import load_to_csv, preview_csv
from datetime import datetime
from logger import get_logger

def run_pipeline():
    """
    Runs the full ETL pipeline:
    1. EXTRACT  - Pull raw weather data from the API
    2. TRANSFORM - Clean and restructure the data
    3. LOAD      - Save the clean data to a CSV file
    """

    print("=" * 50)
    print("   SA WEATHER ETL PIPELINE")
    print(f"   Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print("\nSTEP 1: EXTRACTING data from API...")
    raw_data = extract_all_cities()

    if not raw_data:
        print(" Pipeline stopped — no data was extracted.")
        print("   Check your API key or internet connection.")
        return

    print(f"Extracted data for {len(raw_data)} cities\n")

    
    print("STEP 2: TRANSFORMING raw data...")
    transformed_data = transform_all(raw_data)
    print(f"Transformed {len(transformed_data)} cities\n")

    print("STEP 3: LOADING data into CSV...")
    load_to_csv(transformed_data)

    print("\n" + "=" * 50)
    print("  PIPELINE COMPLETED SUCCESSFULLY")
    print(f"   Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    preview_csv()

logger = get_logger("pipeline")


def run_pipeline():
    """
    Orchestrates the full ETL pipeline.
    """
    logger.info("=" * 50)
    logger.info("SA WEATHER ETL PIPELINE STARTED")
    logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    # STEP 1: EXTRACT
    logger.info("STEP 1: EXTRACTING data from API...")
    raw_data = extract_all_cities()

    if not raw_data:
        logger.error("Pipeline stopped — no data was extracted.")
        logger.error("Check your API key or internet connection.")
        return

    # STEP 2: TRANSFORM
    logger.info("STEP 2: TRANSFORMING raw data...")
    transformed_data = transform_all(raw_data)

    # STEP 3: LOAD
    logger.info("STEP 3: LOADING data into CSV...")
    load_to_csv(transformed_data)

    logger.info("=" * 50)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY")
    logger.info(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    preview_csv()


if __name__ == "__main__":
    run_pipeline()