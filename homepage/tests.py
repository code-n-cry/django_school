from django.test import TestCase, Client
import os


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint(self):
        response = Client().get('/coffee')
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.content.decode('utf-8'), 'Я чайник')
