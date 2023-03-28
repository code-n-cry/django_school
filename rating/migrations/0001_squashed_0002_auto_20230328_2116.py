# Generated by Django 3.2.17 on 2023-03-28 19:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ('rating', '0001_squashed_0003_alter_rating_rating'),
        ('rating', '0002_auto_20230328_2116'),
    ]

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
                        help_text='на сколько оценили',
                        null=True,
                        verbose_name='оценка',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text='когда оценили',
                        verbose_name='дата оценки',
                    ),
                ),
                (
                    'item',
                    models.ForeignKey(
                        help_text='какой товар оценили?',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='item',
                        to='catalog.item',
                        verbose_name='товар',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        help_text='кто оценил?',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='rating',
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
        migrations.AlterField(
            model_name='rating',
            name='item',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='rating',
                to='catalog.item',
                verbose_name='товар',
            ),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveSmallIntegerField(
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
        migrations.AlterField(
            model_name='rating',
            name='item',
            field=models.ForeignKey(
                help_text='какой товар оценили?',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='rating',
                to='catalog.item',
                verbose_name='товар',
            ),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, 'Ненависть'),
                    (2, 'Неприязнь'),
                    (3, 'Нейтрально'),
                    (4, 'Обожание'),
                    (5, 'Любовь'),
                ],
                help_text='на сколько оценили',
                null=True,
                verbose_name='оценка',
            ),
        ),
    ]