import django.db.models


class AbstractModel(django.db.models.Model):
    name = django.db.models.TextField(
        'Название',
        help_text='Добавьте название товара',
        max_length=150,
        validators=[],
    )
    is_published = django.db.models.BooleanField(
        'Опубликовать?',
        help_text='Выберите статус..',
        default=True,
        validators=[],
    )

    class Meta:
        abstract = True


class AbstractProtectionModel(django.db.models.Model):
    name = django.db.models.TextField(max_length=150, unique=True)

    class Meta:
        abstract = True
