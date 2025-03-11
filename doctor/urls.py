from django.urls import path
from . import views

urlpatterns = [
    path("treatments/", views.treatments, name="treatments"),
    path("treatments/<uuid:treatment_id>/", views.treatments, name="delete_treatments"),
]
