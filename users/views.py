import datetime

import django.core.mail
import django.urls
import django.utils.timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

import users.forms
import users.models


def activate_new(request, username):
    user = users.models.User.objects.filter(
        username=username,
        date_joined__range=[
            django.utils.timezone.now() - datetime.timedelta(hours=12),
            django.utils.timezone.now(),
        ],
    ).first()
    if not user:
        messages.error(
            request, 'Прошло больше 12 часов, ссылка уже не работает:('
        )
        return redirect('homepage:index')
    user.is_active = True
    user.save()
    messages.success(request, 'Вы активированы!')
    return redirect('homepage:index')


def activate(request, username):
    user = users.models.User.objects.filter(
        username=username,
        profile__last_failed_login_date__range=[
            django.utils.timezone.now() - datetime.timedelta(weeks=1),
            django.utils.timezone.now(),
        ],
    ).first()
    if not user:
        messages.error(request, 'Прошла неделя, ссылка уже не работает:(')
        return redirect('homepage:index')
    user.is_active = True
    user.save()
    messages.success(request, 'Аккаунт восстановлен')
    return redirect('auth:login')


def signup(request):
    form = users.forms.SignUpForm(request.POST or None)
    template = 'users/signup.html'
    if form.is_valid():
        email_text = ''.join(
            [
                'Ваша ссылка для активации: http://127.0.0.1:8000',
                django.urls.reverse(
                    'auth:activate_new',
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
        users.models.ProxyUser.objects.all()
        .values(
            users.models.ProxyUser.id.field.name,
            users.models.ProxyUser.username.field.name,
        )
        .order_by(users.models.ProxyUser.username.field.name)
    )
    template = 'users/user_list.html'
    context = {'usernames': usernames}
    return render(request, template, context)


def user_detail(request, user_id):
    template = 'users/user_detail.html'
    user = get_object_or_404(users.models.ProxyUser.objects.filter(pk=user_id))
    context = {'user': user}
    return render(request, template, context)


def unauthorized(request):
    template = 'users/unauthorized.html'
    context = {}
    return render(request, template, context)


@login_required
def profile(request):
    template = 'users/profile.html'
    data_form = users.forms.NameEmailForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    profile_form = users.forms.ProfileInfoForm(
        request.POST or None,
        instance=request.user.profile,
    )
    if all((data_form.is_valid(), profile_form.is_valid())):
        if request.FILES:
            request.user.profile.avatar = request.FILES['avatar']
        profile_form.save()
        data_form.save()
    context = {'form': data_form, 'profile_form': profile_form}
    return render(request, template, context)
