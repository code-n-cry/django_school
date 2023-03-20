import django.utils.html
import sorl
from django.contrib.auth.models import User
from django.db import models


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
        if self.avatar:
            return sorl.thumbnail.get_thumbnail(
                self.avatar, '300x300', crop='center', quality=65
            )

    def avatar_tmb(self):
        if self.avatar:
            return django.utils.html.mark_safe(
                f'<img src="{self.get_avatar_300x300().url}">'
            )
        self.avatar_tmb.short_description = 'превью'
        return 'Аватарки нэ будет.'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.avatar = self.get_avatar_300x300()
