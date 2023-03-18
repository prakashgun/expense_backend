from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Customer

VERIFY_LOGIN_URL = reverse('customer:verify-login')


class VerifyLoginTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        country_code = '+91'
        phone = '0123456789'
        full_phone = f'{country_code}{phone}'
        otp = '1234'

        user = get_user_model().objects.create_user(
            username=full_phone,
            first_name='Zaheer',
            last_name='Khan',
            password=f'pass{otp}',
            is_active=True
        )

        user.save()

        Customer.objects.create(
            user=user,
            country_code=country_code,
            phone=phone,
            otp=otp
        ).save()

    def test_user_cannot_login_with_wrong_otp(self):
        response = self.client.post(VERIFY_LOGIN_URL,
                                    data={
                                        'country_code': '+91',
                                        'phone': '0123456789',
                                        'otp': '9999'
                                    })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['Wrong OTP given'])

    def test_user_can_login_with_correct_otp(self):
        response = self.client.post(VERIFY_LOGIN_URL,
                                    data={
                                        'country_code': '+91',
                                        'phone': '0123456789',
                                        'otp': '1234'
                                    })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login Verified')
