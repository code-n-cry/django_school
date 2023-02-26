from django.shortcuts import render


def description(request):
    template = 'about/description.html'
    context = {'title': 'Описание'}
    return render(request, template, context)
