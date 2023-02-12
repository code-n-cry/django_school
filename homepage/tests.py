from http import HTTPStatus

from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        with self.subTest('Homepage is loading'):
            response = Client().get('/')
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_endpoint(self):
        with self.subTest('Coffee endpoint returns 418 status'):
            response = Client().get('/coffee')
            self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
            self.assertEqual(response.content.decode('utf-8'), 'Я чайник')
