import django.core.mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy
from django.views.generic import TemplateView

from feedback import forms, models


class FeedbackFormView(TemplateView):
    form_class = forms.FeedbackForm
    personal_data_form_class = forms.FeedbackPersonalDataForm
    file_form_class = forms.FeedbackFileForm
    template_name = 'feedback/feedback_form.html'

    def get(self, request, *args, **kwargs):
        feedback_form = self.form_class()
        personal_data_form = self.personal_data_form_class()
        file_form = self.file_form_class()
        extra_context = {
            'feedback_form': feedback_form,
            'feedback_personal_data_form': personal_data_form,
            'feedback_file_form': file_form,
        }
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        feedback_form = self.form_class(request.POST)
        personal_data_form = self.personal_data_form_class(request.POST)
        file_form = self.file_form_class(request.POST, request.FILES or None)
        if all(
            (
                feedback_form.is_valid(),
                personal_data_form.is_valid(),
                file_form.is_valid(),
            )
        ):
            django.core.mail.send_mail(
                gettext_lazy('Обращение'),
                feedback_form.cleaned_data['text'],
                settings.EMAIL,
                [personal_data_form.cleaned_data['email']],
                fail_silently=False,
            )
            files = request.FILES.getlist('uploaded_file')
            personal_data = personal_data_form.save(commit=False)
            feedback = feedback_form.save()
            personal_data.feedback = feedback
            personal_data.save()
            for uploaded_file in files:
                models.Files.objects.create(
                    data=feedback,
                    uploaded_file=uploaded_file,
                )
            return django.shortcuts.redirect('about:thanks')
        extra_context = {
            'feedback_form': feedback_form,
            'feedback_personal_data_form': personal_data_form,
            'feedback_file_form': file_form,
        }
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)
