from django import template
from django.utils.safestring import mark_safe

from blog.models import Category

register = template.Library()

@register.simple_tag()
def category_list(label, from_obj):
    category_rels = from_obj.categories.through.objects.filter(**{f'{from_obj.__class__.__name__.lower()}_id': from_obj.id})
    if len(category_rels) < 1:
        return mark_safe('')
    out = []
    for category_rel in category_rels:
        category = Category.objects.get(pk=category_rel.category_id)
        out.append(f'<a href="{ category.get_absolute_url() }">{ category.name }</a>')

    return mark_safe(label + ' ' + '، '.join(out))
