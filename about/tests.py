from http import HTTPStatus

from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    def test_about_endpoint(self):
        with self.subTest(
            'About endpoint is accessible'
        ):
            response = Client().get('/about/')
            self.assertEqual(response.status_code, HTTPStatus.OK)
