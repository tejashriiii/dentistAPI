from django.urls import path
from . import views

urlpatterns = [
    path("sendwhatsapp/", views.send_whatsapp_message),
]