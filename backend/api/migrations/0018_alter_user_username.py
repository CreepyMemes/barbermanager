# Generated by Django 5.2.1 on 2025-07-02 13:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_user_profile_picture_user_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Username may only contain ASCII letters, digits, and underscores (_).', regex='^[a-zA-Z0-9_]+$')]),
        ),
    ]
