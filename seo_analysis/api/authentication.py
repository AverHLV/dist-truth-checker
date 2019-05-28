from django.db import OperationalError
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from utils import secret_dict

try:
    superuser = User.objects.filter(is_superuser=True).first()

except OperationalError:
    superuser = None


class TokenAuthentication(BaseAuthentication):
    """ REST API authentication based on request meta token """

    def authenticate(self, request):
        token = request.META.get('HTTP_X_TOKEN')

        if token is None or token not in secret_dict['service_tokens']:
            raise AuthenticationFailed('Wrong token.')

        return superuser, None
