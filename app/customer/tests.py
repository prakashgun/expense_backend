from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


class CustomerCreateTest(TestCase):

    def test_register(self):
        payload = {
            'username': '9876543210',
            'password': 'test',
            'email': 'test@example.com'
        }

        # user = get_user_model().objects.create_user(payload)
        #
        # print(get_user_model().objects.all())

        res = self.client.post(reverse('customer:register'), data=payload)
        print(res.json())
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
