import markdown as md
from django import template
from django.utils.safestring import mark_safe

from courses.cover import cover_for

register = template.Library()

LEVEL_LABEL = {"basic": "Начальный", "medium": "Средний", "advanced": "Продвинутый"}
LEVEL_TONE = {"basic": "success", "medium": "warning", "advanced": "danger"}


@register.inclusion_tag("courses/_cover.html")
def course_cover(slug, css_class=""):
    a, b, icon = cover_for(slug)
    return {"a": a, "b": b, "icon": mark_safe(icon), "css_class": css_class}


@register.filter
def level_label(code):
    return LEVEL_LABEL.get(code, code)


@register.filter
def level_tone(code):
    return LEVEL_TONE.get(code, "neutral")


@register.filter
def stars(value):
    try:
        v = int(round(float(value or 0)))
    except (TypeError, ValueError):
        v = 0
    v = max(0, min(5, v))
    return "★" * v + "☆" * (5 - v)


@register.filter
def md_to_html(text):
    # Контент уроков авторский (создаётся преподавателем/админом в админке).
    return mark_safe(md.markdown(text or "", extensions=["extra", "sane_lists"]))
