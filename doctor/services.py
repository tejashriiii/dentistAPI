from . import models
from patient import services as patient_services
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from rest_framework import status


def delete_treatment_by_id(treatment_id):
    name = ""
    try:
        treatment_to_delete = models.Treatment.objects.get(id=treatment_id)
        name = treatment_to_delete.name
        treatment_to_delete.delete()
    except models.Treatment.DoesNotExist:
        return None, "This treatment does not exist"
    except ProtectedError:
        return (
            None,
            f"{name} cannot be deleted, it has been referenced in some complaints",
        )
    return name, None


def delete_prescription_by_id(prescription_id):
    name = ""
    try:
        prescription_to_delete = models.Prescription.objects.get(id=prescription_id)
        name = prescription_to_delete.name
        prescription_to_delete.delete()
    except models.Prescription.DoesNotExist:
        return None, "This prescription does not exist"
    except ProtectedError:
        return (
            None,
            f"{name} cannot be deleted, it has been referenced in some complaints",
        )
    return name, None


def fetch_structured_prescriptions():
    structured_prescriptions = {}
    types = list(models.Prescription.objects.all().values_list("type").distinct())
    for prescription_type in types:
        # returns a tuple i.e why ("medication",)[0] = "medication"
        prescription_type = prescription_type[0]
        structured_prescriptions[prescription_type] = (
            models.Prescription.objects.filter(type=prescription_type).values(
                "id", "name"
            )
        )
    return structured_prescriptions


def update_prescription(prescription_id, prescription_data):
    """
    Update the name, type of prescription
    1. prescription_id not valid uuid
    2. prescription_id does not exist
    3. duplicate name given
    4. successful update
    """
    if not patient_services.is_valid_uuid(prescription_id):
        return "Invalid prescription, it does not exist", status.HTTP_404_NOT_FOUND

    try:
        prescription_to_update = models.Prescription.objects.get(id=prescription_id)
    except models.Prescription.DoesNotExist:
        return "Invalid prescription, it does not exist", status.HTTP_404_NOT_FOUND
    prescription_to_update.type = prescription_data["type"]
    prescription_to_update.name = prescription_data["name"]
    try:
        prescription_to_update.save()
    except IntegrityError:
        return (
            "Duplicate entry, prescription with this name exists",
            status.HTTP_409_CONFLICT,
        )
    return None, None


def update_treatment(treatment_id, treatment_data):
    """
    Update the name, type of treatment
    1. treatment_id not valid uuid
    2. treatment_id does not exist
    3. duplicate name given
    4. successful update
    """
    if not patient_services.is_valid_uuid(treatment_id):
        return "Invalid treatment, it does not exist", status.HTTP_404_NOT_FOUND

    try:
        treatment_to_update = models.Treatment.objects.get(id=treatment_id)
    except models.Treatment.DoesNotExist:
        return "Invalid treatment, it does not exist", status.HTTP_404_NOT_FOUND
    treatment_to_update.price = treatment_data["price"]
    treatment_to_update.name = treatment_data["name"]
    try:
        treatment_to_update.save()
    except IntegrityError:
        return (
            "Duplicate entry, treatment with this name exists",
            status.HTTP_409_CONFLICT,
        )
    return None, None
