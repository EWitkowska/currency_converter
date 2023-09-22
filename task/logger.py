import logging
from pathlib import Path


def get_logger(name: str, log_file: str) -> logging.Logger:
    log_folder = Path("logs")

    if not log_folder.exists():
        log_folder.mkdir()

    log_file_path = log_folder / log_file

    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
