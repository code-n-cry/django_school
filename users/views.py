import datetime

import django.core.mail
import django.urls
import django.utils.timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from django.views import View
from django.views.generic import TemplateView

import users.forms
import users.models


class ActivateNewView(View):
    def get(self, request, username, *args, **kwargs):
        user = users.models.User.objects.filter(
            username=username,
            date_joined__range=[
                django.utils.timezone.now() - datetime.timedelta(hours=12),
                django.utils.timezone.now(),
            ],
        ).first()
        if not user:
            messages.error(
                request,
                gettext_lazy(
                    'Прошло больше 12 часов, ссылка уже не работает:('
                ),
            )
            return redirect('homepage:index')
        user.is_active = True
        user.save()
        messages.success(request, gettext_lazy('Вы активированы!'))
        return redirect('homepage:index')


class ActivateView(View):
    def get(self, request, username, *args, **kwargs):
        user = users.models.User.objects.filter(
            username=username,
            profile__last_failed_login_date__range=[
                django.utils.timezone.now() - datetime.timedelta(weeks=1),
                django.utils.timezone.now(),
            ],
        ).first()
        if not user:
            messages.error(
                request,
                gettext_lazy('Прошла неделя, ссылка уже не работает:('),
            )
            return redirect('homepage:index')
        user.is_active = True
        user.save()
        messages.success(request, 'Аккаунт восстановлен')
        return redirect('auth:login')


class SignUpView(TemplateView):
    signup_form_class = users.forms.SignUpForm
    template_name = 'users/signup.html'

    def get(self, request, *args, **kwargs):
        signup_form = self.signup_form_class()
        if request.user.is_authenticated:
            messages.info(request, gettext_lazy('Вы уже авторизованы!'))
            return redirect('homepage:index')
        extra_context = {
            'form': signup_form,
        }
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        signup_form = self.signup_form_class(request.POST)
        if signup_form.is_valid():
            email_text = ''.join(
                [
                    'Ваша ссылка для активации:',
                    request.build_absolute_uri(
                        django.urls.reverse(
                            'auth:activate_new',
                            kwargs={
                                'username': signup_form.cleaned_data[
                                    'username'
                                ]
                            },
                        )
                    ),
                ]
            )
            signup_form.save()
            django.core.mail.send_mail(
                gettext_lazy('Активация'),
                email_text,
                settings.EMAIL,
                [signup_form.cleaned_data['email']],
                fail_silently=False,
            )
            messages.success(request, gettext_lazy('Вы зарегистрированы!'))
            return redirect('auth:login')
        extra_context = {
            'form': signup_form,
        }
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)


class UserListView(TemplateView):
    template_name = 'users/user_list.html'
    usernames = users.models.ProxyUser.objects.active()
    extra_context = {'usernames': usernames}


class UserDetailView(TemplateView):
    template_name = 'users/user_detail.html'

    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(
            users.models.ProxyUser.objects.active().filter(pk=user_id)
        )
        extra_context = {'user': user}
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        self.render_to_response(context)


class UnauthorizedView(TemplateView):
    template_name = 'users/unauthorized.html'


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'users/profile.html'
    data_form_class = users.forms.NameEmailForm
    profile_form = users.forms.ProfileInfoForm

    def get(self, request, *args, **kwargs):
        data_form = self.data_form_class(instance=request.user)
        profile_form = self.profile_form(instance=request.user.profile)
        extra_context = {'form': data_form, 'profile_form': profile_form}
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        data_form = users.forms.NameEmailForm(
            request.POST,
            request.FILES or None,
        )
        profile_form = users.forms.ProfileInfoForm(
            request.POST,
        )
        if all((data_form.is_valid(), profile_form.is_valid())):
            if request.FILES:
                request.user.profile.avatar = request.FILES['avatar']
            profile_form.save()
            data_form.save()
        extra_context = {'form': data_form, 'profile_form': profile_form}
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)
