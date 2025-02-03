from rest_framework import serializers
from . import models


class DetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for Details
    """

    class Meta:
        model = models.Details
        exclude = ["id"]


class AllergySerializer(serializers.ModelSerializer):
    """
    Serializer for Allergy
    """

    class Meta:
        model = models.Allergy
        fields = ["id", "name", "description"]


class MedicalConditionSerializer(serializers.ModelSerializer):
    """
    Serializer for Medical Condition
    """

    class Meta:
        model = models.MedicalCondition
        fields = ["id", "name", "description"]
