import json
from task.config import JSON_DATABASE_NAME
from task.logger import CustomLogger


class JsonFileDatabaseConnector:
    def __init__(self, enable_logging: bool = True) -> None:
        self.logger = CustomLogger(
            __name__, "json_database.log", enable_logging=enable_logging
        ).get_logger()
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict:
        with open(JSON_DATABASE_NAME, "r") as file:
            data = json.load(file)
        return data

    def save(self, entity: dict) -> int:
        data = self._read_data()

        max_id = max(data.keys(), default=0, key=int)
        new_id = int(max_id) + 1

        entity["currency"] = entity["currency"]
        entity["price_in_pln"] = entity["price_in_pln"]

        entity["id"] = new_id
        entity = {"id": entity["id"], **entity}
        data[new_id] = entity

        with open(JSON_DATABASE_NAME, "w") as file:
            json.dump(data, file, indent=4)

        self.logger.info(
            f"Data with ID {new_id} saved successfully to the JSON database"
        )
        return new_id

    def get_all(self) -> dict[dict]:
        data = self._read_data()
        return dict(data.values())

    def get_by_id(self, entity_id: int) -> dict:
        data = self._read_data()
        entity_data = data.get(str(entity_id), {})
        if not entity_data:
            self.logger.warning(
                f"Data with ID {entity_id} not found in the JSON database"
            )
        return entity_data
