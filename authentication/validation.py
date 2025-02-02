from typing import TypedDict


class FieldValidity(TypedDict):
    error: str
    valid: bool


def validate_phonenumber(phonenumber: int) -> FieldValidity:
    """
    1. Valid integer
    2. 10 digits long
    3. Startswith 6, 7, 8 or 9
    """
    phone: str = str(phonenumber)
    starting_numbers = set([6, 7, 8, 9])

    if len(phone) != 10:
        return {"error": "Phonenumber is not 10 digits long", "valid": False}

    if int(phone[0]) not in starting_numbers:
        return {"error": "Phonenumber should start with 6, 7, 8, 9", "valid": False}

    return {"error": None, "valid": True}


def validate_password(password: str) -> FieldValidity:
    """
    Validates the password based on the following criteria:
    1. Length of at least 8 characters
    2. Contains at least one number
    3. Contains at least one uppercase letter
    """
    if len(password) < 8:
        return {"error": "Password should have at least 8 characters", "valid": False}

    contains_number = False
    contains_uppercase = False

    for char in password:
        if char.isdigit():
            contains_number = True
        elif char.isupper():
            contains_uppercase = True

    if not contains_number:
        return {"error": "Password should contain a number", "valid": False}

    if not contains_uppercase:
        return {"error": "Password should contain a capitalized letter", "valid": False}

    return {"error": None, "valid": True}
