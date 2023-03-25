import django.db.models

import feedback.static


def upload_directory_path(instance, filename):
    return f'uploads/{instance.data.pk}/{filename}'


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        verbose_name='содержание',
        help_text='Содержание отзыва',
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='дата и время создания',
        auto_now_add=True,
    )
    status = django.db.models.PositiveSmallIntegerField(
        verbose_name='статус обработки',
        help_text='Статус обработки заявления',
        choices=feedback.static.FEEDBACK_STATUS,
        default=feedback.static.FEEDBACK_STATUS_DICT['Получено'],
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        default_related_name = 'feedback'

    def __str__(self):
        return f'Отзыв №{self.pk}'


class PersonalData(django.db.models.Model):
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
    )
    email = django.db.models.EmailField(
        verbose_name='электронная почта',
        help_text='E-mail отправителя',
        max_length=254,
    )

    class Meta:
        verbose_name = 'персональные данные автора'
        verbose_name_plural = 'персональные данные авторов'
        default_related_name = 'personal_data'

    def __str__(self):
        return f'Персональные данные автора отзыва №{self.feedback.pk}'


class Files(django.db.models.Model):
    uploaded_file = django.db.models.FileField(
        verbose_name='загруженные файлы',
        help_text='Файлы, загруженные для описания',
        upload_to=upload_directory_path,
        blank=True,
        null=True,
    )
    data = django.db.models.ForeignKey(
        Feedback,
        null=True,
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = 'приложенный файл'
        verbose_name_plural = 'приложенные файлы'
        default_related_name = 'files'
