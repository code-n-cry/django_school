import difflib
import re

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

    def detect_terrible_writing(self):
        msg = 'Кажется, похожее название уже существует!'
        normalized_name = ''
        for letter in re.split(r'[\d,!?,.><():;`"\' -]', self.name.lower()):
            if letter:
                normalized_name += letter
        all_unique_names = [
            category.unique_name for category in Category.objects.all()
        ]
        for unique_name in all_unique_names:
            if len(normalized_name) == len(unique_name):
                if (
                    difflib.SequenceMatcher(
                        a=normalized_name,
                        b=unique_name,
                    ).ratio()
                    >= 0.65
                ):
                    raise django.core.exceptions.ValidationError(msg)
        return normalized_name

    def clean(self):
        self.is_cleaned = True
        if not self.unique_name:
            self.unique_name = self.detect_terrible_writing()
        return super(Category, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Tag(core.models.UniqueNameSlugBaseModel):
    def detect_terrible_writing(self):
        msg = 'Кажется, похожее название уже существует!'
        normalized_name = ''
        for letter in re.split(r'[\d,!?,.><():;`"\' -]', self.name.lower()):
            if letter:
                normalized_name += letter
        all_unique_names = [tag.unique_name for tag in Tag.objects.all()]
        for unique_name in all_unique_names:
            if len(normalized_name) == len(unique_name):
                if (
                    difflib.SequenceMatcher(
                        a=normalized_name,
                        b=unique_name,
                    ).ratio()
                    >= 0.65
                ):
                    raise django.core.exceptions.ValidationError(msg)
        return normalized_name

    def clean(self):
        self.is_cleaned = True
        if not self.unique_name:
            self.unique_name = self.detect_terrible_writing()
        return super(Tag, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(Tag, self).save(*args, **kwargs)

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
