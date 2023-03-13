import django.urls
from django.test import Client, TestCase


class ViewTest(TestCase):
    def test_context(self):
        response = Client().get(
            django.urls.reverse('feedback:feedback'),
        )
        self.assertIn('feedback_form', response.context)

    def test_redirect(self):
        form_data = {
            'text': 'test data',
            'email': 'test@email.com',
        }
        response = Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, django.urls.reverse('about:thanks'))
