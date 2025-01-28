from rest_framework import serializers
from .models import User, Allergy, MedicalCondition


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User
    """

    class Meta:
        model = User
        fields = ["id", "role", "phonenumber", "password"]


class AllergySerializer(serializers.ModelSerializer):
    """
    Serializer for Allergy
    """

    class Meta:
        model = Allergy
        fields = ["id", "name", "description"]


class MedicalConditionSerializer(serializers.ModelSerializer):
    """
    Serializer for Medical Condition
    """

    class Meta:
        model = MedicalCondition
        fields = ["id", "name", "description"]
