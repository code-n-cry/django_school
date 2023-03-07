from http import HTTPStatus

import django.urls
from django.test import Client, TestCase

import catalog.models


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = catalog.models.Category.objects.create(
            is_published=True,
            name='Опубликованная тестовая категория',
            slug='published_category',
        )
        cls.unpublished_category = catalog.models.Category.objects.create(
            is_published=False,
            name='Неопубликованная тестовая категория',
            slug='unpublished_category',
        )
        cls.published_tag = catalog.models.Tag.objects.create(
            is_published=True,
            name='Опубликованный тестовый тег',
            slug='published_tag',
        )
        cls.unpublished_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name='Неопубликованный тестовый тег',
            slug='unpublished_tag',
        )

        cls.published_category.save()
        cls.unpublished_category.save()

        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.published_item = catalog.models.Item.objects.create(
            is_published=True,
            is_on_main=True,
            name='Опубликованный товар',
            category=cls.published_category,
        )
        cls.published_item_with_unpublished_category = (
            catalog.models.Item.objects.create(
                is_published=True,
                is_on_main=True,
                name='Опубликованный товар с неопубликованной категорией',
                category=cls.unpublished_category,
            )
        )
        cls.unpublished_item = catalog.models.Item.objects.create(
            is_published=False,
            is_on_main=True,
            name='Неопубликованный товар',
            category=cls.published_category,
        )

        cls.published_item.clean()
        cls.published_item.save()
        cls.published_item.tags.add(cls.published_tag)
        cls.published_item.tags.add(cls.unpublished_tag)

        cls.unpublished_item.clean()
        cls.unpublished_item.save()

        cls.published_item_with_unpublished_category.clean()
        cls.published_item_with_unpublished_category.save()
        cls.published_item_with_unpublished_category.tags.add(
            cls.published_tag
        )

        super().setUpClass()

    def tearDown(self):
        catalog.models.Category.objects.all().delete()
        catalog.models.Item.objects.all().delete()
        catalog.models.Tag.objects.all().delete()
        super().tearDown()

    def test_catalog_page_shows_correct_context(self):
        response = Client().get(django.urls.reverse('catalog:item_list'))
        self.assertIn('items', response.context)

    def test_existing_item_page_shows_correct_context(self):
        response = Client().get(
            django.urls.reverse('catalog:item_detail', kwargs={'number': 1}),
        )
        self.assertIn('item', response.context)

    def test_non_existent_item_page_not_found(self):
        response = Client().get(
            django.urls.reverse('catalog:item_detail', kwargs={'number': 0}),
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
