import django.contrib.auth.forms
import django.forms
import django.utils.html
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy

from core.forms import BootstrapForm
from users.models import Profile, ProxyUser


class BootstrapLoginForm(django.contrib.auth.forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class BootstrapResetPasswordForm(django.contrib.auth.forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class BootstrapChangePasswordForm(
    django.contrib.auth.forms.PasswordChangeForm
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class BootstrapSetPassword(django.contrib.auth.forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class NameEmailForm(BootstrapForm):
    class Meta:
        model = ProxyUser
        fields = (
            ProxyUser.username.field.name,
            ProxyUser.email.field.name,
        )
        labels = {
            ProxyUser.username.field.name: gettext_lazy('Юзернейм'),
            ProxyUser.email.field.name: 'E-mail',
        }
        help_texts = {
            ProxyUser.username.field.name: gettext_lazy('Измените имя'),
            ProxyUser.email.field.name: gettext_lazy('Измените почту'),
        }

    def clean_email(self):
        if self.cleaned_data['email']:
            is_email_unique = ProxyUser.objects.filter(
                ~Q(pk=self.instance.id), email=self.cleaned_data['email']
            ).exists()
            if is_email_unique:
                raise ValidationError(
                    gettext_lazy(
                        'Пользователь с такой почтой уже зарегистрирован!'
                    )
                )
            return ProxyUser.objects.normalize_email(
                self.cleaned_data['email']
            )
        raise ValidationError(
            gettext_lazy('Введите новый email или оставьте старый!')
        )


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        if not self.cleaned_data['email']:
            return self.add_error(
                ProxyUser.email.field.name, gettext_lazy('Укажите email!')
            )
        normalized_email = ProxyUser.objects.normalize_email(
            self.cleaned_data['email']
        )
        is_email_unique = ProxyUser.objects.filter(
            email=normalized_email
        ).exists()
        if is_email_unique:
            return self.add_error(
                ProxyUser.email.field.name,
                gettext_lazy(
                    'Пользователь с такой почтой уже зарегистрирован!'
                ),
            )
        return normalized_email

    def save(self, commit: bool = True):
        cleaned_data = super().clean()
        user = ProxyUser.objects.create_user(
            cleaned_data['username'],
            cleaned_data['email'],
            cleaned_data['password1'],
            is_active=settings.USER_ACTIVE_DEFAULT,
        )
        users_profile = Profile.objects.create(user=user)
        return user, users_profile

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = ProxyUser
        fields = (
            ProxyUser.username.field.name,
            ProxyUser.email.field.name,
        )
        labels = {
            ProxyUser.username.field.name: gettext_lazy('Юзернейм'),
            ProxyUser.email.field.name: 'E-mail',
            ProxyUser.password.field.name: gettext_lazy('Пароль'),
        }
        help_texts = {
            ProxyUser.email.field.name: gettext_lazy('Обязательное поле.'),
        }


class ProfileInfoForm(BootstrapForm):
    class Meta:
        model = Profile
        fields = (
            Profile.avatar.field.name,
            Profile.birthday.field.name,
        )
        labels = {
            Profile.avatar.field.name: gettext_lazy('Аватарка'),
            Profile.birthday.field.name: gettext_lazy('День рождения'),
        }
        help_texts = {
            Profile.avatar.field.name: gettext_lazy(
                'Загрузите аватарку(если хотите)'
            ),
            Profile.birthday.field.name: gettext_lazy(
                'Укажите день рождения(если хотите)'
            ),
        }
        widgets = {
            Profile.birthday.field.name: django.forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
