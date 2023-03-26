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

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_rating', fields=['item', 'user']
            )
        ]
