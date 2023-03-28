from django.utils import timezone

import users.models


def birthday_persons(request):
    active_users_with_birthday = (
        users.models.ProxyUser.objects.active().filter(
            profile__birthday__isnull=False
        )
    )
    have_birthday_today = []
    if active_users_with_birthday:
        have_birthday_today = active_users_with_birthday.filter(
            profile__birthday__day=timezone.now().date().day,
            profile__birthday__month=timezone.now().date().month,
            profile__birthday__year__lte=timezone.now().date().year,
        ).values(
            users.models.ProxyUser.id.field.name,
            users.models.ProxyUser.username.field.name,
            users.models.ProxyUser.email.field.name,
        )
    return {'birthday_persons': have_birthday_today}
