import datetime
import uuid
from . import models
from doctor import models as doc_models
from . import serializers
from . import utils
from authentication.models import User
from django.db import IntegrityError
from django.db.models import F
from django.forms.models import model_to_dict
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


def fetch_patients_with_phone_and_name(phonenumber, name):
    patients = (
        models.Details.objects.select_related("user")
        .filter(id__phonenumber=phonenumber, id__name__icontains=name)
        .annotate(name=F("id_id__name"), phonenumber=F("id_id__phonenumber"))
        .values(
            "id",
            "name",
            "phonenumber",
            "date_of_birth",
            "address",
            "gender",
            "allergies",
            "illnesses",
            "smoking",
            "drinking",
            "tobacco",
        )
    )
    if not len(patients):
        return (
            None,
            f"No patients found with name: {
                name} and phonenumber: {phonenumber}",
        )
    return patients, None


def fetch_patients_with_phone(phonenumber):
    patients = (
        models.Details.objects.select_related("user")
        .filter(id__phonenumber=phonenumber)
        .annotate(name=F("id_id__name"), phonenumber=F("id_id__phonenumber"))
        .values(
            "id",
            "name",
            "phonenumber",
            "date_of_birth",
            "address",
            "gender",
            "allergies",
            "illnesses",
            "smoking",
            "drinking",
            "tobacco",
        )
    )
    if not len(patients):
        return (
            None,
            f"No patients found with phonenumber: {phonenumber}",
        )
    return patients, None


def fetch_patients_with_name(name):
    patients = (
        models.Details.objects.select_related("user")
        .filter(id__name__icontains=name)
        .annotate(name=F("id_id__name"), phonenumber=F("id_id__phonenumber"))
        .values(
            "id",
            "name",
            "phonenumber",
            "date_of_birth",
            "address",
            "gender",
            "allergies",
            "illnesses",
            "smoking",
            "drinking",
            "tobacco",
        )
    )
    if not len(patients):
        return (
            None,
            f"No patients found with name: {name}",
        )
    return patients, None


def fetch_complaint_and_followup_history(patient_id):
    """
    - Fetch complaints and followups for given patient
    1. Invaild patient_id
    2. Success
    """
    try:
        patient = User.objects.get(id=patient_id)
    except User.DoesNotExist:
        return None, "This patient does not exist"
    complaints = models.Complaint.objects.filter(user=patient)
    complaint_followup_mapping = []
    for complaint in complaints:
        followups_by_complaint = (
            models.FollowUp.objects.filter(complaint=complaint)
            .values("title", "date", "completed", "number")
            .order_by("number")
        )
        complaint_details = {
            "complaint": complaint.complaint,
            "date": complaint.date,
        }
        complaint_followup_mapping.append(
            {
                str(complaint.id): {
                    "complaint_details": complaint_details,
                    "followups": followups_by_complaint,
                }
            }
        )
    return complaint_followup_mapping, None


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
                "complaint": followup.complaint.id,
                "sitting": followup.number,
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


def create_bill(bill_data):
    """
    Creating bill for the very first time
    1. Checks if complaint exists
    2. Checks one-to-one relation with complaint
    2. Success
    """
    try:
        complaint = models.Complaint.objects.get(id=bill_data["complaint"])
    except models.Complaint.DoesNotExist:
        return "Can't create bill, invalid complaint", status.HTTP_404_NOT_FOUND
    try:
        bill = models.Bill.objects.create(
            complaint=complaint,
            full_bill=bill_data["full_bill"],
            discount=bill_data["discount"],
        )
        bill.save()
    except IntegrityError:
        return "Bill already exists for this complaint", status.HTTP_409_CONFLICT
    return None, None


def update_bill(bill_update_data):
    """
    Update bill's discount or diagnosis changed so bill updated
    1. Invalid bill id
    2. Success
    """
    try:
        bill = models.Bill.objects.get(id=bill_update_data["id"])
    except models.Bill.DoesNotExist:
        return "Bill does not exist, cannot update"
    bill.full_bill = bill_update_data["full_bill"]
    bill.discount = bill_update_data["discount"]
    bill.save()
    return None


