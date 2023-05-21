import logging

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, VerifyRegisterSerializer, LoginSerializer, VerifyLoginSerializer
from .utilities import PhoneClient

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """Register a customer"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()

            if not PhoneClient.send_otp(otp=customer.otp, full_phone=customer.user.username):
                return Response({'message': 'Failure in sending OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'OTP Sent'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyRegisterSerializer(data=request.data)

        if serializer.is_valid():
            details = serializer.save()
            return Response(
                {
                    'message': 'Registration Verified',
                    'token': details['token'].key,
                    'user': details['user']
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Register a customer"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()

            if not PhoneClient.send_otp(otp=customer.otp, full_phone=customer.user.username):
                return Response({'message': 'Failure in sending OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'OTP Sent'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyLoginView(APIView):
    """Verify authentication credentials"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyLoginSerializer(data=request.data)

        if serializer.is_valid():
            details = serializer.save()
            return Response(
                {'message': 'Login Verified', 'token': details['token'].key, 'user': details['user']},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Logout a user"""

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
