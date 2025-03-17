from django.urls import path
from . import views

urlpatterns = [
    path("details/", views.details),
    path("medical_details/", views.medical_details),
    path("medical_details/<int:phonenumber>/<str:name>/", views.medical_details),
    path("complaints/", views.complaints),
    path("followup/", views.followups),
    path("followup/<uuid:complaint_id>/", views.followups),
    path("diagnosis/", views.diagnosis),
    path("diagnosis/<uuid:complaint_id>/", views.diagnosis),
    path("diagnosis/delete/<uuid:id>/", views.diagnosis),
    path("bill/", views.bills),
    path("bill/<uuid:complaint_id>/", views.bills),
    path("<int:phonenumber>/", views.patients),
    path("<str:name>/", views.patients),
    path("<int:phonenumber>/<str:name>/", views.patients),
]
