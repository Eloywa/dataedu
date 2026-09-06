"""Общие настройки DataEdu — то, что одинаково во всех средах.

Профили лежат рядом: `dev.py` (разработка и защита), `prod.py` (эксплуатация).
Какой применится, решает `config/settings/__init__.py` по переменной `DJANGO_ENV`;
`DJANGO_SETTINGS_MODULE` остаётся прежним — `config.settings`.

Разделение появилось не ради красоты. Пока проект жил на одной машине, различие
между «у меня на ноутбуке» и «на сервере факультета» помещалось в пару переменных
окружения. С выходом на реальную нагрузку разошлось всё: база, кэш, отдача статики,
заголовки безопасности, время жизни соединения. Держать это в одном файле, включая
и выключая ветками `if DEBUG`, — верный способ однажды выкатить наружу DEBUG=True.
"""

import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv

# config/settings/base.py → config/settings → config → корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Переменные окружения из .env (секреты, параметры БД). В git .env не входит.
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default):
    """Булево из окружения. Пустая строка — это «не задано», а не «ложь»."""
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default):
    raw = os.environ.get(name)
    if not raw:
        return list(default)
    return [item.strip() for item in raw.split(",") if item.strip()]


SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-dev-key-change-me")

# Значения по умолчанию — для разработки; профиль prod их ужесточает.
DEBUG = env_bool("DEBUG", True)
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])


# --- Правовой контур (этап 9.6) ---------------------------------------------

# Свободная регистрация. На апробации выключается (REGISTRATION_OPEN=0), а логины
# выдаются пачкой командой `create_pilot_accounts`: так в системе оказываются только
# обезличенные учётные записи, а соответствие «код ↔ студент» остаётся вне системы.
REGISTRATION_OPEN = env_bool("REGISTRATION_OPEN", True)

# Срок хранения событий ленты активности (таблица `activities`). Хранить учебную
# телеметрию бессрочно незачем: для аналитики хватает учебного года, а всё лишнее
# только увеличивает объём обрабатываемых данных. Чистка — `manage.py purge_metrics`.
METRICS_RETENTION_DAYS = int(os.environ.get("METRICS_RETENTION_DAYS", "400"))


# --- Приложения --------------------------------------------------------------
#
# Порядок отражает зависимости: `accounts` не знает ни о чём выше себя, `courses`
# знает про `accounts`, и так далее. Правило направления связей — в ARCHITECTURE.md.

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Приложения проекта
    "core",
    "accounts",
    "courses",
    "assessments",
    "learning",
    "gamification",
    "messaging",
]

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise отдаёт статику самим приложением, без отдельного nginx.
    # Ставится сразу за SecurityMiddleware — так предписывает документация пакета.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Бейдж непрочитанных в шапке — нужен на каждой странице.
                "messaging.context_processors.unread",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# --- База данных -------------------------------------------------------------
#
# Выбор движка — за профилем. Здесь только то, что общее: время жизни соединения.
# `CONN_MAX_AGE` важнее, чем кажется: установка соединения с PostgreSQL стоит
# несколько миллисекунд, и при сотне запросов в секунду переподключение на каждый
# запрос съедает заметную долю времени ответа.
CONN_MAX_AGE = int(os.environ.get("DB_CONN_MAX_AGE", "60"))


def postgres_database():
    """Параметры подключения к PostgreSQL из окружения."""
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "dataedu_django"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": CONN_MAX_AGE,
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            # Запрос, висящий дольше 15 секунд, — почти всегда ошибка, а не
            # медленный отчёт. Без потолка такой запрос держит соединение из пула.
            "options": "-c statement_timeout=15000",
        },
    }


def sqlite_database(name="db.sqlite3"):
    """Файловая база — чтобы проект поднимался на любой машине без установки СУБД."""
    return {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / name,
        "OPTIONS": {
            # WAL и разумный таймаут: без них параллельные запись и чтение в SQLite
            # упираются в «database is locked» уже на паре вкладок.
            "init_command": "PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;",
            "transaction_mode": "IMMEDIATE",
            "timeout": 20,
        },
    }


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True


# --- Статика -----------------------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# PGlite грузит движок через WebAssembly.instantiateStreaming, а тот требует
# строгий Content-Type: application/wasm. На Windows тип берётся из реестра, где
# для .wasm записи может не быть, — регистрируем явно, чтобы тренажёр поднимался
# на любой машине.
mimetypes.add_type("application/wasm", ".wasm", strict=True)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Постраничный вывод ------------------------------------------------------
#
# Единая величина для всех списков. Страница без ограничения количества — это
# отложенная авария: пока курсов десять, «показать все» работает, а на потоке в
# полторы тысячи записей тот же шаблон отрисовывает полторы тысячи карточек.
PAGE_SIZE = int(os.environ.get("PAGE_SIZE", "24"))

# Сколько держать посчитанные отчёты преподавателя. Аналитика собирается тяжело,
# а меняется медленно: студент проходит урок за минуты, не за секунды.
REPORT_CACHE_SECONDS = int(os.environ.get("REPORT_CACHE_SECONDS", "60"))
