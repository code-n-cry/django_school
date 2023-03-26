from django.test import TestCase

from users.managers import ActiveUserManager


class ManagerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_username = 'username'
        cls.yandex_domain_long = '@yandex.ru'
        cls.yandex_domain_short = '@ya.ru'
        cls.google_domain = '@gmail.com'
        super().setUpClass()

    def test_ignore_tags(self):
        test_tags = ['+tag', '+test']
        self.assertEqual(
            ActiveUserManager.normalize_email(
                self.test_username
                + ''.join(test_tags)
                + self.yandex_domain_long,
            ),
            self.test_username + self.yandex_domain_long,
        )
        self.assertEqual(
            ActiveUserManager.normalize_email(
                self.test_username + ''.join(test_tags) + self.google_domain,
            ),
            self.test_username + self.google_domain,
        )

    def test_no_register(self):
        self.assertEqual(
            ActiveUserManager.normalize_email(
                self.test_username.upper() + self.yandex_domain_long.upper()
            ),
            self.test_username + self.yandex_domain_long,
        )

    def test_canonize_yandex_domen(self):
        self.assertEqual(
            ActiveUserManager.normalize_email(
                self.test_username + self.yandex_domain_short
            ),
            ActiveUserManager.normalize_email(
                self.test_username + self.yandex_domain_long
            ),
        )

    def test_dots_replacing_yandex_domen(self):
        test_mail_username = 'example.test.email'
        self.assertEqual(
            ActiveUserManager.normalize_email(
                test_mail_username + self.yandex_domain_long
            ),
            test_mail_username.replace('.', '-') + self.yandex_domain_long,
        )

    def test_gmail_ignore_dots(self):
        test_mail_username = 'example.test.email'
        self.assertEqual(
            ActiveUserManager.normalize_email(
                test_mail_username + self.google_domain
            ),
            test_mail_username.replace('.', '') + self.google_domain,
        )
