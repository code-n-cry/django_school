import django.db.models


class AbstractModel(django.db.models.Model):
    name = django.db.models.TextField(
        verbose_name='название',
        help_text='Добавьте название товара',
        max_length=150,
    )
    is_published = django.db.models.BooleanField(
        verbose_name='опубликовать?',
        help_text='Выберите статус..',
        default=True,
    )

    class Meta:
        abstract = True


class AbstractProtectionModel(django.db.models.Model):
    name = django.db.models.TextField(max_length=150, unique=True)

    class Meta:
        abstract = True
