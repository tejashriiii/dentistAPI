import jwt
from datetime import datetime, timezone, timedelta
import os

key = os.getenv("JWT_KEY")


def create_jwt(role, phonenumber, name):
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    encoded = jwt.encode(
        {
            "role": role,
            "phonenumber": phonenumber,
            "name": name,
            "iat": datetime.now(tz=ist_tz),
            "exp": datetime.now(tz=ist_tz) + timedelta(days=7),
        },
        key,
        algorithm="HS256",
    )
    return encoded


def is_authorized(token, permitted_roles):
    try:
        payload = jwt.decode(
            token,
            key,
            options={"require": ["role", "phonenumber", "name", "iat", "exp"]},
            algorithms="HS256",
        )
    except jwt.ExpiredSignatureError:
        return None, "JWT has expired"
    except jwt.MissingRequiredClaimError:
        return None, "JWT is missing required claims"
    except jwt.DecodeError:
        return None, "Invalid JWT"
    if payload.get("role") not in permitted_roles:
        return None, "You are unauthorized"

    return payload, None
