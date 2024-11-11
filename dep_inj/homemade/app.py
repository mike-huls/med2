from dep_inj.homemade.injection import Injectable, Inject


# Usage example
@Injectable(providedIn="root")
class MyService:
    def __init__(self, name: str = "not set"):
        self.data = f"Hello, {name} from a service1"

    def get_data(self):
        return self.data


@Injectable(providedIn="root")
class SomeOtherService:
    def __init__(self, name: str = "not set"):
        self.data = f"Hello, {name} from a service2"

    def get_data(self):
        return self.data


@Inject
def use_services(my_service: SomeOtherService = None):
    # print(type(my_service))
    # print(my_service)
    # print(my_service.get_data())
    pass


# This would be how you access the singleton instance
service_instance = Injectable.get(MyService)
other_instance = Injectable.get(SomeOtherService)
print(1, service_instance.get_data())
print(1, other_instance.get_data())
# print(service_instance.get_data())
use_services()
