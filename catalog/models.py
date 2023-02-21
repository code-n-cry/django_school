import django.core.validators
import django.db.models

import catalog.validators
import core.models


class Category(core.models.SlugBaseModel):
    weight = django.db.models.PositiveSmallIntegerField(
        'вес',
        help_text='Введите вес(число 0-100)',
        default=100,
        validators=[django.core.validators.MaxValueValidator(32767)],
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Tag(core.models.SlugBaseModel):
    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Item(core.models.PublishedWithNameBaseModel):
    category = django.db.models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=django.db.models.CASCADE,
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name='тег',
        related_name='items',
    )
    text = django.db.models.TextField(
        'описание',
        help_text='Описание(>2 символов, содержит "превосходно, роскошно")',
        validators=[
            catalog.validators.ValidateMustContain('превосходно', 'роскошно'),
        ],
    )

    class Meta:
        default_related_name = 'items'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
