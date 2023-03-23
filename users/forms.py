import django.contrib.auth.forms
import django.forms
import django.utils.html
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q

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
            ProxyUser.username.field.name: 'Юзернейм',
            ProxyUser.email.field.name: 'E-mail',
        }
        help_texts = {
            ProxyUser.username.field.name: 'Измените имя',
            ProxyUser.email.field.name: 'Измените почту',
        }

    def clean_email(self):
        if self.cleaned_data['email']:
            is_email_unique = ProxyUser.objects.filter(
                ~Q(pk=self.instance.id), email=self.cleaned_data['email']
            ).exists()
            if is_email_unique:
                raise ValidationError(
                    'Пользователь с такой почтой уже зарегистрирован!'
                )
            return ProxyUser.objects.normalize_email(
                self.cleaned_data['email']
            )
        raise ValidationError('Введите новый email или оставьте старый!')


class SignUpForm(BootstrapForm):
    repeat_password = django.forms.CharField(
        label='Повторите пароль',
        help_text='Повторите введёный выше пароль',
        widget=django.forms.widgets.PasswordInput(),
    )

    class Meta:
        model = ProxyUser
        fields = (
            ProxyUser.username.field.name,
            ProxyUser.email.field.name,
            ProxyUser.password.field.name,
        )
        labels = {
            ProxyUser.username.field.name: 'Юзернейм',
            ProxyUser.email.field.name: 'E-mail',
            ProxyUser.password.field.name: 'Пароль',
        }
        help_texts = {
            ProxyUser.username.field.name: 'Введите желаемое имя',
            ProxyUser.email.field.name: 'Введите вашу почту',
            ProxyUser.password.field.name: 'Введите пароль',
        }
        widgets = {
            'password': django.forms.widgets.PasswordInput(),
        }

    def clean_username(self):
        if 'username' not in self.cleaned_data.keys():
            return self.add_error(
                ProxyUser.username.field.name, 'Введите имя пользователя!'
            )
        return self.cleaned_data['username']

    def clean_repeat_password(self):
        password = self.cleaned_data['password']
        confirmed_password = self.cleaned_data['repeat_password']
        if password != confirmed_password:
            return self.add_error('repeat_password', 'Пароли не совпадают!')
        return confirmed_password

    def clean_email(self):
        if not self.cleaned_data['email']:
            return self.add_error(ProxyUser.email.field.name, 'Укажите email!')
        normalized_email = ProxyUser.objects.normalize_email(
            self.cleaned_data['email']
        )
        is_email_unique = ProxyUser.objects.filter(
            email=normalized_email
        ).exists()
        if is_email_unique:
            return self.add_error(
                ProxyUser.email.field.name,
                'Пользователь с такой почтой уже зарегистрирован!',
            )
        return normalized_email

    def save(self, commit=True):
        cleaned_data = super().clean()
        user = ProxyUser.objects.create_user(
            cleaned_data['username'],
            cleaned_data['email'],
            cleaned_data['password'],
            is_active=settings.USER_ACTIVE_DEFAULT,
        )
        users_profile = Profile.objects.create(user=user)
        return user, users_profile


class ProfileInfoForm(BootstrapForm):
    class Meta:
        model = Profile
        fields = (
            Profile.avatar.field.name,
            Profile.birthday.field.name,
        )
        labels = {
            Profile.avatar.field.name: 'Аватарка',
            Profile.birthday.field.name: 'День рождения',
        }
        help_texts = {
            Profile.avatar.field.name: 'Загрузите аватарку(если хотите)',
            Profile.birthday.field.name: 'Укажите день рождения(если хотите)',
        }
        widgets = {
            Profile.birthday.field.name: django.forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
