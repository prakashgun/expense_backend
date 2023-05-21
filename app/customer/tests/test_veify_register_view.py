from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..serializers import RegisterSerializer

VERIFY_REGISTER_URL = reverse('customer:verify-register')


class VerifyRegisterViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_cannot_verify_without_country_code(self):
        response = self.client.post(
            VERIFY_REGISTER_URL,
            data={
                "phone": "9791620104",
                "otp": "7777"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_verify_without_phone(self):
        response = self.client.post(
            VERIFY_REGISTER_URL,
            data={
                "country_code": "+91",
                "otp": "7777"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_verify_without_otp(self):
        response = self.client.post(
            VERIFY_REGISTER_URL,
            data={
                "country_code": "+91",
                "phone": "0123456789"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('customer.utilities.Utilities.generate_otp')
    def test_user_cannot_verify_with_wrong_otp(self, generate_otp_mock):
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
                "otp": "7777"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['Wrong OTP given'])

    @patch('customer.utilities.Utilities.generate_otp')
    def test_user_can_verify_with_correct_otp(self, generate_otp_mock):
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
        self.assertEqual(response.data['message'], 'Registration Verified')
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
