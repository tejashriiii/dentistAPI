from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from . import models
import authentication.jsonwebtokens as jsonwebtokens
from jwt.exceptions import DecodeError


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def patients(request, phonenumber=None, active=None):
    """
    1. Retrieve single patient
    2. Retrieve many patients
    """
    # Make sure user is admin or doctor

    if request.method == "GET":
        # Fetch single patient
        if phonenumber:
            patient = models.Details.objects.filter(
                id__phonenumber=phonenumber
            ).values()
            return Response({"patient": patient}, status=status.HTTP_200_OK)

    try:
        token = jsonwebtokens.decode_jwt(request.headers["Authorization"].split(" ")[1])
    except DecodeError:
        return Response(
            {"error": "Invalid JWT"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if token.get("role") != "admin" and token.get("dentist") != "doctor":
        return Response(
            {"error": "Only admin access allowed"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

        # Fetch all patients
        all_patients = models.Details.objects.all().values_list()
        return Response({"patients": all_patients}, status=status.HTTP_200_OK)
