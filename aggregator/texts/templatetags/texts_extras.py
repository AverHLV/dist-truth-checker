from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is not None:
        return dictionary.get(key)
