from django.utils.translation import gettext_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView


import rating.models


class RatingByUsers(ListView):
    queryset = rating.models.Rating.objects.by_users()
    template_name = 'rating_statistics/by_users.html'
    item_context_name = 'users'
    http_method_names = ['get', 'head']
