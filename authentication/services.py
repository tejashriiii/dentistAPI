from . import models
from . import validation
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

    if role == "admin" and (user.role in ["admin", "dentist"]):
        return (
            "Admin cannot change admin/dentist's password. Contact dentist",
            status.HTTP_401_UNAUTHORIZED,
        )
    user.password = ""
    user.save()
    return None, None


def set_new_phonenumber(userData, role):
    """
    1. Check if user is valid
    2. Admin only reset patient's number
    3. Validate new phonenumber
    - returns error and status
    """
    new_phone_validate = validation.validate_phonenumber(userData["new_phonenumber"])
    if not new_phone_validate.get("valid"):
        return (
            f"Invalid new phone.{new_phone_validate.get("error")}",
            status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = models.User.objects.get(
            name=userData.get("name"), phonenumber=userData.get("old_phonenumber")
        )
    except models.User.DoesNotExist:
        return "User does not exist", status.HTTP_404_NOT_FOUND

    if role == "admin" and (user.role in ["admin", "dentist"]):
        return (
            "Admin cannot change admin/dentist's password. Contact dentist",
            status.HTTP_401_UNAUTHORIZED,
        )
    user.phonenumber = userData.get("new_phonenumber")
    user.save()
    return None, None
