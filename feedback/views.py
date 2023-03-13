import django.core.mail
import django.shortcuts
from django.conf import settings

from feedback import forms, models


def feedback(request):
    file_form = forms.FeedbackFileForm(request.POST or None)
    data_form = forms.FeedbackDataForm(
        request.POST or None, request.FILES or None
    )
    form = forms.FeedbackForm(request.POST or None)
    template = 'feedback/feedback_form.html'
    if all((form.is_valid(), data_form.is_valid(), file_form.is_valid())):
        django.core.mail.send_mail(
            'Обращение'.encode('utf-8'),
            data_form.cleaned_data['text'],
            settings.EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
        )
        files = request.FILES.getlist('uploaded_file')
        data = data_form.save()
        feedback = form.save(commit=False)
        feedback.data = data
        feedback.save()
        for uploaded_file in files:
            models.Files.objects.create(
                data=data,
                uploaded_file=uploaded_file,
            )
        return django.shortcuts.redirect('about:thanks')
    context = {
        'feedback_form': form,
        'feedback_data_form': data_form,
        'feedback_file_form': file_form,
    }
    return django.shortcuts.render(request, template, context)
