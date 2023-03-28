from django.test import TestCase

import users.forms
import users.models


class FormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.signup_form = users.forms.SignUpForm()
        cls.profile_form = users.forms.ProfileInfoForm()
        super().setUpClass()

    def test_labels(self):
        email_label = self.signup_form.fields['email'].label
        username_label = self.signup_form.fields['username'].label
        password_label = self.signup_form.fields['password1'].label
        repeat_password_label = self.signup_form.fields['password2'].label
        birthday_label = self.profile_form['birthday'].label
        avatar_label = self.profile_form['avatar'].label
        self.assertEqual(email_label, 'E-mail')
        self.assertEqual(username_label, 'Юзернейм')
        self.assertEqual(password_label, 'Пароль')
        self.assertEqual(repeat_password_label, 'Подтверждение пароля')
        self.assertEqual(birthday_label, 'День рождения')
        self.assertEqual(avatar_label, 'Аватарка')

    def test_help_texts(self):
        email_help_text = self.signup_form.fields['email'].help_text
        username_help_text = self.signup_form.fields['username'].help_text
        password_help_text = self.signup_form.fields['password1'].help_text
        repeat_password_help_text = self.signup_form.fields[
            'password2'
        ].help_text
        birthday_help_text = self.profile_form['birthday'].help_text
        avatar_help_text = self.profile_form['avatar'].help_text
        self.assertEqual(email_help_text, 'Обязательное поле.')
        self.assertEqual(
            username_help_text,
            (
                'Обязательное поле. Не более 150 символов. Только буквы, '
                'цифры и символы @/./+/-/_.'
            ),
        )
        self.assertEqual(
            password_help_text,
            (
                '<ul><li>Пароль не должен быть слишком похож на другую вашу '
                'личную информацию.</li><li>Ваш пароль должен содержать как '
                'минимум 8 символов.</li><li>Пароль не должен быть слишком '
                'простым и распространенным.</li><li>Пароль не может '
                'состоять только из цифр.</li></ul>'
            ),
        )
        self.assertEqual(
            repeat_password_help_text,
            'Для подтверждения введите, пожалуйста, пароль ещё раз.',
        )
        self.assertEqual(
            birthday_help_text, 'Укажите день рождения(если хотите)'
        )
        self.assertEqual(avatar_help_text, 'Загрузите аватарку(если хотите)')
