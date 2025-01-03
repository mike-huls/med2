import abc
import os
import sys
from typing import Dict, List, Protocol


class Connection(abc.ABC):
    @abc.abstractmethod
    def execute(self, stmt: str) -> List[Dict]:
        pass


class PostgresConnection(Connection):
    def __init__(self, constring:str):
        self.constring = constring
    def execute(self, stmt:str) -> List[Dict]:
        print(f"simulating query executing '{stmt}' on {self.constring}..")
        return [{'id': 1, 'data': 'xxx'}]


class SqlServerConnection(Connection):
    def __init__(self, constring:str):
        self.constring = "https://" + constring
    def execute(self, stmt:str) -> List[Dict]:
        print(f"simulating query executing '{stmt}' on {self.constring}..")
        return [{'id': 1, 'data': 'xxx'}]


class DatabaseHelper:
    dbcon:Connection
    def __init__(self, dbcon:Connection):
        self.dbcon = dbcon
    def get_users(self):
        return self.dbcon.execute("select * from users")


def main():
    os.environ['databasetype'] = 'sqlserver'
    if os.environ.get("databasetype") == 'sqlserver':
        dbcon = SqlServerConnection(constring="user:pass@sqlserverhost")
    elif os.environ.get("databasetype") == 'postgres':
        dbcon = PostgresConnection(constring="user:pass@postgreshost")
    else:
        dbcon = SQLiteConnection(constring="user:pass@sqlitehost")
        quit(1)
    dbhelper = DatabaseHelper(dbcon=dbcon)
    users:List[Dict] = dbhelper.get_users()
    print(users)


if __name__ == "__main__":
    main()