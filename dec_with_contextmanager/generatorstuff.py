def generator_fn():
    print("\tbefore yield")
    yield
    print("\tafter yield")


print("before create generator")
gen = generator_fn()
print("after create generator")

print("before next on generator")
next(gen)
print("after next on generator")
