"""Настройка приложения `core` и заплатка сравнения строк в SQLite."""

import re

from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.dispatch import receiver

# Спецсимволы шаблона LIKE: % — любая последовательность, _ — один символ.
_LIKE_SPECIALS = {"%": ".*", "_": "."}


def _like_to_regex(pattern, escape):
    """Перевести шаблон SQL LIKE в регулярное выражение.

    Символ экранирования (Django подставляет `\\`) снимает специальное значение
    у следующего символа: `100\\%` ищет буквальные «100%», а не «начинается со 100».
    """
    out = []
    i = 0
    while i < len(pattern):
        ch = pattern[i]
        if escape and ch == escape and i + 1 < len(pattern):
            out.append(re.escape(pattern[i + 1]))
            i += 2
            continue
        out.append(_LIKE_SPECIALS.get(ch) or re.escape(ch))
        i += 1
    return "".join(out)


def _like(pattern, value, escape=None):
    """Реализация `LIKE`, знающая Юникод.

    Встроенный `LIKE` в SQLite приводит регистр только для латиницы: «Индексы» и
    «индексы» для него разные строки. Платформа русскоязычная целиком, и поиск по
    каталогу в разработке из-за этого молча не находил ничего.

    PostgreSQL — целевая СУБД — так себя не ведёт, и именно поэтому заплатка нужна:
    расхождение поведения между средой разработки и эксплуатацией опаснее самой
    ошибки, потому что тест на SQLite перестаёт что-либо гарантировать.

    Плата — потеря оптимизации `LIKE` по индексу на SQLite. В разработке это
    несущественно, а в эксплуатации функция не регистрируется вовсе.
    """
    if pattern is None or value is None:
        return None
    regex = _like_to_regex(str(pattern), escape)
    return bool(re.match(regex + r"\Z", str(value), re.IGNORECASE | re.DOTALL))


@receiver(connection_created)
def register_unicode_string_functions(sender, connection, **kwargs):
    """Подменить сравнение строк на подключении к SQLite. На PostgreSQL — ничего."""
    if connection.vendor != "sqlite":
        return

    raw = connection.connection
    # Обе арности: `X LIKE Y` и `X LIKE Y ESCAPE Z`. Аргументы приходят в порядке
    # (шаблон, значение) — это соглашение самого SQLite, а не опечатка.
    raw.create_function("like", 2, _like, deterministic=True)
    raw.create_function("like", 3, _like, deterministic=True)

    def upper(value):
        return None if value is None else str(value).upper()

    def lower(value):
        return None if value is None else str(value).lower()

    raw.create_function("UPPER", 1, upper, deterministic=True)
    raw.create_function("LOWER", 1, lower, deterministic=True)


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Платформа"
