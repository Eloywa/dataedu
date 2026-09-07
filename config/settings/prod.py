"""Эксплуатационный профиль: университетский контур, реальная нагрузка.

Отличия от разработки не косметические, поэтому вынесены в отдельный файл, а не в
ветки `if DEBUG`. Ветками легко ошибиться в одну сторону — и наружу уезжает
отладочный режим с трассировками и секретами в них.

Что здесь заложено под нагрузку:

- **PostgreSQL обязателен.** Профиль не стартует без параметров подключения: тихо
  свалиться на файловую базу под нагрузкой — худший из возможных исходов.
- **Постоянные соединения** (`CONN_MAX_AGE`) и потолок времени запроса — в `base`.
- **Кэш.** По умолчанию — в памяти процесса, чего хватает одному экземпляру. При
  нескольких процессах (а под нагрузкой их несколько) нужен общий: задайте
  `REDIS_URL`, и кэш станет общим для всех рабочих процессов. Без общего кэша
  каждый процесс греет свою копию отчётов — это работает, но втрое дороже.
- **Статика.** Отдаётся WhiteNoise с хешами в именах и вечным заголовком кэша:
  отдельный nginx для статики не нужен, а браузер перестаёт её перезапрашивать.
"""

import os

from .base import *  # noqa: F403
from .base import env_bool, env_list, postgres_database

DEBUG = False

# В эксплуатации список хостов обязан быть задан явно: пустой ALLOWED_HOSTS с
# DEBUG=False — это отказ обслуживать запросы, и это лучше, чем принимать любые.
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", [])

SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY не задан. В эксплуатации ключ подписи сессий обязан быть "
        "случайным и храниться вне репозитория."
    )
# Отдельная проверка на отладочный ключ: `.env` обычно копируют из `.env.example`
# вместе со значением по умолчанию, и в эксплуатацию уезжает ключ, который лежит
# в открытом репозитории. Сессии, подписанные им, подделываются кем угодно.
if SECRET_KEY.startswith("django-insecure-") or len(SECRET_KEY) < 32:
    raise RuntimeError(
        "SECRET_KEY выглядит отладочным или слишком коротким. Сгенерируйте новый: "
        'python -c "import secrets; print(secrets.token_urlsafe(64))"'
    )

if not os.environ.get("DB_PASSWORD") and not os.environ.get("DB_HOST"):
    raise RuntimeError(
        "Не заданы параметры PostgreSQL (DB_HOST/DB_NAME/DB_USER/DB_PASSWORD). "
        "Эксплуатационный профиль работает только с PostgreSQL."
    )
DATABASES = {"default": postgres_database()}


_redis_url = os.environ.get("REDIS_URL", "").strip()
if _redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": _redis_url,
        }
    }
    # Сессии в кэше: чтение сессии происходит на каждом запросе, и держать его
    # в той же базе, что и учебные данные, — лишняя нагрузка на неё.
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "dataedu-prod",
        }
    }

# Хеши в именах — для своих файлов, вендор остаётся как есть: PGlite подтягивает
# свои части по путям, вычисляемым во время выполнения. Подробности и история
# поломки — в config/storages.py.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "config.storages.VendorAwareStaticFilesStorage"},
}


# --- Безопасность ------------------------------------------------------------
#
# Значения по умолчанию рассчитаны на работу за HTTPS. Если контур внутренний и
# сертификата нет, выключается переменной SECURE_SSL=0 — но осознанно.

SECURE_SSL = env_bool("SECURE_SSL", True)

SECURE_SSL_REDIRECT = SECURE_SSL
SESSION_COOKIE_SECURE = SECURE_SSL
CSRF_COOKIE_SECURE = SECURE_SSL
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# Приложение почти всегда стоит за обратным прокси, и без этой пары Django считает
# любой запрос небезопасным, зацикливая редирект на HTTPS.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# HSTS включается отдельно и не по умолчанию: заголовок с большим сроком на домене
# без постоянного HTTPS делает сайт недоступным, и откатить это быстро нельзя.
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", False)

CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", [])


# --- Журнал ------------------------------------------------------------------
#
# Пишем в поток вывода: под supervisor/systemd/докером его подхватывает сборщик
# логов, а файлы на диске пришлось бы ротировать самим.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {"format": "{asctime} {levelname} {name} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "plain"},
    },
    "root": {"handlers": ["console"], "level": os.environ.get("LOG_LEVEL", "INFO")},
    "loggers": {
        # Отказы запросов (500, подозрительные операции) — отдельной строкой,
        # иначе они теряются в общем потоке обращений.
        "django.request": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}
