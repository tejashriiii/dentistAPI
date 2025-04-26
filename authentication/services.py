from . import models
from . import validation
from patient import services as patient_services
from rest_framework import status


def set_empty_password(userData, role):
    """
    1. incorrect phonenumber
    2. phone+name user does not exist
    3. admin can only reset patient's password
    4. doctor can reset patient, admin and doctor's password
    - returns error and status
    """
    is_valid_phonenumber: validation.FieldValidity = validation.validate_phonenumber(
        userData.get("phonenumber")
    )
    if not is_valid_phonenumber["valid"]:
        return (
            is_valid_phonenumber["error"],
            status.HTTP_400_BAD_REQUEST,
        )
    try:

        user = models.User.objects.get(
            name=patient_services.capitalize_name(userData.get("name")),
            phonenumber=userData.get("phonenumber"),
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
    1. incorrect phonenumber
    2. Check if user is valid
    3. Admin only reset patient's number
    4. Validate new phonenumber
    - returns error and status
    """
    is_valid_phonenumber: validation.FieldValidity = validation.validate_phonenumber(
        userData.get("old_phonenumber")
    )
    if not is_valid_phonenumber["valid"]:
        return (
            is_valid_phonenumber["error"],
            status.HTTP_400_BAD_REQUEST,
        )

    is_valid_phonenumber: validation.FieldValidity = validation.validate_phonenumber(
        userData.get("new_phonenumber")
    )
    if not is_valid_phonenumber["valid"]:
        return (
            is_valid_phonenumber["error"],
            status.HTTP_400_BAD_REQUEST,
        )

    if userData.get("old_phonenumber") == userData.get("new_phonenumber"):
        return (
            "Old and new phonenumber are same",
            status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = models.User.objects.get(
            name=patient_services.capitalize_name(userData.get("name")),
            phonenumber=userData.get("old_phonenumber"),
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
