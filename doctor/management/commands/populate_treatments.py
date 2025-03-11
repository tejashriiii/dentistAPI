from django.core.management.base import BaseCommand
from doctor import models
import uuid


class Command(BaseCommand):
    help = "Populate the database with default treatments"

    def handle(self, *args, **kwargs):
        treatments = [
            {
                "id": uuid.uuid4(),
                "name": "Wisdom Tooth Extraction (Impaction)",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Mobile/Form Extraction",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "RCT",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Episectomy",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Temporary Filling",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "GIC Filling",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Composite (Light Cure) Filling",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Silver Filling",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Nickel Chrome Metal Cap",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Ceramic Cap",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "VitaCeramic Cap",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Cadcam Cap",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Zirconia Crown Cap",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Removable Orthodontics",
                "price": 1000,
            },
            {
                "id": uuid.uuid4(),
                "name": "Fixed Appliance Orthodontics",
                "price": 1000,
            },
        ]

        for treatment in treatments:
            models.Treatment.objects.get_or_create(**treatment)

        self.stdout.write(self.style.SUCCESS("Successfully populated treatments"))
