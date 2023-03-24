from http import HTTPStatus

from django.db.models import F
from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import Profile
import catalog.models
from django.db import transaction


class HomeView(TemplateView):
    template_name = 'homepage/home.html'

    def get(self, request, *args, **kwargs):
        items = catalog.models.Item.objects.published().filter(is_on_main=True)
        extra_context = {'items': items}
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)


class CoffeeView(TemplateView):
    template_name = 'homepage/coffee.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            Profile.objects.filter(pk=request.user.profile.id).update(coffee_count=F('coffee_count') + 1)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=HTTPStatus.IM_A_TEAPOT)
