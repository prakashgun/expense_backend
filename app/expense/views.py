from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .permissions import IsOwner
from .serializers import AccountSerializer


class AccountList(APIView):
    """List all expense accounts or create a new one"""

    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)

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
