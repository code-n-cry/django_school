import django.contrib.auth.views
import django.urls

import users.views

app_name = 'users'

urlpatterns = [
    django.urls.path('list/', users.views.user_list, name='user-list'),
]
