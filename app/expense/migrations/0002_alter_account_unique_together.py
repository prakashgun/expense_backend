# Generated by Django 4.1.7 on 2023-03-24 17:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='account',
            unique_together={('name', 'owner')},
        ),
    ]
