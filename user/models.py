from django.db import models
from authentication.models import User
import uuid


# ==============================NOTE====================================
# Foreign key names are getting an added "_id" at the end of their names


class Details(models.Model):
    """
    id: <UUID> one-to-one key with user_id from User
    date_of_birth: <Date>
    first_name: <String>
    last_name: <String>
    address: <String>
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

    class Meta:
        db_table = "patient_details"


class MedicalCondition(models.Model):
    """
    id: <UUID>
    name: <String>
    description: <String>
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "medical_conditions"


class Allergy(models.Model):
    """
    id: <UUID>
    name: <String>
    description: <String>
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "allergies"


class MedicalHistory(models.Model):
    """
    id: <UUID> (Primary key)
    user: <UUID> Foreign key from User
    condition: <UUID> Foreign key from condition
    recorded:<Date> When did the medical issue happen
    patient_specific_note: <String>
    created_at: <DateTime> When the record was created
    updated_at: <DateTime> When the record was last updated
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    recorded = models.DateField()
    patient_specific_note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "medical_history"


class AllergyHistory(models.Model):
    """
    id: <UUID> (Primary key)
    user: <UUID> Foreign key from User
    allergy: <UUID> Foreign key from condition
    recorded:<Date> When did the medical issue happen
    patient_specific_note: <String>
    created_at: <DateTime> When the record was created
    updated_at: <DateTime> When the record was last updated
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    recorded = models.DateField()
    patient_specific_note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "allergy_history"


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
