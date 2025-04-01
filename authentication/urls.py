from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("password/", views.password_reprompt, name="password"),
    path("phonenumber/", views.change_phonenumber, name="phonenumber"),
]
