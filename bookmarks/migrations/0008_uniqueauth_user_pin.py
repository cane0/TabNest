# Generated by Django 4.1.2 on 2023-11-15 16:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0007_alter_tab_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='uniqueauth',
            name='user_pin',
            field=models.CharField(default='000000', max_length=6, validators=[django.core.validators.RegexValidator('^\\d{4,6}$', code='invalid_format', message='Enter a valid 4 to 6 digit PIN')]),
        ),
    ]
