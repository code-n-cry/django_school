import django.contrib.auth.views
import django.urls

import users.views

app_name = 'users'

urlpatterns = [
    django.urls.path('list/', users.views.user_list, name='user_list'),
    django.urls.path(
        'detail/<int:user_id>/', users.views.user_detail, name='user_detail'
    ),
    django.urls.path('profile/', users.views.profile, name='profile'),
]
