from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.template.defaultfilters import stringfilter

from blog.models import Category

import markdown
from markdown.extensions.toc import TocExtension, slugify_unicode

import bleach
from bleach import Cleaner
from bleach.linkifier import LinkifyFilter


register = template.Library()

@register.simple_tag()
def get_item(dictionary, key, default):
    return dictionary.get(key, default)

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

@register.simple_tag
def update_icon(obj, update_url=None):
    name = obj.__class__.__name__.lower()
    if not update_url:
        update_url = reverse(f'{name}-update', kwargs={'pk': obj.id})
    html = f"""<a href="{update_url}" class="svgicon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
<path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
</svg></a>"""
    return mark_safe(html)

@register.simple_tag
def delete_icon(obj, delete_url=None):
    name = obj.__class__.__name__.lower()
    if not delete_url:
        delete_url = reverse(f'{name}-delete', kwargs={'pk': obj.id})
    html = f"""<a href="{delete_url}" class="svgicon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-square" viewBox="0 0 16 16">
<path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
<path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
</svg></a>"""
    return mark_safe(html)


@register.simple_tag
def user_update_icon(user):
    return update_icon(user, reverse('user-update', kwargs={'username': user.get_username()}))

@register.simple_tag
def user_delete_icon(user):
    return delete_icon(user, reverse('user-delete', kwargs={'username': user.get_username()}))


BLEACH_ALLOWED_TAGS = bleach.ALLOWED_TAGS + [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'div', 'span', 'br', 'img', 'sub', 'sup', 'hr',
    'table', 'tbody', 'thead', 'tr', 'td', 'th', 'caption', 'col', 'colgroup', 'tfoot',
]
BLEACH_ALLOWED_ATTRIBUTES = {
    'span': ['class'],
    'div': ['class', 'role'],
    'img': ['src', 'width', 'height', 'alt', 'title'],
    'a': ['class', 'id', 'rel'],
    'sub': ['class'],
    'sup': ['class', 'id'],
    'li': ['class', 'id', 'role'],
}
BLEACH_ALLOWED_ATTRIBUTES.update(bleach.ALLOWED_ATTRIBUTES)
cleaner = Cleaner(tags=BLEACH_ALLOWED_TAGS, attributes=BLEACH_ALLOWED_ATTRIBUTES, filters=[LinkifyFilter])
MD_EXTENSIONS = [
    'fenced_code',
    'codehilite',
    'tables',
    'nl2br',
    'footnotes',
    TocExtension(slugify=slugify_unicode),
]
md = markdown.Markdown(extensions=MD_EXTENSIONS)

@register.filter
@stringfilter
def markdown(text):
    html = cleaner.clean(md.convert(text))
    md.reset()
    return mark_safe(html)
