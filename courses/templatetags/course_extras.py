import markdown as md
from django import template
from django.utils.safestring import mark_safe

from courses.cover import cover_for

register = template.Library()

LEVEL_LABEL = {"basic": "Начальный", "medium": "Средний", "advanced": "Продвинутый"}
LEVEL_TONE = {"basic": "success", "medium": "warning", "advanced": "danger"}
TASK_TYPE_LABEL = {"sql": "SQL", "ddl": "DDL", "file": "файл", "text": "текст"}


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
def task_type_label(code):
    return TASK_TYPE_LABEL.get(code, code)


@register.filter
def is_http_url(value):
    """Только http(s)-адрес можно отрисовать ссылкой.

    Поле `file_url` заполняет студент, а `javascript:`- и `data:`-адрес в ссылке на
    странице преподавателя — это готовый XSS. Экранирование шаблона здесь не спасает:
    оно защищает текст, а не схему адреса.
    """
    return str(value or "").strip().lower().startswith(("http://", "https://"))


@register.filter
def md_to_html(text):
    # Контент уроков авторский (создаётся преподавателем/админом в админке).
    return mark_safe(md.markdown(text or "", extensions=["extra", "sane_lists"]))
