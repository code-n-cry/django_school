import django.utils.html
import sorl
from django.contrib.auth.models import User
from django.db import models

import core.models


def avatar_image_path(instance, filename):
    return f'/uploads/{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(
        verbose_name='дата рождения',
        help_text='дата рождения пользователя',
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to=avatar_image_path,
        verbose_name='аватарка',
        help_text='картинка профиля пользователя',
        null=True,
        blank=True,
    )
    coffee_count = models.IntegerField(
        verbose_name='сварено кофе',
        help_text='сколько раз пользователь пытался сварить кофе',
        default=0,
    )

    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'
        default_related_name = 'profile'

    def get_avatar_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image, '300x300', crop='center', quality=65
        )

    def image_tmb(self):
        if self.image:
            return django.utils.html.mark_safe(
                f'<img src="{self.get_image_300x300().url}">'
            )
        self.image_tmb.short_description = 'превью'
        return '(Аватарка)'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.image = self.get_image_300x300()
