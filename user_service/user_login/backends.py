from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

USER = get_user_model()


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(USER.USERNAME_FIELD)

        case_insensitive_username_field = '{}__iexact'.format(USER.USERNAME_FIELD)
        users = USER._default_manager.filter(
            Q(**{case_insensitive_username_field: username}) | Q(email__iexact=username) | Q(mobile_number__iexact=username)
        )

        for user in users:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        if not users:
            USER().set_password(password)
