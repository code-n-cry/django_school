import django.forms

from core.forms import BootstrapForm
from users.models import Profile, User


class NameEmailForm(BootstrapForm):
    class Meta:
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
        )
        labels = {
            User.username.field.name: 'Юзернейм',
            User.email.field.name: 'E-mail',
        }
        help_texts = {
            User.username.field.name: 'Введите желаемое имя',
            User.email.field.name: 'Введите вашу почту',
        }


class SignUpForm(BootstrapForm):
    repeat_password = django.forms.CharField(
        label='Повторите пароль',
        help_text='Повторите введёный выше пароль',
        widget=django.forms.widgets.PasswordInput(),
    )

    class Meta:
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
            User.password.field.name,
        )
        labels = {
            User.username.field.name: 'Юзернейм',
            User.email.field.name: 'E-mail',
            User.password.field.name: 'Пароль',
        }
        help_texts = {
            User.username.field.name: 'Введите желаемое имя',
            User.email.field.name: 'Введите вашу почту',
            User.password.field.name: 'Введите пароль',
        }
        widgets = {
            User.password.field.name: django.forms.widgets.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirmed_password = cleaned_data['repeat_password']
        is_email_unique = User.objects.filter(
            email=cleaned_data['email']
        ).exists()
        if password != confirmed_password:
            self.add_error(
                SignUpForm.repeat_password.field.name, 'Пароли не совпадают!'
            )
        if not cleaned_data['email']:
            self.add_error(User.email.field.name, 'Укажите email!')
        if is_email_unique:
            self.add_error(
                User.email.field.name,
                'Пользователь с такой почтой уже зарегистрирован!',
            )

    def save(self, commit=True):
        cleaned_data = super().clean()
        user = User.objects.create_user(
            cleaned_data['username'],
            cleaned_data['email'],
            cleaned_data['password'],
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
            Profile.avatar.field.name: django.forms.ClearableFileInput(),
            Profile.birthday.field.name: django.forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
