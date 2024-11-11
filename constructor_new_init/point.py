from __future__ import annotations

import math


def this_works():
    class Point(tuple):
        x: int
        y: int

        def __new__(cls, x: float, y: float):
            if x < 0 or y < 0:
                raise ValueError("X and Y must be positive")

            return super().__new__(cls, (x, y))

        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        def distance_from(self, other_point: Point):
            return math.sqrt((other_point.x - self.x) ** 2 + (other_point.y - self.y) ** 2)

    p = Point(1, 2)
    p2 = Point(3, 1)
    print(p.distance_from(other_point=p2))
    print(p)  # Outputs: Point(1, 2)
    print(p[0])  # Outputs: 1 (accessing tuple element)
    print(p[1])  # Outputs: 2 (accessing tuple element)
    print(Point(1, -1))


def this_doesnt_work():
    class Point(tuple):
        def __init__(self, x, y):
            # Initialization (optional in this case as tuple is immutable)
            self.x = x
            self.y = y

    # Usage
    p = Point(1, 2)
    print(p)  # Outputs: Point(1, 2)
    print(p[0])  # Outputs: 1 (accessing tuple element)
    print(p[1])  # Outputs: 2 (accessing tuple element)


# this_doesnt_work()
this_works()

print(tuple((1, 2)))
# print(tuple.__new__(tuple, (1,2)))
print(list([1, 2, 3]))
