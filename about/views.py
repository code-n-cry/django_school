from django.shortcuts import render


def description(request):
    template = 'about/description.html'
    return render(request, template)


def thanks_for_feedback(request):
    template = 'about/feedback_success.html'
    return render(request, template)
