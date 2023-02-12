import os
from http import HTTPStatus

from django.http import HttpResponse
from django.test import Client, TestCase

from lyceum.middleware.middlewares import SimpleMiddleware


class StaticUrlTests(TestCase):
    def test_about_endpoint(self):
        with self.subTest('About endpoint is accessible'):
            response = Client().get('/about/')
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_my_middleware(self):
        my_middleware = SimpleMiddleware(HttpResponse)

        with self.subTest('Middleware is turned on'):
            os.environ['REVERSE'] = '1'
            my_middleware.response_count = 9
            changed_response = my_middleware(Client().get('/about/'))
            self.assertEqual(
                changed_response.content.decode('utf-8'),
                '<body>бО мотэ еткеорп ьтировог ёще огечен (</body>',
            )

        with self.subTest('Middleware is turned off'):
            os.environ['REVERSE'] = '0'
            my_middleware.response_count = 9
            changed_response = my_middleware(Client().get('/about/'))
            self.assertEqual(
                changed_response.content.decode('utf-8'),
                '<body>Об этом проекте говорить ещё нечего (</body>',
            )
