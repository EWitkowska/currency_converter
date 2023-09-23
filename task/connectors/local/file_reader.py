import json
from task.logger import CustomLogger


class LocalFileReader:
    def __init__(self, filename, enable_logging: bool = True) -> None:
        self.filename = filename
        self.logger = CustomLogger(
            __name__, "local_file_reader.log", enable_logging=enable_logging
        ).get_logger()

    def read(self) -> dict:
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError as err:
            self.logger.error(f"File {self.filename} not found: {err}")
            return {}
        except json.JSONDecodeError as err:
            self.logger.error(f"Error decoding JSON in file {self.filename}: {err}")
            return {}
