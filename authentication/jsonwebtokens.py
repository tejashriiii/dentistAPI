import jwt
import os

key = os.getenv("JWT_KEY")


def create_jwt(role, phonenumber):
    encoded = jwt.encode(
        {"role": role, "phonenumber": phonenumber}, key, algorithm="HS256"
    )
    return encoded


def decode_jwt(token):
    roleAndPhone = jwt.decode(token, key, algorithms="HS256")
    return roleAndPhone
