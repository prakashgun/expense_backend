from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .utilities import Utilities
from ..models import Transaction, Account, Category

TRANSACTION_LIST_URL = reverse('expense:transaction-list')
TRANSACTION_DETAIL_URL = reverse('expense:transaction-detail', kwargs={'pk': 'some_id'})
ACCOUNT_LIST_URL = reverse('expense:account-list')
CATEGORY_LIST_URL = reverse('expense:category-list')


class PublicAccountListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_transactions_unauthenticated_permissions(self):
        response = self.client.get(TRANSACTION_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_transaction_unauthenticated_permissions(self):
        response = self.client.get(TRANSACTION_LIST_URL)
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
                "name": "Bank 1",
                "initial_balance": 1300.40,
                "note": "Secondary account"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_category(self):
            response = self.client.post(
                CATEGORY_LIST_URL,
                data={
                    "name": "Category 1",
                    "icon_name": 'Icon name 1',
                    "icon_type": "Icon type 1"
                }
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_transaction(self):
        self.test_add_account()
        account_id = Account.objects.latest('id').id
        self.test_add_category()
        category_id = Category.objects.latest('id').id

        response = self.client.post(
            TRANSACTION_LIST_URL,
            data={
                "name": "Transaction 1",
                "value": 60.50,
                "is_income": False,
                "account_id": account_id,
                "category_id": category_id,
                "transaction_date": "2023-06-04T10:04:04.737664Z"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(TRANSACTION_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Transaction 1')
        self.assertEqual(response.data[0]['value'], 60.50)

    def test_added_transactions_visible_to_owner(self):
        self.test_add_account()
        account_id = Account.objects.latest('id').id
        self.test_add_category()
        category_id = Category.objects.latest('id').id

        response = self.client.post(
            TRANSACTION_LIST_URL,
            data={
                "name": "Transaction 1",
                "value": 19,
                "is_income": False,
                "account_id": account_id,
                "category_id": category_id,
                "transaction_date": "2023-06-04T10:04:04.737664Z"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(TRANSACTION_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Transaction 1')
        self.assertEqual(response.data[0]['value'], 19)

    def test_transaction_is_not_visible_to_non_owners(self):
        self.test_add_account()
        account_id = Account.objects.latest('id').id
        self.test_add_category()
        category_id = Category.objects.latest('id').id

        response = self.client.post(
            TRANSACTION_LIST_URL,
            data={
                "name": "Transaction 1",
                "value": 19.50,
                "is_income": False,
                "account_id": account_id,
                "category_id": category_id,
                "transaction_date": "2023-06-04T10:04:04.737664Z"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(self.user2, token=self.user2.auth_token)

        response = self.client.get(TRANSACTION_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data,
            []
        )

    def test_view_added_transaction(self):
        self.test_add_account()
        account_id = Account.objects.latest('id').id
        self.test_add_category()
        category_id = Category.objects.latest('id').id

        response = self.client.post(
            TRANSACTION_LIST_URL,
            data={
                "name": "Transaction 1",
                "value": 19.50,
                "is_income": False,
                "account_id": account_id,
                "category_id": category_id,
                "transaction_date": "2023-06-04T10:04:04.737664Z"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction_id = Transaction.objects.latest('id').id
        response = self.client.get(reverse('expense:transaction-detail', kwargs={'pk': transaction_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Transaction 1')
