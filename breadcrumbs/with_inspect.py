import inspect

def func_a():
    func_b()

def func_b():
    func_c()

def func_c():
    # Retrieve the call stack
    stack = inspect.stack()
    for frame in stack:
        print(f"Function {frame.function} called from {frame.filename}:{frame.lineno}")

func_a()
