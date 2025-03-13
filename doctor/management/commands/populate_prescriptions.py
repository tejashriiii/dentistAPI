from django.core.management.base import BaseCommand
from doctor import models
import uuid


class Command(BaseCommand):
    help = "Populate the database with default prescriptions"

    def handle(self, *args, **kwargs):
        prescriptions = [
            {
                "id": uuid.uuid4(),
                "name": "Sensiclave 625",
                "type": "Medication",
            },
            {
                "id": uuid.uuid4(),
                "name": "Ordent",
                "type": "Medication",
            },
            {
                "id": uuid.uuid4(),
                "name": "Zerodol SP",
                "type": "Medication",
            },
            {
                "id": uuid.uuid4(),
                "name": "Metrogill 400",
                "type": "Medication",
            },
            {
                "id": uuid.uuid4(),
                "name": "Rabemac DSR",
                "type": "Medication",
            },
            {
                "id": uuid.uuid4(),
                "name": "Voveron",
                "type": "Injection",
            },
            {
                "id": uuid.uuid4(),
                "type": "Toothpaste",
                "name": "Vantage",
            },
            {
                "id": uuid.uuid4(),
                "type": "Toothpaste",
                "name": "Senquel F",
            },
            {
                "id": uuid.uuid4(),
                "type": "Toothpaste",
                "name": "Thermokind F",
            },
            {
                "id": uuid.uuid4(),
                "type": "Mouthwash",
                "name": "CloveHexPlus",
            },
            {
                "id": uuid.uuid4(),
                "type": "Mouthwash",
                "name": "Bitadine Gargle",
            },
            {
                "id": uuid.uuid4(),
                "type": "Gel",
                "name": "MetroHex",
            },
            {
                "id": uuid.uuid4(),
                "type": "Gel",
                "name": "Annabelle",
            },
        ]

        for prescription in prescriptions:
            models.Prescription.objects.get_or_create(**prescription)

        self.stdout.write(self.style.SUCCESS("Successfully populated prescriptions"))
