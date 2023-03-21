from http import HTTPStatus

from django.shortcuts import render

import catalog.models


def home(request):
    template = 'homepage/home.html'
    items = catalog.models.Item.objects.published().filter(is_on_main=True)
    context = {'items': items}
    return render(request, template, context)


def coffee(request):
    template = 'homepage/coffee.html'
    if request.user.is_authenticated:
        request.user.profile.coffee_count += 1
        request.user.profile.save()
    return render(request, template, status=HTTPStatus.IM_A_TEAPOT)
