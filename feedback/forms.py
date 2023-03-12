import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.Feedback
        fields = (
            feedback.models.Feedback.text.field.name,
            feedback.models.Feedback.email.field.name,
        )
        labels = {
            feedback.models.Feedback.text.field.name: 'Содержание обращения',
            feedback.models.Feedback.email.field.name: 'E-Mail',
        }
        help_texts = {
            feedback.models.Feedback.text.field.name: 'Опишите проблему',
            feedback.models.Feedback.email.field.name: 'Ваша почта',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
