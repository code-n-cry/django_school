from django.test import TestCase, Client
from django.http import HttpResponse
from lyceum.middleware.middlewares import SimpleMiddleware
import os


class StaticUrlTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_my_middleware(self):
        os.environ['REVERSE'] = '1'
        my_middleware = SimpleMiddleware(HttpResponse)
        my_middleware.response_count = 9
        changed_response = my_middleware(Client().get('/about/'))
        self.assertEqual(changed_response.content.decode('utf-8'), '<body>бО мотэ еткеорп ьтировог ёще огечен (</body>')
        os.environ['REVERSE'] = '0'
        my_middleware = SimpleMiddleware(HttpResponse)
        my_middleware.response_count = 9
        changed_response = my_middleware(Client().get('/about/'))
        self.assertEqual(changed_response.content.decode('utf-8'), '<body>Об этом проекте говорить ещё нечего (</body>')
