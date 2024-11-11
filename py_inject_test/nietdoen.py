from abc import ABC, abstractmethod
from typing import Protocol


class Dbcon(ABC):
    @abstractmethod
    def get_token(self) -> str:
        ...


class DbconSqlserver(Dbcon):
    dbcon: str

    def __init__(self, password, user):
        self.dbcon = password + user

    def get_token(self) -> str:
        print(self.dbcon, "gets a token")
        return "token123"


class DbconSqlite(Dbcon):
    dbcon: str

    def __init__(self, password, user, filepath):
        self.dbcon = password + user + filepath

    def get_token(self) -> str:
        print(self.dbcon, "gets a token")
        return "token123"


class Apiclient:
    def __init__(self, dbcon: Dbcon):
        self.dbcon = dbcon

    def do_call(self):
        token = self.dbcon.get_token()
        print(f"retrieving data using {token=}")
        return f"data + {token}"


if __name__ == "__main__":
    # dbcon = DbconSqlserver(password='123', user='mike')
    dbcon = DbconSqlite(password="123", user="mike", filepath="root")
    apiClient = Apiclient(dbcon=dbcon)
    found_data = apiClient.do_call()
    print(found_data)
