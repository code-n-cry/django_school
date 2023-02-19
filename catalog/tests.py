from http import HTTPStatus

import django.core.exceptions
import django.db.utils
from django.test import Client, TestCase

import catalog.models


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
                    client.get(url).status_code, HTTPStatus.OK, msg=url
                )

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
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.NOT_FOUND, msg=url
                )

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
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.NOT_FOUND, msg=url
                )

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
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.NOT_FOUND, msg=url
                )

    def test_catalog_re_endpoint(self):
        client = Client()

        with self.subTest('Catalog/re/<int>/ with correct data'):
            urls = [
                '/catalog/re/1/',
                '/catalog/re/2000/',
            ]
            for url in urls:
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.OK, msg=url
                )

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
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.NOT_FOUND, msg=url
                )

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
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.NOT_FOUND, msg=url
                )

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
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.NOT_FOUND, msg=url
                )

    def test_catalog_converter_endpoint(self):
        client = Client()

        with self.subTest('Catalog/converter/<int>/ with correct data'):
            urls = [
                '/catalog/converter/1/',
                '/catalog/converter/2000/',
            ]
            for url in urls:
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.OK, msg=url
                )

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
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.NOT_FOUND, msg=url
                )

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
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.NOT_FOUND, msg=url
                )

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
                self.assertEqual(
                    client.get(url).status_code, HTTPStatus.NOT_FOUND, msg=url
                )


class DataBaseTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name='Test category',
            slug='test-category-slug',
        )
        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name='Test tag',
            slug='test-tag-slug',
        )
        cls.item_count = catalog.models.Item.objects.count()
        cls.category_count = catalog.models.Category.objects.count()
        cls.tags_count = catalog.models.Tag.objects.count()
        return super().setUpClass()

    def test_valid_item(self):
        with self.subTest('Create valid item'):
            self.item = catalog.models.Item(
                name='Test item',
                catalog_category=self.category,
                text='Some !роскошно! text',
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
            self.assertEqual(
                catalog.models.Item.objects.count(),
                self.item_count + 1,
            )

    def test_invalid_item(self):
        with self.subTest('No keywords in item`s description'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.item = catalog.models.Item(
                    name='Invalid test item',
                    catalog_category=self.category,
                    text='Some text',
                )
                self.item.full_clean()
                self.item.save()
                self.item.tags.add(self.tag)

            self.assertEqual(
                catalog.models.Item.objects.count(),
                self.item_count,
            )

        with self.subTest('Too short description'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.item = catalog.models.Item(
                    name='Invalid test item',
                    catalog_category=self.category,
                    text='.',
                )
                self.item.full_clean()
                self.item.save()
                self.item.tags.add(self.tag)

            self.assertEqual(
                catalog.models.Item.objects.count(),
                self.item_count,
            )

        with self.subTest('No name'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.item = catalog.models.Item(
                    catalog_category=self.category,
                    text='Превосходно',
                )
                self.item.full_clean()
                self.item.save()
                self.item.tags.add(self.tag)

            self.assertEqual(
                catalog.models.Item.objects.count(),
                self.item_count,
            )

        with self.subTest('No category'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.item = catalog.models.Item(
                    text='Превосходно',
                )
                self.item.full_clean()
                self.item.save()
                self.item.tags.add(self.tag)

            self.assertEqual(
                catalog.models.Item.objects.count(),
                self.item_count,
            )

        with self.subTest('No tags'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.item = catalog.models.Item(
                    catalog_category=self.category,
                    text='Превосходно',
                )
                self.item.full_clean()
                self.item.save()

            self.assertEqual(
                catalog.models.Item.objects.count(),
                self.item_count,
            )

    def test_valid_category(self):
        with self.subTest('Create valid category'):
            self.category = catalog.models.Category.objects.create(
                name='Test category',
                slug='new-test-category-slug',
            )
            self.category.full_clean()
            self.category.save()
            self.assertEqual(
                catalog.models.Category.objects.count(),
                self.category_count + 1,
            )

    def test_invalid_category(self):
        with self.subTest('Invalud slug'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.category = catalog.models.Category.objects.create(
                    name='Test category',
                    slug='FffF-__инвалидслаг$$$__--FF',
                )
                self.category.full_clean()
                self.category.save()

        with self.subTest('No name'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.category = catalog.models.Category.objects.create(
                    slug='new-test-slug-3'
                )
                self.category.full_clean()
                self.category.save()

        with self.subTest('Negative weight'):
            with self.assertRaises(django.db.utils.IntegrityError):
                self.category = catalog.models.Category.objects.create(
                    name='Test category',
                    slug='test-slug-4',
                    weight=-1,
                )
                self.category.full_clean()
                self.category.save()

    def test_valid_tag(self):
        with self.subTest('Create valid tag'):
            self.tag = catalog.models.Tag.objects.create(
                name='Test tag',
                slug='new-test-tag-slug',
            )
            self.tag.full_clean()
            self.tag.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                self.tags_count + 1,
            )

    def test_invalid_tag(self):
        with self.subTest('Invalid slug'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.tag = catalog.models.Tag.objects.create(
                    name='Test tag',
                    slug='$.!.()())))((((я хочу спать))))',
                )
                self.tag.full_clean()
                self.tag.save()

        with self.subTest('No name'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.tag = catalog.models.Tag.objects.create(
                    slug='new-test-tag-slug',
                )
                self.tag.full_clean()
                self.tag.save()
