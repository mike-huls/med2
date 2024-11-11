import json
from typing import List, Dict


class GenericServiceExample:
    my_args: List
    my_kwargs: Dict

    def __init__(self, *args, **kwargs):
        self.my_args = args
        self.my_kwargs = kwargs

    def __repr__(self):
        return str({"inst": self.__class__.__name__, "id": id(self)} | self.__dict__.copy())

    def __str__(self):
        return self.__repr__()


class DatabaseConnExample(GenericServiceExample):
    def __init__(self, username: str, password: str, host: str, port: int, database: str):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database


class ApiClientExample(GenericServiceExample):
    """Ideally you'd only have one instance of this service."""

    def __init__(self, url: str, token: str, timeout: int):
        self.url = url
        self.token = token
        self.timeout = timeout


class PhotoService(GenericServiceExample):
    """You can have multiople instances of this service"""

    def __init__(self, api_client: ApiClientExample):
        self.apiclient = api_client

    def process_photo(self, photo_thing: str):
        print(f"Processing photo: {photo_thing} to {self.apiclient.url}")


class TopicExample(GenericServiceExample):
    def __init__(self, url: str, path: str, token: str):
        if url is None:
            raise ValueError("Invalid url")
        self.url = url
        self.path = path
        self.token = token


if __name__ == "__main__":
    print(GenericServiceExample(1, 2, 3, 4, 5, 6, a="jojo"))
    print(DatabaseConnExample("jojo", "jojo", "localhost", 3306, database="testdb"))
    print(ApiClientExample(url="http://localhost1", token="token1"))
    print(PhotoService(api_client=ApiClientExample(url="http://localhost2", token="token2")))
