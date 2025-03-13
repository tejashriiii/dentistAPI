from django.db import models
import uuid


class Treatment(models.Model):
    """
    id: <UUID>
    name: <String>
    price: <Integer>
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField(unique=True)
    price = models.IntegerField()

    class Meta:
        db_table = "treatments"


class Prescription(models.Model):
    """
    id: <UUID>
    name: <String>
    type: <String>
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField(unique=True)
    type = models.TextField()

    class Meta:
        db_table = "prescriptions"
