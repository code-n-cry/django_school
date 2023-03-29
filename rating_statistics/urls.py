import django.urls

import rating_statistics.views

app_name = 'statistics'

urlpatterns = [
    django.urls.path(
        'by_users/',
        rating_statistics.views.RatingByUsers.as_view(),
        name='by_users',
    ),
    django.urls.path(
        'by_items/',
        rating_statistics.views.RatingByItems.as_view(),
        name='by_items',
    ),
    django.urls.path(
        'by_user/',
        rating_statistics.views.RatingByCurrentUser.as_view(),
        name='by_user',
    ),
]
