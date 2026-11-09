from extract import extract_all_cities
from transform import transform_all
from validate import validate_all
from load import load_to_csv, load_to_postgres, preview_postgres
from db import create_table
from logger import get_logger
from datetime import datetime

logger = get_logger("pipeline")


def run_pipeline():
    logger.info("=" * 50)
    logger.info("SA WEATHER ETL PIPELINE STARTED")
    logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    logger.info("STEP 1: EXTRACTING data from API...")
    raw_data = extract_all_cities()

    if not raw_data:
        logger.error("Pipeline stopped — no data was extracted.")
        return

    logger.info("STEP 2: TRANSFORMING raw data...")
    transformed_data = transform_all(raw_data)

    logger.info("STEP 3: VALIDATING data quality...")
    validated_data = validate_all(transformed_data)

    if not validated_data:
        logger.error("Pipeline stopped — no data passed validation.")
        return

    logger.info("STEP 4: LOADING data...")
    
    create_table()
    
    load_to_csv(validated_data)
    load_to_postgres(validated_data)

    logger.info("=" * 50)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY")
    logger.info(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    preview_postgres()


if __name__ == "__main__":
    run_pipeline()