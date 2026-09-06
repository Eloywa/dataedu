"""Профиль разработки и защиты проекта.

Главное свойство — **проект должен подниматься на чужой машине без установки СУБД**.
Поэтому база по умолчанию файловая (SQLite): `clone → migrate → runserver` работает
сразу. PostgreSQL включается одной переменной `DB_ENGINE=postgres`, когда нужно
проверить поведение на боевом движке.

Это не значит, что платформа «работает на SQLite». Эксплуатационный профиль требует
PostgreSQL и отказывается стартовать без него: часть решений (составные ключи,
JSONB, оконные функции в отчётах) рассчитана именно на него. SQLite здесь — среда
разработки, а не целевая СУБД.
"""

import os

from .base import *  # noqa: F403
from .base import env_bool, postgres_database, sqlite_database

DEBUG = env_bool("DEBUG", True)

# «postgres» — если явно попросили или если заданы параметры подключения.
_engine = os.environ.get("DB_ENGINE", "").strip().lower()
if _engine in ("postgres", "postgresql"):
    DATABASES = {"default": postgres_database()}
else:
    DATABASES = {"default": sqlite_database()}

# Кэш в памяти процесса: внешнего хранилища в разработке нет и не нужно.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "dataedu-dev",
    }
}

# Статику в разработке отдаёт staticfiles, манифест не нужен: он требует
# collectstatic после каждой правки CSS.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

INTERNAL_IPS = ["127.0.0.1"]

# В разработке статика ещё не собрана (`collectstatic` не запускался), и WhiteNoise
# ругался бы на отсутствующий каталог. USE_FINDERS заставляет его брать файлы там же,
# где их берёт staticfiles — прямо из static/, а AUTOREFRESH снимает кэширование,
# иначе правка CSS не видна без перезапуска.
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Ноль секунд жизни в кэше браузера. Иначе правка CSS или скрипта не видна до
# жёсткого обновления страницы, и время уходит на поиск ошибки, которой нет:
# на сервере уже новый файл, в браузере — старый.
WHITENOISE_MAX_AGE = 0
