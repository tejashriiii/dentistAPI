from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from . import models
import uuid


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.my_patient = models.Role.objects.create(name="patient")
        self.my_dentist = models.Role.objects.create(name="dentist")
        self.my_admin = models.Role.objects.create(name="admin")

    def test_correct_login(self):
        """
        1. Correct signup
        2. Wrong UUID for role
        3. empty name
        4. empty phonenumber
        5. incorrect phonenumber (not valid)
        """
        url = reverse("login")

        # 1. correct signup
        role_id = models.Role.objects.filter(name="admin").values_list("id", flat=True)[
            0
        ]
        data = {"phonenumber": 89898, "password": "hello", "role": role_id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. wrong uuid
        data = {"phonenumber": 89898, "password": "hello", "role": uuid.uuid4()}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
