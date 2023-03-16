from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Account
        fields = '__all__'