def fetch_bill(complaint_id):
    """
    Fetch the bill given the complaint id
    1. Check if bill exists for complaint
    2. Success
    """
    try:
        bill = models.Bill.objects.select_related("complaint").get(
            complaint__id=complaint_id
        )
        bill = model_to_dict(bill)
    except models.Bill.DoesNotExist:
        return None, "Bill doesn't exist for this complaint", status.HTTP_404_NOT_FOUND
    return bill, None, None


def create_patient_prescription(patient_prescription_data):
    """
    Create a prescription entry for a certain sitting of complaint
    1. Invalid complaint
    2. Invalid prescription
    3. Integrity error with duplicate medication
    4. Success
    """
    try:
        complaint = models.Complaint.objects.get(
            id=patient_prescription_data["complaint"]
        )
    except models.Complaint.DoesNotExist:
        return "Invalid complaint, coudn't save prescription", status.HTTP_404_NOT_FOUND
    try:
        prescription = doc_models.Prescription.objects.get(
            id=patient_prescription_data["prescription"]
        )
    except doc_models.Prescription.DoesNotExist:
        return (
            "Invalid medication, coudn't save prescription",
            status.HTTP_404_NOT_FOUND,
        )
    try:
        models.PatientPrescription.objects.create(
            complaint=complaint,
            prescription=prescription,
            sitting=patient_prescription_data["sitting"],
            days=patient_prescription_data["days"],
            dosage=patient_prescription_data["dosage"],
        )
    except IntegrityError:
        return (
            f"{prescription.name} is a duplicate entry cannot save it",
            status.HTTP_404_NOT_FOUND,
        )
    return None, None


def fetch_patients_prescriptions(complaint_id, sitting):
    """
    1. Invalid complaint_id
    2. Invalid sitting
    3. Success
    """
    try:
        complaint = models.Complaint.objects.get(id=complaint_id)
    except models.Complaint.DoesNotExist:
        return None, "Invalid complaint, no prescription found"

    # Only check incase its followup and not initial complaint
    if sitting:
        try:
            models.FollowUp.objects.get(complaint=complaint, number=sitting)
        except models.FollowUp.DoesNotExist:
            return (
                None,
                "Invalid followup, no prescription found",
            )

    try:
        patient_prescription = models.PatientPrescription.objects.get(
            complaint=complaint, sitting=sitting
        )
        patient_prescription = model_to_dict(patient_prescription)
    except models.PatientPrescription.DoesNotExist:
        return (
            None,
            "Prescription is not set for this sitting",
        )

    return patient_prescription, None


def update_patients_prescription(serializer_data):
    """
    Update prescription given data
    {id, prescription, days, dosage}
    1. Invalid patient_prescription
    2. Invalid prescription_id
    3. Success
    """
    try:
        patient_prescription = models.PatientPrescription.objects.get(
            id=serializer_data["id"]
        )
    except models.PatientPrescription.DoesNotExist:
        return "Invalid Prescription entry, coudn't update", status.HTTP_404_NOT_FOUND
    try:
        prescription = doc_models.Prescription.objects.get(
            id=serializer_data["prescription"]
        )
    except doc_models.Prescription.DoesNotExist:
        return (
            "Invalid medication, coudn't save prescription",
            status.HTTP_404_NOT_FOUND,
        )
    try:
        patient_prescription.prescription = prescription
        patient_prescription.dosage = serializer_data["dosage"]
        patient_prescription.days = serializer_data["days"]
        patient_prescription.save()
    except IntegrityError:
        return (
            f"{prescription.name} is a duplicate entry cannot save it",
            status.HTTP_404_NOT_FOUND,
        )
    return None, None


def delete_patient_prescription(patient_prescription_id):
    """
    Delete a prescription from patient's complaint/followup
    1. That medication does not exist in the patient's prescription
    2. Success
    """
    try:
        patient_prescription = models.PatientPrescription.objects.get(
            id=patient_prescription_id
        )
    except models.PatientPrescription.DoesNotExist:
        return None, "Couldn't delete medication"
    name = patient_prescription.prescription.name
    patient_prescription.delete()
    return name, None
