import django.contrib.auth.models
import django.db.models

import users.models


class ActiveUserManager(django.contrib.auth.models.UserManager):
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
