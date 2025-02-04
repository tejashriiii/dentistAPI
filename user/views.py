from django.http import JsonResponse
from typing import List
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
        allergy_list = list(models.Allergy.objects.values_list("name", flat=True))
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
        return JsonResponse({"conditions": conditions_list})


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def patients(request, id=None):
    if request.method == "GET":
        all_patients = models.Details.objects.all().values_list()
        return Response({"patients": all_patients}, status=status.HTTP_200_OK)
