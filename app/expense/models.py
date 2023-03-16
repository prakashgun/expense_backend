import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Account(models.Model):
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    initial_balance = models.FloatField()
    owner = models.ForeignKey(get_user_model(), related_name='accounts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
