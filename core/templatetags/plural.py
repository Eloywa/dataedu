"""Фильтр согласования с числом для шаблонов.

Использование: {{ count }} {{ count|plural_ru:"урок,урока,уроков" }}
"""

from django import template

from core.plural import plural_ru as _plural_ru

register = template.Library()


@register.filter
def plural_ru(value, forms):
    """Три формы через запятую: именительная, родительная, множественная."""
    parts = [part.strip() for part in str(forms).split(",")]
    if len(parts) != 3:
        return ""
    try:
        return _plural_ru(value, *parts)
    except (TypeError, ValueError):
        return parts[2]
