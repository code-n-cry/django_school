from http import HTTPStatus

import django.urls
from django.test import Client, TestCase


class ViewTests(TestCase):
    fixtures = ["catalog_fixture.json"]

    def test_catalog_page_shows_correct_context(self):
        response = Client().get(django.urls.reverse("catalog:item_list"))
        self.assertIn("items", response.context)

    def test_existing_item_page_shows_correct_context(self):
        response = Client().get(
            django.urls.reverse("catalog:item_detail", kwargs={"pk": 1}),
        )
        self.assertIn("item", response.context)

    def test_non_existent_item_page_not_found(self):
        response = Client().get(
            django.urls.reverse("catalog:item_detail", kwargs={"pk": 0}),
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
