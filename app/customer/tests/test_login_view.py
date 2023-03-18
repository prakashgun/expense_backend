from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

LOGIN_URL = reverse('customer:login')


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_cannot_login_without_country_code(self):
        response = self.client.post(
            LOGIN_URL,
            data={
                "phone": "0123456789"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_login_without_phone(self):
        response = self.client.post(
            LOGIN_URL,
            data={
                "country_code": "+91"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # @patch('customer.utilities.PhoneClient.send_otp')
    # def test_user_cannot_login_when_failure_in_sending_otp(self, send_otp_mock):
    #     send_otp_mock.return_value = False
    #
    #     response = self.client.post(
    #         LOGIN_URL,
    #         data={
    #             "country_code": "+91",
    #             "phone": "0123456789"
    #         }
    #     )
    #
    #     print(response.json())
    #     self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     self.assertEqual(response.data['message'], 'Failure in sending OTP')
