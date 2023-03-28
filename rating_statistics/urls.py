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
        'rated/',
        rating_statistics.views.RatedByUser.as_view(),
        name='rated',
    ),
]
