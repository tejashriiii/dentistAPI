from django.urls import path
from . import views

urlpatterns = [
    path("details/", views.details),
    path("complaints/", views.complaints),
    path("followups/", views.followups),
    path("", views.patients),
    path("<int:phonenumber>", views.patients),
]
