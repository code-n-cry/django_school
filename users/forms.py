import django.forms

from core.forms import BootstrapForm
from users import models


class SignUpForm(BootstrapForm):
    repeat_password = django.forms.CharField(
        label='Повторите пароль',
        help_text='Повторите введёный выше пароль',
        widget=django.forms.widgets.PasswordInput(),
    )

    class Meta:
        model = models.User
        fields = (
            models.User.username.field.name,
            models.User.email.field.name,
            models.User.password.field.name,
        )
        labels = {
            models.User.username.field.name: 'Юзернейм',
            models.User.email.field.name: 'E-mail',
            models.User.password.field.name: 'Пароль',
        }
        help_texts = {
            models.User.username.field.name: 'Введите желаемое имя',
            models.User.email.field.name: 'Введите вашу почту',
            models.User.password.field.name: 'Введите пароль',
        }
        widgets = {
            models.User.password.field.name: django.forms.widgets.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirmed_password = cleaned_data['repeat_password']
        if password != confirmed_password:
            self.add_error(
                SignUpForm.repeat_password.field.name, 'Пароли не совпадают!'
            )
        if not cleaned_data['email']:
            self.add_error(models.User.email.field.name, 'Укажите email!')


class ProfileInfoForm(BootstrapForm):
    class Meta:
        model = models.Profile
        fields = (
            models.Profile.avatar.field.name,
            models.Profile.birthday.field.name,
        )
