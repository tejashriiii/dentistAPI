from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from django.conf import settings
import json
import urllib.request

@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def send_whatsapp_message(request):
    """
    Send a WhatsApp message using the WhatsApp Cloud API.
    """
    try:
        # Extract data from request
        phone_number = request.data.get("phone_number")
        template_name = request.data.get("template_name", "hello_world")
        language_code = request.data.get("language_code", "en_US")

        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # WhatsApp API payload
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
            }
        }).encode("utf-8")

        # Headers
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

        # Create API request
        req = urllib.request.Request(settings.WHATSAPP_API_URL, data=payload, headers=headers, method="POST")

        # Send API request
        with urllib.request.urlopen(req) as response:
            result = response.read().decode("utf-8")
            return Response(json.loads(result), status=status.HTTP_200_OK)

    except urllib.error.HTTPError as e:
        error_message = e.read().decode("utf-8")
        return Response(json.loads(error_message), status=e.code)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
