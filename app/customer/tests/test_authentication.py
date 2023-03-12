from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import Mock

USER_PHONE_URL = reverse('customer:user-phone')


class AuthenticationTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_can_register_phone(self):
        res = self.client.post(
            USER_PHONE_URL,
            data={
                "country_code": "+91",
                "phone": "0123456789"
            }
        )

