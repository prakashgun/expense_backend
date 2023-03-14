from django.test import TestCase

from ..utilities import Utilities


class TestUtilities(TestCase):

    def test_generate_otp(self):
        otp = Utilities.generate_otp()
        self.assertGreaterEqual(otp, 1000)
        self.assertLessEqual(otp, 9999)
