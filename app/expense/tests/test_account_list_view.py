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

    def test_add_account(self):
        response = self.client.post(
            ACCOUNT_LIST_URL,
            data={
                "name": "Bank 2",
                "initial_balance": 1300.40
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_adding_duplicate_account_fails(self):
        response = self.client.post(
            ACCOUNT_LIST_URL,
            data={
                "name": "Bank 2",
                "initial_balance": 1300.40
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            ACCOUNT_LIST_URL,
            data={
                "name": "Bank 2",
                "initial_balance": 1781
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['This account name already exists'])

    def test_added_accounts_visible_to_owner(self):
        response = self.client.post(
            ACCOUNT_LIST_URL,
            data={
                "name": "Bank 2",
                "initial_balance": 1300.40
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(ACCOUNT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data,
            [
                {
                    "name": "Bank 2",
                    "initial_balance": 1300.40,
                    "owner": self.user.id
                }
            ]
        )

    def test_account_is_not_visible_to_non_owners(self):
        response = self.client.post(
            ACCOUNT_LIST_URL,
            data={
                "name": "Bank 2",
                "initial_balance": 1300.40
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(self.user2, token=self.user2.auth_token)

        response = self.client.get(ACCOUNT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data,
            []
        )
