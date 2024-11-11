import dataclasses
import sys
import uuid
from typing import Annotated, Any, Type

from annotated.cpt import validate_field


# target


@dataclasses.dataclass
class Person:
    id: str  # uuid
    name: str  # max len 50
    age: int  # less than 150
    fte: float  # between 0 and 1
    has_dog: bool  # 0 or 1


# VALIDATORS
def str_max_length(max_len: int):
    def validator(value: str) -> bool:
        return len(value) <= max_len

    return validator


def str_any_length():
    def validator(value: str) -> bool:
        return True

    return validator


def is_bool():
    def validator(value: bool) -> bool:
        return value in (True, False)

    return validator


def is_int():
    def validator(value: int) -> bool:
        return type(value) == int

    return validator


def is_float():
    def validator(value: int) -> bool:
        return type(value) == float

    return validator


def is_positive():
    def validator(value: int) -> bool:
        return value >= 0

    return validator


def int_max_value(max_val: int):
    def validator(value: int) -> bool:
        return value <= max_val

    return validator


def float_max_value(max_val: float):
    def validator(value: float) -> bool:
        return value <= max_val

    return validator


# TYPES
# all floats are signed
UUID = Annotated[str, str_max_length(36)]
STR = Annotated[str, str_any_length()]
BOOL = Annotated[bool, is_bool()]
FLOAT_32 = Annotated[float, float_max_value(sys.float_info.max / 2)]
FLOAT_64 = Annotated[float, float_max_value(sys.float_info.max)]
INT_U8 = Annotated[int, is_int(), is_positive(), int_max_value(255)]


# Annotated
@dataclasses.dataclass
class Person:
    id: UUID  # uuid
    name: STR  # max len 50
    age: INT_U8  # less than 150
    fte: FLOAT_32  # between 0 and 1
    has_dog: BOOL

    def validate(self):
        """Validates the data set"""
        col: Any
        anno: Type
        for col, anno in self.__annotations__.items():
            if not "__metadata__" in anno.__dict__.keys():
                raise AttributeError(f"The type for field '{col}' is not annotated correctly")

            for annotation in anno.__metadata__:
                try:
                    is_valid = annotation(self.__getattribute__(col))
                    if not (is_valid):
                        raise ValueError("Invalid; didn't conform to annotation")
                except AttributeError as e:
                    raise AttributeError(f"The type for field '{col}' is not annotated correctly: {e}")
                except Exception as e:
                    raise ValueError(f"Unable to validate: {e}")


if __name__ == "__main__":
    p = Person(id=str(uuid.uuid4()), name="mike", age=34, has_dog=False, fte=0.8)
    p.validate()
