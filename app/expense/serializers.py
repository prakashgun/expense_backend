from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Account, Category, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'initial_balance', 'owner', 'note', 'created')
        validators = [UniqueTogetherValidator(
            queryset=Account.objects.all(),
            fields=('name', 'owner'),
            message='This account name already exists'
        )]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Category.objects.all(),
            fields=('name', 'owner'),
            message='This category name already exists'
        )]

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
