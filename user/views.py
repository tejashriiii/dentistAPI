from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Allergy, MedicalCondition


def allergies(request):
    """
    Returns all the allergies stored in the database
    """
    if request.method == "GET":
        allergy_list = list(Allergy.objects.values_list("name", flat=True))
        return JsonResponse({"allergies": allergy_list})


def medical_conditions(request):
    """
    Returns all the medical conditions stored in the database
    """
    if request.method == "GET":
        conditions_list = list(MedicalCondition.objects.values_list("name", flat=True))
        return JsonResponse({"conditions": conditions_list})


def register_details(request):
    # TODO: here you have to make both the user and the details object for a patient
    # First make the user objects save the password as a blank field
    # Then use the primary key from User as primary key in Details
    pass
