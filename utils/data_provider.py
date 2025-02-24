import json


class DataProvider:

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        with open(file_path, 'r') as file:
            self.data = json.load(file)
