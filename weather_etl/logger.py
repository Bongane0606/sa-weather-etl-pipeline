import logging
import os
from datetime import datetime

LOGS_FOLDER = "logs"

def get_logger(name):
    """
    Creates and returns a logger that writes to both
    the terminal AND a log file simultaneously.
    """

    if not os.path.exists(LOGS_FOLDER):
        os.makedirs(LOGS_FOLDER)

    
    log_filename = os.path.join(
        LOGS_FOLDER,
        f"pipeline_{datetime.now().strftime('%Y-%m-%d')}.log"
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger