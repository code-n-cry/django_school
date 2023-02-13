from http import HTTPStatus

from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    def test_catalog_endpoint(self):
        client = Client()

        with self.subTest(
            'Catalog endpoint is accessible'
        ):
            right_response = Client().get('/catalog/')
            self.assertEqual(right_response.status_code, HTTPStatus.OK)

        with self.subTest(
            'Catalog/<int>/ with correct data'
        ):
            right_responses = [
                client.get('/catalog/1/'),
                client.get('/catalog/2000/'),
                client.get('/catalog/0/'),
                client.get('/catalog/010/'),
                client.get('/catalog/01/'),
            ]
            for response in right_responses:
                self.assertEqual(response.status_code, HTTPStatus.OK)

        with self.subTest(
            'Catalog/<int>/ endpoint not work with literal data'
        ):
            wrong_responses = [
                client.get('/catalog/hmmm/'),
                client.get('/catalog/1ab/'),
                client.get('/catalog/ab1/'),
                client.get('/catalog/1ab1'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest(
            'Catalog/<int>/ endpoint not work with negative and float digit'
        ):
            wrong_responses = [
                client.get('/catalog/-1/'),
                client.get('/catalog/0.0/'),
                client.get('/catalog/1.0/'),
                client.get('/catalog/0.1/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest(
            'Catalog/<int>/ endpoint not work with special signs'
        ):
            wrong_responses = [
                client.get('/catalog/1^/'),
                client.get('/catalog/^1/'),
                client.get('/catalog/$1/'),
                client.get('/catalog/1$/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_catalog_re_endpoint(self):
        client = Client()

        with self.subTest(
            'Catalog/re/<int>/ with correct data'
        ):
            right_responses = [
                client.get('/catalog/re/1/'),
                client.get('/catalog/re/2000/'),
            ]
            for response in right_responses:
                self.assertEqual(response.status_code, HTTPStatus.OK)

        with self.subTest(
            'Catalog/re/<int>/ endpoint not work with literal data'
        ):
            wrong_responses = [
                client.get('/catalog/re/hmmm/'),
                client.get('/catalog/re/1ab/'),
                client.get('/catalog/re/ab1/'),
                client.get('/catalog/re/1ab1'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest(
            'Catalog/re/<int>/ endpoint not work with non-int, non-positive'
        ):
            wrong_responses = [
                client.get('/catalog/re/-1/'),
                client.get('/catalog/re/0.0/'),
                client.get('/catalog/re/1.0/'),
                client.get('/catalog/re/0.1/'),
                client.get('/catalog/re/0/'),
                client.get('/catalog/re/010/'),
                client.get('/catalog/re/01/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest(
            'Catalog/re/<int>/ endpoint not work with special signs'
        ):
            wrong_responses = [
                client.get('/catalog/re/1^/'),
                client.get('/catalog/re/^1/'),
                client.get('/catalog/re/$1/'),
                client.get('/catalog/re/1$/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_catalog_converter_endpoint(self):
        client = Client()

        with self.subTest(
            'Catalog/converter/<int>/ with correct data'
        ):
            right_responses = [
                client.get('/catalog/converter/1/'),
                client.get('/catalog/converter/2000/'),
            ]
            for response in right_responses:
                self.assertEqual(response.status_code, HTTPStatus.OK)

        with self.subTest(
            'Catalog/converter/<int>/ endpoint not work with literal data'
        ):
            wrong_responses = [
                client.get('/catalog/converter/hmmm/'),
                client.get('/catalog/converter/1ab/'),
                client.get('/catalog/converter/ab1/'),
                client.get('/catalog/converter/1ab1'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest(
            'Catalog/converter/<int>/ endpoint not work with non-int, non-positive'
        ):
            wrong_responses = [
                client.get('/catalog/converter/-1/'),
                client.get('/catalog/converter/0.0/'),
                client.get('/catalog/converter/1.0/'),
                client.get('/catalog/converter/0.1/'),
                client.get('/catalog/converter/0/'),
                client.get('/catalog/converter/010/'),
                client.get('/catalog/converter/01/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        with self.subTest(
            'Catalog/<int>/ endpoint not work with special signs'
        ):
            wrong_responses = [
                client.get('/catalog/converter/1^/'),
                client.get('/catalog/converter/^1/'),
                client.get('/catalog/converter/$1/'),
                client.get('/catalog/converter/1$/'),
            ]
            for response in wrong_responses:
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
