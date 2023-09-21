import json
from task.config import JSON_DATABASE_NAME


class JsonFileDatabaseConnector:
    def __init__(self) -> None:
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict:
        try:
            with open(JSON_DATABASE_NAME, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"File {JSON_DATABASE_NAME} not found")
            return {}

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

        return new_id

    def get_all(self) -> dict[dict]:
        data = self._read_data()
        return dict(data.values())

    def get_by_id(self, entity_id: int) -> dict:
        data = self._read_data()
        return data.get(str(entity_id), {})
