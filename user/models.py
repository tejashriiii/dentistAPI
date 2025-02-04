from django.db import models
from authentication.models import User
import uuid
from django.utils import timezone


# ==============================NOTE====================================
# Foreign key names are getting an added "_id" at the end of their names


class Details(models.Model):
    """
    id: <UUID> one-to-one key with user_id from User
    date_of_birth: <Date>
    first_name: <String>
    last_name: <String>
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
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    address = models.TextField()
    gender = models.CharField(
        max_length=1, choices=GenderChoices.choices, default=GenderChoices.MALE
    )
    allergies = models.TextField(default="[]")
    illnesses = models.TextField(default="[]")

    class Meta:
        db_table = "patient_details"


class Complaint(models.Model):
    """
    id: <UUID> (Primary key)
    complaint: <UUID> Primary Key
    complaint: <String> Foreign key from condition
    date:<Date> appointment is scheduled
    time: <Time> Time when appointment is scheduled
    xray: <Int> Tooth number's xray
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    complaint = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    xray = models.IntegerField()

    class Meta:
        db_table = "complaints"
