import django.db.models

import feedback.static


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        verbose_name='содержание',
    )
    email = django.db.models.EmailField(
        verbose_name='электронная почта',
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='дата и время создания',
        auto_now_add=True,
    )
    status = django.db.models.PositiveSmallIntegerField(
        verbose_name='статус обработки',
        choices=feedback.static.FEEDBACK_STATUS,
        default=feedback.static.FEEDBACK_STATUS_DICT['Получено'],
    )
