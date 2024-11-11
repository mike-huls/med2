## args vs kwargs
def greeter(subject: str, greeting: str, shout: bool = False) -> None:
    greet = f"{greeting}, {subject}"
    if shout:
        greet = greet.upper() + "!"
    print(greet)


greeter("PyGrunn", "hello", False)  # hello, PyGrunn
greeter("PyGrunn", "hello", True)  # HELLO, PYGRUNN!
greeter(True, "PyGrunn", "hello")  # PYGRUNN, TRUE!


greeter(subject="PyGrunn", greeting="hello", shout=False)  # hello, PyGrunn
greeter(subject="PyGrunn", greeting="hello", shout=True)  # HELLO, PYGRUNN!
greeter(shout=True, greeting="hello", subject="PyGrunn")  # HELLO, PYGRUNN!


quit()
greeter("hello", "PyGrunn", False)


greeter(greeting="hello", subject="PyGrunn")


# this means that the order matters
greeter("PyGrunn", "Hi")  # >> PyGrunn, Hi!
# pass positionally
greeter("Hi", "PyGrunn")  # >> Hi, PyGrunn!


# parameters have type hints but no enforcement
def multiply_by_two(my_number: int) -> int:
    return my_number * 2


multiply_by_two(2)  # prints 4
multiply_by_two("hello")  # prints "hellohello"
