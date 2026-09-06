"""Профиль тестового прогона.

Отличается от разработки тремя вещами, и каждая — ради того, чтобы тест проверял
то, что заявлено:

1. **Кэш отчётов выключен.** С кэшем второй вызов возвращал бы прошлый результат,
   и тест, проверяющий пересчёт после изменения данных, проходил бы вхолостую.
2. **Быстрое хеширование паролей.** По умолчанию Django намеренно делает хеш
   медленным; в тестах, где пользователи создаются сотнями, это основная статья
   расхода времени.
3. **База — SQLite в памяти**, если явно не попросили PostgreSQL. Прогон не
   оставляет файлов и не требует поднятой СУБД.

Профиль выбирается автоматически в `manage.py` при команде `test`.
"""

import os

from .base import *  # noqa: F403
from .base import postgres_database

DEBUG = False

_engine = os.environ.get("DB_ENGINE", "").strip().lower()
if _engine in ("postgres", "postgresql"):
    # Прогон на боевом движке: часть поведения (составные ключи, JSONB, оконные
    # функции) стоит проверять именно на PostgreSQL перед выкладкой.
    DATABASES = {"default": postgres_database()}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
            "TEST": {"NAME": ":memory:"},
        }
    }

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
REPORT_CACHE_SECONDS = 0

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Регистрация открыта: закрытый контур проверяется отдельным тестом через
# override_settings, а не глобальной настройкой прогона.
REGISTRATION_OPEN = True

# То же, что в разработке: тестовый прогон не собирает статику.
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
