import django.contrib.auth.views
import django.urls

import users.forms

app_name = 'auth'

urlpatterns = [
    django.urls.path(
        'login/',
        django.contrib.auth.views.LoginView.as_view(
            template_name='users/login.html',
        ),
        name='login',
    ),
    django.urls.path(
        'logout/',
        django.contrib.auth.views.LogoutView.as_view(
            template_name='users/logged_out.html',
        ),
        name='logout',
    ),
    django.urls.path(
        'password_change/',
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
        ),
        name='password_change',
    ),
    django.urls.path(
        'password_change/done',
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    django.urls.path(
        'password_reset/',
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
        ),
        name='password_reset',
    ),
    django.urls.path(
        'password_reset/done/',
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    django.urls.re_path(
        'reset/$',
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    django.urls.path(
        'password_reset/complete/',
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    django.urls.path('signup/', users.views.signup, name='signup'),
    django.urls.path(
        'activate/<str:username>', users.views.activate, name='activate'
    ),
]