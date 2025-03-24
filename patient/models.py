from django.db import models
from authentication.models import User
import uuid
from doctor.models import Treatment, Prescription


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
    description: <String> What doctor did during sitting
    date:<Date> when complaint was registered
    time: <Time> when complaint was registered
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.TextField()
    description = models.TextField(default="")
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


class Bill(models.Model):
    """
    id: <UUID>
    complaint: <Complaint> along with which bill is associated
    full_bill: <Integer> Total amount (without discount)
    discount: <Integer> Amount of discount given by the dentist
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE)
    full_bill = models.IntegerField()
    discount = models.IntegerField()

    class Meta:
        db_table = "bills"


class PatientPrescription(models.Model):
    """
    id: <UUID>
    complaint: <Complaint>
    sitting: = 0 for complaint, >= 1 for followups
    prescription: <Prescription>
    days: <Integer>
    dosage: <OD | BD | TD | Half BD | Half TD | "">
    """

    class DosageChoices(models.TextChoices):
        OD = "OD"
        BD = "BD"
        TD = "TD"
        HALF_BD = "HALF BD"
        HALF_TDS = "HALF TDS"
        EMPTY = ""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    sitting = models.IntegerField()
    prescription = models.ForeignKey(Prescription, on_delete=models.PROTECT)
    days = models.IntegerField()
    dosage = models.CharField(
        max_length=10, choices=DosageChoices.choices, default=DosageChoices.EMPTY
    )

    class Meta:
        db_table = "patient_prescriptions"
        constraints = [
            models.UniqueConstraint(
                fields=["complaint", "sitting", "prescription"],
                name="unique_complaint+sitting+prescription",
            )
        ]
