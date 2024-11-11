class DingesFactory:
    _args_instance = {}

    def __new__(cls, *args, **kwargs):
        key = (str(args), str(kwargs))

        if key in cls._args_instance.keys():
            return cls._args_instance[key]
        else:
            instance = super(DingesFactory, cls).__new__(cls)
            cls._args_instance[key] = instance
            return instance


# Usage
conn1 = DingesFactory("a")
conn2 = DingesFactory("b")

# Simulate closing and reusing a connection
conn3 = DingesFactory("b")

print(id(conn1))
print(id(conn2))
print(id(conn3))

# Should print True because conn3 reuses the connection returned to the pool by conn1
print(conn2 is conn3)
