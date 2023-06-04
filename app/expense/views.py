from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account, Category, Transaction
from .permissions import IsOwner
from .serializers import AccountSerializer, CategorySerializer, TransactionSerializer


class AccountList(APIView):
    """List all expense accounts or create a new one"""

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        accounts = Account.objects.filter(owner=request.user)

        for account in accounts:
            self.check_object_permissions(request, account)

        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {
            'name': request.data['name'],
            'note': request.data['note'],
            'initial_balance': request.data['initial_balance'],
            'owner': request.user.id
        }

        serializer = AccountSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AccountDetail(APIView):
    """Retrieve, update or delete an account instance"""

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        account = self.get_object(pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk):
        account = self.get_object(pk)
        serializer = AccountSerializer(account, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = self.get_object(pk)
        account.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    """List all expense categories or create a new one"""

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        categories = Category.objects.filter(owner=request.user)

        for category in categories:
            self.check_object_permissions(request, category)

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {
            'name': request.data['name'],
            'icon_name': request.data['icon_name'],
            'icon_type': request.data['icon_type'],
            'owner': request.user.id
        }

        serializer = CategorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryDetail(APIView):
    """Retrieve, update or delete an category instance"""

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionList(APIView):
    """List all expense transactions or create a new one"""

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        transactions = Transaction.objects.filter(owner=request.user)

        for transaction in transactions:
            self.check_object_permissions(request, transaction)

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {
            'name': request.data['name'],
            'value': request.data['value'],
            'transaction_date': request.data['transaction_date'],
            'account': request.data['account_id'],
            'category': request.data['category_id'],
            'owner': request.user.id
        }

        serializer = TransactionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionDetail(APIView):
    """Retrieve, update or delete an transaction instance"""

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = self.get_object(pk)
        transaction.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)