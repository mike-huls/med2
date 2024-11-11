import os

import inject

from .services import SomeService, DatabaseConnection


class DBSystem(DatabaseConnection):
    pass


class DBCustomer(DatabaseConnection):
    pass


def config(binder: inject.Binder):
    print(type(binder))
    print("configuring inject")

    (binder.bind(SomeService, SomeService()),)
    binder.bind(DBCustomer, DatabaseConnection(database="customers", name=os.environ.get("dbname"), password=os.environ.get("dbpass")))
    # todo check customerdata and systemdata
    binder.bind(DBSystem, DatabaseConnection(database="system", name=os.environ.get("dbnasdfame"), password=os.environ.get("dasdfbpass")))


def configure_di():
    print("setting env varaibles for test")
    os.environ["dbname"] = "mike"
    os.environ["dbpass"] = "secret_pasword"
    inject.configure(config)
