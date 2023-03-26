import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('catalog', '0001_squashed_0002_auto_20230310_1656'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
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
                    'rating',
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (1, 'Ненависть'),
                            (2, 'Неприязнь'),
                            (3, 'Нейтрально'),
                            (4, 'Обожание'),
                            (5, 'Любовь'),
                        ],
                        null=True,
                        verbose_name='оценка',
                    ),
                ),
                (
                    'item',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='item',
                        to='catalog.item',
                        verbose_name='товар',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='user',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='пользователь',
                    ),
                ),
            ],
            options={
                'verbose_name': 'оценка',
                'verbose_name_plural': 'оценки',
                'default_related_name': 'rating',
            },
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(
                fields=('item', 'user'), name='unique_rating'
            ),
        ),
    ]
