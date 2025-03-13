from django.urls import path
from . import views

urlpatterns = [
    path("treatment/", views.treatments, name="treatments"),
    path("treatment/<uuid:treatment_id>/", views.treatments, name="delete_treatments"),
    path("prescription/", views.prescriptions, name="prescription"),
    path(
        "prescription/<uuid:prescription_id>/",
        views.prescriptions,
        name="delete_prescriptions",
    ),
]
