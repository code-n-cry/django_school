from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticUrlTest(TestCase):
    def test_signup_endpoint(self):
        response = Client().get(reverse('auth:signup'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recover_endpoint(self):
        response = Client().get(
            reverse('auth:recover', kwargs={'username': '1'})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_activate_new_endpoint(self):
        response = Client().get(
            reverse('auth:activate_new', kwargs={'username': '1'})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_list_endpoint(self):
        response = Client().get(reverse('users:user_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_endpoint(self):
        response = Client().get(reverse('users:profile'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
