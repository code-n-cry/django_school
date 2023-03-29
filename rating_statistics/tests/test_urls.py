from http import HTTPStatus

import django.urls
from django.test import Client, TestCase


class UrlTest(TestCase):
    def test_by_users_endpoint_exists(self):
        response = Client().get(django.urls.reverse('statistics:by_users'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_by_items_endpoint_exists(self):
        response = Client().get(django.urls.reverse('statistics:by_items'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_by_user_unauthorized_redirects(self):
        response = Client().get(django.urls.reverse('statistics:by_user'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
