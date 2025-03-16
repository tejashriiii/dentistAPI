from django.db import models
from authentication.models import User
import uuid
from doctor.models import Treatment


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
    smoking: <Bool>
    drinking: <Bool>
    tobacco: <Bool>
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
    allergies = models.TextField(default="", blank=True)
    illnesses = models.TextField(default="", blank=True)
    smoking = models.BooleanField(default=False)
    drinking = models.BooleanField(default=False)
    tobacco = models.BooleanField(default=False)

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


class Diagnosis(models.Model):
    """
    id: <UUID> (Primary key)
    complaint: <Complaint> (Foreign Key for User)
    tooth_number:<Int> when complaint was registered
    treatment: <Treatment> (Foreight Key for treatment)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    tooth_number = models.IntegerField()
    treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT)

    class Meta:
        db_table = "diagnosis"
        constraints = [
            models.UniqueConstraint(
                fields=["complaint", "tooth_number"],
                name="unique_complaint+tooth_number",
            )
        ]


class FollowUp(models.Model):
    """
    id: <UUID> (Primary key)
    complaint: <Complaint> (Foreign Key for Complaint)
    title:<String> The name of followup that patient sees
    description:<String> What the dentist ended up doing in this sitting (private)
    date: <Date> When followup is scheduled
    time: <Time> When followup is scheduled
    completed: <Bool> Whether sitting has been completed or not
    number: <Int> Followup no. since complaint
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    number = models.IntegerField()

    class Meta:
        db_table = "followups"
        constraints = [
            models.UniqueConstraint(
                fields=["complaint", "number"], name="unique_complaint+number"
            )
        ]
