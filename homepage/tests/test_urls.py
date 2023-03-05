from http import HTTPStatus

import django.db.models.fields.related_descriptors
import django.urls
from django.test import Client, TestCase

import catalog.models


class StaticUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = catalog.models.Category.objects.create(
            is_published=True,
            name='Тестовая категория',
            slug='published_test_category',
        )
        cls.unpublished_category = catalog.models.Category.objects.create(
            is_published=False,
            name='Тестовая категория(неопубликована)',
            slug='unpublished_test_category',
        )
        cls.published_tag = catalog.models.Tag.objects.create(
            is_published=True,
            name='Тестовый тег',
            slug='published_test_tag',
        )
        cls.unpublished_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name='Тестовый тег(неопубликованный)',
            slug='unpublished_test_tag',
        )

        cls.published_category.save()
        cls.unpublished_category.save()

        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.published_item = catalog.models.Item.objects.create(
            is_published=True,
            is_on_main=True,
            name='Тестовый товар',
            category=cls.published_category,
        )
        cls.unpublished_item = catalog.models.Item.objects.create(
            is_published=False,
            is_on_main=True,
            name='Тестовый товар(неопубликованный)',
            category=cls.published_category,
        )

        cls.published_item.clean()
        cls.published_item.save()
        cls.published_item.tags.add(cls.published_tag)
        cls.published_item.tags.add(cls.unpublished_tag)

        cls.unpublished_item.clean()
        cls.unpublished_item.save()

        super().setUpClass()

    def tearDown(self):
        self.category = catalog.models.Category.objects.all().delete()
        self.item = catalog.models.Item.objects.all().delete()
        self.tag = catalog.models.Tag.objects.all().delete()
        super().tearDown()

    def test_home_page_shows_correct_context(self):
        response = Client().get(django.urls.reverse('homepage:index'))
        self.assertIn('items', response.context)

    def test_coffee_endpoint_status(self):
        with self.subTest('Coffee endpoint returns 418 status'):
            response = Client().get('/coffee/')
            self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_endpoint_content(self):
        with self.subTest('Coffee endpoint returns "Я чайник"'):
            response = Client().get('/coffee/')
            self.assertEqual(response.content.decode('utf-8'), 'Я чайник')
