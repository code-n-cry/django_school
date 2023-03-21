import django.forms
import django.utils.html
from django.conf import settings
from django.db.models import Q

from core.forms import BootstrapForm
from users.models import Profile, ProxyUser


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

    def clean(self):
        is_email_unique = ProxyUser.objects.filter(
            ~Q(pk=self.instance.id), email=self.cleaned_data['email']
        ).exists()
        if is_email_unique:
            self.add_error(
                ProxyUser.email.field.name,
                'Пользователь с такой почтой уже зарегистрирован!',
            )


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
            ProxyUser.password.field.name: django.forms.widgets.PasswordInput(),
        }

    def clean(self):
        password = self.cleaned_data['password']
        confirmed_password = self.cleaned_data['repeat_password']
        is_email_unique = ProxyUser.objects.filter(
            email=self.cleaned_data['email']
        ).exists()
        if password != confirmed_password:
            self.add_error('repeat_password', 'Пароли не совпадают!')
        if not self.cleaned_data['email']:
            self.add_error(ProxyUser.email.field.name, 'Укажите email!')
        if is_email_unique:
            self.add_error(
                ProxyUser.email.field.name,
                'Пользователь с такой почтой уже зарегистрирован!',
            )

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
