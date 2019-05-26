from os import environ
from importlib import import_module


def version(_):
    """ Context processor for setting staticfiles version """

    return {'version': import_module(environ['DJANGO_SETTINGS_MODULE']).STATIC_VERSION}
