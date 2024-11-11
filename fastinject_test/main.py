import random
import time

from fastinject import inject, injectable


@injectable()
class Timer():
    ts_start:float
    def __init__(self) -> None:
        self.ts_start = time.time()
    def check(self):
        print(f"{time.time() - self.ts_start} seconds")

@inject()
def main(timer:Timer):
    print("simulating some work")
    for i in range(3):
        time.sleep(random.random() / 2)
        timer.check()

if __name__ == "__main__":
    main()