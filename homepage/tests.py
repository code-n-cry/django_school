from django.test import TestCase, Client
from django.http import HttpResponse
import os
from lyceum.middleware.middlewares import SimpleMiddleware


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint(self):
        response = Client().get('/coffee')
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.content.decode('utf-8'), 'Я чайник')

    def test_my_middleware(self):
        os.environ['REVERSE'] = '1'
        my_middleware = SimpleMiddleware(HttpResponse)
        my_middleware.response_count = 9
        changed_response = my_middleware(Client().get('/'))
        self.assertEqual(
            changed_response.content.decode('utf-8'),
            '<body>яанвалГ ацинартс o_O</body>'
        )
        os.environ['REVERSE'] = '0'
        my_middleware = SimpleMiddleware(HttpResponse)
        my_middleware.response_count = 9
        changed_response = my_middleware(Client().get('/'))
        self.assertEqual(
            changed_response.content.decode('utf-8'),
            '<body>Главная страница O_o</body>'
        )
