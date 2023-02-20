# Generated by Django 3.2.17 on 2023-02-20 18:30

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import catalog.validators


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0004_categoriesuniquenames_tagsuniquenames'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(
                help_text='Напишите код для url(только лат. буквы, цифры и `-`, `_`)',
                max_length=200,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        '^[0-9a-zA-Z-_]*$',
                        'Использовать можно только цифры, буквы латиницы и `-`, `_`',
                    )
                ],
                verbose_name='символьный код для url',
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='catalog_category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='items',
                to='catalog.category',
                verbose_name='категория',
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(
                related_name='items', to='catalog.Tag', verbose_name='тег'
            ),
        ),
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
                verbose_name='описание',
            ),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(
                help_text='Напишите код для url(только лат. буквы, цифры и `-`, `_`)',
                max_length=200,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        '^[0-9a-zA-Z-_]*$',
                        'Использовать можно только цифры, буквы латиницы и `-`, `_`',
                    )
                ],
                verbose_name='символьный код для url',
            ),
        ),
    ]