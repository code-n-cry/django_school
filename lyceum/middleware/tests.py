import os

from django.http import HttpResponse
from django.test import Client, TestCase

from lyceum.middleware.middlewares import SimpleMiddleware


class StaticUrlTests(TestCase):
    def test_my_middleware(self):
        my_middleware = SimpleMiddleware(HttpResponse)

        with self.subTest('Middleware is turned on, works on all endpoints'):
            os.environ['REVERSE'] = '1'
            endpoints = [
                Client().get('/about/'),
                Client().get('/catalog/'),
                Client().get('/'),
            ]
            right_contents = [
                '<body>бО мотэ еткеорп ьтировог ёще огечен (</body>',
                '<body>косипС вотнемелэ</body>',
                '<body>яанвалГ ацинартс o_O</body>',
            ]
            for url_index in range(len(endpoints)):
                my_middleware.response_count = 9
                changed_response = my_middleware(endpoints[url_index])
                self.assertEqual(
                    changed_response.content.decode('utf-8'),
                    right_contents[url_index]
                )

        with self.subTest('Middleware is turned off, about/ endpoint'):
            os.environ['REVERSE'] = '0'
            endpoints = [
                Client().get('/about/'),
                Client().get('/catalog/'),
                Client().get('/'),
            ]
            right_contents = [
                '<body>Об этом проекте говорить ещё нечего (</body>',
                '<body>Список элементов</body>',
                '<body>Главная страница O_o</body>',
            ]
            for url_index in range(len(endpoints)):
                my_middleware.response_count = 9
                unchanged_response = my_middleware(endpoints[url_index])
                self.assertEqual(
                    unchanged_response.content.decode('utf-8'),
                    right_contents[url_index]
                )
