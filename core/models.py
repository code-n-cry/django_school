import django.core.validators
import django.db.models


class PublishedWithNameBaseModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        verbose_name='опубликовать?',
        help_text='Выберите статус публикации',
        default=True,
    )
    name = django.db.models.CharField(
        verbose_name='название',
        help_text='Добавьте название товара',
        max_length=150,
        unique=True,
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        abstract = True


class SlugBaseModel(PublishedWithNameBaseModel):
    slug = django.db.models.CharField(
        'слаг',
        help_text='Напишите код для url(латинские буквы, цифры и `-`, `_`)',
        max_length=200,
        unique=True,
        validators=[django.core.validators.validate_slug],
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
