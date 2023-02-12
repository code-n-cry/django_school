import os
from http import HTTPStatus

from django.http import HttpResponse
from django.test import Client, TestCase

from lyceum.middleware.middlewares import SimpleMiddleware


class StaticUrlTests(TestCase):
    def test_catalog_endpoint(self):
        with self.subTest('Catalog endpoint is accessible'):
            right_response = Client().get('/catalog/')
            self.assertEqual(right_response.status_code, HTTPStatus.OK)

        with self.subTest('Catalog/<int>/ with correct data'):
            right_responses = [
                Client().get('/catalog/1/'),
                Client().get('/catalog/2000/'),
                Client().get('/catalog/0/'),
                Client().get('/catalog/010/'),
                Client().get('/catalog/01/'),
            ]
            for response in right_responses:
                self.assertEqual(response.status_code, HTTPStatus.OK)

        with self.subTest('Catalog/<int>/ endpoint not work with literal data'):
            wrong_responses = [
                Client().get('/catalog/hmmm/'),
                Client().get('/catalog/1ab/'),
                Client().get('/catalog/ab1/'),
                Client().get('/catalog/1ab1'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest('Catalog/<int>/ endpoint not work with negative and float digit'):
            wrong_responses = [
                Client().get('/catalog/-1/'),
                Client().get('/catalog/0.0/'),
                Client().get('/catalog/1.0/'),
                Client().get('/catalog/0.1/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest('Catalog/<int>/ endpoint not work with special signs'):
            wrong_responses = [
                Client().get('/catalog/1^/'),
                Client().get('/catalog/^1/'),
                Client().get('/catalog/$1/'),
                Client().get('/catalog/1$/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_catalog_re_endpoint(self):
        with self.subTest('Catalog/re/<int>/ with correct data'):
            right_responses = [
                Client().get('/catalog/re/1/'),
                Client().get('/catalog/re/2000/'),
                Client().get('/catalog/re/0/'),
                Client().get('/catalog/re/010/'),
                Client().get('/catalog/re/01/'),
            ]
            for response in right_responses:
                self.assertEqual(response.status_code, HTTPStatus.OK)

        with self.subTest('Catalog/re/<int>/ endpoint not work with literal data'):
            wrong_responses = [
                Client().get('/catalog/re/hmmm/'),
                Client().get('/catalog/re/1ab/'),
                Client().get('/catalog/re/ab1/'),
                Client().get('/catalog/re/1ab1'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest('Catalog/re/<int>/ endpoint not work with negative and float digit'):
            wrong_responses = [
                Client().get('/catalog/re/-1/'),
                Client().get('/catalog/re/0.0/'),
                Client().get('/catalog/re/1.0/'),
                Client().get('/catalog/re/0.1/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest('Catalog/re/<int>/ endpoint not work with special signs'):
            wrong_responses = [
                Client().get('/catalog/re/1^/'),
                Client().get('/catalog/re/^1/'),
                Client().get('/catalog/re/$1/'),
                Client().get('/catalog/re/1$/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_catalog_converter_endpoint(self):
        with self.subTest('Catalog/converter/<int>/ with correct data'):
            right_responses = [
                Client().get('/catalog/converter/1/'),
                Client().get('/catalog/converter/2000/'),
                Client().get('/catalog/converter/0/'),
                Client().get('/catalog/converter/010/'),
                Client().get('/catalog/converter/01/'),
            ]
            for response in right_responses:
                self.assertEqual(response.status_code, HTTPStatus.OK)

        with self.subTest('Catalog/converter/<int>/ endpoint not work with literal data'):
            wrong_responses = [
                Client().get('/catalog/converter/hmmm/'),
                Client().get('/catalog/converter/1ab/'),
                Client().get('/catalog/converter/ab1/'),
                Client().get('/catalog/converter/1ab1'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest('Catalog/converter/<int>/ endpoint not work with negative and float digit'):
            wrong_responses = [
                Client().get('/catalog/converter/-1/'),
                Client().get('/catalog/converter/0.0/'),
                Client().get('/catalog/converter/1.0/'),
                Client().get('/catalog/converter/0.1/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest('Catalog/<int>/ endpoint not work with special signs'):
            wrong_responses = [
                Client().get('/catalog/converter/1^/'),
                Client().get('/catalog/converter/^1/'),
                Client().get('/catalog/converter/$1/'),
                Client().get('/catalog/converter/1$/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_my_middleware(self):
        my_middleware = SimpleMiddleware(HttpResponse)

        with self.subTest('Middleware is turned on'):
            os.environ['REVERSE'] = '1'
            my_middleware.response_count = 9
            changed_response = my_middleware(Client().get('/catalog/'))
            self.assertEqual(
                changed_response.content.decode('utf-8'),
                '<body>косипС вотнемелэ</body>',
            )

        with self.subTest('Middleware is turned off'):
            os.environ['REVERSE'] = '0'
            my_middleware = SimpleMiddleware(HttpResponse)
            my_middleware.response_count = 9
            changed_response = my_middleware(Client().get('/catalog/'))
            self.assertEqual(
                changed_response.content.decode('utf-8'),
                '<body>Список элементов</body>',
            )
