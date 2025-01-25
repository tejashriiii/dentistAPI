from django.db import models
import uuid


# ==============================NOTE====================================
# Foreign key names are getting an added "_id" at the end of their names


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    permission_name = models.CharField(max_length=50)

    class Meta:
        db_table = "permissions"


class Role(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = "admin"
        DOC = "dentist"
        PATIENT = "patient"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    role_name = models.CharField(
        max_length=7, choices=RoleChoices.choices, default=RoleChoices.PATIENT
    )

    class Meta:
        db_table = "roles"


class RolePermissions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = "rolepermissions"
        constraints = [
            models.UniqueConstraint(
                fields=["role", "permission"],
                name="unique_role_permission_mapping",
            )
        ]


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    phonenumber = models.BigIntegerField(unique=True)
    password = models.TextField()

    class Meta:
        db_table = "users"


class Details(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    address = models.TextField()

    class Meta:
        db_table = "patient_details"


class MedicalCondition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "medical_conditions"


class Allergy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "allergies"


class MedicalHistory(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    recorded = models.DateField()
    patient_specific_note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "allergy_history"
