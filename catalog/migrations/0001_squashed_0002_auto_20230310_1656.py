# Generated by Django 3.2.17 on 2023-03-10 13:58

import ckeditor.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import catalog.validators


class Migration(migrations.Migration):
    replaces = [
        ('catalog', '0001_squashed_0003_auto_20230307_2011'),
        ('catalog', '0002_auto_20230310_1656'),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=True,
                        help_text='Выберите статус публикации',
                        verbose_name='опубликовать?',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Добавьте название',
                        max_length=150,
                        unique=True,
                        verbose_name='название',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        help_text='Напишите код для url(латинские буквы, цифры и `-`, `_`)',
                        max_length=200,
                        unique=True,
                        verbose_name='слаг',
                    ),
                ),
                (
                    'weight',
                    models.PositiveSmallIntegerField(
                        default=100,
                        help_text='Введите вес(число 0-100)',
                        validators=[
                            django.core.validators.MaxValueValidator(32767)
                        ],
                        verbose_name='вес',
                    ),
                ),
                (
                    'unique_name',
                    models.CharField(
                        editable=False,
                        help_text='Колонка для проверки уникальности названия',
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name='уникальное имя',
                    ),
                ),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=True,
                        help_text='Выберите статус публикации',
                        verbose_name='опубликовать?',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Добавьте название',
                        max_length=150,
                        unique=True,
                        verbose_name='название',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        help_text='Напишите код для url(латинские буквы, цифры и `-`, `_`)',
                        max_length=200,
                        unique=True,
                        verbose_name='слаг',
                    ),
                ),
                (
                    'unique_name',
                    models.CharField(
                        editable=False,
                        help_text='Колонка для проверки уникальности названия',
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name='уникальное имя',
                    ),
                ),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
                'default_related_name': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=True,
                        help_text='Выберите статус публикации',
                        verbose_name='опубликовать?',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Добавьте название',
                        max_length=150,
                        unique=True,
                        verbose_name='название',
                    ),
                ),
                (
                    'text',
                    ckeditor.fields.RichTextField(
                        help_text='Описание(>2 символов, содержит 'превосходно, роскошно')',
                        validators=[
                            catalog.validators.ValidateMustContain(
                                'превосходно', 'роскошно'
                            )
                        ],
                        verbose_name='описание',
                    ),
                ),
                (
                    'category',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='items',
                        to='catalog.category',
                        verbose_name='категория',
                    ),
                ),
                (
                    'tags',
                    models.ManyToManyField(
                        related_name='items',
                        to='catalog.Tag',
                        verbose_name='тег',
                    ),
                ),
                (
                    'is_on_main',
                    models.BooleanField(
                        default=False,
                        help_text='Публиковать товар на главной странице?',
                        verbose_name='публикация на главной странице',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='дата добавления товара',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True, verbose_name='дата изменения товара'
                    ),
                ),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'default_related_name': 'items',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ItemDescriptionsImages',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        help_text='загрузите картинки для уточнения описания',
                        upload_to='uploaded/',
                        verbose_name='изображение(будет масштабировано до 300x300)',
                    ),
                ),
                (
                    'item',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='description_images',
                        to='catalog.item',
                        verbose_name='галерея изображений товара',
                    ),
                ),
            ],
            options={
                'default_related_name': 'description_images',
                'verbose_name': 'галерея фото товара',
                'verbose_name_plural': 'ещё фотографии товара',
            },
        ),
        migrations.CreateModel(
            name='ItemMainImage',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        help_text='загрузите картинки для уточнения описания',
                        upload_to='uploaded/',
                        verbose_name='изображение(будет масштабировано до 300x300)',
                    ),
                ),
                (
                    'item',
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='main_image',
                        to='catalog.item',
                        verbose_name='главное фото',
                    ),
                ),
            ],
            options={
                'default_related_name': 'main_image',
                'verbose_name': 'главное изображение товара(одна картинка)',
            },
        ),
    ]
