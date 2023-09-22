import json
from task.logger import get_logger

logger = get_logger(__name__, "local_file_reader.log")


class LocalFileReader:
    def __init__(self, filename) -> None:
        self.filename = filename

    def read(self) -> dict:
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError as err:
            logger.error(f"File {self.filename} not found: {err}")
            return {}
        except json.JSONDecodeError as err:
            logger.error(f"Error decoding JSON in file {self.filename}: {err}")
            return {}
