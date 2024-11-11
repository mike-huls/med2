from typing import Dict


class SomeService:
    def perform(self):
        return "Service performed!"


class DatabaseConnection:
    name: str
    password: str

    def __init__(self, database: str, name: str, password: str):
        self.database = database
        self.name = name
        self.password = password
        print(f"Connecting with {name=} and {password=} ({database=})")

    def insert_record(self, record: Dict) -> None:
        print(f"Inserting {record} using engine with {self.name}:{self.password}")
