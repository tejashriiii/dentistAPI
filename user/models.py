from django.db import models


# ==============================NOTE====================================
# Foreign key names are getting an added "_id" at the end of their names


class Permission(models.Model):
    permission_id = models.TextField(primary_key=True)
    permission_name = models.TextField(max_length=255)

    class Meta:
        db_table = "permission"


class Role(models.Model):
    role_id = models.TextField(primary_key=True)
    role_name = models.TextField(max_length=20)

    class Meta:
        db_table = "role"


class RolePermissions(models.Model):
    mapping_id = models.TextField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = "rolepermissions"
        constraints = [
            models.UniqueConstraint(
                fields=["role_id", "permission_id"],
                name="unique_role_permission_mapping",
            )
        ]


class User(models.Model):
    user_id = models.TextField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    phonenumber = models.BigIntegerField(unique=True)
    password = models.TextField()

    class Meta:
        db_table = "users"
