from rest_framework import serializers
from . import models


class DetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for Details
    """

    class Meta:
        model = models.Details
        exclude = ["id", "allergies", "illnesses",
                   "tobacco", "smoking", "drinking"]


class ComplaintSerializer(serializers.Serializer):
    """
    chief_complaint: <String> Description of complaint
    name: <String> Name of the person
    """

    chief_complaint = serializers.CharField()
    name = serializers.CharField()
