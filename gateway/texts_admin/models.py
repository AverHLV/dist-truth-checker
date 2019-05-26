from django.db.models import CharField
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from os import urandom
from config import constants


def create_user_token():
    """ Generate unique user token """

    token = urandom(constants.token_bytes).hex()

    try:
        while token in TextsAdmin.objects.values_list('token', flat=True):
            token = urandom(constants.token_bytes).hex()

    except TypeError:
        # prevent migration errors if table does not exists

        return '1' * constants.token_bytes

    return token


class TextsAdmin(AbstractUser):
    """ User model with unique token for api authentication """

    token = CharField(
        max_length=constants.token_length, unique=True, default=create_user_token,
        validators=[
            RegexValidator(regex=r'^.{%s}$' % constants.token_length, message='Wrong user token length.')
        ]
    )

    class Meta:
        db_table = 'users'
