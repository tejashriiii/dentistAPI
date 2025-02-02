# from authentication.models import User
from authentication.serializers import CredentialSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import status
from . import models
from . import validation
import bcrypt
import os

SALT = os.getenv("SALT")
SALT_BYTES = bytes(SALT, "utf-8")


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def signup(request):
    # TODO: Add password validation here aklfja;fajfklj
    """
    Allows users who have their details stored to create a password for them\n
    1. Form error: 400 BAD REQUEST
    2. Phonenumber not in `User` database: 404 NOT FOUND
    3. Invalid phonenumber: 400 BAD REQUEST
    4. Already registered: 409 CONFLICT
    5. Password validation fail: 400 BAD REQUEST
    6. Successful registration: 201 CREATED

    Flow:\n
    - Admin first creates a `User` object in database and keeps password field empty
    - Patient comes in their details are registered by admin in `Details`, using
    primary key from `User`
    - patient then has to signup and setup their password
    - Once that is done, they can login to their account

    Expected JSON:\n
    All JSON values will be strings only because of JSON works)\n
    ```
    {
        "phonenumber": "7880589921",
        "password": "A1plain_text_password"
    }
    ```
    """
    if request.method == "POST":
        # Case 1
        serializer = CredentialSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Case 2
        is_valid_phonenumber: validation.FieldValidity = (
            validation.validate_phonenumber(serializer.data["phonenumber"])
        )
        if not is_valid_phonenumber["valid"]:
            return Response(
                {"error": is_valid_phonenumber["error"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Case 3
        try:
            user_object = models.User.objects.get(
                phonenumber=serializer.data["phonenumber"]
            )
        except models.User.DoesNotExist:
            return Response(
                {"error": "Phonenumber is not registered by admin"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Case 4
        if user_object.password != "":
            return Response(
                {"error": "Password already set for this phonenumber"},
                status=status.HTTP_409_CONFLICT,
            )

        # Case 5
        is_valid_password: validation.FieldValidity = validation.validate_password(
            serializer.data["password"]
        )
        if not is_valid_password["valid"]:
            return Response(
                {"error": is_valid_password["error"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Case 6
        bytes_password: bytes = bytes(serializer.data["password"], "utf-8")
        hashed_password: bytes = bcrypt.hashpw(bytes_password, SALT_BYTES)
        password_to_store: str = hashed_password.decode("utf-8")
        user_object.password = password_to_store
        user_object.save()
        return Response(
            {"message": "Signup successful!"},
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def login(request):
    """
    Allows the user to login to their account\n
    1. Some form field is empty, invalid etc: returns 400 BAD REQUEST
    2. Not a valid indian number: returns 400 BAD REQUEST
    3. Not in database: returns 404 NOT FOUND
    4. Registered but first signup pending: returns 409 CONFLICT
    5. Incorrect credentials: returns 409 CONFLICT
    6. Correct credentials: returns 200 OK

    Expected JSON:\n
    `{
        "phonenumber": "7880589921",
        "password": "A1plain_text_password"
    }`
    """

    if request.method == "POST":
        # Case 1
        serializer = CredentialSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Case 2
        is_valid_phonenumber: validation.FieldValidity = (
            validation.validate_phonenumber(serializer.data["phonenumber"])
        )
        if not is_valid_phonenumber["valid"]:
            return Response(
                {"error": is_valid_phonenumber["error"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Case 3
        try:
            stored_password: str = models.User.objects.get(
                phonenumber=serializer.data["phonenumber"]
            ).password

        except models.User.DoesNotExist:
            return Response(
                {"error": "Phonenumber isn't registered by admin"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Case 4
        if stored_password == "":
            return Response(
                {"error": "You haven't set up your password. Signup first!"},
                status=status.HTTP_409_CONFLICT,
            )

        # Case 5
        password: bytes = bytes(serializer.data["password"], "utf-8")
        hashed_password: bytes = bytes(stored_password, "utf-8")

        if not bcrypt.checkpw(password, hashed_password):
            return Response(
                {"error": "Incorrect password"}, status=status.HTTP_409_CONFLICT
            )
        # Case 6
        return Response({"token": "should_be_a_token"}, status=status.HTTP_201_CREATED)


# TODO: add dentist (only dentist perm)
# TODO: add admin (only dentist perm)
# TODO: add JWT with "role" as a claim (1 week expiration)
# TODO: change password endpoint
# TODO: change phonenumber endpoint
# TODO: maybe add refresh tokens
