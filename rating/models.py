from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models import Item
from users.models import User


class Rating(models.Model):
    RATING_CHOICES = [
        (1, _('Ненависть')),
        (2, _('Неприязнь')),
        (3, _('Нейтрально')),
        (4, _('Обожание')),
        (5, _('Любовь')),
    ]

    rating = models.PositiveSmallIntegerField(
        verbose_name='оценка',
        choices=RATING_CHOICES,
        blank=True,
        null=True,
    )
    item = models.ForeignKey(
        Item,
        verbose_name='товар',
        on_delete=models.CASCADE,
        related_name='item',
    )
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='user',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_rating', fields=['item', 'user']
            )
        ]
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
        default_related_name = 'rating'
