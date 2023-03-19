from django.forms.widgets import ClearableFileInput

from core.forms import BootstrapForm
from feedback import models


class FeedbackFileForm(BootstrapForm):
    class Meta:
        model = models.Files
        fields = (models.Files.uploaded_file.field.name,)
        labels = {
            models.Files.uploaded_file.field.name: ''.join(
                'Файлы для подробного описания(если хотите)'
            ),
        }
        help_texts = {
            models.Files.uploaded_file.field.name: 'Прикрепите файлы',
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
            models.PersonalData.email.field.name: 'Ваша почта',
        }


class FeedbackForm(BootstrapForm):
    class Meta:
        model = models.Feedback
        fields = (models.Feedback.text.field.name,)
        labels = {
            models.Feedback.text.field.name: 'Содержание обращения',
        }
        help_texts = {
            models.Feedback.text.field.name: 'Опишите проблему',
        }
