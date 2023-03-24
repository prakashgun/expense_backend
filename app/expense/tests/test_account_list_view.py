from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .utilities import Utilities

ACCOUNT_LIST_URL = reverse('expense:account-list')


class PublicAccountListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_accounts_unauthenticated_permissions(self):
        response = self.client.get(ACCOUNT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAccountListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = Utilities.sample_user()

        self.user2 = Utilities.sample_user(
            username='123451234',
            password='test2',
            email='test2@example.com'
        )

        self.client.force_authenticate(user=self.user, token=self.user.auth_token)

    # def test_add_account(self):
    #     response = self.client.post(
    #         ACCOUNT_LIST_URL,
    #         data={
    #             "name": "Bank 2,",
    #             "initial_balance": 1300.40
    #         }
    #     )
    #     print(response.json())
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
