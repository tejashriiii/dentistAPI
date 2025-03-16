import datetime
import uuid
from . import models
from . import serializers
from . import utils
from authentication.models import User
from django.db import IntegrityError
from rest_framework import status


def capitalize_name(name, snake_case=False):
    separated_name = []
    if snake_case:
        separated_name = list(map(lambda x: x.capitalize() + " ", name.split("_")))
    else:
        separated_name = list(map(lambda x: x.capitalize() + " ", name.split()))
    capitalized_name = ""
    for name in separated_name:
        capitalized_name += name
    return capitalized_name.strip()


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


def fetch_medical_details(capitalized_name, phonenumber):
    """
    Fetch the medical details of patient
    - illnesses, allergies, smoking, drinking, tobacco
    """
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


def fetch_diagnosis_by_complaint(complaint_id):
    diagnoses = (
        models.Diagnosis.objects.select_related("complaint")
        .filter(complaint__id=complaint_id)
        .values()
    )
    if not len(diagnoses):
        return None, "Invalid complaint, no diagnosis found"
    return diagnoses, None


def create_diagnosis(diagnosis_data):
    """
    Create a new diagnosis entry in the database
    1. Invalid treatment UUID
    2. Invalid complaint UUID
    3. Duplicate diagnosis (complaint+tooth should be unique)
    3. Success
    """
    try:
        complaint = models.Complaint.objects.get(id=diagnosis_data["complaint"])
    except models.Complaint.DoesNotExist:
        return (
            f"For {diagnosis_data["tooth_number"]} Invalid chief-complaint",
            status.HTTP_404_NOT_FOUND,
        )
    try:
        treatment = models.Treatment.objects.get(id=diagnosis_data["treatment"])
    except models.Treatment.DoesNotExist:
        return (
            f"For {diagnosis_data["tooth_number"]} Invalid chief-complaint",
            status.HTTP_404_NOT_FOUND,
        )
    try:
        models.Diagnosis.objects.create(
            complaint=complaint,
            treatment=treatment,
            tooth_number=diagnosis_data["tooth_number"],
        )
    except IntegrityError:
        return (
            f"For {diagnosis_data["tooth_number"]
                   } Duplicate diagnosis, diagnosis for this tooth already exists",
            status.HTTP_409_CONFLICT,
        )
    return None, None


def update_diagnosis(diagnosis_update_data):
    try:
        diagnosis_to_update = models.Diagnosis.objects.get(
            id=diagnosis_update_data["id"]
        )
    except models.Diagnosis.DoesNotExist:
        return "Diagnosis not found"
    try:
        updated_treatment = models.Treatment.objects.get(
            id=diagnosis_update_data["treatment"]
        )
    except models.Treatment.DoesNotExist:
        return "Treatment not found"

    diagnosis_to_update.treatment = updated_treatment
    diagnosis_to_update.save()
    return None


def delete_diagnosis(diagnosis_id):
    try:
        diagnosis_to_delete = models.Diagnosis.objects.get(id=diagnosis_id)
    except models.Diagnosis.DoesNotExist:
        return None, "Diagnosis not found"
    tooth_number = diagnosis_to_delete.tooth_number
    diagnosis_to_delete.delete()
    return tooth_number, None


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


def fetch_followups_by_complaint(complaint_id):
    """
    Fetch all the past followups for a particular complaint
    """
    # filter method fails gracefully so now DoesNotExist is raised
    # i.e why "if" instead of "try-except"
    past_followups = (
        models.FollowUp.objects.select_related("complaint")
        .filter(complaint__id=complaint_id)
        .values()
    )
    if not len(past_followups):
        return None, "No followups present this complaint"
    return past_followups, None


def is_valid_uuid(uuid_string):
    try:
        uuid.UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True


def create_followup(complaint_id, followup_data):
    """
    - Checks if complaint_id is valid or not then creates a followup with
    serialized data
    - Errors Handled:
        1. Invalid UUID for complaint_id
        2. Non-existent complaint_id
        3. Duplicate constraint (complaint, number)
    """
    if not is_valid_uuid(complaint_id):
        return "Invalid followup, chief complaint is not registered"

    try:
        complaint_data = models.Complaint.objects.get(id=complaint_id)
    except models.Complaint.DoesNotExist:
        return "Invalid followup, chief complaint is not registered"
    try:
        models.FollowUp.objects.create(
            complaint=complaint_data,
            title=followup_data["title"],
            description=followup_data["description"],
            date=followup_data["date"],
            time=followup_data["time"],
            number=followup_data["number"],
        )
    except IntegrityError:
        return "Duplicate followup, it already exists"
    return None


def update_followup(followup_data):
    """
    After the followup is done, the doctor updates fields like
    description, completed, date, time
    """
    try:
        followup_to_update = models.FollowUp.objects.get(id=followup_data["id"])
    except models.FollowUp.DoesNotExist:
        "Invalid followup, it does not exist"

    followup_to_update.description = followup_data["description"]
    followup_to_update.date = followup_data["date"]
    followup_to_update.time = followup_data["time"]
    followup_to_update.completed = followup_data["completed"]
    followup_to_update.save()
    return None
