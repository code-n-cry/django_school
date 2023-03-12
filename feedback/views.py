import django.core.mail
import django.shortcuts
from django.conf import settings

from feedback import forms


def feedback(request):
    form = forms.FeedbackForm(request.POST or None)
    template = 'feedback/feedback_form.html'
    if form.is_valid():
        django.core.mail.send_mail(
            'Обращение'.encode('utf-8'),
            form.cleaned_data['text'],
            settings.EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
        )
        form.save()
        return django.shortcuts.redirect('about:thanks')
    context = {'feedback_form': form}
    return django.shortcuts.render(request, template, context)
