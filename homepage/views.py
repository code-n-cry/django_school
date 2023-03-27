from http import HTTPStatus

from django.db.models import F
from django.views.generic import ListView, TemplateView

import catalog.models
from users.models import Profile


class HomeView(ListView):
    template_name = 'homepage/home.html'
    queryset = catalog.models.Item.objects.published().filter(is_on_main=True)
    context_object_name = 'items'


class CoffeeView(TemplateView):
    template_name = 'homepage/coffee.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            Profile.objects.filter(pk=request.user.profile.id).update(
                coffee_count=F('coffee_count') + 1
            )
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=HTTPStatus.IM_A_TEAPOT)
