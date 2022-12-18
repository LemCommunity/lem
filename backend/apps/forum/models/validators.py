import re


def validate_alphabetic(value):
    if not re.match("^[a-zA-Z]*$", value):
        raise ValueError("Input must contain only alphabetic characters")
