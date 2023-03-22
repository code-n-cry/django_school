import django.core.mail
import django.utils.timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(
                Q(email=username) | Q(username=username)
            )
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(
                user
            ):
                user.profile.failed_logins = 0
                user.profile.save()
                return user
            if not user.check_password(password):
                user.profile.failed_logins += 1
                user.profile.last_failed_login_date = (
                    django.utils.timezone.now()
                )
                user.profile.save()
                if user.profile.failed_logins >= settings.MAX_LOGIN_AMOUNT:
                    user.is_active = False
                    user.save()
                    email_text = ''.join(
                        [
                            'Совершено много неудачных попыток входа в Ваш'
                            'аккаунт! Для безопасности он был отключён.\n',
                            'Ваша ссылка для восстановления:'
                            'http://127.0.0.0:8000',
                            django.urls.reverse(
                                'auth:recover',
                                kwargs={'username': user.get_username()},
                            ),
                        ]
                    )
                    django.core.mail.send_mail(
                        'Восстановление'.encode('utf-8'),
                        email_text,
                        settings.EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
        return None
