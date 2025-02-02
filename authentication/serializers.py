from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User
    """

    class Meta:
        model = User
        fields = ["id", "role", "phonenumber", "password"]


class CredentialSerializer(serializers.Serializer):
    """
    Serializer for credentials during signup and login
    """

    phonenumber = serializers.IntegerField()
    password = serializers.CharField()
