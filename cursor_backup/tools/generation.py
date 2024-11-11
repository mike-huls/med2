import random
import string


def generate_string(size=10) -> str:
    # Define the characters to use: all lowercase, uppercase letters, and digits
    characters = string.ascii_letters + string.digits

    # Generate a random string of the given size
    random_name = "".join(random.choice(characters) for _ in range(size))

    return random_name
