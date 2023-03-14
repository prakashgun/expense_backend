from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

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

    # def test_user_cannot_verify_with_wrong_otp(self):
    #
    #
    #     response = self.client.post(
    #         VERIFY_REGISTER_URL,
    #         data={
    #             "country_code": "+91",
    #             "phone": "0123456789",
    #             "otp": "7777"
    #         }
    #     )
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)