from . import models


def delete_treatment_by_id(treatment_id):
    name = ""
    try:
        treatment_to_delete = models.Treatment.objects.get(id=treatment_id)
        name = treatment_to_delete.name
        treatment_to_delete.delete()
    except models.Treatment.DoesNotExist:
        return None, "This treatment does not exist"
    return name, None


def delete_prescription_by_id(prescription_id):
    name = ""
    try:
        prescription_to_delete = models.Prescription.objects.get(id=prescription_id)
        name = prescription_to_delete.name
        prescription_to_delete.delete()
    except models.Prescription.DoesNotExist:
        return None, "This prescription does not exist"
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
