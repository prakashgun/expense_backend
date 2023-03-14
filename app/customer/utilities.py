import random


class Utilities:
    """Basic utilities"""

    @staticmethod
    def generate_otp():
        return random.randrange(1111, 9999)
