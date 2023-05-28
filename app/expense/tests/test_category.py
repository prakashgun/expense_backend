from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .utilities import Utilities
from ..models import Category

CATEGORY_LIST_URL = reverse('expense:category-list')
CATEGORY_DETAIL_URL = reverse('expense:category-detail', kwargs={'pk': 'some_id'})


class PublicAccountListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_categories_unauthenticated_permissions(self):
        response = self.client.get(CATEGORY_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_category_unauthenticated_permissions(self):
        response = self.client.get(CATEGORY_LIST_URL)
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

    def test_adding_duplicate_category_fails(self):
        response = self.client.post(
            CATEGORY_LIST_URL,
            data={
                "name": "Category 1",
                "icon_name": 'Icon name 1',
                "icon_type": "Icon type 1"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            CATEGORY_LIST_URL,
            data={
                "name": "Category 1",
                "icon_name": 'Icon name 1',
                "icon_type": "Icon type 1"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['This category name already exists'])

    def test_added_categories_visible_to_owner(self):
        response = self.client.post(
            CATEGORY_LIST_URL,
            data={
                "name": "Category 1",
                "icon_name": 'Icon name 1',
                "icon_type": "Icon type 1"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(CATEGORY_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Category 1')
        self.assertEqual(response.data[0]['icon_name'], 'Icon name 1')
        self.assertEqual(response.data[0]['icon_type'], 'Icon type 1')

    def test_category_is_not_visible_to_non_owners(self):
        response = self.client.post(
            CATEGORY_LIST_URL,
            data={
                "name": "Category 1",
                "icon_name": 'Icon name 1',
                "icon_type": "Icon type 1"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(self.user2, token=self.user2.auth_token)

        response = self.client.get(CATEGORY_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data,
            []
        )

    def test_view_added_category(self):
        response = self.client.post(
            CATEGORY_LIST_URL,
            data={
                "name": "Category 1",
                "icon_name": 'Icon name 1',
                "icon_type": "Icon type 1"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = Category.objects.latest('id').id
        response = self.client.get(reverse('expense:category-detail', kwargs={'pk': category_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Category 1')
