from py_inject_test.app_setup import configure_di
from py_inject_test.clients import Client, add_to_db


if __name__ == "__main__":
    configure_di()

    add_to_db(record={"name": "Mike", "age": 34})

    # Using the Client class, which automatically gets SomeService injected
    client = Client()
    client.insert_record(record={"some": "record"})
    client.insert_customer_record(record={"my": "Customer"})
