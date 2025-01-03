from typing import Dict, List


class PostgresConnection:
    def __init__(self, constring:str):
        self.constring = constring
    def execute(self, stmt:str) -> List[Dict]:
        print(f"simulating query executing '{stmt}' on {self.constring}..")
        return [{'id': 1, 'data': 'xxx'}]

class DatabaseHelper:
    dbcon:PostgresConnection
    def __init__(self, constring:str):
        self.dbcon = PostgresConnection(constring=constring)
    def get_users(self):
        return self.dbcon.execute("select * from users")


def main():
    dbhelper = DatabaseHelper(constring="user:passs@mydatabase")
    users:List[Dict] = dbhelper.get_users()
    print(users)


if __name__ == "__main__":
    main()