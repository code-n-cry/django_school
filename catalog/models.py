import django.core.validators
import django.db.models

import catalog.validators
import core.models


class Category(core.models.AbstractModel):
    slug = django.db.models.TextField(
        'Символьный код для url',
        help_text='Напишите код для url(только лат. буквы, цифры и `-`, `_`)',
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.RegexValidator(
                r'^[0-9a-zA-Z-_]*$',
                'Использовать можно только цифры, буквы латиницы и `-`, `_`',
            )
        ],
    )
    weight = django.db.models.PositiveSmallIntegerField(
        'Вес',
        help_text='Введите вес(число 0-100)',
        default=100,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(core.models.AbstractModel):
    slug = django.db.models.TextField(
        'Символьный код для url',
        help_text='Напишите код для url(только лат. буквы, цифры и `-`, `_`)',
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.RegexValidator(
                r'^[0-9a-zA-Z-_]*$',
                'Использовать можно только цифры, буквы латиницы и `-`, `_`',
            )
        ],
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Item(core.models.AbstractModel):
    text = django.db.models.TextField(
        'Описание',
        help_text='Описание(>2 символов, содержит "превосходно, роскошно")',
        validators=[
            django.core.validators.MinLengthValidator(2),
            catalog.validators.ValidateMustContain('превосходно', 'роскошно'),
        ],
    )
    catalog_category = django.db.models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=django.db.models.CASCADE,
        related_name='items',
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='items',
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
