from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models import Item
from rating.managers import RatingManager
from users.models import User


class Rating(models.Model):
    objects = RatingManager()

    RATING_CHOICES = [
        (1, _('Ненависть')),
        (2, _('Неприязнь')),
        (3, _('Нейтрально')),
        (4, _('Обожание')),
        (5, _('Любовь')),
    ]

    rating = models.PositiveSmallIntegerField(
        verbose_name='оценка',
        help_text='на сколько оценили',
        choices=RATING_CHOICES,
        blank=False,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name='дата оценки',
        help_text='когда оценили',
        auto_now_add=True,
    )
    item = models.ForeignKey(
        Item,
        verbose_name='товар',
        help_text='какой товар оценили?',
        on_delete=models.CASCADE,
        related_name='rating',
    )
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        help_text='кто оценил?',
        on_delete=models.CASCADE,
        related_name='rating',
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
