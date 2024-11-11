class Turtle:
    name: str

    def __init__(self, name: str):
        self.name = name

    def move(self):
        print(f"A Turtle named {self.name} is slowly moving forward..")


class Hare:
    name: str

    def __init__(self, name: str):
        self.name = name

    def move(self):
        print(f"A hare named {self.name} is racing forward!")


class AnimalFactory:
    def __new__(cls, animal: str, name: str, *args, **kwargs):
        animal = animal.lower()
        name = name.capitalize()
        if animal == "turtle":
            return Turtle(name=name)
        elif animal == "hare":
            return Hare(name=name)


turtle1 = AnimalFactory(animal="turtle", name="bertrand")
turtle1.move()

turtle2 = AnimalFactory(animal="tURTle", name="percy")
turtle2.move()

hare = AnimalFactory(animal="HAre", name="hare1")
hare.move()
