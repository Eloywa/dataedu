#!/usr/bin/env python
"""Точка входа для служебных команд Django."""

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    # Тесты идут в своём профиле: он отключает кэш отчётов и ускоряет хеширование
    # паролей. Выбор делается здесь, а не переменной окружения, чтобы `manage.py test`
    # нельзя было случайно запустить с боевыми настройками — например, с настоящей
    # базой, которую тестовый прогон стал бы пересоздавать.
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        os.environ["DJANGO_ENV"] = "test"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Проверьте, что виртуальное окружение "
            "активировано, а зависимости установлены."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
