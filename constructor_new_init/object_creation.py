class SimleObject:
    greet_name: str

    def __init__(self, name: str):
        self.greet_name = name

    def say_hello(self) -> None:
        print(f"Hello {self.greet_name}!")


my_instance = SimleObject(name="bob")
my_instance.say_hello()


class SimpleObject:
    """my docstring"""

    greet_name: str

    def __new__(cls, *args, **kwargs):
        print("__new__ method")
        instance = super().__new__(cls)
        return instance

    def __init__(self, name: str):
        print("__init__ method")
        self.greet_name = name

    def say_hello(self) -> None:
        print(f"Hello {self.greet_name}!")


my_instance = SimpleObject(name="bob")
my_instance = SimpleObject.__new__(SimpleObject)
my_instance.__init__(name="bob")
my_instance.say_hello()
print(type(my_instance))
my_instance = SimpleObject(name="bob")
print(isinstance(my_instance, object))
print(isinstance(42, object))
print(isinstance("hello world", object))
print(isinstance({"my": "dict"}, object))

my = object.__new__(SimpleObject)
print(type(my))

# print(dir(object))
# print(object.__hash__(my_instance))
# print(my_instance.__hash__())
# print("dok")
# print(my_instance.__doc__())
