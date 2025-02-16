# from celery import shared_task
# from django.utils import timezone
# from myapp.models import Appointment  # Import your model 
# import json
# import urllib.request
# from django.conf import settings

# @shared_task
# def send_whatsapp_reminder():
#     """
#     Fetch appointments from the database and send reminders via WhatsApp API.
#     Runs 24 hours before the appointment time.
#     """
#     now = timezone.now()
#     reminder_time = now + timezone.timedelta(days=1)  # 24 hours before

#     # Get appointments scheduled for tomorrow
#     appointments = Appointment.objects.filter(followup_datetime__date=reminder_time.date())

#     for appointment in appointments:
#         phone_number = appointment.patient_phone
#         template_name = "appointment_reminder"
#         language_code = "en_US"

#         payload = json.dumps({
#             "messaging_product": "whatsapp",
#             "to": phone_number,
#             "type": "template",
#             "template": {
#                 "name": template_name,
#                 "language": {"code": language_code},
#             },
#         }).encode("utf-8")

#         headers = {
#             "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
#             "Content-Type": "application/json",
#         }

#         try:
#             req = urllib.request.Request(settings.WHATSAPP_API_URL, data=payload, headers=headers, method="POST")
#             with urllib.request.urlopen(req) as response:
#                 response.read()
#         except Exception as e:
#             print(f"Failed to send message to {phone_number}: {e}")

#     return f"Sent {len(appointments)} reminders"

from celery import shared_task
from django.utils import timezone
import json
import urllib.request
from django.conf import settings

@shared_task
def send_whatsapp_message():
    """
    Send a WhatsApp message using the WhatsApp Cloud API.
    """

    try:
        phone_number = "91XXXXXXXXXX" # Change this to your phone number
        template_name = "hello_world"
        language_code = "en_US"

        # WhatsApp API payload
        payload = json.dumps(
            {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": language_code},
                },
            }
        ).encode("utf-8")

        # Headers
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

        # Create API request
        req = urllib.request.Request(
            settings.WHATSAPP_API_URL, data=payload, headers=headers, method="POST"
        )

        # Send API request
        with urllib.request.urlopen(req) as response:
            result = response.read().decode("utf-8")
            

    except urllib.error.HTTPError as e:
        error_message = e.read().decode("utf-8")
        return Response(json.loads(error_message), status=e.code)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
