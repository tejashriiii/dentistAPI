from django.urls import path
from . import views

urlpatterns = [
    path("allergies/", views.allergies),
    path("medical_conditions/", views.medical_conditions),
    path("patients/", views.patients),
]
