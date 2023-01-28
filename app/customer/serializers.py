from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Customer, UserPhone


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class UserPhoneSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=10)
    phone = serializers.CharField(max_length=15)

    def create(self, validated_data):
        return UserPhone(**validated_data)

    def update(self, instance, validated_data):
        instance.country_code = validated_data.get('country_code', instance.country_code)
        instance.phone = validated_data.get('phone', instance.phone)

        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
