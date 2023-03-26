from http import HTTPStatus

from django.test import Client, TestCase


class StaticUrlTest(TestCase):
    def test_feedback_endpoint(self):
        right_response = Client().get('/feedback/')
        self.assertEqual(right_response.status_code, HTTPStatus.OK)
