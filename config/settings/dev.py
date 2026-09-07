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


# Вшитые сторонние файлы: движок PGlite (16 МБ) и шрифты. Их не правят, и
# запрещать их хранить нельзя — тренажёр качал бы движок заново при каждом
# заходе, да ещё дважды: предзагрузчик шкалы и сам PGlite.
VENDOR_PREFIX = "/static/vendor/"


def _no_store(headers, path, url):
    """Запрещаем браузеру хранить свою статику; чужую — наоборот, разрешаем.

    Одного `max-age=0` для своей не хватает: браузер понимает его как «хранить
    можно, но перепроверь», и в пределах сессии отдаёт файл из памяти без
    обращения к серверу. С ES-модулями это особенно неприятно — правка модуля не
    видна, а страница падает на экспорте, которого в новой версии файла уже нет.

    В эксплуатации заголовки другие (см. prod), там вся статика неизменяемая.
    """
    if url.startswith(VENDOR_PREFIX):
        headers["Cache-Control"] = "public, max-age=86400"
    else:
        headers["Cache-Control"] = "no-store, max-age=0"


WHITENOISE_ADD_HEADERS_FUNCTION = _no_store

# Без этой строки заголовок выше не применяется: при DEBUG статику отдаёт
# собственный обработчик runserver, а не WhiteNoise, и до заголовков WhiteNoise
# дело не доходит. `runserver_nostatic` снимает обработчик — раздачей в
# разработке занимается тот же WhiteNoise, что и в эксплуатации. Приложение
# обязано стоять перед `django.contrib.staticfiles`.
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + [
    app for app in INSTALLED_APPS if app != "whitenoise.runserver_nostatic"  # noqa: F405
]
