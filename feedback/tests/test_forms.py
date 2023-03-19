import django.urls
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

import feedback.forms
import feedback.models


class FormTest(TestCase):
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

    def test_labels(self):
        email_label = self.personal_data_form.fields['email'].label
        text_label = self.form['text'].label
        file_label = self.file_form['uploaded_file'].label
        self.assertEqual(email_label, 'E-Mail')
        self.assertEqual(text_label, 'Содержание обращения')
        self.assertEqual(
            file_label, 'Файлы для подробного описания(если хотите)'
        )

    def test_help_texts(self):
        email_help_text = self.personal_data_form.fields['email'].help_text
        text_help_text = self.form['text'].help_text
        file_help_text = self.file_form['uploaded_file'].help_text
        self.assertEqual(email_help_text, 'Ваша почта')
        self.assertEqual(text_help_text, 'Опишите проблему')
        self.assertEqual(file_help_text, 'Прикрепите файлы')
