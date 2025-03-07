import datetime
from . import models
from . import serializers
from . import utils
from authentication.models import User


def capitalize_name(name, snake_case=False):
    separated_name = []
    if snake_case:
        separated_name = list(
            map(lambda x: x.capitalize() + " ", name.split("_")))
    else:
        separated_name = list(
            map(lambda x: x.capitalize() + " ", name.split()))
    capitalized_name = ""
    for name in separated_name:
        capitalized_name += name
    return capitalized_name.strip()


def fetch_followups_by_date(date: datetime.datetime.date):
    """
    Returns list of all the followups for the given date
    """
    followups_for_date = models.FollowUp.objects.select_related(
        "complaint", "complaint__user", "complaint__user__details"
    ).filter(date=date)
    formatted_followups = []
    for followup in followups_for_date:
        formatted_followups.append(
            {
                "name": followup.complaint.user.name,
                "age": utils.get_age(followup.complaint.user.details.date_of_birth),
                "phonenumber": followup.complaint.user.phonenumber,
                "time": followup.time,
                "followup": followup.title,
            }
        )
    if not formatted_followups:
        return ["No followups today"]
    return formatted_followups


def serialize_identity(medical_data):
    identity = serializers.PhoneNameSerializer(data=medical_data)
    if not identity.is_valid():
        return None, identity.error_messages
    return identity.data, None


def serialize_medical_details(medical_data):
    """
    1. Check identity validity (name, phonenumber)
    2. Check medical_details validity (allergies, illnesses, smoking, tobacco, drinking)
    """

    identity_data, error = serialize_identity(medical_data.get("identity"))
    if error:
        return None, error

    # Check for errors in medical_data
    medical_details = serializers.MedicalDetailsSerializer(
        data=medical_data.get("medical_details")
    )
    if not medical_details.is_valid():
        return None, medical_details.error_messages

    serialized_data = {
        "identity": identity_data,
        "medical_details": medical_details.data,
    }
    return serialized_data, None


def fetch_details_object(name, phonenumber):
    """
    Using name and phonenumber fetch the details of a patient
    """
    try:
        user_details = User.objects.select_related("details").get(
            name=name,
            phonenumber=phonenumber,
        )
    except User.DoesNotExist:
        return "User not found", None
    return None, user_details.details


def add_medical_details(data):
    """
    1. Creates medical details for first time
    1. Updates medical details if details already filled
    """
    error, user_details = fetch_details_object(
        data["identity"].get("name"), data["identity"].get("phonenumber")
    )
    if error:
        return error

    # Bringing allergies and illnesses to csv format instead of lists
    allergies, illnesses = "", ""
    for allergy in data["medical_details"]["allergies"]:
        allergies += allergy + ","
    for illness in data["medical_details"]["illnesses"]:
        illnesses += illness + ","

    user_details.illnesses = illnesses[:-1]
    user_details.allergies = allergies[:-1]
    user_details.smoking = data["medical_details"]["smoking"]
    user_details.tobacco = data["medical_details"]["tobacco"]
    user_details.drinking = data["medical_details"]["drinking"]
    user_details.save()
    return None


def fetch_medical_details(name, phonenumber):
    """
    1. Convert to capitalcase from snakecase
    2. Fetch the medical details of patient
    - illnesses, allergies, smoking, drinking, tobacco
    """
    capitalized_name = capitalize_name(name, snake_case=True)
    error, user_details = fetch_details_object(capitalized_name, phonenumber)
    if error:
        return None, error

    medical_details = {
        "illnesses": user_details.illnesses.split(","),
        "allergies": user_details.allergies.split(","),
        "smoking": user_details.smoking,
        "drinking": user_details.drinking,
        "tobacco": user_details.tobacco,
    }
    return medical_details, None
