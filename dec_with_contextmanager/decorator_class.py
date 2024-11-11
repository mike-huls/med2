class MyDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("calling func")
        self.func(*args, **kwargs)
        print("after")


def do_something():
    print("doing something")


my_dec_instance = MyDecorator(func=do_something)
my_dec_instance()
quit()


@MyDecorator
def do_something():
    print("doing something")


do_something()
