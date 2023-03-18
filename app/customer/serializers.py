from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Customer
from .utilities import Utilities


class RegisterSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=10)
    phone = serializers.CharField(max_length=15)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)

    def validate(self, attrs):
        full_phone = f"{attrs['country_code']}{attrs['phone']}"
        if get_user_model().objects.filter(username=full_phone).exists():
            raise serializers.ValidationError(
                'This phone number is already registered. Please use login page.'
            )

        return attrs

    def create(self, validated_data):
        full_phone = f"{validated_data['country_code']}{validated_data['phone']}"
        otp = Utilities.generate_otp()

        user = get_user_model().objects.create_user(
            username=full_phone,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=f'pass{otp}',
            is_active=False
        )
        user.save()

        return Customer.objects.create(
            user=user,
            country_code=validated_data['country_code'],
            phone=validated_data['phone'],
            otp=otp
        )

    def update(self, instance, validated_data):
        pass


class VerifyRegisterSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=10)
    phone = serializers.CharField(max_length=15)
    otp = serializers.IntegerField()

    def validate(self, attrs):
        if not Customer.objects.filter(
                country_code=attrs['country_code'],
                phone=attrs['phone'],
                otp=attrs['otp']
        ).exists():
            raise serializers.ValidationError('Wrong OTP given')

        return attrs

    def create(self, validated_data):
        full_phone = f"{validated_data['country_code']}{validated_data['phone']}"
        user = get_user_model().objects.get(username=full_phone)
        user.is_active = True
        user.save()
        customer = Customer.objects.filter(user=user)

        return customer

    def update(self, instance, validated_data):
        pass


class LoginSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=10)
    phone = serializers.CharField(max_length=15)

    def validate(self, attrs):
        full_phone = f"{attrs['country_code']}{attrs['phone']}"
        if not get_user_model().objects.filter(username=full_phone).exists():
            raise serializers.ValidationError(
                'Cannot verify user. Please use register page if using first time.'
            )

        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return Customer.objects.get(
            country_code=validated_data['country_code'],
            phone=validated_data['phone']
        )


class VerifyLoginSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=10)
    phone = serializers.CharField(max_length=15)
    otp = serializers.IntegerField()

    def validate(self, attrs):
        if not Customer.objects.filter(
                country_code=attrs['country_code'],
                phone=attrs['phone'],
                otp=attrs['otp']
        ).exists():
            raise serializers.ValidationError('Wrong OTP given')

        return attrs

    def create(self, validated_data):
        full_phone = f"{validated_data['country_code']}{validated_data['phone']}"
        user = get_user_model().objects.get(username=full_phone)
        token, created = Token.objects.get_or_create(user=user)

        return {**validated_data, 'token': token}

    def update(self, instance, validated_data):
        pass
