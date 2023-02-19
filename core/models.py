import django.db.models


class AbstractModel(django.db.models.Model):
    name = django.db.models.TextField(
        'Название',
        help_text='Добавьте название товара',
        max_length=150,
    )
    is_published = django.db.models.BooleanField(
        'Опубликовать?',
        help_text='Выберите статус..',
        default=True,
    )

    class Meta:
        abstract = True
