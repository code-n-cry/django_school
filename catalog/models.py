import django.core.exceptions
import django.core.validators
import django.db.models

import catalog.validators
import core.models


class Category(core.models.UniqueNameSlugBaseModel):
    weight = django.db.models.PositiveSmallIntegerField(
        'вес',
        help_text='Введите вес(число 0-100)',
        default=100,
        validators=[django.core.validators.MaxValueValidator(32767)],
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Tag(core.models.UniqueNameSlugBaseModel):
    class Meta:
        default_related_name = 'tags'
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


class ItemMainImage(core.models.ImageModel):
    item = django.db.models.OneToOneField(
        Item,
        verbose_name='главное фото',
        null=True,
        on_delete=django.db.models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'главное изображение товара(одна картинка)'
        default_related_name = 'main_image'


class ItemDescriptionsImages(core.models.ImageModel):
    item = django.db.models.ForeignKey(
        Item,
        verbose_name='галерея изображений товара',
        on_delete=django.db.models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'галерея фото товара'
        verbose_name_plural = 'ещё фотографии товара'
        default_related_name = 'description_images'
