from django.contrib.auth import get_user_model


class Utilities:

    @staticmethod
    def sample_user(**params):
        defaults = {
            'username': '0123456789',
            'password': 'test',
            'email': 'test@example.com'
        }

        defaults.update(params)

        return get_user_model().objects.create(**params)
