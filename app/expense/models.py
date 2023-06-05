import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Account(models.Model):
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    initial_balance = models.FloatField()
    owner = models.ForeignKey(get_user_model(), related_name='accounts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('name', 'owner')


class Category(models.Model):
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=100)
    icon_type = models.CharField(max_length=100)
    owner = models.ForeignKey(get_user_model(), related_name='categories', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'


class Transaction(models.Model):
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True)
    value = models.FloatField()
    is_income = models.BooleanField(default=False)
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='transactions', on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), related_name='transactions', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
