from typing import Dict


def stackoverflow():
    def getId(self):
        return self.__id

    def addID(original_class):
        orig_init = original_class.__init__
        # Make copy of original __init__, so we can call it without recursion

        def __init__(self, id, *args, **kws):
            self.__id = id
            self.getId = getId
            orig_init(self, *args, **kws)  # Call the original __init__

        original_class.__init__ = __init__  # Set the class' __init__ to the new one
        return original_class

    class Foo:
        def __init__(self):
            print("init of foo")

    Foo = addID(Foo)

    @addID
    class Foo:
        pass


def cgpt():
    class AddMethodDecorator:
        def __init__(self, cls):
            self.cls = cls

        def __call__(self):
            # Add a new method to the class
            def new_method(self):
                return "This is a new method added by the class decorator"

            # Attach the new method to the class
            self.cls.new_method = new_method
            return self.cls

    @AddMethodDecorator
    class MyClass:
        def method(self):
            return "This is a method"

    # Since the decorator is a class, it needs to be instantiated with MyClass as argument,
    # which is automatically done by the @ syntax. However, the resulting object is a
    # AddMethodDecorator instance, to get the modified class, we call the instance.
    MyDecoratedClass = MyClass()

    # Create an instance of the decorated class
    my_instance = MyDecoratedClass()

    # Call the existing method
    print(my_instance.method())  # Output: This is a method

    # Call the new method added by the decorator
    print(my_instance.new_method())  # Output: This is a new method added by the class decorator


def cgpt2():
    class Injectable:
        cls: type
        _registry: Dict[type, object] = {}

        def __init__(self, cls):
            self.cls = cls

        def __call__(self, cls):
            # Add a new method to the class
            print(cls, "<<<")
            print(type(self.cls))
            print(self.cls.__name__)
            print(self.cls.__name__)
            self._registry[self.cls] = self.cls()

            # def new_method(self):
            #     return "This is a new method added by the class decorator"
            #
            # # Attach the new method to the class
            # self.cls.new_method = new_method
            return self.cls

    @Injectable()
    class MyClass:
        def method(self):
            return "This is a method"

    # Since the decorator is a class, it needs to be instantiated with MyClass as argument,
    # which is automatically done by the @ syntax. However, the resulting object is a
    # AddMethodDecorator instance, to get the modified class, we call the instance.
    MyDecoratedClass = MyClass()

    # Create an instance of the decorated class
    my_instance = MyDecoratedClass()

    # Call the existing method
    print(my_instance.method())  # Output: This is a method


cgpt2()
