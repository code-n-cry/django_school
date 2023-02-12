from django.test import TestCase, Client
from django.http import HttpResponse
from lyceum.middleware.middlewares import SimpleMiddleware
import os


class StaticUrlTests(TestCase):
    def test_catalog_endpoint(self):
        right_response_1 = Client().get('/catalog/')
        right_response_2 = Client().get('/catalog/1/')
        error_response_1 = Client().get('/catalog/hmmm/')
        error_response_2 = Client().get('/catalog/-1/')
        self.assertEqual(right_response_1.status_code, 200)
        self.assertEqual(right_response_2.status_code, 200)
        self.assertEqual(error_response_1.status_code, 404)
        self.assertEqual(error_response_2.status_code, 404)

    def test_catalog_re_endpoint(self):
        right_response_1 = Client().get('/catalog/re/1/')
        right_response_2 = Client().get('/catalog/re/10000/')
        error_response_1 = Client().get('/catalog/re/sleep/')
        error_response_2 = Client().get('/catalog/re/-1/')
        self.assertEqual(right_response_1.status_code, 200)
        self.assertEqual(right_response_2.status_code, 200)
        self.assertEqual(error_response_1.status_code, 404)
        self.assertEqual(error_response_2.status_code, 404)

    def test_catalog_converter_endpoint(self):
        right_response_1 = Client().get('/catalog/converter/1/')
        right_response_2 = Client().get('/catalog/converter/10000/')
        error_response_1 = Client().get('/catalog/converter/sleep/')
        error_response_2 = Client().get('/catalog/converter/-1/')
        self.assertEqual(right_response_1.status_code, 200)
        self.assertEqual(right_response_2.status_code, 200)
        self.assertEqual(error_response_1.status_code, 404)
        self.assertEqual(error_response_2.status_code, 404)

    def test_my_middleware(self):
        os.environ['REVERSE'] = '1'
        my_middleware = SimpleMiddleware(HttpResponse)
        my_middleware.response_count = 9
        changed_response = my_middleware(Client().get('/catalog/'))
        self.assertEqual(
            changed_response.content.decode('utf-8'), '<body>косипС вотнемелэ</body>'
        )
        os.environ['REVERSE'] = '0'
        my_middleware = SimpleMiddleware(HttpResponse)
        my_middleware.response_count = 9
        changed_response = my_middleware(Client().get('/catalog/'))
        self.assertEqual(
            changed_response.content.decode('utf-8'), '<body>Список элементов</body>'
        )
