import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_squashed_0002_auto_20230310_1656'),
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
                        choices=[
                            (1, 'Ненависть'),
                            (2, 'Неприязнь'),
                            (3, 'Нейтрально'),
                            (4, 'Обожание'),
                            (5, 'Любовь'),
                        ]
                    ),
                ),
                (
                    'item',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='catalog.item',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(
                fields=('item', 'user'), name='unique_rating'
            ),
        ),
    ]
