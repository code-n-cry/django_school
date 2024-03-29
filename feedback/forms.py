from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy

from core.forms import BootstrapForm
from feedback import models


class FeedbackFileForm(BootstrapForm):
    class Meta:
        model = models.Files
        fields = (models.Files.uploaded_file.field.name,)
        labels = {
            models.Files.uploaded_file.field.name: ''.join(
                gettext_lazy('Файлы для подробного описания(если хотите)')
            ),
        }
        help_texts = {
            models.Files.uploaded_file.field.name: gettext_lazy(
                'Прикрепите файлы'
            ),
        }
        widgets = {
            models.Files.uploaded_file.field.name: ClearableFileInput(
                attrs={'multiple': True},
            ),
        }


class FeedbackPersonalDataForm(BootstrapForm):
    class Meta:
        model = models.PersonalData
        fields = (models.PersonalData.email.field.name,)
        labels = {
            models.PersonalData.email.field.name: 'E-Mail',
        }
        help_texts = {
            models.PersonalData.email.field.name: gettext_lazy('Ваша почта'),
        }


class FeedbackForm(BootstrapForm):
    class Meta:
        model = models.Feedback
        fields = (models.Feedback.text.field.name,)
        labels = {
            models.Feedback.text.field.name: gettext_lazy(
                'Содержание обращения'
            ),
        }
        help_texts = {
            models.Feedback.text.field.name: gettext_lazy('Опишите проблему'),
        }
