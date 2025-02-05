from django.urls import path
from . import views

urlpatterns = [
    path("patients/", views.patients),
    path("patients/<int:phonenumber>", views.patients),
]
