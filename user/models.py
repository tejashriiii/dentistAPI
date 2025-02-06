from django.db import models
from authentication.models import User
import uuid


# ==============================NOTE====================================
# Foreign key names are getting an added "_id" at the end of their names


class Details(models.Model):
    """
    id: <UUID> one-to-one key with user_id from User
    date_of_birth: <Date>
    address: <String>
    gender: <M | F | T | O>
    allergies: <String but list inside>
    illnesses: <String but list inside>
    """

    class GenderChoices(models.TextChoices):
        MALE = "M"
        FEMALE = "F"
        TRANSSEXUAL = "T"
        OTHER = "O"

    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    gender = models.CharField(
        max_length=1, choices=GenderChoices.choices, default=GenderChoices.MALE
    )
    allergies = models.TextField(default="")
    illnesses = models.TextField(default="")

    class Meta:
        db_table = "patient_details"


class Complaint(models.Model):
    """
    id: <UUID> (Primary key)
    user: <UUID> (Foreign Key for User)
    complaint: <String> Description of complaint
    date:<Date> when complaint was registered
    time: <Time> when complaint was registered
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.TextField()
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "complaints"
