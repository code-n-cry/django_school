from django.views.generic import ListView

import rating.models


class RatingByUsers(ListView):
    queryset = rating.models.Rating.objects.by_users()
    template_name = 'rating_statistics/by_users.html'
    item_context_name = 'users'
    http_method_names = ['get', 'head']


class RatingByItems(ListView):
    queryset = rating.models.Rating.objects.by_items()
    template_name = 'rating_statistics/by_items.html'
    item_context_name = 'items'
    http_method_names = ['get', 'head']
