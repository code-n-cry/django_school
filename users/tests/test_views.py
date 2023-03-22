from http import HTTPStatus

import django.db.utils
import django.urls
import mock
import pytz
from django.test import Client, TestCase, override_settings
from django.utils import timezone

import users.forms
import users.models


class ViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.signup_form = users.forms.SignUpForm()
        cls.profile_form = users.forms.ProfileInfoForm()
        cls.name_email_form = users.forms.NameEmailForm()
        cls.test_username = 'test_username'
        cls.test_email = 'test@email.com'
        cls.test_password = 'testpassword1'
        cls.correct_signup_data = {
            'username': cls.test_username,
            'email': cls.test_email,
            'password': cls.test_password,
            'repeat_password': cls.test_password,
        }
        super().setUpClass()

    def tearDown(self):
        users.models.Profile.objects.all().delete()
        users.models.ProxyUser.objects.all().delete()
        super().tearDown()

    def test_signup_context(self):
        response = Client().get(
            django.urls.reverse('auth:signup'),
        )
        self.assertIn('signup_form', response.context)

    def test_profile_context(self):
        client = Client()
        test_user = users.models.ProxyUser.objects.create_user(
            username=self.test_username, password=self.test_password
        )
        users.models.Profile.objects.create(user=test_user)
        client.login(username=self.test_username, password=self.test_password)
        response = client.get(
            django.urls.reverse('users:profile'),
        )
        self.assertIn('data_form', response.context)
        self.assertIn('profile_form', response.context)

    def test_no_user_no_profile(self):
        response = Client().get(
            django.urls.reverse('users:profile'),
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_correct_signup(self):
        users_count = users.models.ProxyUser.objects.count()
        Client().post(
            django.urls.reverse('auth:signup'),
            data=self.correct_signup_data,
            follow=True,
        )
        self.assertTrue(
            users.models.ProxyUser.objects.filter(
                email=self.test_email,
            ).exists()
        )
        self.assertEqual(
            users.models.ProxyUser.objects.count(), users_count + 1
        )

    def test_signup_no_username(self):
        users_count = users.models.ProxyUser.objects.count()
        invalid_signup_data = {
            'email': self.test_email,
            'password': self.test_password,
            'repeat_password': self.test_password,
        }
        Client().post(
            django.urls.reverse('auth:signup'),
            data=invalid_signup_data,
            follow=True,
        )
        self.assertFalse(
            users.models.ProxyUser.objects.filter(
                email=self.test_email,
            ).exists()
        )
        self.assertEqual(users.models.ProxyUser.objects.count(), users_count)

    def test_signup_no_email(self):
        users_count = users.models.ProxyUser.objects.count()
        invalid_signup_data = {
            'username': self.test_username,
            'password': self.test_password,
            'repeat_password': self.test_password,
        }
        Client().post(
            django.urls.reverse('auth:signup'),
            data=invalid_signup_data,
            follow=True,
        )
        self.assertEqual(users.models.ProxyUser.objects.count(), users_count)

    def test_signup_passwords_dont_match(self):
        users_count = users.models.ProxyUser.objects.count()
        invalid_signup_data = {
            'username': self.test_username,
            'email': self.test_email,
            'password': self.test_password,
            'repeat_password': self.test_password + 's',
        }
        Client().post(
            django.urls.reverse('auth:signup'),
            data=invalid_signup_data,
            follow=True,
        )
        self.assertEqual(users.models.ProxyUser.objects.count(), users_count)

    def test_signup_with_not_unique_email(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.correct_signup_data,
            follow=True,
        )
        users_count = users.models.ProxyUser.objects.count()
        new_signup_data = {
            'username': self.test_username + 's',
            'email': self.test_email,
            'password': self.test_password,
            'repeat_password': self.test_password,
        }
        client.post(
            django.urls.reverse('auth:signup'),
            data=new_signup_data,
            follow=True,
        )
        self.assertEqual(users.models.ProxyUser.objects.count(), users_count)

    @override_settings(USER_ACTIVE_DEFAULT=False)
    def test_activate_works_for_new_user(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.correct_signup_data,
            follow=True,
        )
        client.get(
            django.urls.reverse(
                'auth:activate', kwargs={'username': self.test_username}
            )
        )
        self.assertTrue(
            users.models.ProxyUser.objects.filter(username=self.test_username)
            .first()
            .is_active
        )

    @override_settings(USER_ACTIVE_DEFAULT=False)
    @mock.patch('django.utils.timezone.now')
    def test_activate_doesnt_work_within_twelve_hours(self, mock_now):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.correct_signup_data,
            follow=True,
        )
        utc = pytz.UTC
        mock_now.return_value = utc.localize(timezone.datetime(2024, 4, 1))
        client.get(
            django.urls.reverse(
                'auth:activate', kwargs={'username': self.test_username}
            )
        )
        self.assertFalse(
            users.models.ProxyUser.objects.filter(username=self.test_username)
            .first()
            .is_active
        )

    def test_login_with_username(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.correct_signup_data,
            follow=True,
        )
        credentials = {
            'username': self.test_username,
            'password': self.test_password,
        }
        response = client.post(
            django.urls.reverse('auth:login'),
            data=credentials,
            follow=True,
        )
        self.assertTrue(response.context['user'].is_active)

    def test_login_with_email(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.correct_signup_data,
            follow=True,
        )
        credentials = {
            'username': self.test_email,
            'password': self.test_password,
        }
        response = client.post(
            django.urls.reverse('auth:login'),
            data=credentials,
            follow=True,
        )
        self.assertTrue(response.context['user'].is_active)
