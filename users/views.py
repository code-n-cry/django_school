import datetime

import django.core.mail
import django.urls
import django.utils.timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView

import users.forms
import users.models


class ActivateNewView(View):
    http_method_names = ['get', 'head']

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
    http_method_names = ['get', 'head']

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


class SignUpView(FormView):
    form_class = users.forms.SignUpForm
    model = users.models.ProxyUser
    success_url = django.urls.reverse_lazy('auth:login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        email_text = ''.join(
            [
                'Ваша ссылка для активации:',
                django.urls.reverse(
                    'auth:activate_new',
                    kwargs={'username': form.cleaned_data['username']},
                ),
            ]
        )
        form.save()
        django.core.mail.send_mail(
            gettext_lazy('Активация'),
            email_text,
            settings.EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
        )
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, gettext_lazy('Вы уже авторизованы!'))
            return redirect('homepage:index')
        return self.render_to_response(self.get_context_data(**kwargs))


class UserListView(ListView):
    template_name = 'users/user_list.html'
    queryset = users.models.ProxyUser.objects.active()
    context_object_name = 'usernames'
    http_method_names = ['get', 'head']


class UserDetailView(DetailView):
    template_name = 'users/user_detail.html'
    queryset = users.models.ProxyUser.objects.active()
    context_object_name = 'user'
    http_method_names = ['get', 'head']


class UnauthorizedView(TemplateView):
    template_name = 'users/unauthorized.html'
    http_method_names = ['get', 'head']


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'users/profile.html'
    data_form_class = users.forms.NameEmailForm
    profile_form = users.forms.ProfileInfoForm
    http_method_names = ['get', 'head', 'post']

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
