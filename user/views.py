from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Allergy, MedicalCondition
from .serializers import AllergySerializer, MedicalConditionSerializer

# from rest_framework.parsers import JSONParser


@csrf_exempt
def allergies(request):
    """
    Returns all the allergies stored in the database
    """
    if request.method == "GET":
        all_allergies = Allergy.objects.all()
        serializer = AllergySerializer(all_allergies, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def medical_conditions(request):
    """
    Returns all the medical conditions stored in the database
    """
    if request.method == "GET":
        all_medical_conditions = MedicalCondition.objects.all()
        serializer = MedicalConditionSerializer(all_medical_conditions, many=True)
        return JsonResponse(serializer.data, safe=False)


"""
from http import HTTPStatus
from django.http import HttpResponse, JsonResponse
import json
import bcrypt
    #TODO: Send this to auth app instead of user here
    @csrf_exempt
    def login(request):
        if request.method == "POST":
           login_json = json.loads(request.body)
           byte_password = login_json["password"].encode("UTF-8")
           hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
           User.objects.create(
                role=login_json["role"],
                phonenumber=login_json["phonenumber"],
                password=hashed_password,
            )
            print("hello there")
            print(f"password: {login_json["password"]}")
            print(f"byte password: {byte_password}")
            print(f"hashed password: {hashed_password}")
            # TODO: Duplicate phonenumber validation
            response = HttpResponse()
            response.status_code = HTTPStatus.CREATED
            response.reason_phrase = "User created"
        return response
"""
