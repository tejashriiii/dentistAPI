from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
import authentication.jsonwebtokens as jsonwebtokens
from . import models
from . import serializers
from . import services

# Create your views here.


@api_view(["GET", "POST", "DELETE", "PUT"])
@permission_classes((permissions.AllowAny,))
def treatments(request, treatment_id=None):
    """
    1. GET: Fetch all treatments
    2. POST: Add new treatment
    Expected JSON:
    {
        "name": "RCT"
        "price": 1000,
    }
    3. DELETE: Remove treatment
    2. PUT: Update treatment
    Expected JSON:
    {
        "id": "21ed0219-6358-4555-9efe-b996d2e94508",
        "treatment": {
            "name": "Temporary Filling",
            "price": 2000
        }
    }
    """
    # JWT authentication
    token, error = jsonwebtokens.is_authorized(
        request.headers["Authorization"].split(" ")[1], set(["dentist"])
    )
    if error:
        return Response(
            {"error": error},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "GET":
        treatments = models.Treatment.objects.all().values()
        return Response({"treatments": treatments})

    if request.method == "DELETE":
        if treatment_id:
            name, error = services.delete_treatment_by_id(treatment_id)
            if error:
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": f"{name} deleted"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Treatment could not be deleted"},
                status=status.HTTP_404_NOT_FOUND,
            )
    if request.method == "POST":
        # serialize data
        treatment_serializer = serializers.TreatmentSerializer(
            data=request.data)
        if not treatment_serializer.is_valid():
            return Response(
                {"error": "Duplicate Treatment, it already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # create record
        treatment_serializer.save()

    elif request.method == "PUT":
        treatment_serializer = serializers.TreatmentUpdateSerializer(
            data=request.data["treatment"]
        )
        if not treatment_serializer.is_valid():
            return Response(
                {"error": "Invalid field, check all fields properly"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        error, error_status = services.update_treatment(
            request.data["id"], treatment_serializer.data
        )
        if error:
            return Response({"error": error}, status=error_status)
        return Response(
            {"success": f"{treatment_serializer.data["name"]} updated!"},
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "POST", "DELETE", "PUT"])
@permission_classes((permissions.AllowAny,))
def prescriptions(request, prescription_id=None):
    """
    1. GET: Fetch all prescriptions
    2. POST: Add new prescriptions
    Expected JSON:
    {
        "name": "Voveron"
        "type": "Medication",
    }
    3. DELETE: Remove treatment
    4. PUT: Update treatment
    {
        "id": <UUID>,
        "prescription": {
            "name": "Voveron 300"
            "type": "Injection"
        }
    }
    """
    # JWT authentication
    token, error = jsonwebtokens.is_authorized(
        request.headers["Authorization"].split(" ")[1], set(["dentist"])
    )
    if error:
        return Response(
            {"error": error},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "GET":
        prescriptions = services.fetch_structured_prescriptions()
        return Response({"prescriptions": prescriptions})

    if request.method == "DELETE":
        if prescription_id:
            name, error = services.delete_prescription_by_id(prescription_id)
            if error:
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": f"{name} deleted"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Prescription could not be deleted"},
                status=status.HTTP_404_NOT_FOUND,
            )
    elif request.method == "POST":
        prescription_serializer = serializers.PrescriptionSerializer(
            data=request.data)
        if not prescription_serializer.is_valid():
            return Response(
                {"error": "Duplicate Prescription, it already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        prescription_serializer.save()
        return Response(
            {"success": f"{prescription_serializer.data["name"]} created!"},
            status=status.HTTP_200_OK,
        )
    elif request.method == "PUT":
        prescription_serializer = serializers.PrescriptionUpdateSerializer(
            data=request.data["prescription"]
        )
        if not prescription_serializer.is_valid():
            return Response(
                {"error": "Invalid field, check all fields properly"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # fetch the old prescription
        error, error_status = services.update_prescription(
            request.data["id"], prescription_serializer.data
        )
        if error:
            return Response({"error": error}, status=error_status)
        return Response(
            {"success": f"{prescription_serializer.data["name"]} updated!"},
            status=status.HTTP_200_OK,
        )
