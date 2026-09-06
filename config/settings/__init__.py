"""Выбор профиля настроек.

`DJANGO_SETTINGS_MODULE` во всём проекте остаётся прежним — `config.settings`,
а какой профиль применить, решает переменная `DJANGO_ENV`:

    DJANGO_ENV=dev    (по умолчанию) — разработка и защита
    DJANGO_ENV=prod   — эксплуатация
    DJANGO_ENV=test   — прогон тестов (ставится автоматически в manage.py)

Такой способ выбран вместо `DJANGO_SETTINGS_MODULE=config.settings.prod` намеренно:
модуль настроек указывается в четырёх местах (manage.py, wsgi, asgi, tox/CI), и
рассинхронизация между ними даёт запуск не в том профиле, о котором думает человек.
Здесь точка принятия решения одна.
"""

import os

DJANGO_ENV = os.environ.get("DJANGO_ENV", "dev").strip().lower()

if DJANGO_ENV in ("prod", "production"):
    from .prod import *  # noqa: F401,F403
elif DJANGO_ENV == "test":
    from .test import *  # noqa: F401,F403
elif DJANGO_ENV in ("dev", "development", "local", ""):
    from .dev import *  # noqa: F401,F403
else:
    raise RuntimeError(f"Неизвестный DJANGO_ENV={DJANGO_ENV!r}: ожидается dev или prod")
