import django.core.mail
import django.shortcuts
from django.conf import settings

from feedback import forms, models


def feedback(request):
    file_form = forms.FeedbackFileForm(
        request.POST or None, request.FILES or None
    )
    personal_data_form = forms.FeedbackPersonalDataForm(request.POST or None)
    form = forms.FeedbackForm(request.POST or None)
    template = 'feedback/feedback_form.html'
    if all(
        (form.is_valid(), personal_data_form.is_valid(), file_form.is_valid())
    ):
        django.core.mail.send_mail(
            'Обращение'.encode('utf-8'),
            form.cleaned_data['text'],
            settings.EMAIL,
            [personal_data_form.cleaned_data['email']],
            fail_silently=False,
        )
        files = request.FILES.getlist('uploaded_file')
        personal_data = personal_data_form.save()
        feedback = form.save(commit=False)
        feedback.personal_data = personal_data
        feedback.save()
        for uploaded_file in files:
            models.Files.objects.create(
                data=feedback,
                uploaded_file=uploaded_file,
            )
        return django.shortcuts.redirect('about:thanks')
    context = {
        'feedback_form': form,
        'feedback_personal_data_form': personal_data_form,
        'feedback_file_form': file_form,
    }
    return django.shortcuts.render(request, template, context)
