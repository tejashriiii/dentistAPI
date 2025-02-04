from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from . import models


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def allergies(request):
    """
    Returns all the allergies stored in the database
    """
    if request.method == "GET":
        allergy_list = list(
            models.Allergy.objects.values_list("name", flat=True))
        print(allergy_list)
        return JsonResponse({"allergies": allergy_list})


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def medical_conditions(request):
    """
    Returns all the medical conditions stored in the database
    """
    if request.method == "GET":
        conditions_list = list(
            models.MedicalCondition.objects.values_list("name", flat=True)
        )
        print(conditions_list)
        return JsonResponse({"conditions": conditions_list})


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def patients(request, phonenumber=None):
    if request.method == "GET":
        if id:
            patient = models.Details.objects.filter(
                id__phonenumber=phonenumber
            ).values()
            print(patient)
            return Response({"patient": patient}, status=status.HTTP_200_OK)
        all_patients = models.Details.objects.all().values_list()
        return Response({"patients": all_patients}, status=status.HTTP_200_OK)
