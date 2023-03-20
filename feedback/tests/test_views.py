import django.urls
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
import feedback.forms
import feedback.models


class ViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.personal_data_form = feedback.forms.FeedbackPersonalDataForm()
        cls.file_form = feedback.forms.FeedbackFileForm()
        cls.form = feedback.forms.FeedbackForm()
        cls.test_feedback_text = 'Test feedback text'
        cls.test_email = 'test@gmail.com'
        cls.correct_form_data = {
            'text': cls.test_feedback_text,
            'email': cls.test_email,
        }
        super().setUpClass()

    def test_correct_feedback_creation_no_file(self):
        feedback_count = feedback.models.Feedback.objects.count()
        Client().post(
            django.urls.reverse('feedback:feedback'),
            data=self.correct_form_data,
            follow=True,
        )
        self.assertTrue(
            feedback.models.PersonalData.objects.filter(
                email=self.test_email,
            ).exists()
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(), feedback_count + 1
        )

    def test_correct_feedback_creation_with_file(self):
        photo = SimpleUploadedFile(
            name='image', content=b'photo', content_type='image/png'
        )
        feedback_count = feedback.models.Feedback.objects.count()
        self.correct_form_data['uploaded_file'] = photo
        Client().post(
            django.urls.reverse('feedback:feedback'),
            data=self.correct_form_data,
            follow=True,
        )
        self.assertTrue(
            feedback.models.PersonalData.objects.filter(
                email=self.test_email,
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
