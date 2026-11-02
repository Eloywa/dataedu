from django import template
from django.utils.safestring import mark_safe

from accounts.avatars import avatar_icon

register = template.Library()


@register.inclusion_tag("accounts/_avatar.html")
def avatar(person, css_class=""):
    icon = avatar_icon(person.avatar)
    return {
        "icon": mark_safe(icon) if icon else None,
        "letter": person.label[:1].upper(),
        "css_class": css_class,
    }
