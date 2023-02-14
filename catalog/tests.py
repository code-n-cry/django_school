from http import HTTPStatus

from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    def test_catalog_endpoint(self):
        client = Client()

        with self.subTest('Catalog endpoint is accessible'):
            right_response = Client().get('/catalog/')
            self.assertEqual(right_response.status_code, HTTPStatus.OK)

        with self.subTest('Catalog/<int>/ with correct data'):
            urls = [
                '/catalog/1/',
                '/catalog/2000/',
                '/catalog/0/',
                '/catalog/010/',
                '/catalog/01/',
            ]
            for url in urls:
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.OK, msg=url)

        with self.subTest(
            'Catalog/<int>/ endpoint not work with literal data'
        ):
            urls = [
                '/catalog/hmmm/',
                '/catalog/1ab/',
                '/catalog/ab1/',
                '/catalog/1ab1/',
            ]
            for url in urls:
                self.assertEqual(client.get(url).status_code,
                                 HTTPStatus.NOT_FOUND, msg=url)

        with self.subTest(
            'Catalog/<int>/ endpoint not work with negative and float digit'
        ):
            urls = [
                '/catalog/-1/',
                '/catalog/0.0/',
                '/catalog/1.0/',
                '/catalog/0.1/',
            ]
            for url in urls:
                self.assertEqual(client.get(url).status_code,
                                 HTTPStatus.NOT_FOUND, msg=url)

        with self.subTest(
            'Catalog/<int>/ endpoint not work with special characters'
        ):
            urls = [
                '/catalog/1^/',
                '/catalog/^1/',
                '/catalog/$1/',
                '/catalog/1$/',
            ]
            for url in urls:
                self.assertEqual(client.get(url).status_code,
                                 HTTPStatus.NOT_FOUND, msg=url)

    def test_catalog_re_endpoint(self):
        client = Client()

        with self.subTest('Catalog/re/<int>/ with correct data'):
            urls = [
                '/catalog/re/1/',
                '/catalog/re/2000/',
            ]
            for url in urls:
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.OK, msg=url)

        with self.subTest(
            'Catalog/re/<int>/ endpoint not work with literal data'
        ):
            urls = [
                '/catalog/re/hmmm/',
                '/catalog/re/1ab/',
                '/catalog/re/ab1/',
                '/catalog/re/1ab1/',
            ]
            for url in urls:
                self.assertEqual(client.get(url).status_code,
                                 HTTPStatus.NOT_FOUND, msg=url)

        with self.subTest(
            'Catalog/re/<int>/ endpoint not work with non-int, non-positive'
        ):
            urls = [
                '/catalog/re/-1/',
                '/catalog/re/0.0/',
                '/catalog/re/1.0/',
                '/catalog/re/0.1/',
                '/catalog/re/0/',
                '/catalog/re/010/',
                '/catalog/re/01/',
            ]
            for url in urls:
                self.assertEqual(client.get(url).status_code,
                                 HTTPStatus.NOT_FOUND, msg=url)

        with self.subTest(
            'Catalog/re/<int>/ endpoint not work with special characters'
        ):
            urls = [
                '/catalog/re/1^/',
                '/catalog/re/^1/',
                '/catalog/re/$1/',
                '/catalog/re/1$/',
            ]
            for url in urls:
                self.assertEqual(client.get(url).status_code,
                                 HTTPStatus.NOT_FOUND, msg=url)

    def test_catalog_converter_endpoint(self):
        client = Client()

        with self.subTest('Catalog/converter/<int>/ with correct data'):
            urls = [
                '/catalog/converter/1/',
                '/catalog/converter/2000/',
            ]
            for url in urls:
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.OK, msg=url)

        with self.subTest(
            'Catalog/converter/<int>/ endpoint not work with literal data'
        ):
            urls = [
                '/catalog/converter/hmmm/',
                '/catalog/converter/1ab/',
                '/catalog/converter/ab1/',
                '/catalog/converter/1ab1/',
            ]
            for url in urls:
                self.assertEqual(client.get(url).status_code,
                                 HTTPStatus.NOT_FOUND, msg=url)

        with self.subTest(
            'Catalog/converter/<int>/ endpoint not work with non-int,'
            'non-positive'
        ):
            urls = [
                '/catalog/converter/-1/',
                '/catalog/converter/0.0/',
                '/catalog/converter/1.0/',
                '/catalog/converter/0.1/',
                '/catalog/converter/0/',
                '/catalog/converter/010/',
                '/catalog/converter/01/',
            ]
            for url in urls:
                self.assertEqual(client.get(url).status_code,
                                 HTTPStatus.NOT_FOUND, msg=url)

        with self.subTest(
            'Catalog/<int>/ endpoint not work with special characters'
        ):
            urls = [
                '/catalog/converter/1^/',
                '/catalog/converter/^1/',
                '/catalog/converter/$1/',
                '/catalog/converter/1$/',
            ]
            for url in urls:
                self.assertEqual(client.get(url).status_code,
                                 HTTPStatus.NOT_FOUND, msg=url)
