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
