import typing
from typing import Annotated


# Define a constraint as metadata
def max_length(max_len: int):
    def validator(value: str) -> bool:
        print(value)
        return len(value) <= max_len

    return validator
    # return len(value) <= max_len


# A hypothetical function that uses the metadata for validation
def validate_field(field_value: typing.Any, field_type: typing._AnnotatedAlias):
    # Imagine this function knows how to interpret the annotations
    # and perform validation based on them. This is pseudocode.
    print("J j")
    print(field_type)
    print(type(field_type))
    for annotation in field_type.__metadata__:
        print(annotation)
        print(type(annotation))
        # if not annotation(field_value):
        #     raise ValueError("Validation failed")


if __name__ == "__main__":
    # Use Annotated to attach a max_length constraint to a string
    MaxLengthString = Annotated[str, max_length(10), "dingen"]

    # Using the annotated type
    validate_field(field_value="aaa", field_type=MaxLengthString)  # Hypothetical validation call
