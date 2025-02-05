from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from . import models


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def patients(request, phonenumber=None):
    if request.method == "GET":
        if phonenumber:
            patient = models.Details.objects.filter(
                id__phonenumber=phonenumber
            ).values()
            return Response({"patient": patient}, status=status.HTTP_200_OK)
        all_patients = models.Details.objects.all().values_list()
        return Response({"patients": all_patients}, status=status.HTTP_200_OK)
