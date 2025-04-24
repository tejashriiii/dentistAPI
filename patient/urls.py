from django.urls import path
from . import views

urlpatterns = [
    path("details/", views.details),
    path("medical_details/", views.medical_details),
    path("medical_details/<int:phonenumber>/<str:name>/", views.medical_details),
    path("complaints/", views.complaints),
    path("followup/", views.followups),
    path("followup/<uuid:complaint_id>/", views.followups),
    path("followup/<str:date>/", views.followups),
    path("diagnosis/", views.diagnosis),
    path("diagnosis/<uuid:complaint_id>/", views.diagnosis),
    path("diagnosis/delete/<uuid:id>/", views.diagnosis),
    path("prescription/", views.prescription),
    path("prescription/<uuid:complaint_id>/<int:sitting>/", views.prescription),
    path("prescription/delete/<uuid:patient_prescription_id>/", views.prescription),
    path("prescription/pdf/<uuid:complaint_id>/<int:sitting>/", views.pdf_prescription),
    path("bill/discount/<uuid:complaint_id>/", views.bills),
    path("bill/discount/", views.bills),
    path("bill/consultation/", views.bills),
    path("history/<uuid:patient_id>/", views.patient_history),
    path("<int:phonenumber>/", views.patients),
    path("<str:name>/", views.patients),
    path("<int:phonenumber>/<str:name>/", views.patients),
]
