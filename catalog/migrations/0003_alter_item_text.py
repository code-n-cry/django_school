# Generated by Django 3.2.17 on 2023-02-19 20:08

import django.core.validators
from django.db import migrations, models

import catalog.validators


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0002_auto_20230219_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(
                help_text='Описание(>2 символов, содержит "превосходно, роскошно")',
                validators=[
                    django.core.validators.MinLengthValidator(2),
                    catalog.validators.ValidateMustContain(
                        'превосходно', 'роскошно'
                    ),
                ],
                verbose_name='Описание',
            ),
        ),
    ]
