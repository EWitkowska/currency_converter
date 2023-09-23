import logging
from pathlib import Path


class CustomLogger:
    def __init__(
        self,
        name: str,
        log_file: str,
        enable_logging: bool = True,
    ):
        self.logger = logging.getLogger(name)
        self.enable_logging = enable_logging

        if enable_logging:
            log_folder = Path("logs")

            if not log_folder.exists():
                log_folder.mkdir()

            log_file_path = log_folder / log_file

            self.logger.setLevel(logging.WARNING)

            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
        else:
            self.logger.addHandler(logging.NullHandler())
            self.logger.setLevel(logging.CRITICAL)

    def get_logger(self):
        return self.logger
