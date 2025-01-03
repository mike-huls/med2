from prefect import task, flow

@task
def say_hello(name):
    print(f"Hello, {name}!")

@flow
def greet_flow():
    say_hello("World")

if __name__ == "__main__":
    greet_flow()
