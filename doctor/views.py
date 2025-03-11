from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
import authentication.jsonwebtokens as jsonwebtokens
from . import models

# Create your views here.


@api_view(["GET", "POST", "DELETE"])
@permission_classes((permissions.AllowAny,))
def treatments(request):
    """
    1. GET: Fetch all treatments
    2. POST: Add new treatment
    3. DELETE: Remove treatment
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
