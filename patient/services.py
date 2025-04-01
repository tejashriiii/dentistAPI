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
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Line


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

    illnesses = user_details.illnesses.split(",")
    if not user_details.illnesses:
        illnesses = []
    allergies = user_details.allergies.split(",")
    if not user_details.allergies:
        allergies = []

    medical_details = {
        "illnesses": illnesses,
        "allergies": allergies,
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
        complaint_object = {
            "complaint": followup.complaint.complaint,
            "time": followup.complaint.time,
            "date": followup.complaint.date,
            "description": followup.complaint.description,
        }

        formatted_followups.append(
            {
                "name": followup.complaint.user.name,
                "patient_id": followup.complaint.user.id,
                "age": utils.get_age(followup.complaint.user.details.date_of_birth),
                "phonenumber": followup.complaint.user.phonenumber,
                "time": followup.time,
                "followup": followup.title,
                "id": followup.complaint.id,
                "complaint_object": complaint_object,
                "sitting": followup.number,
            }
        )
    if not formatted_followups:
        return []
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
        return []
    return past_followups


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

    followup_to_update.title = followup_data["title"]
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
            status.HTTP_409_CONFLICT,
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

    patient_prescription = (
        models.PatientPrescription.objects.filter(complaint=complaint, sitting=sitting)
        .annotate(
            prescription_name=F("prescription_id__name"),
            prescription_type=F("prescription_id__type"),
        )
        .values(
            "id",
            "sitting",
            "complaint",
            "prescription_name",
            "prescription_type",
            "prescription_id",
            "days",
            "dosage",
        )
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


def fetch_followup_and_personal_data_for_prescription_pdf(
    complaint_id, current_sitting
):
    """
    - Personal data using current followup
    - Data for next followup
    """
    if current_sitting == 0:
        current_complaint = models.Complaint.objects.get(id=complaint_id)
        personal = {
            "name": current_complaint.user.name,
            "age": utils.get_age(current_complaint.user.details.date_of_birth),
            "complaint": current_complaint.complaint,
            "current_date": current_complaint.date,
        }

    else:
        current_followup = models.FollowUp.objects.select_related("complaint").get(
            complaint__id=complaint_id, number=current_sitting
        )
        personal = {
            "name": current_followup.complaint.user.name,
            "age": utils.get_age(current_followup.complaint.user.details.date_of_birth),
            "complaint": current_followup.complaint.complaint,
            "current_date": current_followup.date,
        }
    print("personal: ", personal)

    try:
        followup = models.FollowUp.objects.select_related("complaint").get(
            complaint__id=complaint_id, number=current_sitting + 1
        )
        followup = {
            "followup": followup.title,
            "next_date": followup.date,
            "time": followup.time,
            "sitting": followup.number,
        }
    except models.FollowUp.DoesNotExist:
        return {"personal": personal, "followup": {}}
    return {"personal": personal, "followup": followup}


def create_pdf(response, followup_and_personal_data, prescriptions):
    """ """
    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        textColor=colors.darkblue,
        fontSize=20,
        alignment=1,
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Heading2"],
        textColor=colors.darkblue,
        fontSize=16,
        alignment=1,
    )
    address_style = ParagraphStyle(
        "AddressStyle",
        parent=styles["BodyText"],
        textColor=colors.darkblue,
        fontSize=12,
        alignment=1,
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        textColor=colors.black,
        fontSize=12,
        leading=16,
    )

    # Title
    elements.append(Paragraph("Ojas Dental Clinic", title_style))
    elements.append(
        Paragraph(
            "4G24+MQF, Hospital Rd, Panchavati Colony, Baran, Rajasthan 325205",
            address_style,
        )
    )
    elements.append(Spacer(1, 5))
    header_divider = create_divider(440, 1, colors.darkblue)
    elements.append(header_divider)
    elements.append(Spacer(1, 20))

    # Patient Info
    if followup_and_personal_data:
        elements.append(
            Paragraph(
                f"Patient: <b>{followup_and_personal_data.get("personal").get("name")}</b>",
                body_style,
            )
        )
        elements.append(
            Paragraph(
                f"Age: <b>{followup_and_personal_data.get("personal").get("age")}</b>",
                body_style,
            )
        )
        elements.append(
            Paragraph(
                f"Date: <b>{followup_and_personal_data.get("personal").get("current_date")}</b>",
                body_style,
            )
        )
        elements.append(Paragraph("Doctor: <b>Dr. Neha Gupta</b>", body_style))
        elements.append(
            Paragraph(
                f"Complaint: <b>{followup_and_personal_data.get("personal").get("complaint")}</b>",
                body_style,
            )
        )
        elements.append(Spacer(1, 12))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<u>Prescription</u>", subtitle_style))
    elements.append(Spacer(1, 5))
    # Medicines Table
    if len(prescriptions):
        data = [["Medication", "Dosage", "Days"]]
        for prescription in prescriptions:
            if prescription.get("prescription_type") == "Medication":
                data.append(
                    [
                        prescription.get("prescription_name"),
                        prescription.get("dosage"),
                        prescription.get("days"),
                    ]
                )
            else:
                data.append([prescription.get("prescription_name"), "-", "-"])

        table = Table(data, colWidths=[240, 100, 100])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.darkblue),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 1, colors.lightgrey),
                ]
            )
        )
        elements.append(table)
    else:
        elements.append(Paragraph("No prescriptions given", address_style))

    # Followup section
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<u>Followup</u>", subtitle_style))
    elements.append(Spacer(1, 5))
    if followup_and_personal_data.get("followup"):
        followup_data = [
            ["Sitting", "Followup", "Date", "Time"],
            [
                followup_and_personal_data.get("followup").get("sitting"),
                followup_and_personal_data.get("followup").get("followup"),
                followup_and_personal_data.get("followup").get("next_date"),
                followup_and_personal_data.get("followup").get("time"),
            ],
        ]
        table = Table(followup_data, colWidths=[40, 240, 80, 80])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.darkblue),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 1, colors.lightgrey),
                ]
            )
        )
        elements.append(table)
    else:
        elements.append(Paragraph("No followups scheduled up next", address_style))
    d = Drawing(150, 10)
    d.add(Line(0, 5, 100, 5, strokeColor=colors.black, strokeWidth=1))

    # Add the text below the line
    elements.append(Spacer(1, 100))
    elements.append(Spacer(400, 1))
    elements.append(d)
    elements.append(Paragraph("<b>Doctor's Signature</b>", body_style))

    # Build PDF
    pdf.build(elements)


def create_divider(width=500, height=1, color=colors.black):
    d = Drawing(width, height)
    d.add(Line(0, height / 2, width, height / 2, strokeColor=color, strokeWidth=1))
    return d
