def greet_something(thing_to_greet: str, greeting: str, extra_kind: bool) -> None:
    what_to_say = f"{greeting}, {thing_to_greet}!"
    if extra_kind:
        what_to_say += " Have a nice day!"
    print(what_to_say)


# pass positionally
greet_something("Hi", "PyGrunn", True)
# this means that the order matters
greet_something("PyGrunn", "Hi", True)
# And can even lead to very strance behavior
greet_something("PyGrunn", True, "Hi")


# pass with keyword arguments
greet_something(thing_to_greet="PyGrunn", greeting="Hi", extra_kind=True)
# order doesnt matter
greet_something(greeting="Hi", thing_to_greet="PyGrunn", extra_kind=True)
greet_something(thing_to_greet="PyGrunn", extra_kind=True, greeting="Hi")
