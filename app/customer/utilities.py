import logging
import os
import random

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)


class Utilities:
    """Basic utilities"""

    @staticmethod
    def generate_otp():
        return random.randrange(1111, 9999)


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
