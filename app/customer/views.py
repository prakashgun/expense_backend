from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import os
import logging
from twilio.rest import Client

from .models import Customer
from .permissions import IsPostOrAdmin
from .serializers import CustomerSerializer, UserPhoneSerializer


class UserPhoneView(APIView):

    permission_classes = [AllowAny]

    """Register a customer"""
    def post(self, request):
        serializer = UserPhoneSerializer(data=request.data)

        if serializer.is_valid():
            # Send otp to user
            try:
                account_sid = os.environ['TWILIO_ACCOUNT_SID']
                auth_token = os.environ['TWILIO_AUTH_TOKEN']
                client = Client(account_sid, auth_token)
            except KeyError as e:
                logger = logging.getLogger(__name__)
                logger.error(e)
                return Response('SMS environment not found', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            client.messages.create(
                body="Hello from Expense App",
                from_="+13464854151",
                to="+919791620104"
            )

            return Response('OTP Sent', status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
