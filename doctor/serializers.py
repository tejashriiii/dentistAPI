from rest_framework import serializers
from . import models


class TreatmentSerializer(serializers.ModelSerializer):
    """
    name: <String>
    price: <Int>
    """

    class Meta:
        model = models.Treatment
        exclude = ["id"]


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    name: <String>
    type: <String>
    """

    class Meta:
        model = models.Prescription
        exclude = ["id"]
