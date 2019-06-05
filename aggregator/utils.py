from django.core.exceptions import ImproperlyConfigured
from json import loads
from config import constants


def get_secret(filename):
    """ Get the secret from json file or raise exception """

    fields = 'secret_key', 'db_admin', 'db_pass', 'db_name', 'db_host', 'db_port', 'hazelcast-ips', 'hosts', 'admins'

    try:
        with open(filename) as secret:
            secret = loads(secret.read())

        return {field: secret[field] for field in fields}

    except KeyError as k:
        raise ImproperlyConfigured('Add the {0} field to json secret'.format(k))

    except IOError:
        # local and ci settings

        return {}


secret_dict = get_secret(constants.secret_filename)
