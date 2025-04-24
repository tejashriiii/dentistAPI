from rest_framework import serializers
from . import models


class DetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for Details
    date_of_birth: <Date>
    address: <String>
    Gender: <M | F | T | O>
    """

    class Meta:
        model = models.Details
        exclude = ["id", "allergies", "illnesses", "tobacco", "smoking", "drinking"]


class MedicalDetailsSerializer(serializers.Serializer):
    """
    allergies: <String>
    illnesses: <String>
    smoking: <Bool>
    tobacco: <Bool>
    drinking: <Bool>
    """

    allergies = serializers.ListField(child=serializers.CharField(), default=[])
    illnesses = serializers.ListField(child=serializers.CharField(), default=[])
    smoking = serializers.BooleanField(default=False)
    tobacco = serializers.BooleanField(default=False)
    drinking = serializers.BooleanField(default=False)


class ComplaintSerializer(serializers.Serializer):
    """
    chief_complaint: <String> Description of complaint
    name: <String> Name of the person
    """

    chief_complaint = serializers.CharField()
    name = serializers.CharField()


class PhoneNameSerializer(serializers.Serializer):
    """
    phonenumber: <Int> Phonenumber of patient
    name: <String> Name of patient
    """

    phonenumber = serializers.IntegerField()
    name = serializers.CharField()


class DiagnosisSerializer(serializers.Serializer):
    """
    treatment: <UUID> for treatment
    complaint: <UUID> for complaint
    tooth_number: <Integer>
    price: <Integer>
    """

    treatment = serializers.UUIDField()
    complaint = serializers.UUIDField()
    tooth_number = serializers.IntegerField()


class DiagnosisUpdateSerializer(serializers.Serializer):
    """
    id: <UUID> for diagnosis
    treatment: <UUID> for treatment
    tooth_number: <Integer>
    """

    treatment = serializers.UUIDField()
    id = serializers.UUIDField()
    tooth_number = serializers.IntegerField()


class FollowupSerializer(serializers.ModelSerializer):
    """
    title:<String> The name of followup that patient sees
    description:<String> What the dentist ended up doing in this sitting (private)
    date: <Date> When followup is scheduled
    time: <Time> When followup is scheduled
    completed: <Bool> Whether sitting has been completed or not
    """

    class Meta:
        model = models.FollowUp
        exclude = ["id", "complaint"]


class FollowupUpdateSerializer(serializers.Serializer):
    """
    id: <UUID>
    title:<String> The name of followup that patient sees
    description:<String> What the dentist ended up doing in this sitting (private)
    date: <Date> When followup is scheduled
    time: <Time> When followup is scheduled
    completed: <Bool> Whether sitting has been completed or not
    """

    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    time = serializers.TimeField()
    date = serializers.DateField()
    completed = serializers.BooleanField()


class DiscountSerializer(serializers.Serializer):
    """
    complaint: <UUID> along with which bill is associated
    discount: <Integer> Amount of discount given by the dentist
    """

    complaint = serializers.UUIDField()
    discount = serializers.IntegerField()


class PatientPrescriptionSerializer(serializers.Serializer):
    """
    complaint: <UUID>
    prescription: <UUID>
    days: <Integer>
    dosage: <Integer>
    dosage: <OD | BD | TD | Half BD | Half TD | "">
    """

    complaint = serializers.UUIDField()
    sitting = serializers.IntegerField()
    prescription = serializers.UUIDField()
    days = serializers.IntegerField()
    dosage = serializers.ChoiceField(
        choices=models.PatientPrescription.DosageChoices.choices,
        default=models.PatientPrescription.DosageChoices.EMPTY,
    )


class PatientPrescriptionUpdateSerializer(serializers.Serializer):
    """
    id: <UUID>
    prescription: <UUID>
    days: <Integer>
    dosage: <Integer>
    """

    id = serializers.UUIDField()
    prescription = serializers.UUIDField()
    days = serializers.IntegerField()
    dosage = serializers.ChoiceField(
        choices=models.PatientPrescription.DosageChoices.choices,
        default=models.PatientPrescription.DosageChoices.EMPTY,
    )
