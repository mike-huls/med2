def multiply(a, b):
    return a * b




def dingen(
        *args, **kwargs
):
    print(args)
    print(kwargs)
    pass

def multiply(a, b, *args):
    result = a * b
    for arg in args:
        result = result * arg
    return result


def introduce(firstname, lastname, **kwargs):
    introduction = f"I am {firstname} {lastname}"
    for key, value in kwargs.items():
        introduction += f", my {key} is {value} "
    return introduction


# ARGS

print(multiply(2, 3))                   # --> 6
print(multiply(multiply(2, 3), 6))      # --> 36

print(multiply(2, 3))                   # --> 6
print(multiply(2, 3, 6))                # --> 36
print(multiply(2, 3, 6, 3, 4))          # --> 432

# KWargs

# prints: "I am Mike Huls"
print(introduce(firstname="Mike", lastname="Huls"))
# prints: "I am Mike Huls, my age is 34, my website is mikehuls.com"
print(introduce(firstname="Mike", lastname="Huls", age=34, website="mikehuls.com"))

print(introduce('mike', 'huls'))


def multiply(a, b, *):
    return a * b
