from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models


def home(request):
    template = 'homepage/home.html'
    items = catalog.models.Item.objects.published().filter(is_on_main=True)
    context = {'items': items}
    return render(request, template, context)


def coffee(request):
    return HttpResponse(
        'Я чайник', content_type='text/plain', status=HTTPStatus.IM_A_TEAPOT
    )
