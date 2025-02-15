from django.db import models

# Create your models here.
import uuid


# ==============================NOTE====================================
# Foreign key names are getting an added "_id" at the end of their names


class User(models.Model):
    """
    id: <UUID> user id
    role: <UUID> whether doctor, admin or patient
    name: <String>
    phonenumber: <BigInt>
    password: <String>
    active: <Bool>
    """

    class RoleChoices(models.TextChoices):
        ADMIN = "admin"
        DOC = "dentist"
        PATIENT = "patient"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    role = models.CharField(
        max_length=10, choices=RoleChoices.choices, default=RoleChoices.PATIENT
    )
    name = models.CharField(max_length=50)
    phonenumber = models.BigIntegerField()
    password = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "credentials"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "phonenumber"], name="unique_phone+name"
            )
        ]
