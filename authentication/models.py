from django.db import models

# Create your models here.
import uuid


# ==============================NOTE====================================
# Foreign key names are getting an added "_id" at the end of their names


class Permission(models.Model):
    """
    id: <UUID>
    permission_name: <String>
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "permissions"


class Role(models.Model):
    """
    id: <UUID>
    name: <admin | dentist | patient>
    """

    class RoleChoices(models.TextChoices):
        ADMIN = "admin"
        DOC = "dentist"
        PATIENT = "patient"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(
        max_length=7, choices=RoleChoices.choices, default=RoleChoices.PATIENT
    )

    class Meta:
        db_table = "roles"


class RolePermissions(models.Model):
    """
    id: <UUID>
    role: <UUID>
    permission: <UUID>
    """

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
    """
    id: <UUID> user id
    role: <UUID> whether doctor, admin or patient
    phonenumber: <BigInt>
    password: <String>
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    phonenumber = models.BigIntegerField(unique=True)
    password = models.TextField(blank=True)
    active = models.BooleanField()

    class Meta:
        db_table = "credentials"
