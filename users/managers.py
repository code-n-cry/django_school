import django.contrib.auth.models
import django.db.models

import users.models


class ActiveUserManager(django.contrib.auth.models.UserManager):
    @classmethod
    def normalize_email(cls, email):
        email = email or ''
        try:
            username, domain = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            username_no_tags = username.split('+')[0].lower()
            if domain.lower() in ['yandex.ru', 'ya.ru']:
                username_no_tags = username_no_tags.replace('.', '-')
                domain = 'yandex.ru'
            if domain.lower() == 'gmail.com':
                username_no_tags = username_no_tags.replace('.', '')
            email = '@'.join([username_no_tags, domain.lower()])
        return email

    def active(self):
        return (
            self.get_queryset()
            .filter(
                is_active=True,
            )
            .select_related(
                users.models.ProxyUser.profile.related.related_name
            )
            .only(
                users.models.ProxyUser.pk.field.name,
                users.models.ProxyUser.username.field.name,
                users.models.ProxyUser.email.field.name,
                '__'.join(
                    [
                        users.models.ProxyUser.profile.field.name,
                        users.models.Profile.birthday.field.name,
                    ]
                ),
                '__'.join(
                    [
                        users.models.ProxyUser.profile.field.name,
                        users.models.Profile.avatar.field.name,
                    ]
                ),
                '__'.join(
                    [
                        users.models.ProxyUser.profile.field.name,
                        users.models.Profile.coffee_count.field.name,
                    ]
                ),
            )
            .order_by(users.models.ProxyUser.username.field.name)
        )
