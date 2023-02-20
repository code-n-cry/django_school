import catalog.validators
import core.models
import django.core.validators
import django.db.models


class TagsUniqueNames(core.models.AbstractProtectionModel):
    pass


class CategoriesUniqueNames(core.models.AbstractProtectionModel):
    pass


class Category(core.models.AbstractModel):
    slug = django.db.models.CharField(
        'символьный код для url',
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
        'вес',
        help_text='Введите вес(число 0-100)',
        default=100,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Tag(core.models.AbstractModel):
    slug = django.db.models.CharField(
        'символьный код для url',
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
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Item(core.models.AbstractModel):
    text = django.db.models.TextField(
        'описание',
        help_text='Описание(>2 символов, содержит "превосходно, роскошно")',
        validators=[
            catalog.validators.ValidateMustContain('превосходно', 'роскошно'),
        ],
    )
    catalog_category = django.db.models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=django.db.models.CASCADE,
        related_name='items',
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name='тег',
        related_name='items',
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name
