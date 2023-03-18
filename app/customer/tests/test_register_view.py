from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

REGISTER_URL = reverse('customer:register')


class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_cannot_register_without_country_code(self):
        response = self.client.post(
            REGISTER_URL,
            data={
                "phone": "0123456789",
                "first_name": "Zaheer",
                "last_name": "Khan"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_without_phone(self):
        response = self.client.post(
            REGISTER_URL,
            data={
                "country_code": "91",
                "first_name": "Zaheer",
                "last_name": "Khan"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_without_first_name(self):
        response = self.client.post(
            REGISTER_URL,
            data={
                "country_code": "91",
                "phone": "0123456789",
                "last_name": "Khan"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_without_last_name(self):
        response = self.client.post(
            REGISTER_URL,
            data={
                "country_code": "91",
                "phone": "0123456789",
                "first_name": "Zaheer"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('customer.utilities.PhoneClient.send_otp')
    def test_user_cannot_register_with_failure_sending_otp(self, send_otp_mock):
        send_otp_mock.return_value = False

        response = self.client.post(
            REGISTER_URL,
            data={
                "country_code": "+91",
                "phone": "0123456789",
                "first_name": "Zaheer",
                "last_name": "Khan"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['message'], 'Failure in sending OTP')

    @patch('customer.utilities.PhoneClient.send_otp')
    def test_user_can_register_with_correct_data(self, send_otp_mock):
        send_otp_mock.return_value = True

        response = self.client.post(
            REGISTER_URL,
            data={
                "country_code": "+91",
                "phone": "0123456789",
                "first_name": "Zaheer",
                "last_name": "Khan"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'OTP Sent')

    @patch('customer.utilities.PhoneClient.send_otp')
    def test_user_cannot_register_with_same_number_again(self, send_otp_mock):
        send_otp_mock.return_value = True

        response = self.client.post(
            REGISTER_URL,
            data={
                "country_code": "+91",
                "phone": "0123456789",
                "first_name": "Zaheer",
                "last_name": "Khan"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'OTP Sent')

        response = self.client.post(
            REGISTER_URL,
            data={
                "country_code": "+91",
                "phone": "0123456789",
                "first_name": "Zaheer",
                "last_name": "Khan"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['non_field_errors'],
            ['This phone number is already registered. Please use login page.']
        )

