import logging
import os

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from .serializers import RegisterSerializer, VerifyRegisterSerializer

logger = logging.getLogger(__name__)


class PhoneClient:

    @staticmethod
    def send_otp(otp, full_phone):
        """Send otp to user"""
        try:
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid, auth_token)
        except KeyError as e:
            logger.error(e)
            return False

        try:
            client.messages.create(
                body=f"Your OTP is {otp}",
                from_=os.environ['TWILIO_PHONE_NUMBER'],
                to=full_phone
            )

            return True
        except TwilioRestException as e:
            logger.error(e)
            return False


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
            serializer.save()
            return Response({'message': 'Registration Verified'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
