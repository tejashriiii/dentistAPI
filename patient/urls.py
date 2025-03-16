from django.urls import path
from . import views

urlpatterns = [
    path("", views.patients),
    path("<int:phonenumber>", views.patients),
    path("details/", views.details),
    path("medical_details/", views.medical_details),
    path("medical_details/<int:phonenumber>/<str:name>/", views.medical_details),
    path("complaints/", views.complaints),
    path("followup/", views.followups),
    path("followup/<uuid:complaint_id>/", views.followups),
    path("diagnosis/", views.diagnosis),
    path("diagnosis/<uuid:complaint_id>/", views.diagnosis),
    path("diagnosis/delete/<uuid:id>/", views.diagnosis),
]
