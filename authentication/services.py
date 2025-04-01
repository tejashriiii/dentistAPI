from . import models
from rest_framework import status


def set_empty_password(userData, role):
    """
    1. phone+name user does not exist
    2. admin can only reset patient's password
    3. doctor can reset patient, admin and doctor's password
    - returns error and status
    """
    try:
        user = models.User.objects.get(
            name=userData.get("name"), phonenumber=userData.get("phonenumber")
        )
    except models.User.DoesNotExist:
        return "User does not exist", status.HTTP_404_NOT_FOUND

    user_role = user.role
    if role == "admin" and (user_role in ["admin", "dentist"]):
        return (
            "Admin cannot change admin/dentist's password. Contact dentist",
            status.HTTP_401_UNAUTHORIZED,
        )
    user.password = ""
    user.save()
    return None, None
