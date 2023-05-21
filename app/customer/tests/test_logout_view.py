from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..serializers import RegisterSerializer

LOGOUT_URL = reverse('customer:logout')
VERIFY_REGISTER_URL = reverse('customer:verify-register')


class LogoutViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('customer.utilities.Utilities.generate_otp')
    def test_logout_call(self, generate_otp_mock):
        generate_otp_mock.return_value = '7865'

        register = RegisterSerializer(
            data={
                "country_code": "+91",
                "phone": "0123456789",
                "first_name": "Jasprit",
                "last_name": "Bumrah"
            }
        )

        if register.is_valid():
            register.save()

        response = self.client.post(
            VERIFY_REGISTER_URL,
            data={
                "country_code": "+91",
                "phone": "0123456789",
                "otp": "7865"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        user = get_user_model().objects.get(username='+910123456789')
        self.client.force_authenticate(user=user, token=response.data['token'])
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.data['message'], 'Logged out')
