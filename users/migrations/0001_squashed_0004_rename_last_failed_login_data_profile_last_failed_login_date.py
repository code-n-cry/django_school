# Generated by Django 3.2.17 on 2023-03-22 10:57

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import users.models


class Migration(migrations.Migration):
    replaces = [
        ('users', '0001_squashed_0002_proxyuser'),
        ('users', '0002_profile_failed_logins'),
        ('users', '0003_profile_last_failed_login_data'),
        (
            'users',
            '0004_rename_last_failed_login_data_profile_last_failed_login_date',
        ),
    ]

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyUser',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
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
                    'birthday',
                    models.DateField(
                        blank=True,
                        help_text='дата рождения пользователя',
                        null=True,
                        verbose_name='дата рождения',
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='profile',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'coffee_count',
                    models.IntegerField(
                        default=0,
                        help_text='сколько раз пользователь пытался сварить кофе',
                        verbose_name='сварено кофе',
                    ),
                ),
                (
                    'avatar',
                    models.ImageField(
                        blank=True,
                        help_text='картинка профиля пользователя',
                        null=True,
                        upload_to=users.models.avatar_image_path,
                        verbose_name='аватарка',
                    ),
                ),
                (
                    'failed_logins',
                    models.IntegerField(
                        default=0,
                        help_text='сколько раз был провален вход в аккаунт',
                        verbose_name='количество неудачных входов с момента удачного',
                    ),
                ),
                (
                    'last_failed_login_date',
                    models.DateTimeField(
                        null=True,
                        verbose_name='дата последней неудачной попытки входа',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Информация о пользователе',
                'verbose_name_plural': 'Информация о пользователях',
                'default_related_name': 'profile',
            },
        ),
    ]