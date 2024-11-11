from typing import Dict

import inject

from py_inject_test.app_setup import DBCustomer
from py_inject_test.services import SomeService, DatabaseConnection


class Client:
    @inject.autoparams()
    def __init__(self, service: SomeService):
        self.service = service

    def operate(self):
        return self.service.perform()

    @inject.autoparams()
    def insert_record(self, record: Dict, db_service: DatabaseConnection):
        print(id(db_service))
        db_service.insert_record(record=record)

    @inject.autoparams()
    def insert_customer_record(self, record: Dict, db_service: DBCustomer):
        print(id(db_service))
        db_service.insert_record(record=record)


@inject.autoparams()
def add_to_db(record: Dict, database_service: DatabaseConnection):
    print(id(database_service))
    database_service.insert_record(record=record)


@inject.autoparams()
def delete_record(record_id: int, dbservice: DatabaseConnection):
    print(f"deleting record {record_id} from {dbservice}")
    return 1
