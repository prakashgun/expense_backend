# Generated by Django 4.1.7 on 2023-05-25 16:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_account_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('icon_name', models.CharField(max_length=100)),
                ('icon_type', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
