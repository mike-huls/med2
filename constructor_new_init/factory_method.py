class Shape:
    # This is a base class for different shapes
    pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def __str__(self):
        return f"Circle with radius {self.radius}"


class Square(Shape):
    def __init__(self, side: float):
        self.side = side

    def __str__(self):
        return f"Square with side {self.side}"


class ShapeFactory:
    @staticmethod
    def __new__(cls, shape_type: str, *args, **kwargs):
        if shape_type == "circle":
            return Circle(*args, **kwargs)
        elif shape_type == "square":
            return Square(*args, **kwargs)
        else:
            raise ValueError("Unknown shape type")


# Usage
circle = ShapeFactory("circle", radius=5)
square = ShapeFactory("square", side=10)

print(circle)  # Circle with radius 5
print(square)  # Square with side 10
