from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'initial_balance', 'owner')
        validators = [UniqueTogetherValidator(
            queryset=Account.objects.all(),
            fields=('name', 'owner'),
            message='This account name already exists'
        )]
