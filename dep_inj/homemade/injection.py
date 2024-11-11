from typing import Dict, Callable


class Injectable:
    _registry = {}

    def __init__(self, providedIn="root"):
        self.providedIn = providedIn

    def __call__(self, cls):
        # print(cls, "<<<", type(cls))
        if self.providedIn == "root":
            instance = cls()
            Injectable._registry[cls] = instance
            return instance
        else:
            return cls

    @staticmethod
    def get(classs: object):
        return Injectable._registry.get(classs.__class__, None)

    def get_registry(self):
        pass


# class Inject:
#
#     def __init__(self, *args, **kwargs):
#         print('init', args, "&&&", kwargs)
#         pass
#
#     def __call__(self, *args, **kwargs):
#     # def __call__(self, func: Callable, *args, **kwargs):
#         print(args, "&&&", kwargs)
#         # if self.providedIn == 'root':
#         #     instance = cls()
#         #     Injectable.get[cls] = instance
#         #     return instance
#         # else:
#         #     return cls


class Inject:
    func: Callable
    call_count: int = 0

    def __init__(self, func):
        self.func = func
        print("init", func)

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        print(self.func.__annotations__)
        for k, v in self.func.__annotations__.items():
            print(f"{k=} : {v=}")
            print(v.get_data())
            print(f"\t {type(k)=} {type(v)=}")
        print("----called")
        print(f"Called {self.func.__name__} for the {self.call_count}th time")
        return self.func(*args, **kwargs)
