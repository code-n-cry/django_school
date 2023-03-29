import django.urls
from django.test import Client, TestCase


class ViewTest(TestCase):
    def test_by_users_context(self):
        response = Client().get(django.urls.reverse('statistics:by_users'))
        self.assertIn('object_list', response.context)

    def test_by_items_context(self):
        response = Client().get(django.urls.reverse('statistics:by_items'))
        self.assertIn('object_list', response.context)

    def unauthorized_by_user_not_allowed(self):
        response = Client().get(django.urls.reverse('statistics:by_user'))
        self.assertRedirects(response, django.urls('auth:login'))
