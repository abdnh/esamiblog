from django import template

register = template.Library()

# @register.filter
@register.simple_tag()
def get_item(dictionary, key, default):
    return dictionary.get(key, default)
