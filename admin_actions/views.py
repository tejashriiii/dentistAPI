from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from authentication import models as auth
from user import models as user
from user.serializers import DetailsSerializer, ComplaintSerializer
import user.validation as validation
from django.db import IntegrityError


# Create your views here.
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def details(request):
    """
    Expected JSON

        {
            "phonenumber": "7880589921",
            "details": {
                "first_name": "john",
                "last_name": "doe",
                "date_of_birth": "1990-02-14",
                "address": "avenue street, gotham city",
                "gender": "M",
                "illnesses": "fever,diabetes-1",
                "allergies": "pollen,peanute"
            }
        }

    - create a user object first
    - create details object first
    """
    if request.method == "POST":
        # get roleid
        id = auth.Role.objects.get(name="patient")

        # TODO: add check for duplicate phonenumber (spoiler alert you never will)
        try:
            user_object = auth.User.objects.create(
                phonenumber=request.data.get("phonenumber"), role=id, password=""
            )
        except IntegrityError:
            return Response(
                {"error": "Duplicate phonenumber"}, status=status.HTTP_409_CONFLICT
            )

        # Case 2
        is_valid_phonenumber: validation.FieldValidity = (
            validation.validate_phonenumber(request.data.get("phonenumber"))
        )
        if not is_valid_phonenumber["valid"]:
            return Response(
                {"error": is_valid_phonenumber["error"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DetailsSerializer(data=request.data.get("details"))
        if not serializer.is_valid():
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user.Details.objects.create(
                id=user_object,
                date_of_birth=serializer.data["date_of_birth"],
                first_name=serializer.data["first_name"],
                last_name=serializer.data["last_name"],
                address=serializer.data["address"],
                gender=serializer.data["gender"],
                illnesses=serializer.data["illnesses"],
                allergies=serializer.data["allergies"],
            )
        except IntegrityError:
            return Response(
                {"error": "Tried entering details again for recorded phonenumber"},
                status=status.HTTP_409_CONFLICT,
            )

        # get role
        return Response(
            {"message": "details have been registered"}, status=status.HTTP_200_OK
        )


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def save_appointment(request):
    """
    Registering appointments for patients
    Expected JSON

    ```
    {
        date: "2025-02-14",
        time: "06:00",
        chief_complaint: "tooth-ache",
        xray: "42",
    }

    ```

    """
    if request.method == "POST":
        serializer = ComplaintSerializer(request.data)
        if not serializer.is_valid():
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )

        user
        user.Complaint.objects.create()
        return Response({"message": "complaint registered"}, status=status.HTTP)
