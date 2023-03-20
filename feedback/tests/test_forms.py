from django.test import TestCase

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
