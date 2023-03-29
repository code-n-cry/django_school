from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

import catalog.models
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


@method_decorator(login_required, name='dispatch')
class RatingByCurrentUser(ListView):
    template_name = 'rating_statistics/by_user.html'
    item_context_name = 'ratings'
    http_method_names = ['get', 'head']

    def get_queryset(self):
        return (
            rating.models.Rating.objects.filter(
                user=self.request.user,
            )
            .select_related(rating.models.Rating.item.field.name)
            .values(
                '__'.join(
                    [
                        rating.models.Rating.item.field.name,
                        catalog.models.Item.id.field.name,
                    ]
                ),
                '__'.join(
                    [
                        rating.models.Rating.item.field.name,
                        catalog.models.Item.name.field.name,
                    ]
                ),
                rating.models.Rating.rating.field.name,
            )
        ).order_by(f'-{rating.models.Rating.rating.field.name}')
