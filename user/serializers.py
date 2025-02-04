from rest_framework import serializers
from . import models


class DetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for Details
    """

    class Meta:
        model = models.Details
        exclude = ["id"]


class ComplaintSerializer(serializers.ModelSerializer):
    """
    Serializer for Appointments
    """

    class Meta:
        model = models.Complaint
        exclude = ["id"]

    pass
