from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    template = 'homepage/home.html'
    context = {'title': 'Главная'}
    return render(request, template, context)


def coffee(request):
    return HttpResponse(
        'Я чайник', content_type='text/plain', status=HTTPStatus.IM_A_TEAPOT
    )
