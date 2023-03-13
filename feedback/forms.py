from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput

from feedback import models


class FeedbackFileForm(ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class FeedbackDataForm(ModelForm):
    class Meta:
        model = models.Data
        fields = (models.Data.text.field.name,)
        labels = {
            models.Data.text.field.name: 'Содержание обращения',
        }
        help_texts = {
            models.Data.text.field.name: 'Опишите проблему',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class FeedbackForm(ModelForm):
    class Meta:
        model = models.Feedback
        fields = (models.Feedback.email.field.name,)
        labels = {
            models.Feedback.email.field.name: 'E-Mail',
        }
        help_texts = {
            models.Feedback.email.field.name: 'Ваша почта',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
