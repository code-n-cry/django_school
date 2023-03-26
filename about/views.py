from django.views.generic import TemplateView


class DescriptionView(TemplateView):
    template_name = 'about/description.html'


class ThanksForFeedbackView(TemplateView):
    template_name = 'about/feedback_success.html'
