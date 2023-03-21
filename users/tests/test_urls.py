from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticUrlTest(TestCase):
    def test_signup_endpoint(self):
        response = Client().get(reverse('auth:signup'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_activate_endpoint(self):
        response = Client().get(
            reverse('auth:activate', kwargs={'username': '1'})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
