import json


class LocalFileReader:
    def __init__(self, filename) -> None:
        self.filename = filename

    def read(self) -> dict:
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"File {self.filename} not found")
            return {}
