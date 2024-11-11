import traceback

def func_a():
    func_b()

def func_b():
    func_c()

def func_c():
    # Print the call stack
    stack = traceback.format_stack()
    print("".join(stack))

func_a()
