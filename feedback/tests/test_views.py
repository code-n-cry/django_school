import django.urls
from django.test import Client, TestCase

import feedback.forms
import feedback.models


class ViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.form = feedback.forms.FeedbackForm()
        cls.test_feedback_text = 'Test feedback text'
        cls.test_email = 'test@gmail.com'
        cls.correct_form_data = {
            'text': cls.test_feedback_text,
            'email': cls.test_email,
        }
        super().setUpClass()

    def test_redirect(self):
        form_data = {
            'text': self.test_feedback_text,
            'email': self.test_email,
        }
        response = Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, django.urls.reverse('about:thanks'))

    def test_correct_feedback_creation(self):
        feedback_count = feedback.models.Feedback.objects.count()
        Client().post(
            django.urls.reverse('feedback:feedback'),
            data=self.correct_form_data,
            follow=True,
        )
        self.assertTrue(
            feedback.models.Feedback.objects.filter(
                text=self.test_feedback_text,
            ).exists()
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(), feedback_count + 1
        )

    def test_invalid_text_feedback_creation(self):
        feedback_count = feedback.models.Feedback.objects.count()
        form_data = {
            'text': '',
            'email': self.test_email,
        }
        Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(), feedback_count
        )

    def test_invalid_email_feedback_creation(self):
        feedback_count = feedback.models.Feedback.objects.count()
        form_data = {
            'text': self.test_feedback_text,
            'email': 'examplegmail.com',
        }
        Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(), feedback_count
        )

    def test_labels(self):
        text_label = self.form.fields['text'].label
        email_label = self.form.fields['email'].label
        self.assertEqual(text_label, 'Содержание обращения')
        self.assertEqual(email_label, 'E-Mail')

    def test_help_texts(self):
        text_help_text = self.form.fields['text'].help_text
        email_help_text = self.form.fields['email'].help_text
        self.assertEqual(
            text_help_text,
            'Опишите проблему',
        )
        self.assertEqual(email_help_text, 'Ваша почта')

    def test_context(self):
        response = Client().get(
            django.urls.reverse('feedback:feedback'),
        )
        self.assertIn('feedback_form', response.context)
