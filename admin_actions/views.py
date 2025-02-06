from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from authentication import models as auth
from user.models import Complaint, Details
from user.serializers import DetailsSerializer, ComplaintSerializer
import authentication.validation as validation
import authentication.jsonwebtokens as jsonwebtokens
from jwt.exceptions import DecodeError
from django.db import IntegrityError


# Create your views here.
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def details(request):
    """
    Expected JSON
        "phonenumber": "7880589921"
        "details": {
            "name": "john doe",
            "date_of_birth": "1990-02-14",
            "address": "avenue street, gotham city",
            "gender": "M",
        }

    - create a user object first
    - create details object first
    """
    if request.method == "POST":
        # Make sure user is admin
        try:
            token = jsonwebtokens.decode_jwt(
                request.headers["Authorization"].split(" ")[1]
            )
        except DecodeError:
            return Response(
                {"error": "Invalid JWT"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if token.get("role") != "admin":
            return Response(
                {"error": "Only admin access allowed"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Case 2
        phonenumber = request.data.get("phonenumber")
        is_valid_phonenumber: validation.FieldValidity = (
            validation.validate_phonenumber(int(phonenumber))
        )

        if not is_valid_phonenumber["valid"]:
            return Response(
                {"error": is_valid_phonenumber["error"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_object = auth.User.objects.create(
            phonenumber=phonenumber,
            name=request.data.get("details").get("name"),
            role="patient",
            password="",
        )

        serializer = DetailsSerializer(data=request.data.get("details"))
        if not serializer.is_valid():
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Details.objects.create(
                id=user_object,
                date_of_birth=serializer.data["date_of_birth"],
                address=serializer.data["address"],
                gender=serializer.data["gender"],
            )
        except IntegrityError:
            return Response(
                {"error": "Account exists for this name and phonenumber"},
                status=status.HTTP_409_CONFLICT,
            )

        # get role
        return Response(
            {"message": "Details have been registered"}, status=status.HTTP_200_OK
        )


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def complaints(request):
    """
    Registering complaints/appointments for patients

    Flow:
    1. Check if invoker is admin
        - 401 UNAUTHORIZED: Invalid JWT
        - 401 UNAUTHORIZED: Not admin
    2. Validate phonenumber
        - 400 BAD REQUEST: invalid phonenumber
    3. Validate complaint
        - 400 BAD REQUEST: invalid complaint details
    4. Fetch user_id
        - 404 NOT FOUND: User not registered
    5. Register complaint

    Expected JSON

        {
            "phonenumber": "7880589921",
            complaint: {
                "name": "John Doe",
                "chief_complaint": "tooth-ache",
            }
        }


    """
    if request.method == "POST":
        # Make sure user is admin
        try:
            token = jsonwebtokens.decode_jwt(
                request.headers["Authorization"].split(" ")[1]
            )
        except DecodeError:
            return Response(
                {"error": "Invalid JWT"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if token.get("role") != "admin":
            return Response(
                {"error": "Only admin access allowed"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Validate phonenumber
        phonenumber = request.data.get("phonenumber")
        is_valid_phonenumber: validation.FieldValidity = (
            validation.validate_phonenumber(int(phonenumber))
        )
        if not is_valid_phonenumber["valid"]:
            return Response(
                {"error": is_valid_phonenumber["error"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate complaint
        serializer = ComplaintSerializer(data=request.data.get("complaint"))
        if not serializer.is_valid():
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch user_id
        try:
            user = auth.User.objects.get(
                phonenumber=phonenumber, name=serializer.data["name"]
            )
        except auth.User.DoesNotExist:
            return Response(
                {"error": "User is not registered. Register them please"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Register Complaint
        # REMEMBER: Time is being saved as GMT(UTC)
        Complaint.objects.create(
            user=user,
            complaint=serializer.data["chief_complaint"],
        )

        # REMEMBER: When complaint is diagnosed sitting is done, billing is done
        # set user's "active" to False So that we can fetch people who are still
        # "active" the next day for doctor, incase someone is left out
        # Or some followup has been delayed.
        # Also whenever the billing is done (flow ends), update the day in the database for their complaint

        return Response({"message": "complaint registered"}, status=status.HTTP_200_OK)
