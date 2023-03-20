import datetime

import django.core.mail
import django.urls
import django.utils.timezone
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

import users.forms
import users.models


def activate(request, username):
    user = users.models.User.objects.filter(
        username=username,
        date_joined__range=[
            django.utils.timezone.now() - datetime.timedelta(hours=12),
            django.utils.timezone.now(),
        ],
    )
    if not user:
        messages.error(
            request, 'Прошло больше 12 часов, ссылка уже не работает:('
        )
        return redirect('homepage:index')
    messages.success(request, 'Вы активированы!')
    return redirect('homepage:index')


def signup(request):
    form = users.forms.SignUpForm(request.POST or None)
    template = 'users/signup.html'
    if form.is_valid():
        email_text = ''.join(
            [
                'Ваша ссылка для активации: ',
                django.urls.reverse(
                    'auth:activate',
                    kwargs={'username': form.cleaned_data['username']},
                ),
            ]
        )
        django.core.mail.send_mail(
            'Активация'.encode('utf-8'),
            email_text,
            settings.EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
        )
        form.save()
        messages.success(request, 'Вы зарегистрированы!')
        return redirect('auth:login')
    context = {
        'form': form,
    }
    return render(request, template, context)


def user_list(request):
    usernames = (
        users.models.User.objects.filter(is_active=True)
        .values(users.models.User.username.field.name)
        .order_by(users.models.User.username.field.name)
    )
    template = 'users/user_list.html'
    context = {'usernames': usernames}
    return render(request, template, context)


def user_detail(request, user_id):
    template = 'users/user_detail.html'
    usr = users.models.User.objects.filter(pk=user_id)
    print(usr[0].profile)
    user = get_object_or_404(
        users.models.User.objects.filter(pk=user_id)
        .select_related(users.models.User.profile.related.related_name)
        .values(
            users.models.User.email.field.name,
            users.models.User.first_name.field.name,
            users.models.User.last_name.field.name,
            '__'.join(
                [
                    users.models.User.profile.related.related_name,
                    users.models.Profile.birthday.field.name,
                ]
            ),
            '__'.join(
                [
                    users.models.User.profile.related.related_name,
                    users.models.Profile.avatar.field.name,
                ]
            ),
            '__'.join(
                [
                    users.models.User.profile.related.related_name,
                    users.models.Profile.coffee_count.field.name,
                ]
            ),
        )
    )
    context = {'user': user}
    return render(request, template, context)


def unauthorized(request):
    template = 'users/unauthorized.html'
    context = {}
    return render(request, template, context)


def profile(request):
    template = 'users/profile.html'
    if request.user.is_authenticated:
        data_form = users.forms.NameEmailForm(
            request.POST or None,
            initial={
                'email': request.user.email,
                'username': request.user.get_username(),
            },
        )
        profile_form = users.forms.ProfileInfoForm(request.POST or None)
        context = {'data_form': data_form, 'profile_form': profile_form}
        return render(request, template, context)
    return redirect('auth:unauthorized')
