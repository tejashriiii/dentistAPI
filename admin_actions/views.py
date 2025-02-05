from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from authentication import models as auth
from user.models import Complaint, Details
from user.serializers import DetailsSerializer, ComplaintSerializer
import authentication.validation as validation
import authentication.jsonwebtokens as jsonwebtokens
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
        # get roleid
        token = jsonwebtokens.decode_jwt(request.headers["Authorization"].split(" ")[1])
        phonenumber = request.data.get("phonenumber")
        if token.get("role") != "admin":
            return Response(
                {"error": "Only admin access allowed"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Case 2
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

        print(request.data.get("details"))
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
    Registering appointments for patients
    Expected JSON

        {
            "phonenumber": "7880589921",
            "complaint": {
                "date": "2025-02-14",
                "time": "06:00",
                "chief_complaint": "tooth-ache",
                "xray": "42"
            }
        }


    """
    if request.method == "POST":
        is_valid_phonenumber: validation.FieldValidity = (
            validation.validate_phonenumber(request.data.get("phonenumber"))
        )
        if not is_valid_phonenumber["valid"]:
            return Response(
                {"error": is_valid_phonenumber["error"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get user
        try:
            user = auth.User.objects.get(phonenumber=request.data.get("phonenumber"))
        except auth.User.DoesNotExist:
            return Response(
                {"error": "Phonenumber does not belong to registered user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        print(request.data)
        serializer = ComplaintSerializer(data=request.data.get("complaint"))
        if not serializer.is_valid():
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )

        # TODO: add validation for not having time clashes
        Complaint.objects.create(
            user=user,
            time=serializer.data["time"],
            date=serializer.data["date"],
            xray=serializer.data["xray"],
            chief_complaint=serializer.data["chief_complaint"],
        )

        return Response({"message": "complaint registered"}, status=status.HTTP_200_OK)
