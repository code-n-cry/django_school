import datetime

from django.test import Client, TestCase
from django.urls import reverse

import users.models


class ContextProcessorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        now_date = datetime.date.today()
        now_day = now_date.day
        cls.birthday_today = now_date
        cls.birthday_same_day_one_year_ago = datetime.date(
            now_date.year - 1, now_date.month, now_day
        )
        not_now_day = 28 if now_day != 28 else 29
        cls.birthday_not_this_day = datetime.date(
            now_date.year, now_date.month, not_now_day
        )
        cls.birthday_not_this_year = datetime.date(
            now_date.year + 1, now_date.month, now_day
        )
        cls.test_username = 'test'
        cls.test_password = '1234'
        cls.test_user_data = {
            'username': cls.test_username,
            'password': cls.test_password,
        }
        super().setUpClass()

    def tearDown(self):
        users.models.ProxyUser.objects.all().delete()
        users.models.Profile.objects.all().delete()
        super().tearDown()

    def test_birthday_today_in_context(self):
        test_user = users.models.ProxyUser.objects.create_user(
            username=self.test_username, password=self.test_password
        )
        users.models.Profile.objects.create(
            user=test_user, birthday=self.birthday_today
        )
        response = Client().get(reverse('homepage:index'))
        self.assertIn('birthday_persons', response.context)
        self.assertEqual(
            response.context['birthday_persons'][0]['username'],
            self.test_username,
        )

    def test_birthday_same_day_in_context(self):
        test_user = users.models.ProxyUser.objects.create_user(
            username=self.test_username, password=self.test_password
        )
        users.models.Profile.objects.create(
            user=test_user, birthday=self.birthday_same_day_one_year_ago
        )
        response = Client().get(reverse('homepage:index'))
        self.assertIn('birthday_persons', response.context)
        self.assertEqual(
            response.context['birthday_persons'][0]['username'],
            self.test_username,
        )

    def test_birthday_not_same_day_not_in_context(self):
        test_user = users.models.ProxyUser.objects.create_user(
            username=self.test_username, password=self.test_password
        )
        users.models.Profile.objects.create(
            user=test_user, birthday=self.birthday_not_this_day
        )
        response = Client().get(reverse('homepage:index'))
        self.assertFalse(
            response.context['birthday_persons'],
        )

    def test_birthday_future_year_not_in_context(self):
        test_user = users.models.ProxyUser.objects.create_user(
            username=self.test_username, password=self.test_password
        )
        users.models.Profile.objects.create(
            user=test_user, birthday=self.birthday_not_this_year
        )
        response = Client().get(reverse('homepage:index'))
        self.assertFalse(
            response.context['birthday_persons'],
        )
