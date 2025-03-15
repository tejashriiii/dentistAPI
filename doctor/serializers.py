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


class PrescriptionUpdateSerializer(serializers.Serializer):
    """
    Had to create separate serializer because
    - "name" had unique constraint violations that needed
      to be loosened up in this case
    - handling the unique constraint during updation instead
      of validation
    name: <String>
    type: <String>
    """

    name = serializers.CharField()
    type = serializers.CharField()


class TreatmentUpdateSerializer(serializers.Serializer):
    """
    Had to create separate serializer because
    - "name" had unique constraint violations that needed
      to be loosened up in this case
    - handling the unique constraint during updation instead
      of validation
    name: <String>
    price: <Int>
    """

    name = serializers.CharField()
    price = serializers.IntegerField()
