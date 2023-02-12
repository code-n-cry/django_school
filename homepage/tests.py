import os
from http import HTTPStatus

from django.http import HttpResponse
from django.test import Client, TestCase

from lyceum.middleware.middlewares import SimpleMiddleware


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

    def test_my_middleware(self):
        my_middleware = SimpleMiddleware(HttpResponse)
        
        with self.subTest('Middleware is turned on'):
            os.environ['REVERSE'] = '1'
            my_middleware.response_count = 9
            changed_response = my_middleware(Client().get('/'))
            self.assertEqual(
                changed_response.content.decode('utf-8'),
                '<body>яанвалГ ацинартс o_O</body>',
            )

        with self.subTest('Middleware is turned off'):
            os.environ['REVERSE'] = '0'
            my_middleware.response_count = 9
            changed_response = my_middleware(Client().get('/'))
            self.assertEqual(
                changed_response.content.decode('utf-8'),
                '<body>Главная страница O_o</body>',
            )
