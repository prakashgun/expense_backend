from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    pass


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserPhone:
    def __init__(self, country_code, phone):
        self.country_code = country_code
        self.phone = phone


class Customer(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    country_code = models.CharField(max_length=5, default='+91')
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=4)
